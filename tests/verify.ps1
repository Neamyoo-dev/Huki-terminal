$proc = Start-Process -FilePath python -ArgumentList 'main.py' -WindowStyle Hidden -PassThru
Start-Sleep -Seconds 5
if (-not $proc.HasExited) {
    Write-Host 'complete success'
    $proc.Kill()
} else {
    Write-Host ('exited with code ' + $proc.ExitCode)
}
