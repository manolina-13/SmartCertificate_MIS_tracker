import streamlit as st
import pandas as pd
import datetime as dt
from utils import add_certificate, get_certificates, delete_certificate, edit_certificate
import io

st.set_page_config(page_title="MIS Certificate Tracker", layout="wide")
st.title("📜 MIS Certificate Tracker")
ALERT_DAYS = 20

# ===== SIDEBAR =====
with st.sidebar:
    st.header("Navigation")
    page = st.radio("Select Action", ["📊 Dashboard", "➕ Add Certificate", "✏️ Manage Certificates"])
    
    st.divider()
    
    # Fetch certificates
    df = get_certificates()
    
    if not df.empty:
        df["Maturity_Date"] = pd.to_datetime(df["Maturity_Date"])
        today_ts = pd.Timestamp(dt.date.today())
        df["Days_Left"] = (df["Maturity_Date"].dt.normalize() - today_ts).dt.days
        df["Time_Left"] = df["Days_Left"].apply(
            lambda d: "Matured" if d < 0 else ("Today" if d == 0 else f"{d} day(s)")
        )
        
        # Summary stats
        due = df[df["Days_Left"] <= ALERT_DAYS]
        st.metric("Total Certificates", len(df))
        st.metric("Due Soon (<20 days)", len(due), delta=None)
        
        st.divider()
        st.subheader("Certificate Quick View")
        
        # Search/filter
        search_text = st.text_input("🔍 Search by cert #", placeholder="e.g., CERT001")
        sort_by = st.selectbox("Sort by", ["Certificate #", "Maturity Date", "Amount"])
        
        if search_text:
            filtered_df = df[df["Certificate_Number"].str.contains(search_text, case=False, na=False)]
        else:
            filtered_df = df.copy()
        
        # Sorting
        if sort_by == "Maturity Date":
            filtered_df = filtered_df.sort_values("Maturity_Date")
        elif sort_by == "Amount":
            filtered_df = filtered_df.sort_values("Amount", ascending=False)
        else:
            filtered_df = filtered_df.sort_values("Certificate_Number")
        
        # Display list with color coding
        for idx, row in filtered_df.iterrows():
            status_emoji = "🔴" if row["Days_Left"] <= ALERT_DAYS else "🟢"
            status_text = f"Due in {row['Days_Left']}d" if row["Days_Left"] > 0 else "Due Today"
            st.write(f"{status_emoji} {row['Certificate_Number']} | {status_text}")

# ===== MAIN AREA =====
if page == "📊 Dashboard":
    st.subheader("Certificate Tracker Dashboard")
    
    if not df.empty:
        df["Maturity_Date"] = pd.to_datetime(df["Maturity_Date"])
        today_ts = pd.Timestamp(dt.date.today())
        df["Days_Left"] = (df["Maturity_Date"].dt.normalize() - today_ts).dt.days
        df["Time_Left"] = df["Days_Left"].apply(
            lambda d: "Matured" if d < 0 else ("Today" if d == 0 else f"{d} day(s)")
        )
        
        # Alert banner
        due = df[df["Days_Left"] <= ALERT_DAYS]
        if not due.empty:
            st.error(f"🔔 **{len(due)} certificate(s) maturing in {ALERT_DAYS} days or less!**")
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Certificates", len(df))
        col2.metric("Total Amount", f"₹{df['Amount'].sum():,.0f}")
        col3.metric("Average Days Left", f"{df['Days_Left'].mean():.0f}")
        col4.metric("Due Soon", len(due))
        
        st.divider()
        
        # Full certificates table with progress bars
        st.subheader("All Certificates")
        display_df = df[["Certificate_Number", "Amount", "Maturity_Date", "Days_Left", "Time_Left"]].copy()
        display_df["Maturity_Date"] = display_df["Maturity_Date"].dt.strftime("%Y-%m-%d")
        
        # Color rows based on urgency
        def highlight_due(row):
            if row["Days_Left"] <= ALERT_DAYS:
                return ['background-color: #ffcccc'] * len(row)
            elif row["Days_Left"] <= 30:
                return ['background-color: #fff3cd'] * len(row)
            else:
                return ['background-color: #d4edda'] * len(row)
        
        st.dataframe(
            display_df.style.apply(highlight_due, axis=1),
            use_container_width=True
        )
        
        # Due certificates with progress bars
        if not due.empty:
            st.warning(f"⚠️ **Certificates Due Soon ({ALERT_DAYS} days)**")
            for idx, row in due.iterrows():
                col1, col2 = st.columns([3, 1])
                with col1:
                    progress = max(0, min(1, 1 - (row["Days_Left"] / ALERT_DAYS)))
                    st.progress(progress, text=f"{row['Certificate_Number']} - {row['Days_Left']} days")
                with col2:
                    st.write(f"₹{row['Amount']:,.0f}")
        
        # Export button
        st.divider()
        csv = display_df.to_csv(index=False)
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name=f"certificates_{dt.date.today()}.csv",
            mime="text/csv"
        )
    else:
        st.info("No certificates yet. Add one to get started!")

elif page == "➕ Add Certificate":
    st.subheader("Add New Certificate")
    
    with st.form("add_cert_form"):
        col1, col2 = st.columns(2)
        with col1:
            cert_no = st.text_input("Certificate Number *", placeholder="e.g., CERT001")
            issue_date = st.date_input("Issue Date *")
        with col2:
            amount = st.number_input("Amount (₹) *", min_value=0.0, step=1000.0)
            maturity_date = st.date_input("Maturity Date *")
        
        submitted = st.form_submit_button("➕ Add Certificate", use_container_width=True)
        
        if submitted:
            cert_no_clean = (cert_no or "").strip()
            if not cert_no_clean:
                st.error("Certificate Number is required.")
            elif maturity_date < issue_date:
                st.error("Maturity Date cannot be earlier than Issue Date.")
            else:
                add_certificate(cert_no_clean, amount, issue_date, maturity_date)
                st.success("✅ Certificate added successfully!")
                st.rerun()

elif page == "✏️ Manage Certificates":
    st.subheader("Manage Certificates")
    
    if df.empty:
        st.info("No certificates to manage.")
    else:
        df["Maturity_Date"] = pd.to_datetime(df["Maturity_Date"])
        today_ts = pd.Timestamp(dt.date.today())
        df["Days_Left"] = (df["Maturity_Date"].dt.normalize() - today_ts).dt.days
        
        # Certificate selection
        options = {
            f"{row['Certificate_Number']} | ₹{row['Amount']} (Maturity: {row['Maturity_Date'].strftime('%Y-%m-%d')})": row["Key"]
            for _, row in df.iterrows()
        }
        
        selected = st.selectbox("Select Certificate to Manage", list(options.keys()))
        key = options[selected]
        selected_row = df.loc[df["Key"] == key].iloc[0]
        
        # Display current details
        st.info(f"**Current Details**: Cert #{selected_row['Certificate_Number']} | Amount: ₹{selected_row['Amount']}")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Edit Certificate")
            with st.form("edit_cert_form"):
                new_cert_no = st.text_input("Certificate Number", value=selected_row["Certificate_Number"])
                new_cert_no_clean = (new_cert_no or "").strip()
                
                col_a, col_b = st.columns(2)
                with col_a:
                    new_amount = st.number_input("Amount (₹)", value=float(selected_row["Amount"]), step=1000.0)
                    new_issue = st.date_input("Issue Date", value=pd.to_datetime(selected_row["Issue_Date"]))
                with col_b:
                    new_maturity = st.date_input("Maturity Date", value=pd.to_datetime(selected_row["Maturity_Date"]))
                
                submitted_edit = st.form_submit_button("💾 Save Changes", use_container_width=True)
                
                if submitted_edit:
                    if not new_cert_no_clean:
                        st.error("Certificate Number is required.")
                    elif new_maturity < new_issue:
                        st.error("Maturity Date cannot be earlier than Issue Date.")
                    else:
                        edit_certificate(key, new_cert_no_clean, new_amount, new_issue, new_maturity)
                        st.success("✏️ Certificate updated successfully!")
                        st.rerun()
        
        with col2:
            st.subheader("Delete")
            st.warning("Deleting cannot be undone!")
            if st.button("🗑️ Delete Certificate", use_container_width=True):
                delete_certificate(key)
                st.success("Certificate deleted!")
                st.rerun()
