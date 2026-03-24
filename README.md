# MIS Certificate Tracker

A Streamlit app for tracking MIS certificates with Firebase authentication and user-scoped data management.

## Features

**Authentication & Security**
- User registration and login with Firebase Authentication
- Secure session management with logout functionality
- Each user can only view and manage their own certificates

**Certificate Management**
- Add new MIS certificates
- View all your certificates in a dashboard
- Edit certificate details
- Delete certificates
- Search and sort certificates by number, date, or amount

 **Smart Alerts**
- Highlight certificates nearing maturity (20 days or less)
- Visual color-coded urgency indicators
- CSV export for certificate records

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python, Pandas
- **Database**: Firebase Realtime Database
- **Authentication**: Firebase Authentication
- **API Requests**: Requests library

## Local Setup

### Prerequisites
- Python 3.8+
- Firebase project with Authentication enabled

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd mis_frontend
   ```

2. **Create and activate a Python environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   source .venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Firebase Secrets**
   - Create `.streamlit/secrets.toml` in your project root
   - Add your Firebase credentials (see Configuration section below)
   - ** Never commit `secrets.toml` to GitHub** (use `.gitignore`)

5. **Run the app**
   ```bash
   streamlit run app.py
   ```

   The app will open at `http://localhost:8501`

## Configuration

### Required Firebase Setup

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a project or use existing one
3. Enable **Authentication** (Email/Password method)
4. Create a web app in Project Settings
5. Get your Firebase credentials

### Streamlit Secrets File

Create `.streamlit/secrets.toml` with:

```toml
[firebase]
database_url = "https://your-project-id-default-rtdb.firebaseio.com"
api_key = "YOUR_WEB_API_KEY"

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
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/..."
universe_domain = "googleapis.com"
```

## Streamlit Community Cloud Deployment

1. Push this repository to GitHub
2. Go to [Streamlit Community Cloud](https://streamlit.io/cloud)
3. Click "New app" and select your repository
4. Set **Main file path** to `app.py`
5. In **Advanced settings** → **Secrets**, paste your `secrets.toml` content
6. Click "Deploy"

## Project Structure

```
mis_frontend/
├── app.py                    # Main Streamlit application
├── utils.py                  # Firebase and authentication utilities
├── requirements.txt          # Python dependencies
├── secrets.toml             # Firebase credentials (DO NOT COMMIT)
├── .gitignore               # Files to exclude from Git
├── README.md                # This file
├── AUTHENTICATION_SETUP.md   # Detailed authentication setup guide
└── LICENSE
```

## Usage Guide

### First-Time Setup
1. Click **"📝 Sign Up"** on the login page
2. Enter your email and password (min 6 characters)
3. Click **"✅ Create Account"**

### Logging In
1. Enter your registered email
2. Enter your password
3. Click **"🔓 Login"**

### Managing Certificates
- **📊 Dashboard**: View all your certificates with status indicators
- **➕ Add Certificate**: Register a new certificate
- **✏️ Manage Certificates**: Edit or delete existing certificates

### Certificate Data Storage
- All data is stored in Firebase Realtime Database
- Each user's certificates are stored separately
- Format: `users/{user_id}/certificates/{cert_id}`

## Security Notes

**Best Practices**
- Never commit `secrets.toml` to GitHub
- Use `.gitignore` to exclude sensitive files
- Rotate Firebase keys regularly in production
- Use strong, unique passwords
- Enable two-factor authentication on Firebase console account

## Database Schema

```
users/
├── {user_id}/
│   └── certificates/
│       ├── {cert_id}: {
│           "Certificate_Number": "CERT001",
│           "Amount": 50000,
│           "Issue_Date": "2024-01-01",
│           "Maturity_Date": "2025-01-01",
│           "user_id": "{user_id}"
│       }
│       └── {cert_id2}: {...}
└── {user_id2}/
    └── certificates/ {...}
```

## Troubleshooting

### Authentication Issues
- **"Invalid email or password"**: Check credentials spelling
- **"Email already exists"**: Use a different email or login
- **"Missing api_key"**: Add api_key to `secrets.toml`

### Firebase Errors
- **"Permission denied"**: Verify database rules allow authenticated users
- **"Certificate not found"**: Ensure you're logged in and certificate belongs to your account

For detailed authentication setup, see [AUTHENTICATION_SETUP.md](AUTHENTICATION_SETUP.md)

## Support

For issues or questions:
1. Check the [AUTHENTICATION_SETUP.md](AUTHENTICATION_SETUP.md) guide
2. Review Firebase documentation

## Security Notes

- Never commit real `secrets.toml` or `.streamlit/secrets.toml` to GitHub.
- Rotate any previously exposed Firebase private keys.
- Keep Firebase Realtime Database rules appropriately locked down.

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## Contact

Manolina Das - [GitHub Profile](https://github.com/manolina-13)

