EmailBlast Pro Setup Guide

Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Gmail account with 2-Factor Authentication enabled
- Text editor or IDE

Installation Steps

Step 1: Clone Repository

git clone https://github.com/yourusername/emailblast-pro.git
cd emailblast-pro

Step 2: Create Virtual Environment

On Windows:
python -m venv venv
venv\Scripts\activate

On macOS/Linux:
python3 -m venv venv
source venv/bin/activate

Step 3: Install Dependencies

pip install -r requirements.txt

This will install:
- streamlit (UI framework)
- pandas (data handling)
- python-dotenv (environment variables)

Step 4: Gmail Configuration

Go to https://myaccount.google.com/

Enable 2-Step Verification:
- Click Security in left menu
- Find 2-Step Verification
- Complete the setup

Generate App Password:
- Go to https://myaccount.google.com/apppasswords
- Select: Mail
- Select: Your device
- Click Generate
- Copy the 16-character password

Step 5: Create .env File

Create a file named .env in your project root:

EMAIL_USER=your-email@gmail.com
EMAIL_PASS=your-16-char-app-password

Replace with your actual credentials.

Step 6: Run Application

streamlit run streamlit.py

The app will open at http://localhost:8501

Step 7: Prepare Your Contacts

Create contacts.csv file with your leads:

email,name
john@example.com,John Doe
jane@example.com,Jane Smith
bob@example.com,Bob Wilson

Step 8: Use the Application

1. Open http://localhost:8501
2. Upload your contacts.csv
3. Write your email subject and body
4. Use {name} for personalization
5. Set delay between emails (1-2 seconds)
6. Click Send Campaign
7. Monitor progress

Troubleshooting

Module Import Errors

Solution:
- Make sure virtual environment is activated
- Run: pip install -r requirements.txt again
- Restart the terminal

SMTP Authentication Failed

Solution:
- Verify you are using App Password (not regular password)
- Check 2-Factor Authentication is enabled
- Verify no extra spaces in password
- Try generating a new App Password

Email Credentials Not Found

Solution:
- Check .env file exists in project root
- Verify EMAIL_USER and EMAIL_PASS are set
- Reload the application: streamlit run streamlit.py

Emails Not Sending

Solution:
- Check internet connection
- Verify recipient email addresses are correct
- Check if Gmail temporarily blocked you
- Review failed emails in results

Gmail Rate Limiting

Solution:
- Increase delay between emails (2-3 seconds)
- Send fewer emails per session
- Wait 24 hours before retrying

Streamlit Not Opening

Solution:
- Check that streamlit is installed
- Run: pip install streamlit==1.28.1
- Make sure port 8501 is not in use
- Try: streamlit run streamlit.py --logger.level=debug

File Structure

emailblast-pro/
|- streamlit.py          Main application
|- mailer.py             Email sending module
|- requirements.txt      Python dependencies
|- .env                  Credentials (create yourself)
|- contacts.csv          Contact list (create yourself)
|- README.md             Full documentation
|- SETUP.md              This file
|- .gitignore            Git ignore rules
|- LICENSE               MIT License

Environment Variables

EMAIL_USER
Your Gmail address. Example: user@gmail.com

EMAIL_PASS
Your Gmail App Password (16 characters). Example: abcd efgh ijkl mnop
Do not use your regular Gmail password.

Security Notes

1. Never share your .env file
2. Do not commit .env to version control
3. Use App Password, not regular password
4. Enable 2-Factor Authentication on Gmail
5. Do not hardcode credentials in scripts

Testing Before Full Campaign

1. Create test contacts.csv with 1-2 emails
2. Write your test email
3. Set delay to 1 second
4. Send to test contacts
5. Verify email format and content
6. Then proceed with full campaign

CSV Requirements

Column: email (required)
- Must be valid email address
- Example: john@example.com

Column: name (optional)
- Used for {name} personalization
- Example: John Doe

Performance Tips

- Test with small batches first (5-10 emails)
- Use 1-2 second delays between emails
- Monitor failed emails
- Do not exceed 500 emails per day
- Check for bounce-backs

Common Issues and Solutions

Issue: Virtual environment not activating

Solution:
- Windows: venv\Scripts\activate.bat
- Linux/Mac: source venv/bin/activate
- Verify: (venv) should appear in terminal

Issue: pip command not found

Solution:
- Try: python -m pip install -r requirements.txt
- Or: python3 -m pip install -r requirements.txt

Issue: Port 8501 already in use

Solution:
- streamlit run streamlit.py --server.port 8502
- Or kill process using port 8501

Issue: CSV file not recognized

Solution:
- Make sure file is named exactly: contacts.csv
- File must be in project root directory
- Verify CSV format is correct (comma-separated)

Getting Help

1. Check README.md for detailed information
2. Review Troubleshooting section above
3. Check your Gmail settings
4. Verify .env file credentials
5. Check internet connection

Next Steps

1. Complete installation
2. Test with 1-2 contacts
3. Create your email template
4. Upload your full contact list
5. Send your first campaign

Success Checklist

- Python 3.8+ installed: Yes/No
- Virtual environment created: Yes/No
- Dependencies installed: Yes/No
- .env file created: Yes/No
- Gmail App Password generated: Yes/No
- contacts.csv file created: Yes/No
- Streamlit running: Yes/No
- Test email sent: Yes/No

Made for simple and effective email campaigns

Version 1.0 | Setup Complete | Ready to Use
