Remove-Item -Path "build" -Recurse -ErrorAction SilentlyContinue -Force
Sleep 2
mkdir build -ErrorAction SilentlyContinue -Force
mkdir dist -ErrorAction SilentlyContinue -Force

Copy-Item -Path "src" -Destination "build/src" -Exclude "*__pycache__*", "*.pyc" -Recurse
Copy-Item -Path "migrations" -Destination "build/migrations" -Exclude "*__pycache__*", "*.pyc" -Recurse
Copy-Item -Path "main.py" -Destination "build/main.py"
Copy-Item -Path "alembic.ini" -Destination "build/alembic.ini"
Copy-Item -Path "Procfile" -Destination "build/Procfile"
Copy-Item "requirements.txt" "build/requirements.txt"
Copy-Item "rds-ca-bundle.pem" "build/rds-ca-bundle.pem"


$dist = Get-Item ".\dist" | Select-Object -ExpandProperty FullName

$zipName = Join-path   $dist "$(Get-Date -Format "yyyy-MM-dd_HH-mm-ss")_build.zip"

Write-host "Output to $zipName"
Set-Location "build"
& "C:\Program Files\7-Zip\7z.exe" a $zipName "*" -tzip
Set-Location ..

