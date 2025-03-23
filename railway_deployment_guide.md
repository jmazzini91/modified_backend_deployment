# Railway Deployment Guide for Plus500 Trading Platform Backend

This guide provides step-by-step instructions for deploying the Plus500 Trading Platform backend to Railway, enabling real-time data integration with Yahoo Finance APIs.

## Prerequisites

- A Railway account (sign up at [railway.app](https://railway.app) if you don't have one)
- Git installed on your local machine
- The Plus500 Trading Platform backend code (from the provided zip file)

## Step 1: Prepare Your Project for Deployment

1. Extract the trading_platform.zip file to a local directory
2. Navigate to the backend directory
3. Ensure the following files are present:
   - `app.py` - The main Flask application
   - `data_fetcher.py` - The Yahoo Finance API integration
   - `recommendation_engine.py` - The trading recommendation logic
   - `requirements.txt` - Dependencies list
   - `Procfile` - Process file for web servers

## Step 2: Create a Git Repository

1. Initialize a new Git repository:
```bash
cd /path/to/trading_platform/backend
git init
```

2. Add all files to the repository:
```bash
git add .
```

3. Commit the files:
```bash
git commit -m "Initial commit for backend deployment"
```

## Step 3: Deploy to Railway

### Option 1: Deploy via Railway CLI (Recommended)

1. Install the Railway CLI:
```bash
npm i -g @railway/cli
```

2. Login to Railway:
```bash
railway login
```

3. Initialize a new Railway project:
```bash
railway init
```

4. Deploy the project:
```bash
railway up
```

5. Generate a public URL:
```bash
railway domain
```

### Option 2: Deploy via Railway Dashboard

1. Go to [railway.app](https://railway.app) and log in
2. Click "New Project" and select "Deploy from GitHub repo"
3. Connect your GitHub account if not already connected
4. Select the repository containing your backend code
5. Configure the deployment:
   - Set the root directory to the backend folder
   - Set the start command to `gunicorn app:app`
6. Click "Deploy"

## Step 4: Configure Environment Variables

1. In the Railway dashboard, navigate to your project
2. Go to the "Variables" tab
3. Add the following environment variables:
   - `PORT`: 5000
   - `FLASK_ENV`: production

## Step 5: Verify Deployment

1. Once deployed, Railway will provide a URL for your backend API
2. Test the health check endpoint by visiting `https://your-railway-url.up.railway.app/health`
3. You should see a JSON response with status "healthy" and a timestamp

## Step 6: Connect Frontend to Backend

1. Update the frontend code to use the deployed backend API:
   - Open the `app.js` file in the frontend directory
   - Update the `API_BASE_URL` variable to your Railway deployment URL:
   ```javascript
   const API_BASE_URL = 'https://your-railway-url.up.railway.app';
   ```

2. Deploy the updated frontend code to your hosting provider (e.g., Netlify)

## Troubleshooting

### Common Issues

1. **Deployment Fails**: Check the logs in the Railway dashboard for specific error messages
2. **API Connection Issues**: Ensure CORS is properly configured in the backend
3. **Missing Dependencies**: Verify all required packages are listed in requirements.txt
4. **Port Configuration**: Make sure the PORT environment variable is set correctly

### Logs and Monitoring

1. View logs in the Railway dashboard under the "Logs" tab
2. Monitor API performance and errors in the "Metrics" tab

## Maintenance

1. To update your deployment, push changes to your Git repository:
```bash
git add .
git commit -m "Update backend code"
git push
```

2. Railway will automatically redeploy your application with the changes

## Next Steps

1. Set up a custom domain for your API (optional)
2. Configure automatic scaling for high traffic (Railway Pro feature)
3. Set up monitoring and alerts for API availability
