# Assignment 1 – Securing and Monitoring an Authenticated Flask App

##  Overview

This project demonstrates how to build and deploy a secure, production-ready Flask application using **Auth0 for authentication** and **Azure Monitor with KQL** for user activity monitoring and alerting. The application:

- Uses Auth0 for Single Sign-On (SSO)
- Logs user activity on protected endpoints
- Detects excessive access to sensitive routes
- Sends alerts based on suspicious behavior

---

##  Setup Instructions

### 1. Auth0 Setup

1. Log in to [Auth0](https://auth0.com/) and create a new **Regular Web Application**.
2. In the application settings, configure the following:

   - **Allowed Callback URLs**  
     `http://localhost:3000/callback`
     
   - **Allowed Logout URLs**  
     `http://localhost:3000/logout`
     
   - **Allowed Web Origins**  ebsites.
     `http://localhost:3000`

3. Copy the following Auth0 credentials:
   - `AUTH0_CLIENT_ID`
   - `AUTH0_CLIENT_SECRET`
   - `AUTH0_DOMAIN`

---

### 2. Local Environment Setup

1. Create a `.env` file in your project root:

   ```env
   AUTH0_CLIENT_ID=your_client_id
   AUTH0_CLIENT_SECRET=your_client_secret
   AUTH0_DOMAIN=your_domain.auth0.com
   APP_SECRET_KEY=your_flask_secret_key
   ```
   
 2. To generate a secure APP_SECRET_KEY, run this command in your terminal
     ```openssl rand -hex 32```

 3. Install required packages
   ``` pip install -r requirements.txt```

4. Run the app locally:
   ``` python server.py ```
---
### 3. Azure Deployment Steps

1. Create Resources:

- Azure App Service 
- Log Analytics Workspace

2. Deploy Code to App Service:

- Use GitHub.
- Upload the .env variables in App Service → Environment varibles.
- Set the Startup Command in App Service → Configuration → Startup Command: ``` gunicorn -w 4 server:app ```
  
3. Enable Logging:
   
- Go to App Service → Diagnostic settings
- Enable AppServiceConsoleLogs and connect them to  Log Analytics workspace.  
---
