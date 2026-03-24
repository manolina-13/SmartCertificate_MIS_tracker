import firebase_admin
import pandas as pd
import json
from typing import Any
import requests
from firebase_admin import credentials, db, auth
import streamlit as st

def init_firebase(firebase_secrets):
    database_url = firebase_secrets.get("database_url")
    if not database_url:
        raise ValueError(
            "Missing 'firebase.database_url' in Streamlit secrets. "
            "Example: https://<project-id>-default-rtdb.firebaseio.com"
        )

    service_account = firebase_secrets.get("service_account")
    if not service_account:
        raise ValueError("Missing 'firebase.service_account' in Streamlit secrets.")

    # Allow either a nested TOML table or JSON string in Streamlit secrets
    if isinstance(service_account, str):
        service_account = json.loads(service_account)
    else:
        service_account = dict(service_account)

    if not firebase_admin._apps:
        cred = credentials.Certificate(service_account)
        firebase_admin.initialize_app(cred, {"databaseURL": database_url})

import streamlit as st
init_firebase(st.secrets["firebase"])

# ===== AUTHENTICATION FUNCTIONS =====

def signup_user(email: str, password: str) -> dict:
    """Create a new user account in Firebase Authentication"""
    try:
        user = auth.create_user(email=email, password=password)
        return {"success": True, "uid": user.uid, "message": "Account created successfully!"}
    except auth.EmailAlreadyExistsError:
        return {"success": False, "message": "This email is already registered. Please login instead."}
    except ValueError as e:
        if "password" in str(e).lower():
            return {"success": False, "message": "Password must be at least 6 characters long."}
        return {"success": False, "message": f"Invalid input: {str(e)}"}
    except Exception as e:
        return {"success": False, "message": f"Error creating account: {str(e)}"}

def verify_login(email: str, password: str) -> dict:
    """Verify user credentials using Firebase REST API"""
    try:
        api_key = st.secrets["firebase"]["api_key"]
        rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
        
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        
        response = requests.post(
            rest_api_url,
            params={"key": api_key},
            json=payload
        )
        
        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "uid": data["localId"],
                "email": data["email"],
                "idToken": data["idToken"],
                "message": "Login successful!"
            }
        else:
            error_data = response.json()
            error_message = error_data.get("error", {}).get("message", "Invalid credentials")
            return {"success": False, "message": error_message}
    except Exception as e:
        return {"success": False, "message": f"Login error: {str(e)}"}

def logout_user():
    """Clear session state on logout"""
    if "user_id" in st.session_state:
        del st.session_state.user_id
    if "user_email" in st.session_state:
        del st.session_state.user_email
    if "auth_token" in st.session_state:
        del st.session_state.auth_token

# --- Certificate Functions (Updated for User-Specific Data) ---

def add_certificate(cert_no, amount, issue_date, maturity_date):
    """Add certificate for the logged-in user"""
    user_id = st.session_state.get("user_id")
    if not user_id:
        return {"success": False, "message": "User not authenticated"}
    
    data = {
        "Certificate_Number": cert_no,
        "Amount": float(amount),
        "Issue_Date": str(issue_date),
        "Maturity_Date": str(maturity_date),
        "user_id": user_id
    }
    
    try:
        new_ref = db.reference(f"users/{user_id}/certificates").push()
        new_ref.set(data)
        return {"success": True, "message": "Certificate added successfully!"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}

def get_certificates():
    """Get certificates for the logged-in user only"""
    user_id = st.session_state.get("user_id")
    if not user_id:
        return pd.DataFrame(columns=["Key", "Certificate_Number", "Amount", "Issue_Date", "Maturity_Date"])
    
    try:
        certs: Any = db.reference(f"users/{user_id}/certificates").get()
        if certs is None:
            return pd.DataFrame(columns=["Key", "Certificate_Number", "Amount", "Issue_Date", "Maturity_Date"])
        if not isinstance(certs, dict):
            return pd.DataFrame(columns=["Key", "Certificate_Number", "Amount", "Issue_Date", "Maturity_Date"])
        
        data = []
        for key, value in certs.items():
            if not isinstance(value, dict):
                continue
            record = value
            record["Key"] = key
            data.append(record)

        df = pd.DataFrame(data)
        # Reorder columns
        df = df[["Key", "Certificate_Number", "Amount", "Issue_Date", "Maturity_Date"]]
        return df
    except Exception as e:
        st.error(f"Error fetching certificates: {str(e)}")
        return pd.DataFrame(columns=["Key", "Certificate_Number", "Amount", "Issue_Date", "Maturity_Date"])

def delete_certificate(key):
    """Delete certificate for the logged-in user"""
    user_id = st.session_state.get("user_id")
    if not user_id:
        return {"success": False, "message": "User not authenticated"}
    
    try:
        db.reference(f"users/{user_id}/certificates").child(key).delete()
        return {"success": True, "message": "Certificate deleted successfully!"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}

def edit_certificate(key, cert_no, amount, issue_date, maturity_date):
    """Edit certificate for the logged-in user"""
    user_id = st.session_state.get("user_id")
    if not user_id:
        return {"success": False, "message": "User not authenticated"}
    
    data = {
        "Certificate_Number": cert_no,
        "Amount": float(amount),
        "Issue_Date": str(issue_date),
        "Maturity_Date": str(maturity_date),
        "user_id": user_id
    }
    
    try:
        db.reference(f"users/{user_id}/certificates").child(key).update(data)
        return {"success": True, "message": "Certificate updated successfully!"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
