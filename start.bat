@echo off
echo 🚀 Starting CIDion AI Server...
echo 📍 Location: %cd%
echo.

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  .env file not found!
    echo 📝 Creating .env from example...
    copy .env.example .env
    echo ✅ .env file created. Please edit it with your API keys.
    echo.
)

REM Install requirements
echo 📦 Installing requirements...
pip install -r requirements.txt

echo.
echo 🚀 Starting server...
echo 📱 Web Interface: http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs
echo 🔧 Press Ctrl+C to stop
echo ==================================================

REM Start the server
python -m uvicorn src.api.app:create_app --factory --host localhost --port 8000 --reload

pause
