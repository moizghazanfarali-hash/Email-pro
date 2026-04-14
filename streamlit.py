import streamlit as st
import pandas as pd
import csv
import os
from datetime import datetime
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage

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
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        html, body, [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
            color: #e2e8f0;
        }
        
        [data-testid="stHeader"] {
            background: transparent;
            border-bottom: 1px solid rgba(148, 163, 184, 0.2);
        }
        
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
            border-right: 1px solid rgba(148, 163, 184, 0.2);
        }
        
        .main-header {
            text-align: center;
            padding: 2rem 0;
            margin-bottom: 2rem;
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(168, 85, 247, 0.1));
            border-radius: 12px;
            border: 1px solid rgba(148, 163, 184, 0.1);
        }
        
        .main-header h1 {
            font-size: 2.5rem;
            background: linear-gradient(135deg, #60a5fa, #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            letter-spacing: -1px;
        }
        
        .main-header p {
            color: #94a3b8;
            margin-top: 0.5rem;
            font-size: 0.95rem;
        }
        
        .card {
            background: linear-gradient(135deg, #1e293b, #0f172a);
            border: 1px solid rgba(148, 163, 184, 0.2);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
        }
        
        .card:hover {
            border-color: rgba(148, 163, 184, 0.4);
            box-shadow: 0 8px 12px rgba(99, 102, 241, 0.2);
        }
        
        .section-title {
            font-size: 1.3rem;
            font-weight: 700;
            color: #e2e8f0;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid rgba(99, 102, 241, 0.3);
        }
        
        .success-box {
            background: linear-gradient(135deg, rgba(34, 197, 94, 0.1), rgba(34, 197, 94, 0.05));
            border-left: 4px solid #22c55e;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
        }
        
        .error-box {
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.1), rgba(239, 68, 68, 0.05));
            border-left: 4px solid #ef4444;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
        }
        
        .info-box {
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(59, 130, 246, 0.05));
            border-left: 4px solid #3b82f6;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
        }
        
        .stat-box {
            background: linear-gradient(135deg, #1e293b, #0f172a);
            border: 1px solid rgba(148, 163, 184, 0.2);
            padding: 1.5rem;
            border-radius: 10px;
            text-align: center;
        }
        
        .stat-number {
            font-size: 2rem;
            font-weight: 800;
            background: linear-gradient(135deg, #60a5fa, #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .stat-label {
            color: #94a3b8;
            font-size: 0.9rem;
            margin-top: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        button {
            transition: all 0.3s ease;
        }
        
        [data-testid="stButton"] > button {
            width: 100%;
            padding: 0.8rem 1rem;
            border-radius: 8px;
            font-weight: 600;
            border: none;
            transition: all 0.3s ease;
        }
        
        [data-testid="stButton"] > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(99, 102, 241, 0.3);
        }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State
if 'uploaded_df' not in st.session_state:
    st.session_state.uploaded_df = None
if 'total_sent' not in st.session_state:
    st.session_state.total_sent = 0
if 'total_failed' not in st.session_state:
    st.session_state.total_failed = 0

def send_personalized_email(to_email, subject, body):
    """Send email using Gmail SMTP"""
    try:
        SENDER_EMAIL = os.getenv("EMAIL_USER")
        APP_PASSWORD = os.getenv("EMAIL_PASS")
        
        if not SENDER_EMAIL or not APP_PASSWORD:
            return False, "Email credentials not found in .env file"
        
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = to_email
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(SENDER_EMAIL, APP_PASSWORD)
            smtp.send_message(msg)
        
        return True, "Email sent successfully"
    except Exception as e:
        return False, str(e)

# Main Header
st.markdown("""
    <div class="main-header">
        <h1>📧 EmailBlast Pro</h1>
        <p>Professional Email Campaign Manager | Personalized Bulk Messaging</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    
    sender_email = st.text_input("📧 Sender Email", type="password", help="Your Gmail address")
    app_password = st.text_input("🔐 App Password", type="password", help="Gmail App Password (not your regular password)")
    
    if st.button("💾 Save Credentials", use_container_width=True):
        # Save to .env file
        with open('.env', 'w') as f:
            f.write(f"EMAIL_USER={sender_email}\n")
            f.write(f"EMAIL_PASS={app_password}\n")
        st.success("✅ Credentials saved to .env file")
        load_dotenv()
    
    st.markdown("---")
    st.markdown("### 📊 Dashboard Stats")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
            <div class="stat-box">
                <div class="stat-number">{st.session_state.total_sent}</div>
                <div class="stat-label">Emails Sent</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="stat-box">
                <div class="stat-number">{st.session_state.total_failed}</div>
                <div class="stat-label">Failed</div>
            </div>
        """, unsafe_allow_html=True)

# Main Content
tab1, tab2, tab3 = st.tabs(["🚀 Campaign Manager", "📋 Preview", "📖 Documentation"])

with tab1:
    st.markdown('<div class="section-title">Campaign Setup</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 📤 Upload CSV File")
        uploaded_file = st.file_uploader(
            "Choose your CSV file",
            type=['csv'],
            help="CSV should have columns: email, name (optional for personalization)"
        )
        
        if uploaded_file is not None:
            st.session_state.uploaded_df = pd.read_csv(uploaded_file)
            st.success(f"✅ Loaded {len(st.session_state.uploaded_df)} contacts")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 📝 Email Template")
        
        subject = st.text_input(
            "Subject Line",
            placeholder="Enter email subject...",
            help="Use {name} to personalize"
        )
        
        email_body = st.text_area(
            "Email Body",
            placeholder="Write your email here...\n\nHi {name},\n\nYour message here...",
            height=200,
            help="Use {name} for personalization"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Email Sending Section
    if st.session_state.uploaded_df is not None:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 🎯 Send Campaign")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            send_all = st.checkbox("Send to All Contacts", value=False)
        
        with col2:
            if not send_all:
                num_to_send = st.number_input(
                    "Number to Send",
                    min_value=1,
                    max_value=len(st.session_state.uploaded_df),
                    value=min(5, len(st.session_state.uploaded_df))
                )
            else:
                num_to_send = len(st.session_state.uploaded_df)
        
        with col3:
            delay_seconds = st.number_input(
                "Delay (seconds)",
                min_value=0,
                max_value=10,
                value=1,
                help="Delay between emails to avoid rate limiting"
            )
        
        # Send Button
        if st.button("🚀 Send Campaign", use_container_width=True):
            if not subject or not email_body:
                st.error("❌ Please fill in subject and body")
            else:
                progress_bar = st.progress(0)
                status_placeholder = st.empty()
                results_placeholder = st.empty()
                
                sent_count = 0
                failed_count = 0
                failed_emails = []
                
                # Determine which rows to send
                rows_to_send = st.session_state.uploaded_df.head(num_to_send)
                
                for idx, row in rows_to_send.iterrows():
                    # Personalization
                    personalized_subject = subject
                    personalized_body = email_body
                    
                    if 'name' in row and pd.notna(row['name']):
                        personalized_subject = subject.replace("{name}", str(row['name']))
                        personalized_body = email_body.replace("{name}", str(row['name']))
                    
                    email = row['email']
                    
                    # Send email
                    success, message = send_personalized_email(email, personalized_subject, personalized_body)
                    
                    if success:
                        sent_count += 1
                        status = "✅"
                    else:
                        failed_count += 1
                        failed_emails.append((email, message))
                        status = "❌"
                    
                    # Update progress
                    progress = (idx + 1) / len(rows_to_send)
                    progress_bar.progress(progress)
                    status_placeholder.write(f"{status} Processed {idx + 1}/{len(rows_to_send)}: {email}")
                    
                    # Delay
                    if delay_seconds > 0 and idx < len(rows_to_send) - 1:
                        import time
                        time.sleep(delay_seconds)
                
                # Update session state
                st.session_state.total_sent += sent_count
                st.session_state.total_failed += failed_count
                
                # Results
                st.markdown('<div class="success-box">', unsafe_allow_html=True)
                st.markdown(f"### ✅ Campaign Completed")
                st.markdown(f"- **Sent:** {sent_count} emails")
                st.markdown(f"- **Failed:** {failed_count} emails")
                st.markdown('</div>', unsafe_allow_html=True)
                
                if failed_emails:
                    with st.expander("📋 Failed Emails Details"):
                        for email, error in failed_emails:
                            st.markdown(f"<div class='error-box'><b>{email}</b><br>{error}</div>", unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="section-title">Campaign Preview</div>', unsafe_allow_html=True)
    
    if st.session_state.uploaded_df is not None:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 📊 CSV Preview")
        st.dataframe(st.session_state.uploaded_df.head(10), use_container_width=True)
        
        st.markdown(f"**Total Rows:** {len(st.session_state.uploaded_df)}")
        st.markdown(f"**Columns:** {', '.join(st.session_state.uploaded_df.columns.tolist())}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Sample Email Preview
        if st.session_state.uploaded_df is not None and len(st.session_state.uploaded_df) > 0:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("#### 📧 Sample Email Preview")
            
            sample_idx = st.slider("Select sample contact", 0, len(st.session_state.uploaded_df) - 1)
            sample_row = st.session_state.uploaded_df.iloc[sample_idx]
            
            sample_name = sample_row.get('name', 'User') if 'name' in sample_row and pd.notna(sample_row['name']) else 'User'
            
            # Display sample
            st.markdown(f"**To:** {sample_row['email']}")
            st.divider()
            
            if 'subject' in st.session_state:
                subject_preview = st.session_state.get('last_subject', 'Sample Subject').replace("{name}", str(sample_name))
                st.markdown(f"**Subject:** {subject_preview}")
            
            if 'body' in st.session_state:
                body_preview = st.session_state.get('last_body', 'Sample body').replace("{name}", str(sample_name))
                st.markdown(f"**Body:**\n\n{body_preview}")
            
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("📌 Upload a CSV file in the Campaign Manager tab to see preview")
        st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="section-title">Documentation</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
    
    ### 🎯 How to Use EmailBlast Pro
    
    #### Step 1: Set Up Credentials
    1. Go to your Gmail account settings
    2. Enable 2-Factor Authentication
    3. Generate an "App Password" (16 characters)
    4. Copy it and paste in the sidebar
    5. Click "Save Credentials"
    
    #### Step 2: Prepare Your CSV
    Your CSV file should have:
    - **email** column (required) - Contact email addresses
    - **name** column (optional) - Use {name} in your template for personalization
    
    Example CSV:
    ```
    email,name
    john@example.com,John Doe
    jane@example.com,Jane Smith
    ```
    
    #### Step 3: Create Your Campaign
    1. Upload your CSV file
    2. Write your subject line
    3. Write your email body
    4. Use {name} placeholders for personalization
    
    #### Step 4: Send Campaign
    1. Choose number of contacts to send to
    2. Set delay between emails (recommended: 1-2 seconds)
    3. Click "Send Campaign"
    4. Monitor progress in real-time
    
    ### ⚠️ Important Notes
    
    - **Gmail Limits:** Gmail allows ~500 emails per day from personal accounts
    - **Delay:** Use 1-2 second delays to avoid rate limiting
    - **Test First:** Send to 1-2 contacts before full campaign
    - **App Password:** Use Gmail App Password, NOT your regular password
    - **2FA Required:** Gmail requires 2-Factor Authentication
    
    ### 🔐 Security
    
    - Credentials are stored locally in .env file
    - Never share your App Password
    - Don't commit .env file to version control
    
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #94a3b8; font-size: 0.85rem; margin-top: 2rem;'>
    <p>EmailBlast Pro v1.0 | Built with Streamlit | © 2024</p>
    <p>Made with ❤️ for professional email campaigns</p>
    </div>
""", unsafe_allow_html=True)