$exclude = @("venv", "bot-orange.zip")
$files = Get-ChildItem -Path . -Exclude $exclude
Compress-Archive -Path $files -DestinationPath "bot-orange.zip" -Force