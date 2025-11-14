@echo off
echo Building Docker image...
docker build -t liveness-poc .

echo Stopping old container if exists...
docker stop liveness >nul 2>&1
docker rm liveness >nul 2>&1

echo Running new container...
docker run -d --name liveness -p 8000:8000 liveness-poc

echo Done! Container running at http://localhost:8000
pause
