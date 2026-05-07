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
    page_title="Send Quick Email",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Professional Light Theme
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

        * { margin: 0; padding: 0; box-sizing: border-box; }

        html, body, [data-testid="stAppViewContainer"] {
            background: #f4f1ec;
            color: #1a1a2e;
            font-family: 'DM Sans', sans-serif;
        }

        [data-testid="stHeader"] {
            background: #f4f1ec;
            border-bottom: 1px solid #d6cfc3;
        }

        [data-testid="stSidebar"] {
            background: #ffffff;
            border-right: 2px solid #e8e0d5;
        }

        [data-testid="stSidebar"] > div {
            padding: 1.5rem 1.2rem;
        }

        /* Main Header */
        .main-header {
            text-align: left;
            padding: 2.5rem 2rem 2rem 2rem;
            margin-bottom: 2rem;
            background: #ffffff;
            border-radius: 16px;
            border: 1px solid #e2d9cc;
            box-shadow: 0 2px 20px rgba(0,0,0,0.05);
            display: flex;
            align-items: center;
            gap: 1.5rem;
            position: relative;
            overflow: hidden;
        }

        .main-header::before {
            content: '';
            position: absolute;
            top: 0; right: 0;
            width: 300px; height: 100%;
            background: linear-gradient(135deg, #fef3e2 0%, #fde8c8 100%);
            clip-path: polygon(30% 0%, 100% 0%, 100% 100%, 0% 100%);
        }

        .header-icon {
            font-size: 3rem;
            background: #1a1a2e;
            width: 72px; height: 72px;
            border-radius: 18px;
            display: flex; align-items: center; justify-content: center;
            flex-shrink: 0;
            z-index: 1;
        }

        .header-text { z-index: 1; }

        .main-header h1 {
            font-family: 'Playfair Display', serif;
            font-size: 2.2rem;
            color: #1a1a2e;
            font-weight: 700;
            letter-spacing: -0.5px;
            line-height: 1.1;
        }

        .main-header p {
            color: #7a6f5e;
            font-size: 0.95rem;
            margin-top: 0.3rem;
            font-weight: 400;
        }

        /* Cards */
        .card {
            background: #ffffff;
            border: 1px solid #e2d9cc;
            border-radius: 14px;
            padding: 1.8rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 1px 8px rgba(0,0,0,0.04);
            transition: box-shadow 0.2s ease;
        }

        .card:hover {
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        }

        .section-title {
            font-family: 'Playfair Display', serif;
            font-size: 1.2rem;
            font-weight: 600;
            color: #1a1a2e;
            margin-bottom: 1.2rem;
            padding-bottom: 0.7rem;
            border-bottom: 2px solid #f0e8de;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .section-title .dot {
            width: 8px; height: 8px;
            background: #c8703a;
            border-radius: 50%;
            display: inline-block;
        }

        /* Stats */
        .stat-box {
            background: #f9f6f1;
            border: 1px solid #e2d9cc;
            padding: 1.2rem 1rem;
            border-radius: 12px;
            text-align: center;
        }

        .stat-number {
            font-size: 2rem;
            font-weight: 700;
            color: #c8703a;
            font-family: 'Playfair Display', serif;
            line-height: 1;
        }

        .stat-label {
            font-size: 0.75rem;
            color: #7a6f5e;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-top: 0.3rem;
            font-weight: 500;
        }

        /* Sidebar sections */
        .sidebar-section-title {
            font-size: 0.7rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            color: #9e917f;
            margin-bottom: 0.8rem;
            margin-top: 1.5rem;
        }

        /* Badge */
        .badge {
            display: inline-block;
            background: #fef3e2;
            color: #c8703a;
            border: 1px solid #f5dab4;
            border-radius: 999px;
            padding: 0.2rem 0.75rem;
            font-size: 0.75rem;
            font-weight: 600;
        }

        /* Status messages */
        .success-box {
            background: #f0faf4;
            border-left: 3px solid #3baa6d;
            padding: 0.9rem 1.2rem;
            border-radius: 0 8px 8px 0;
            margin: 1rem 0;
            font-size: 0.9rem;
            color: #1f5c3a;
        }

        .error-box {
            background: #fdf3f3;
            border-left: 3px solid #e05c5c;
            padding: 0.9rem 1.2rem;
            border-radius: 0 8px 8px 0;
            margin: 1rem 0;
            font-size: 0.9rem;
            color: #7a2020;
        }

        /* Divider */
        .divider {
            height: 1px;
            background: linear-gradient(90deg, transparent, #d6cfc3, transparent);
            margin: 1.5rem 0;
        }

        /* Streamlit overrides */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            background: #faf8f5 !important;
            border: 1.5px solid #d6cfc3 !important;
            border-radius: 10px !important;
            color: #1a1a2e !important;
            font-family: 'DM Sans', sans-serif !important;
        }

        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: #c8703a !important;
            box-shadow: 0 0 0 3px rgba(200, 112, 58, 0.12) !important;
        }

        .stButton > button {
            background: #1a1a2e !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 10px !important;
            font-family: 'DM Sans', sans-serif !important;
            font-weight: 600 !important;
            font-size: 0.9rem !important;
            padding: 0.65rem 1.5rem !important;
            transition: all 0.2s ease !important;
        }

        .stButton > button:hover {
            background: #c8703a !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 14px rgba(200, 112, 58, 0.3) !important;
        }

        .stProgress > div > div {
            background: linear-gradient(90deg, #c8703a, #e8924a) !important;
            border-radius: 999px !important;
        }

        .stProgress > div {
            background: #f0e8de !important;
            border-radius: 999px !important;
        }

        .stFileUploader > div {
            background: #faf8f5 !important;
            border: 2px dashed #d6cfc3 !important;
            border-radius: 12px !important;
        }

        .stFileUploader > div:hover {
            border-color: #c8703a !important;
        }

        .stTabs [data-baseweb="tab-list"] {
            background: #f4f1ec !important;
            border-radius: 12px !important;
            padding: 4px !important;
            gap: 4px !important;
        }

        .stTabs [data-baseweb="tab"] {
            background: transparent !important;
            border-radius: 8px !important;
            color: #7a6f5e !important;
            font-family: 'DM Sans', sans-serif !important;
            font-weight: 500 !important;
        }

        .stTabs [aria-selected="true"] {
            background: #ffffff !important;
            color: #1a1a2e !important;
            font-weight: 600 !important;
            box-shadow: 0 1px 6px rgba(0,0,0,0.08) !important;
        }

        .stSlider > div > div > div > div {
            background: #c8703a !important;
        }

        .stCheckbox > label {
            color: #1a1a2e !important;
            font-family: 'DM Sans', sans-serif !important;
        }

        label {
            color: #4a4035 !important;
            font-size: 0.88rem !important;
            font-weight: 500 !important;
        }

        .stSelectbox > div > div {
            background: #faf8f5 !important;
            border: 1.5px solid #d6cfc3 !important;
            border-radius: 10px !important;
        }

        [data-testid="stNumberInput"] > div > div > input {
            background: #faf8f5 !important;
            border: 1.5px solid #d6cfc3 !important;
            border-radius: 10px !important;
        }

        .stDataFrame {
            border-radius: 12px !important;
            overflow: hidden !important;
            border: 1px solid #e2d9cc !important;
        }

        /* Alert overrides */
        [data-testid="stAlert"] {
            border-radius: 10px !important;
        }

        /* Scrollbar */
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: #f4f1ec; }
        ::-webkit-scrollbar-thumb { background: #c8b8a2; border-radius: 999px; }
        ::-webkit-scrollbar-thumb:hover { background: #a8987e; }
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
st.markdown("""
    <div class="main-header">
        <div class="header-icon">📧</div>
        <div class="header-text">
            <h1>Send Quick Email</h1>
            <p>Professional Email Campaign Manager — Send smarter, reach further</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown('<div class="sidebar-section-title">📬 Sender Configuration</div>', unsafe_allow_html=True)
    s_email = st.text_input("Email Address", value=os.getenv("EMAIL_USER", ""), placeholder="you@gmail.com")
    a_pass = st.text_input("App Password", value=os.getenv("EMAIL_PASS", ""), type="password", placeholder="••••••••••••••••")

    if st.button("💾 Save Credentials", use_container_width=True):
        with open('.env', 'w') as f:
            f.write(f"EMAIL_USER={s_email}\nEMAIL_PASS={a_pass}\n")
        st.success("✓ Credentials saved successfully!")
        load_dotenv()

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section-title">📊 Session Stats</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
            <div class="stat-box">
                <div class="stat-number">{st.session_state.total_sent}</div>
                <div class="stat-label">Sent</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div class="stat-box">
                <div class="stat-number" style="color:#c0392b;">{st.session_state.total_failed}</div>
                <div class="stat-label">Failed</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Connection status
    if os.getenv("EMAIL_USER") and os.getenv("EMAIL_PASS"):
        st.markdown('<span class="badge">✓ Configured</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="badge" style="background:#fdf3f3;color:#e05c5c;border-color:#f5c0c0;">⚠ Not Configured</span>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🚀  Campaign", "  📋  Preview", "  📖  Help"])

with tab1:
    st.markdown('<div class="section-title"><span class="dot"></span> Setup Your Campaign</div>', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1], gap="large")

    with c1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("**📁 Contact List**")
        st.caption("Upload a CSV with at least an `email` column. A `name` column enables personalization.")
        u_file = st.file_uploader("Upload CSV file", type=['csv'], label_visibility="collapsed")
        if u_file:
            df = pd.read_csv(u_file)
            df.columns = df.columns.str.strip().str.lower()
            st.session_state.uploaded_df = df
            st.success(f"✓ {len(df)} contacts loaded")
            st.caption(f"Columns detected: `{'`, `'.join(df.columns)}`")
        elif st.session_state.uploaded_df is not None:
            st.info(f"Using previously uploaded file — {len(st.session_state.uploaded_df)} contacts")
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("**✍️ Message Composer**")
        st.caption("Use `{name}` as a placeholder for personalized greetings.")
        subj = st.text_input("Subject Line", placeholder="Hello {name}, we have something for you!")
        body = st.text_area("Email Body", placeholder="Hi {name},\n\nWe wanted to reach out personally...", height=160)
        st.session_state.last_subject = subj
        st.session_state.last_body = body
        st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.uploaded_df is not None:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title"><span class="dot"></span> Campaign Settings</div>', unsafe_allow_html=True)

        col_a, col_b, col_c = st.columns([1, 1, 1])
        with col_a:
            send_all = st.checkbox("Send to all contacts", value=False)
        with col_b:
            num = len(st.session_state.uploaded_df) if send_all else st.number_input(
                "Number of recipients", 1, len(st.session_state.uploaded_df), min(5, len(st.session_state.uploaded_df))
            )
        with col_c:
            delay = st.slider("Delay between emails (sec)", 0, 5, 1)

        st.markdown('<div style="margin-top: 1rem;"></div>', unsafe_allow_html=True)

        if st.button("🚀 Launch Campaign", use_container_width=True):
            if 'email' not in st.session_state.uploaded_df.columns:
                st.error("⚠️ Your CSV must contain an `email` column.")
            elif not subj.strip() or not body.strip():
                st.error("⚠️ Please fill in both the subject and body before sending.")
            else:
                prog = st.progress(0)
                status = st.empty()
                rows = st.session_state.uploaded_df.head(int(num))
                s_count, f_count = 0, 0

                for i, (idx, row) in enumerate(rows.iterrows()):
                    name = str(row.get('name', 'User'))
                    target_email = str(row['email'])

                    p_subj = subj.replace("{name}", name)
                    p_body = body.replace("{name}", name)

                    ok, msg = send_personalized_email(target_email, p_subj, p_body)
                    if ok:
                        s_count += 1
                    else:
                        f_count += 1
                        st.markdown(f'<div class="error-box">✗ Failed — {target_email}: {msg}</div>', unsafe_allow_html=True)

                    prog.progress((i + 1) / int(num))
                    status.caption(f"Processing {i+1} of {int(num)}: {target_email}")
                    time.sleep(delay)

                st.session_state.total_sent += s_count
                st.session_state.total_failed += f_count
                st.balloons()
                st.markdown(f'<div class="success-box">✓ Campaign complete — <strong>{s_count} sent</strong>, {f_count} failed</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    if st.session_state.uploaded_df is not None:
        st.markdown('<div class="section-title"><span class="dot"></span> Data Preview</div>', unsafe_allow_html=True)
        st.dataframe(st.session_state.uploaded_df.head(5), use_container_width=True)

        st.markdown('<div style="margin-top: 1.5rem;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title"><span class="dot"></span> Message Preview</div>', unsafe_allow_html=True)

        max_idx = max(0, len(st.session_state.uploaded_df) - 1)
        idx = st.number_input("Preview row index", 0, max_idx, 0)
        sample = st.session_state.uploaded_df.iloc[idx]

        s_name = str(sample.get('name', 'User'))
        s_mail = str(sample.get('email', 'missing@mail.com'))

        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(f"**To:** `{s_mail}`")
            st.markdown(f"**Name:** `{s_name}`")
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(f"**Subject:** {st.session_state.last_subject.replace('{name}', s_name) or '(no subject entered)'}")
            st.markdown("**Body:**")
            st.text_area(
                "Preview",
                st.session_state.last_body.replace('{name}', s_name) or "(no body entered)",
                height=120,
                disabled=True,
                label_visibility="collapsed"
            )
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("📋 Upload a CSV file in the Campaign tab to preview your messages.")

with tab3:
    st.markdown('<div class="section-title"><span class="dot"></span> Quick Start Guide</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("**📄 CSV Format**")
        st.caption("Your CSV file must follow this structure:")
        st.code("email,name\njohn@example.com,John\njane@example.com,Jane", language="csv")
        st.markdown("- `email` column is **required**")
        st.markdown("- `name` column is optional but recommended")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("**✏️ Personalization**")
        st.caption("Use `{name}` anywhere in your subject or body:")
        st.code("Subject: Hello {name}!\n\nBody: Hi {name}, we have an\nexclusive offer just for you.", language="text")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("**🔐 Gmail App Password Setup**")
    st.markdown("""
    1. Go to your Google Account → **Security**
    2. Enable **2-Step Verification** if not already on
    3. Search for **App passwords** in the search bar
    4. Create a new app password for "Mail"
    5. Copy the 16-character password and paste it in the sidebar
    """)
    st.warning("⚠️ Never use your main Gmail password. Always use an App Password.")
    st.markdown('</div>', unsafe_allow_html=True)
