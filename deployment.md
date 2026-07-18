# Full Deployment Guide: FastAPI to Render & PostgreSQL to Neon

This guide explains how to deploy your FastAPI application directly from GitHub without using Docker. We will use **Neon** for the PostgreSQL database and **Render** (a popular, free-tier friendly cloud provider) to host the FastAPI application.

Your code has been updated to automatically handle Neon's `postgres://` or `postgresql://` connection strings so it seamlessly works with the modern `psycopg` driver you are using. A `requirements.txt` has also been generated to ensure any cloud platform can easily install your dependencies.

## Step 1: Push your Code to GitHub
Ensure all recent changes are committed and pushed to your GitHub repository:
```bash
git add .
git commit -m "Fix database URL scheme and add requirements.txt"
git push origin main
```

## Step 2: Set up PostgreSQL on Neon
1. Go to [Neon.tech](https://neon.tech/) and sign up / log in.
2. Click **New Project** and provide a name (e.g., `blood-donation-db`).
3. Once the database is created, you will see a connection string on the dashboard.
4. Copy the connection string. It will look something like this:
   `postgresql://neondb_owner:YOUR_PASSWORD@ep-xxx-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require`

## Step 3: Deploy FastAPI on Render
1. Go to [Render.com](https://render.com/) and sign up / log in with your GitHub account.
2. Click **New +** and select **Web Service**.
3. Connect your GitHub repository that contains this project.
4. Fill in the deployment details:
   - **Name**: `blood-donation-backend` (or any name you prefer)
   - **Environment**: `Python`
   - **Region**: (Choose the one closest to your Neon database region)
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT`

## Step 4: Configure Environment Variables
Scroll down on the Render setup page to the **Environment Variables** section and add the following keys:

1. **Key**: `DATABASE_URL`
   **Value**: Paste the Neon connection string you copied in Step 2.
   *(Note: Our code update will automatically handle converting this to `postgresql+psycopg://` under the hood).*

2. **Key**: `SECRET_KEY`
   **Value**: A long random string. (You can generate one using `openssl rand -hex 32` in your terminal).

3. **Key**: `ENVIRONMENT`
   **Value**: `production`

4. **Key**: `CORS_ORIGINS`
   **Value**: `https://your-frontend-domain.com` (If you have a frontend app. Multiple URLs can be separated by commas).

5. **Key**: `PYTHON_VERSION`
   **Value**: `3.12` (Important: explicitly tell Render to use Python 3.12).

## Step 5: Deploy
Click **Create Web Service**. 
Render will automatically:
1. Pull your code from GitHub.
2. Install the dependencies using the `requirements.txt`.
3. Run the database migrations (`alembic upgrade head`) on your Neon database.
4. Start the FastAPI server (`uvicorn`).

Once it says "Live", click the URL provided by Render (e.g., `https://blood-donation-backend.onrender.com/docs`) to view your live Swagger API documentation!

## Troubleshooting
- **Database Connection Issues**: Make sure your `DATABASE_URL` is exactly as provided by Neon. The config handles the `psycopg` conversion automatically.
- **Missing Tables**: If your API returns 500 errors regarding missing tables, check the Render deployment logs. Ensure `alembic upgrade head` ran successfully in the Start Command.
