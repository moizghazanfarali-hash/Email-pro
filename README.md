EmailBlast Pro - Simple Email Campaign Manager

A professional email campaign manager built with Streamlit for sending personalized bulk emails with complete control over content.

Features

* Professional Streamlit UI with dark theme
* CSV file upload for contact management
* Email template builder with personalization support
* Real-time campaign progress tracking
* Bulk email sending with configurable delays
* Rate limiting to avoid Gmail blocks
* Preview system to see emails before sending
* Secure credential management with .env file
* Campaign statistics and error tracking
* Support for email personalization with {name} placeholders

Tech Stack

* Frontend: Streamlit 1.28+
* Backend: Python 3.8+
* Email: Gmail SMTP
* Data: Pandas 2.0+
* Configuration: Python-dotenv 1.0+

Requirements

* Python 3.8 or higher
* pip (Python package manager)
* Gmail account with App Password enabled
* Basic CSV file with email addresses

Installation

1. Clone the repository
   git clone https://github.com/yourusername/emailblast-pro.git
   cd emailblast-pro

2. Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies
   pip install -r requirements.txt

4. Create .env file with your credentials
   EMAIL_USER=your-email@gmail.com
   EMAIL_PASS=your-app-password

5. Run the application
   streamlit run streamlit.py

Gmail Setup

1. Go to https://myaccount.google.com/
2. Enable 2-Step Verification if not already enabled
3. Go to https://myaccount.google.com/apppasswords
4. Select Mail and your device
5. Copy the 16-character app password
6. Add to .env file as EMAIL_PASS

CSV Format

Create a CSV file with your contacts:

email,name
john@example.com,John Doe
jane@example.com,Jane Smith
bob@example.com,Bob Wilson

Required columns:
* email - Contact email address (required)
* name - Contact name (optional, used for personalization)

How to Use

1. Open the application
   streamlit run streamlit.py

2. In the sidebar, enter your Gmail credentials or use the saved .env file

3. Upload your CSV file with contacts

4. Create your email template
   * Enter subject line
   * Enter email body
   * Use {name} for personalization

5. Configure sending options
   * Choose number of contacts to send to
   * Set delay between emails (1-2 seconds recommended)
   * Review preview of emails

6. Send campaign
   * Click Send Campaign button
   * Monitor real-time progress
   * Check results and failed emails

Personalization

You can personalize emails using {name} placeholder:

Subject: Hello {name}!

Body:
Hi {name},

Thank you for your interest. We would like to discuss opportunities with you.

Best regards,
Your Team

The {name} will be replaced with actual names from your CSV file.

Email Delays

Use these delay recommendations:

* 0-1 second - Small campaigns (less than 50 emails)
* 1-2 seconds - Medium campaigns (50-200 emails)
* 2-3 seconds - Large campaigns (200+ emails)

Delays prevent Gmail from rate limiting your account.

Rate Limits

Gmail has these limitations:

* Personal accounts: ~500 emails per day
* If you hit the limit, wait 24 hours before sending again
* Use delays between emails to avoid triggering limits
* Monitor failed emails for bounce backs

Troubleshooting

Email credentials not found

Check that .env file exists in the project root
Verify EMAIL_USER and EMAIL_PASS are set correctly
Or use sidebar to save credentials

SMTP authentication failed

Verify you are using App Password, not regular Gmail password
Check that 2-Factor Authentication is enabled
Verify no extra spaces in password

Emails not sending

Check internet connection
Verify recipient email addresses are correct
Check if Gmail blocked the sending attempt
Look for failed emails in the results section

Rate limiting

Increase delay between emails
Send fewer emails per session
Wait 24 hours if Gmail temporarily blocked you

Project Structure

emailblast-pro/
|- streamlit.py          Main Streamlit application
|- mailer.py             Email sending module
|- requirements.txt      Python dependencies
|- .env                  Configuration (create yourself)
|- contacts.csv          Example contact list
|- README.md             This file
|- .gitignore            Git ignore rules
|- LICENSE               MIT License

Security

* Credentials are stored in .env file
* Use Gmail App Password, not your regular password
* .env file is excluded from version control
* SMTP uses SSL/TLS encryption
* Never commit .env to git

Example Email Templates

Welcome Email

Subject: Welcome {name}!

Body:
Hi {name},

Welcome to our community! We are excited to have you join us.

Get started by exploring our resources at https://example.com

Best regards,
The Team


Meeting Request

Subject: Let's Connect, {name}

Body:
Hi {name},

I would like to discuss potential opportunities with you and see how we can work together.

Are you available for a 15-minute call next week?

Looking forward to hearing from you.

Best regards,
[Your Name]


Follow-up Email

Subject: Quick Follow-up, {name}

Body:
Hi {name},

Just wanted to check in and see if you had a chance to review the information I sent earlier.

Feel free to reach out if you have any questions.

Talk soon,
[Your Name]

Tips for Best Results

* Test with 1-2 contacts first before sending to larger lists
* Use 1-2 second delays to avoid Gmail rate limiting
* Monitor failed emails and retry them later
* Keep emails short and professional
* Use clear and honest subject lines
* Personalize emails with actual names from your contact list
* Do not exceed 500 emails per day
* Follow email best practices and respect recipients

Common Mistakes to Avoid

* Sending generic emails without personalization
* Not testing before full campaign
* Sending too many emails too quickly
* Using wrong Gmail password (use App Password)
* Not enabling 2-Factor Authentication
* Sending misleading or false information
* Forgetting to set delays between emails
* Not monitoring for failed emails

Supported Features

* CSV file upload
* Gmail SMTP integration
* Email personalization with {name}
* Bulk email sending
* Rate limiting with configurable delays
* Real-time progress tracking
* Error handling and failed email reporting
* Campaign statistics
* Email preview before sending
* Responsive dark theme UI
* Secure credential management

License

This project is licensed under the MIT License - see LICENSE file for details.

Contributing

Contributions are welcome. Please fork the repository and submit a pull request.

Support

For issues or questions:

1. Check the Troubleshooting section above
2. Review the FAQ
3. Check your Gmail and Streamlit settings
4. Verify internet connection
5. Open an issue on GitHub if problem persists

FAQ

Q: What is the maximum number of emails I can send?
A: Gmail allows approximately 500 emails per day from personal accounts.

Q: Do I need a special Gmail account?
A: No, you can use any Gmail account. Just enable 2-Factor Authentication and generate an App Password.

Q: What is an App Password?
A: An App Password is a 16-character password generated by Gmail for third-party applications. It is more secure than your regular password.

Q: Can I use other email providers?
A: Currently only Gmail is supported. Other providers would require code changes.

Q: What if an email fails to send?
A: Failed emails are listed in the results. You can check the error message and retry later.

Q: Is my data secure?
A: Your credentials are stored locally in .env file and never sent to external servers. SMTP uses secure SSL/TLS encryption.

Q: How do I update my email credentials?
A: Edit the .env file and update EMAIL_USER and EMAIL_PASS, or use the Streamlit sidebar to save new credentials.

Q: Can I schedule emails for later?
A: Current version sends immediately. Scheduling is a planned feature for future versions.

Q: What should I do if Gmail blocks my account?
A: Wait 24 hours and try again. Reduce the number of emails and increase delays between sends.

Made with care for professional email campaigns

Version 1.0 | Production Ready | Clean and Simple
