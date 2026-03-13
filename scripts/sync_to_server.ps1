param(
  [string]$ServerUser = "your_user",
  [string]$ServerHost = "your.server.ip",
  [string]$ServerProjectDir = "~/paper_assistant_ft",
  [string]$LocalProjectDir = "D:\llm_train\paper_assistant_ft"
)

$ErrorActionPreference = "Stop"
$Target = Join-Path $PSScriptRoot "server\\sync_to_server.ps1"
& $Target @PSBoundParameters
