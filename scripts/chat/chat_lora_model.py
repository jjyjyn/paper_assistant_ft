#!/usr/bin/env python3
"""Interactive chat entry for a Qwen base model plus LoRA adapter."""

from __future__ import annotations

import argparse
from typing import Any

SYSTEM_PROMPT_NO_THINK = (
    "Provide only the final answer. "
    "Do not output hidden reasoning, chain-of-thought, or <think> tags."
)


def strip_think_content(text: str) -> str:
    import re

    text = text.strip()
    if not text:
        return text

    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()
    if text.startswith("<think>"):
        return ""
    return text.strip()


def load_model(base_model_path: str, adapter_path: str) -> tuple[Any, Any]:
    import torch
    from peft import PeftModel
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(base_model_path, trust_remote_code=True)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token

    dtype = torch.bfloat16 if torch.cuda.is_available() else torch.float32
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_path,
        torch_dtype=dtype,
        trust_remote_code=True,
    )
    if hasattr(base_model, "generation_config"):
        base_model.generation_config.do_sample = False
        for attr in ("temperature", "top_p", "top_k"):
            if hasattr(base_model.generation_config, attr):
                setattr(base_model.generation_config, attr, None)

    model = PeftModel.from_pretrained(base_model, adapter_path)
    if torch.cuda.is_available():
        model = model.to("cuda")
    model.eval()
    return model, tokenizer


def generate_response(
    model: Any,
    tokenizer: Any,
    history: list[dict[str, str]],
    user_prompt: str,
    max_new_tokens: int,
    disable_thinking: bool,
    system_prompt: str,
) -> tuple[str, str, str]:
    import torch

    messages: list[dict[str, str]] = []
    if disable_thinking:
        messages.append({"role": "system", "content": system_prompt})
    messages.extend(history)
    messages.append({"role": "user", "content": user_prompt})

    chat_kwargs = {
        "add_generation_prompt": True,
        "tokenize": True,
        "return_tensors": "pt",
    }
    thinking_control_mode = "default"

    if disable_thinking:
        try:
            inputs = tokenizer.apply_chat_template(
                messages,
                enable_thinking=False,
                **chat_kwargs,
            )
            thinking_control_mode = "chat_template_enable_thinking_false"
        except TypeError:
            fallback_messages = list(messages)
            fallback_messages[-1] = {
                "role": "user",
                "content": f"{user_prompt}\n\n/no_think",
            }
            inputs = tokenizer.apply_chat_template(fallback_messages, **chat_kwargs)
            thinking_control_mode = "prompt_no_think_fallback"
    else:
        inputs = tokenizer.apply_chat_template(messages, **chat_kwargs)

    if torch.cuda.is_available():
        inputs = inputs.to("cuda")

    with torch.no_grad():
        output_ids = model.generate(
            inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            temperature=None,
            top_p=None,
            top_k=None,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )

    new_tokens = output_ids[0, inputs.shape[-1] :]
    raw_response = tokenizer.decode(new_tokens, skip_special_tokens=True).strip()
    cleaned_response = strip_think_content(raw_response)
    return raw_response, cleaned_response, thinking_control_mode


def run_single_turn(args: argparse.Namespace, model: Any, tokenizer: Any) -> int:
    raw_response, response, thinking_control_mode = generate_response(
        model=model,
        tokenizer=tokenizer,
        history=[],
        user_prompt=args.prompt,
        max_new_tokens=args.max_new_tokens,
        disable_thinking=args.disable_thinking,
        system_prompt=args.system_prompt,
    )
    print(response)
    if args.show_raw and raw_response != response:
        print("\n[raw]")
        print(raw_response)
    if args.show_meta:
        print(f"\n[meta] thinking_control_mode={thinking_control_mode}")
    return 0


def run_interactive(args: argparse.Namespace, model: Any, tokenizer: Any) -> int:
    history: list[dict[str, str]] = []
    print("Interactive chat started.")
    print("Commands: /clear, /exit, /quit")
    print(f"disable_thinking={args.disable_thinking}")

    while True:
        try:
            user_prompt = input("\nYou> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExit.")
            return 0

        if not user_prompt:
            continue
        if user_prompt in {"/exit", "/quit"}:
            print("Exit.")
            return 0
        if user_prompt == "/clear":
            history.clear()
            print("History cleared.")
            continue

        raw_response, response, thinking_control_mode = generate_response(
            model=model,
            tokenizer=tokenizer,
            history=history,
            user_prompt=user_prompt,
            max_new_tokens=args.max_new_tokens,
            disable_thinking=args.disable_thinking,
            system_prompt=args.system_prompt,
        )
        history.append({"role": "user", "content": user_prompt})
        history.append({"role": "assistant", "content": response})

        print(f"\nAssistant> {response}")
        if args.show_raw and raw_response != response:
            print("\n[raw]")
            print(raw_response)
        if args.show_meta:
            print(f"\n[meta] thinking_control_mode={thinking_control_mode}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Chat with a LoRA-adapted model.")
    parser.add_argument("--base-model", required=True, help="Base model path.")
    parser.add_argument("--adapter-path", required=True, help="LoRA adapter directory.")
    parser.add_argument("--prompt", default="", help="Single-turn prompt. Empty means interactive mode.")
    parser.add_argument("--max-new-tokens", type=int, default=512)
    parser.add_argument(
        "--disable-thinking",
        action="store_true",
        help="Try to disable thinking output via chat template or prompt fallback.",
    )
    parser.add_argument(
        "--system-prompt",
        default=SYSTEM_PROMPT_NO_THINK,
        help="System prompt used when --disable-thinking is enabled.",
    )
    parser.add_argument(
        "--show-raw",
        action="store_true",
        help="Print raw model output when it differs from the cleaned response.",
    )
    parser.add_argument(
        "--show-meta",
        action="store_true",
        help="Print thinking-control metadata for debugging.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    print(f"Loading base model: {args.base_model}")
    print(f"Loading adapter: {args.adapter_path}")
    model, tokenizer = load_model(args.base_model, args.adapter_path)
    if args.prompt:
        return run_single_turn(args, model, tokenizer)
    return run_interactive(args, model, tokenizer)


if __name__ == "__main__":
    raise SystemExit(main())
