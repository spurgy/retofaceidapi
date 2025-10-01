# Face Recognition API

## Local Run
1. Create virtual environment: `python -m venv venv`
2. Activate: `venv\Scripts\activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `hypercorn app:app --reload --bind 0.0.0.0:8000`

## Railway Deployment
1. Push this repo to GitHub
2. On Railway:
   - New Project → Deploy from GitHub → select repo
   - Railway automatically builds Dockerfile
   - App will run on assigned $PORT