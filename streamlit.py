import streamlit as st
import pandas as pd
import csv
import os
import time
from datetime import datetime
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage

# Load existing environment variables
load_dotenv()

# Page Configuration
st.set_page_config(
    page_title="EmailBlast Pro",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Modern Design
st.markdown("""
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        html, body, [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
            color: #e2e8f0;
        }
        [data-testid="stHeader"] { background: transparent; border-bottom: 1px solid rgba(148, 163, 184, 0.2); }
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
            border-right: 1px solid rgba(148, 163, 184, 0.2);
        }
        .main-header {
            text-align: center; padding: 2rem 0; margin-bottom: 2rem;
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(168, 85, 247, 0.1));
            border-radius: 12px; border: 1px solid rgba(148, 163, 184, 0.1);
        }
        .main-header h1 {
            font-size: 2.5rem; background: linear-gradient(135deg, #60a5fa, #a78bfa);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            font-weight: 800; letter-spacing: -1px;
        }
        .card {
            background: linear-gradient(135deg, #1e293b, #0f172a);
            border: 1px solid rgba(148, 163, 184, 0.2);
            border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem;
        }
        .section-title {
            font-size: 1.3rem; font-weight: 700; color: #e2e8f0;
            margin-bottom: 1rem; padding-bottom: 0.5rem;
            border-bottom: 2px solid rgba(99, 102, 241, 0.3);
        }
        .success-box { background: rgba(34, 197, 94, 0.1); border-left: 4px solid #22c55e; padding: 1rem; border-radius: 8px; margin: 1rem 0; }
        .error-box { background: rgba(239, 68, 68, 0.1); border-left: 4px solid #ef4444; padding: 1rem; border-radius: 8px; margin: 1rem 0; }
        .stat-box { background: #1e293b; border: 1px solid rgba(148, 163, 184, 0.2); padding: 1rem; border-radius: 10px; text-align: center; }
        .stat-number { font-size: 1.8rem; font-weight: 800; color: #60a5fa; }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State
if 'uploaded_df' not in st.session_state: st.session_state.uploaded_df = None
if 'total_sent' not in st.session_state: st.session_state.total_sent = 0
if 'total_failed' not in st.session_state: st.session_state.total_failed = 0
if 'last_subject' not in st.session_state: st.session_state.last_subject = ""
if 'last_body' not in st.session_state: st.session_state.last_body = ""

def send_personalized_email(to_email, subject, body):
    try:
        sender_email = os.getenv("EMAIL_USER")
        app_password = os.getenv("EMAIL_PASS")
        
        if not sender_email or not app_password:
            return False, "Credentials missing in .env"
        
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = to_email
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, app_password)
            smtp.send_message(msg)
        return True, "Sent"
    except Exception as e:
        return False, str(e)

# Main Header
st.markdown('<div class="main-header"><h1>📧 EmailBlast Pro</h1><p>Professional Email Campaign Manager</p></div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    s_email = st.text_input("📧 Sender Email", value=os.getenv("EMAIL_USER", ""), type="default")
    a_pass = st.text_input("🔐 App Password", value=os.getenv("EMAIL_PASS", ""), type="password")
    
    if st.button("💾 Save Credentials", use_container_width=True):
        with open('.env', 'w') as f:
            f.write(f"EMAIL_USER={s_email}\nEMAIL_PASS={a_pass}\n")
        st.success("Credentials Saved!")
        load_dotenv()
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    col1.markdown(f'<div class="stat-box"><div class="stat-number">{st.session_state.total_sent}</div>Sent</div>', unsafe_allow_html=True)
    col2.markdown(f'<div class="stat-box"><div class="stat-number">{st.session_state.total_failed}</div>Failed</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🚀 Campaign", "📋 Preview", "📖 Help"])

with tab1:
    st.markdown('<div class="section-title">Setup Campaign</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        u_file = st.file_uploader("Upload CSV", type=['csv'])
        if u_file:
            df = pd.read_csv(u_file)
            # CRITICAL: Clean column names to prevent KeyError
            df.columns = df.columns.str.strip().str.lower()
            st.session_state.uploaded_df = df
            st.success(f"Loaded {len(df)} contacts. Columns: {list(df.columns)}")
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        subj = st.text_input("Subject", placeholder="Hello {name}...")
        body = st.text_area("Body", placeholder="Hi {name}, how are you?", height=150)
        st.session_state.last_subject = subj
        st.session_state.last_body = body
        st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.uploaded_df is not None:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        send_all = st.checkbox("Send to All")
        num = len(st.session_state.uploaded_df) if send_all else st.number_input("Limit", 1, len(st.session_state.uploaded_df), 5)
        delay = st.slider("Delay (sec)", 0, 5, 1)

        if st.button("🚀 Start Campaign", use_container_width=True):
            if 'email' not in st.session_state.uploaded_df.columns:
                st.error("CSV must have an 'email' column!")
            else:
                prog = st.progress(0)
                status = st.empty()
                
                rows = st.session_state.uploaded_df.head(num)
                s_count, f_count = 0, 0
                
                for idx, row in rows.iterrows():
                    name = str(row.get('name', 'User'))
                    target_email = str(row['email'])
                    
                    p_subj = subj.replace("{name}", name)
                    p_body = body.replace("{name}", name)
                    
                    ok, msg = send_personalized_email(target_email, p_subj, p_body)
                    if ok: s_count += 1
                    else: f_count += 1; st.error(f"Failed {target_email}: {msg}")
                    
                    prog.progress((idx + 1) / num)
                    status.text(f"Processing {idx+1}/{num}: {target_email}")
                    time.sleep(delay)
                
                st.session_state.total_sent += s_count
                st.session_state.total_failed += f_count
                st.balloons()
                st.success(f"Done! Sent: {s_count}, Failed: {f_count}")
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    if st.session_state.uploaded_df is not None:
        st.write("### Data Preview")
        st.dataframe(st.session_state.uploaded_df.head(5))
        
        st.write("### Sample Message Preview")
        idx = st.number_input("Sample Row Index", 0, len(st.session_state.uploaded_df)-1, 0)
        sample = st.session_state.uploaded_df.iloc[idx]
        
        # Safe access to columns
        s_name = str(sample.get('name', 'User'))
        s_mail = str(sample.get('email', 'missing@mail.com'))
        
        st.info(f"**To:** {s_mail}")
        st.markdown(f"**Subject:** {st.session_state.last_subject.replace('{name}', s_name)}")
        st.text_area("Body Preview", st.session_state.last_body.replace('{name}', s_name), height=100)
    else:
        st.warning("Please upload a CSV file first.")

with tab3:
    st.markdown("""
    ### 📖 Quick Guide
    1. **CSV Format:** Must have an `email` column. `name` is optional.
    2. **Placeholders:** Use `{name}` in subject or body.
    3. **Gmail setup:** Use an **App Password**, not your main password. 2FA must be ON.
    """)
