@echo off

echo Installing Python dependencies...
pip install -r requirements.txt || exit /b

echo Installing React app dependencies...
cd path\to\your\react\app
npm install || exit /b

echo Setup complete! You can now run your backend server and React app!
pause