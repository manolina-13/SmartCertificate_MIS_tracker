import streamlit as st
import pandas as pd
import datetime as dt
from utils import add_certificate, get_certificates, delete_certificate, edit_certificate

st.set_page_config(page_title="MIS Certificate Tracker", layout="centered")
st.title("📜 MIS Certificate Tracker")
ALERT_DAYS = 20

# --- Form to Add Certificate ---
with st.form("mis_form"):
    cert_no = st.text_input("Certificate Number")
    cert_no_clean = (cert_no or "").strip()
    amount = st.number_input("Amount (₹)", min_value=0.0)
    issue_date = st.date_input("Issue Date")
    maturity_date = st.date_input("Maturity Date")
    submitted = st.form_submit_button("Add Certificate")
    
    if submitted:
        if not cert_no_clean:
            st.error("Certificate Number is required.")
        elif maturity_date < issue_date:
            st.error("Maturity Date cannot be earlier than Issue Date.")
        else:
            add_certificate(cert_no_clean, amount, issue_date, maturity_date)
            st.success("✅ Certificate added successfully!")
            st.rerun()

# --- Display Certificates ---
st.subheader("📅 All Certificates")
df = get_certificates()

# Calculate Days Left
if not df.empty:
    df["Maturity_Date"] = pd.to_datetime(df["Maturity_Date"])
    today_ts = pd.Timestamp(dt.date.today())
    df["Days_Left"] = (df["Maturity_Date"].dt.normalize() - today_ts).dt.days
    df["Time_Left"] = df["Days_Left"].apply(
        lambda d: "Matured" if d < 0 else ("Today" if d == 0 else f"{d} day(s)")
    )

    due = df[df["Days_Left"] <= ALERT_DAYS]
    if not due.empty:
        st.error(f"🔔 {len(due)} certificate(s) are due in {ALERT_DAYS} days or less.")

    # Highlight certificates <= ALERT_DAYS days
    def highlight_due(row):
        return ['background-color: #FFCCCC' if row.Days_Left <= ALERT_DAYS else '' for _ in row]

    # Display full table with highlight
    st.dataframe(df.style.apply(highlight_due, axis=1))

    # Show warning table for due certificates
    if not due.empty:
        st.warning(f"⚠️ Certificates maturing in {ALERT_DAYS} days or less!")
        st.dataframe(due.drop(columns=["Key"]))

# --- Edit/Delete Section ---
st.subheader("✏️ Edit or Delete Certificate")
if not df.empty:
    options = {
        f"{row['Certificate_Number']} | ₹{row['Amount']} | {row['Key'][:8]}": row["Key"]
        for _, row in df.iterrows()
    }
    selected = st.selectbox("Select certificate", list(options.keys()))
    key = options[selected]
    selected_row = df.loc[df["Key"] == key].iloc[0]

    # Delete button
    if st.button("Delete"):
        delete_certificate(key)
        st.success("🗑️ Certificate deleted successfully!")
        st.rerun()

    # Edit form
    with st.form("edit_form"):
        new_cert_no = st.text_input("Certificate Number", value=selected_row["Certificate_Number"])
        new_cert_no_clean = (new_cert_no or "").strip()
        new_amount = st.number_input("Amount", value=float(selected_row["Amount"]))
        new_issue = st.date_input("Issue Date", value=pd.to_datetime(selected_row["Issue_Date"]))
        new_maturity = st.date_input("Maturity Date", value=pd.to_datetime(selected_row["Maturity_Date"]))
        submitted_edit = st.form_submit_button("Save Changes")
        
        if submitted_edit:
            if not new_cert_no_clean:
                st.error("Certificate Number is required.")
            elif new_maturity < new_issue:
                st.error("Maturity Date cannot be earlier than Issue Date.")
            else:
                edit_certificate(key, new_cert_no_clean, new_amount, new_issue, new_maturity)
                st.success("✏️ Certificate updated successfully!")
                st.rerun()
