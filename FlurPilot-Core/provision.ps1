
# FlurPilot Infrastructure Provisioning
# Usage: .\provision.ps1

$ErrorActionPreference = "Stop"

# 1. Set Token (From User Input)
$Env:TF_VAR_hcloud_token = "1TMXkHYbk13IzW5PrUXb8zMJXbCinSz7s5xsETi2j6VlWW2ylaaaHRfEWcCBT0bu"

Write-Host "🚀 Starting FlurPilot Infrastructure Provisioning..." -ForegroundColor Green

# 2. Check Terraform
if (Get-Command "terraform" -ErrorAction SilentlyContinue) {
    Write-Host "✅ Terraform found."
    
    Set-Location "infrastructure"
    
    Write-Host "Initializing Terraform..."
    terraform init
    
    Write-Host "Applying Configuration (This creates real server costs!)..."
    terraform apply -auto-approve
    
    Write-Host "✅ Infrastructure Deployed."
}
else {
    Write-Host "❌ Terraform is not installed or not in PATH." -ForegroundColor Red
    
    # Try to install via Winget
    if (Get-Command "winget" -ErrorAction SilentlyContinue) {
        Write-Host "Attempting auto-install via Winget..."
        try {
            winget install HashiCorp.Terraform --accept-source-agreements --accept-package-agreements --silent
            Write-Host "✅ Terraform installed successfully." -ForegroundColor Green
            Write-Host "⚠️  PLEASE RESTART YOUR TERMINAL (Close and Re-open) to update your PATH, then run this script again." -ForegroundColor Yellow
            exit
        }
        catch {
            Write-Host "Winget install failed." -ForegroundColor Red
        }
    }
    
    Write-Host "Please install Terraform manually: https://developer.hashicorp.com/terraform/install"
}
