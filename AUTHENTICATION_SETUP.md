# Authentication Setup Guide

## Summary of Changes

Your MIS Certificate Tracker now includes **user authentication** with login/sign-up functionality and **user-specific certificate storage**. Users can only see their own certificates.

### What Changed:

#### 1. **New Authentication System**
- ✅ Login page with email/password authentication
- ✅ Sign-up page for new users
- ✅ Firebase Authentication integration
- ✅ Session management with logout functionality

#### 2. **User-Scoped Certificates**
- ✅ Certificates are now stored per user (not globally)
- ✅ Database structure: `users/{user_id}/certificates`
- ✅ Each user only sees their own certificates
- ✅ Prevents cross-user certificate visibility

#### 3. **Updated Files**
- `app.py` - Complete rewrite with authentication pages and protected routes
- `utils.py` - Updated functions to include auth functions and user filtering
- `requirements.txt` - Added `requests` and `PyJWT` packages
- `secrets.toml` - Added `api_key` field for Firebase REST API

---

## Setup Instructions

### Step 1: Install Dependencies
Run this in your terminal:
```bash
pip install -r requirements.txt
```

### Step 2: Update Firebase API Key

You need to add your Firebase **Web API Key** to `secrets.toml`:

**How to find your API Key:**

**Step 1: Create a Web App in Firebase**
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project (`mis-certificate-tracker`)
3. Click **Project Settings** (gear icon, top-left)
4. You'll see: **"There are no apps in your project"**
5. Click **"</> Web"** (Web platform icon) to add a web app
6. Enter an app name (e.g., "MIS Certificate Tracker Web")
7. Click "Register app"
8. Firebase will show you a config block like this:

```javascript
const firebaseConfig = {
  apiKey: "AIzaSyDq54321_ABCxyz1234567890",  // ← COPY THIS VALUE
  authDomain: "mis-certificate-tracker.firebaseapp.com",
  databaseURL: "https://mis-certificate-tracker-default-rtdb.firebaseio.com",
  projectId: "mis-certificate-tracker",
  storageBucket: "mis-certificate-tracker.appspot.com",
  messagingSenderId: "123456789012",
  appId: "1:123456789012:web:abcdef1234567890"
};
```

**Step 2: Copy the apiKey**
From the config above, copy the `apiKey` value (the long alphanumeric string after `apiKey: `)

**Example:**
- Your API Key might look like: `AIzaSyDq54321_ABCxyz1234567890`

**Step 3: Update secrets.toml:**
Find this line:
```toml
api_key = "YOUR_FIREBASE_API_KEY"
```

**Update secrets.toml:**
Find this line:
```toml
api_key = "YOUR_FIREBASE_API_KEY"
```

Replace `YOUR_FIREBASE_API_KEY` with your actual API Key (without the quotes).

**Example format (with fake key):**
```toml
api_key = "AIzaSy_XXXX_YOUR_ACTUAL_KEY_HERE_XXXX"
```

### Step 3: Enable Firebase Authentication

1. In [Firebase Console](https://console.firebase.google.com/)
2. Go to **Authentication** → **Sign-in method**
3. Enable **Email/Password**

### Step 4: Run Your App
```bash
streamlit run app.py
```

---

## How It Works

### **Login Flow:**
1. User arrives at the app → sees Login/Sign-up page
2. User clicks "Sign Up" and creates account with email/password
3. User logs in with credentials
4. Session state stores `user_id` and `user_email`
5. App loads certificate management interface

### **Certificate Management:**
- All certificates are stored in path: `users/{user_id}/certificates/{cert_key}`
- When user logs out, session state clears
- Next login shows only that user's certificates
- No cross-user visibility of certificates

### **Data Structure (Firebase):**
```
users/
├── user_id_1/
│   └── certificates/
│       ├── cert_key_1: {Certificate_Number, Amount, ...}
│       └── cert_key_2: {Certificate_Number, Amount, ...}
└── user_id_2/
    └── certificates/
        └── cert_key_1: {Certificate_Number, Amount, ...}
```

---

## Features

✨ **New Authentication Features:**
- 🔐 Secure login with password validation
- 📝 Sign-up page for new users
- 🚪 Logout button in sidebar
- 👤 User email displayed in sidebar
- 🔒 User-scoped certificate storage

📊 **Existing Dashboard Features (Now User-Specific):**
- Certificate tracking with maturity dates
- Due-soon alerts (20 days)
- Add/Edit/Delete certificates
- CSV export
- Search and sort by multiple criteria

---

## Testing Your Setup

1. **Create a test user:**
   - Click "Sign Up"
   - Enter: `test@example.com` / `password123`
   - Should see "Account created successfully!"

2. **Login with test account:**
   - Click "Login"
   - Enter same email/password
   - Should see dashboard with "No certificates yet"

3. **Add a certificate:**
   - Click "➕ Add Certificate"
   - Fill in details and submit
   - Should appear in dashboard

4. **Logout and login as different user:**
   - Click "🚪 Logout"
   - Create/login with different email
   - Confirm new user has empty certificate list

---

## Troubleshooting

### ❌ "Login error: Invalid email or password"
- Check email spelling
- Ensure password is at least 6 characters
- Verify Firebase Authentication is enabled

### ❌ "Missing 'firebase.api_key' in Streamlit secrets"
- Update `secrets.toml` with your Web API Key
- Must be added to `[firebase]` section

### ❌ "EmailAlreadyExistsError" when signing up
- Email already registered
- Use different email or login with existing account

### ❌ Certificates showing as empty after login
- This is correct! Each user starts with no certificates
- Add a new certificate using "➕ Add Certificate"

---

## Database Migration (Optional)

If you had certificates in the old shared database, you need to manually move them to user folders:

1. Get old certificates from: `certificates/`
2. Move to: `users/{your_user_id}/certificates/`
3. Using Firebase Console's data export/import feature

Or run this once after logging in:
```python
# In Firebase Console - Realtime Database:
# Manually drag old certificates to users/{your_uid}/certificates/
```

---

## Next Steps

✅ Setup complete! You now have:
- User authentication with login/signup
- User-scoped certificate storage
- Sessions that prevent cross-user visibility
- All original certificate tracking features

Enjoy your secure certificate tracker! 🎉
