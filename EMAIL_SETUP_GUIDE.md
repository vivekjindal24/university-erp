io"""
Email Configuration Setup Guide for University ERP System

This guide helps you configure real email sending for the admission system.
You can use Gmail, Outlook, or any other SMTP provider.

OPTION 1: GMAIL CONFIGURATION
=============================

1. Enable 2-Factor Authentication on your Gmail account
2. Generate an App Password:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
   - Copy the 16-character password

3. Update settings.py with these values:
   EMAIL_HOST_USER = 'your-gmail@gmail.com'
   EMAIL_HOST_PASSWORD = 'your-16-char-app-password'

OPTION 2: OUTLOOK/HOTMAIL CONFIGURATION
======================================

EMAIL_HOST = 'smtp-mail.outlook.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@outlook.com'
EMAIL_HOST_PASSWORD = 'your-password'

OPTION 3: OTHER SMTP PROVIDERS
==============================

For other providers, update these settings:
- EMAIL_HOST: Your SMTP server (e.g., smtp.yourdomain.com)
- EMAIL_PORT: Usually 587 (TLS) or 465 (SSL)
- EMAIL_USE_TLS: True for port 587
- EMAIL_USE_SSL: True for port 465
- EMAIL_HOST_USER: Your email address
- EMAIL_HOST_PASSWORD: Your password

SECURITY RECOMMENDATIONS
========================

1. Use environment variables for sensitive data:
   - Create a .env file in your project root
   - Add: EMAIL_HOST_USER=your-email@gmail.com
   - Add: EMAIL_HOST_PASSWORD=your-app-password
   - Install python-decouple: pip install python-decouple

2. Add .env to .gitignore to avoid committing credentials

3. For production, use environment variables or secrets management

TESTING THE EMAIL SETUP
=======================

1. Update the email credentials in settings.py
2. Restart the Django server
3. Go to admin interface and admit a student
4. Check if the email is sent successfully
5. Check Django logs for any email errors

CURRENT SETTINGS
===============

The system is configured to use Gmail SMTP.
Update EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in settings.py with your credentials.
"""
