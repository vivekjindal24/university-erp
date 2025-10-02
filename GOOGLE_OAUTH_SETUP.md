
# Google OAuth Setup Guide for University ERP

## Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Enter project name: "University ERP OAuth"
4. Click "Create"

## Step 2: Enable Required APIs

1. In the Google Cloud Console, go to "APIs & Services" → "Library"
2. Search and enable these APIs:
   - Google+ API
   - Google Identity Services API
   - People API (optional, for more user data)

## Step 3: Configure OAuth Consent Screen

1. Go to "APIs & Services" → "OAuth consent screen"
2. Choose "External" user type
3. Fill in required fields:
   - App name: "University ERP System"
   - User support email: your email
   - Developer contact information: your email
4. Add scopes:
   - email
   - profile
   - openid
5. Save and continue

## Step 4: Create OAuth Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth 2.0 Client IDs"
3. Choose "Web application"
4. Name: "University ERP Web Client"
5. Add Authorized redirect URIs:
   - http://localhost:8000/accounts/google/login/callback/
   - http://127.0.0.1:8000/accounts/google/login/callback/
   - http://localhost:3000 (for React frontend)
   - http://127.0.0.1:3000 (for React frontend)
6. Click "Create"
7. Copy your Client ID and Client Secret

## Step 5: Test URLs

- Google OAuth Test Page: http://localhost:8000/api/auth/google-test/
- Admin Panel: http://localhost:8000/admin/
- API Endpoint: http://localhost:8000/api/auth/google-login/

## Step 6: Test the Integration

1. Visit the test page
2. Select user type (student/faculty/admin/staff)
3. Click "Sign in with Google"
4. Check the response for JWT tokens
5. Use tokens for authenticated API calls

## Troubleshooting

- Make sure redirect URIs match exactly
- Ensure APIs are enabled
- Check that Client ID is correct in test page
- Verify .env file has correct credentials
