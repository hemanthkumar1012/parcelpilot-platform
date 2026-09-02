import sys
import os

# Add the root directory to the python path so the 'app' module can be resolved
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app

# Vercel requires the application to be named 'app' in the entry point file
