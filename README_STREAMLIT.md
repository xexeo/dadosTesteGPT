# Deploying this repository as a Streamlit app

This PR adds a minimal Streamlit entrypoint wrapper (streamlit_app.py) and deployment helper files
(requirements.txt, .streamlit/config.toml, Procfile, runtime.txt, Dockerfile) so you can deploy
this project to Streamlit Community Cloud, Heroku, or with Docker.

How to use on Streamlit Cloud
1. Push this branch and open Streamlit Community Cloud: https://share.streamlit.io
2. Click "New app", select the repository and branch, and set "File path" to `streamlit_app.py`.
3. Add any required secrets (OpenAI API keys, etc.) in Settings → Secrets.
4. Deploy.

If your repository already has a Streamlit entrypoint named `app.py`, `main.py`, or `streamlit_app.py`,
Streamlit Cloud can point directly to that file instead of this wrapper.

Local testing
1. pip install -r requirements.txt
2. streamlit run streamlit_app.py

Docker
- Build: docker build -t my-streamlit-app .
- Run: docker run -p 8501:8501 my-streamlit-app

Notes
- Update requirements.txt to include any other libraries your app requires.
- If you want a different Python version for Heroku, update runtime.txt.
