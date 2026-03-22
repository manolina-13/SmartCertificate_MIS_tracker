import firebase_admin
import pandas as pd
import json
from typing import Any
from firebase_admin import credentials, db

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

# --- Certificate Functions ---

def add_certificate(cert_no, amount, issue_date, maturity_date):
    data = {
        "Certificate_Number": cert_no,
        "Amount": float(amount),
        "Issue_Date": str(issue_date),
        "Maturity_Date": str(maturity_date)
    }
    new_ref = db.reference("certificates").push()
    new_ref.set(data)

def get_certificates():
    certs: Any = db.reference("certificates").get()
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

def delete_certificate(key):
    db.reference("certificates").child(key).delete()

def edit_certificate(key, cert_no, amount, issue_date, maturity_date):
    data = {
        "Certificate_Number": cert_no,
        "Amount": float(amount),
        "Issue_Date": str(issue_date),
        "Maturity_Date": str(maturity_date)
    }
    db.reference("certificates").child(key).update(data)
