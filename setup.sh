#!/bin/bash

echo "Installing Python dependencies..."
pip install -r requirements.txt || { echo 'Python dependencies installation failed' ; exit 1; }

echo "Installing React app dependencies..."
cd /path/to/your/react/app
npm install || { echo 'React app dependencies installation failed' ; exit 1; }

echo "Setup complete! You can now run your backend server and React app!"