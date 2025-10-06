Remove-Item -Path "build" -Recurse -ErrorAction SilentlyContinue -Force
Sleep 2
mkdir build -ErrorAction SilentlyContinue -Force
mkdir dist -ErrorAction SilentlyContinue -Force

Copy-Item -Path "src" -Destination "build/src" -Exclude "*__pycache__*", "*.pyc" -Recurse
Copy-Item -Path "migrations" -Destination "build/migrations" -Exclude "*__pycache__*", "*.pyc" -Recurse
Copy-Item -Path "main.py" -Destination "build/main.py"
Copy-Item -Path "Procfile" -Destination "build/Procfile"

./venv/Scripts/poetry.exe export --without-hashes -f requirements.txt --output "build/requirements.txt"

$dist = Get-Item ".\dist" | Select -ExpandProperty FullName

$zipName = Join-path   $dist "$(date -f "yyyy-MM-dd_HH-mm-ss")_build.zip"

Write-host "Output to $zipName"
cd "build"
& "C:\Program Files\7-Zip\7z.exe" a $zipName "*" -tzip
cd ..

