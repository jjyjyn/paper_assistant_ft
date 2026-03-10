param(
  [string]$ServerUser = "your_user",
  [string]$ServerHost = "your.server.ip",
  [string]$ServerProjectDir = "~/paper_assistant_ft",
  [string]$LocalProjectDir = "D:\llm_train\paper_assistant_ft"
)

$ErrorActionPreference = "Stop"

Write-Host "[1/3] Push local code to GitHub"
Set-Location $LocalProjectDir
git add .
git commit -m "chore: day1 docs and server bootstrap" 2>$null
git push

Write-Host "[2/3] Pull latest code on server"
ssh "$ServerUser@$ServerHost" "mkdir -p $ServerProjectDir && cd $ServerProjectDir && if [ -d .git ]; then git pull; else git clone https://github.com/jjyjyn/paper_assistant_ft.git .; fi"

Write-Host "[3/3] Done"
