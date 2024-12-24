"# panda_records_api" 
In Django, you can remove the database structure using the flush command, which removes all data from the database and resets the structure to the state it was in when you first ran migrate. Here's how to do it:
python manage.py flush

python manage.py custom_qcluster


# Email Sending Setup Guide

To be able to send emails to users from your application, you need to create an app password for your Google account. Follow these steps:

### Step 1: Enable Two-Factor Authentication

1. Go to your [Google Account](https://myaccount.google.com/).
2. Under **Security**, enable **Two-Factor Authentication**.

### Step 2: Create an App Password

1. Once two-factor authentication is enabled, go to the **App Passwords** section: [App Passwords](https://myaccount.google.com/apppasswords).
2. Select the app and device you want to generate a password for (e.g., choose "Mail" and "Other (Custom name)" for your project).
3. Click **Generate** to create a new app password.
4. Copy the generated app password (you will use this in your `.env` file).

### Step 3: Update Your `.env` File

1. In your `.env` file, add the following variables:

```env
EMAIL_SENDER=your_email@gmail.com
EMAIL_APP_PASSWORD_SENDER=your_app_password
