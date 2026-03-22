# MIS Certificate Tracker

A Streamlit app for tracking MIS certificates with Firebase Realtime Database.

## Features

- Add MIS certificates
- View all certificates
- Highlight certificates nearing maturity (`Days_Left <= 20`)
- Edit and delete records

## Tech Stack

- Streamlit
- Pandas
- Firebase Admin SDK
- Firebase Realtime Database

## Local Setup

1. Create and activate a Python environment.
2. Install dependencies from `requirements.txt`.
3. Create local secrets file at `.streamlit/secrets.toml` using `.streamlit/secrets.toml.example`.
4. Run Streamlit app:

   `streamlit run app.py`

## Streamlit Community Cloud Deployment

1. Push this repository to GitHub.
2. Open Streamlit Community Cloud and create a new app from the repo.
3. Set **Main file path** to `app.py`.
4. In app settings, open **Secrets** and paste the content from `.streamlit/secrets.toml.example` with your real values.
5. Deploy.

## Required Streamlit Secrets

Use this format in Streamlit Cloud Secrets:

```toml
[firebase]
database_url = "https://your-project-id-default-rtdb.firebaseio.com"

[firebase.service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "firebase-adminsdk-xxxxx@your-project-id.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-xxxxx%40your-project-id.iam.gserviceaccount.com"
```

## Security Notes

- Never commit real `secrets.toml` or `.streamlit/secrets.toml` to GitHub.
- Rotate any previously exposed Firebase private keys.
- Keep Firebase Realtime Database rules appropriately locked down.
