# Hocus Focus API - Deployment Guide for Render.com

This guide will walk you through deploying the Hocus Focus Django API to Render.com.

## Prerequisites

- A GitHub account with your code repository
- A Render.com account (free tier available)
- Your Django project in the `cerulean` folder

## Project Structure

Your Django API includes:
- **3 Main Endpoints** (matching the .NET version):
  - `POST /challenge` - Create a new challenge
  - `POST /christmas` - Create a Christmas-themed challenge
  - `GET /challenge/{id}` - Get a challenge by ID
- **Additional Endpoints**:
  - `GET /challenges` - List all challenges
  - `POST /solve` - Create a solve record
  - `POST /api/auth/token/` - Get authentication token

## Step 1: Prepare Your Repository

1. **Push your code to GitHub**:
   ```bash
   cd cerulean
   git init
   git add .
   git commit -m "Initial Django API setup"
   git branch -M main
   git remote add origin https://github.com/yourusername/hocus-focus-api.git
   git push -u origin main
   ```

## Step 2: Create a Web Service on Render

1. **Log in to Render.com** and click "New +"
2. **Select "Web Service"**
3. **Connect your GitHub repository**
4. **Configure the service**:
   - **Name**: `hocus-focus-api`
   - **Region**: Choose closest to your users
   - **Branch**: `main`
   - **Root Directory**: `cerulean` (important!)
   - **Runtime**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn hocus_focus_api.wsgi:application`

## Step 3: Set Environment Variables

In the Render dashboard, go to your service's "Environment" tab and add these **required** environment variables:

```
SECRET_KEY=your-super-secret-key-here-make-it-long-and-random
DEBUG=False
ALLOWED_HOSTS=your-service-name.onrender.com
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com,https://hocus-focus.netlify.app
```

**Critical**: The `SECRET_KEY` environment variable is **required** and must be set, or your application will fail to start.

**How to generate a secure SECRET_KEY**:
1. **Option 1**: Use Django's built-in generator:
   ```python
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
2. **Option 2**: Use an online generator like https://djecrety.ir/
3. **Option 3**: Generate manually with at least 50 random characters including letters, numbers, and symbols

**Important**:
- The SECRET_KEY must be unique and kept secret
- Replace `your-service-name` with your actual Render service name
- Add your actual frontend domains to CORS_ALLOWED_ORIGINS

## Step 4: Add a PostgreSQL Database

1. **In Render dashboard**, click "New +" → "PostgreSQL"
2. **Configure**:
   - **Name**: `hocus-focus-db`
   - **Region**: Same as your web service
   - **Plan**: Free tier is fine for development
3. **Connect to your web service**:
   - Go to your web service's "Environment" tab
   - Render will automatically add `DATABASE_URL` environment variable

## Step 5: Deploy

1. **Click "Create Web Service"**
2. **Wait for deployment** (first deploy takes 5-10 minutes)
3. **Check logs** for any errors in the "Logs" tab

## Step 6: Test Your API

Once deployed, test your endpoints:

### Create a Challenge
```bash
curl -X POST https://your-service-name.onrender.com/challenge \
  -H "Content-Type: application/json" \
  -d '{
    "clue": "Find the hidden object",
    "image_key": "test_image_123",
    "goals": [30, 60, 90, 120, 150]
  }'
```

### Get a Challenge
```bash
curl https://your-service-name.onrender.com/challenge/1
```

### Create Christmas Challenge
```bash
curl -X POST https://your-service-name.onrender.com/christmas \
  -H "Content-Type: application/json" \
  -d '{
    "clue": "Find Santa!",
    "before_message": "Happy Holidays!",
    "before_title": "Christmas Special",
    "theme": "12"
  }'
```

## Step 7: Set Up Admin Access (Optional)

To access Django admin panel:

1. **Create a superuser** via Render shell:
   - Go to your service → "Shell" tab
   - Run: `python manage.py createsuperuser`
   - Follow prompts to create admin user

2. **Access admin**: `https://your-service-name.onrender.com/admin/`

## API Documentation

### Authentication

The API supports token-based authentication:
```bash
# Get token
curl -X POST https://your-service-name.onrender.com/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'

# Use token in requests
curl -H "Authorization: Token your-token-here" \
  https://your-service-name.onrender.com/challenges
```

### Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/challenge` | Create challenge | No |
| POST | `/christmas` | Create Christmas challenge | No |
| GET | `/challenge/{id}` | Get challenge by ID | No |
| GET | `/challenges` | List all challenges | No |
| POST | `/solve` | Create solve record | No |
| POST | `/api/auth/token/` | Get auth token | No |

### CORS Configuration

The API is configured to accept requests from:
- `localhost:3000` (development)
- `127.0.0.1:3000` (development)
- Your configured frontend domains

## Troubleshooting

### Common Issues

1. **Build fails**: Check that `Root Directory` is set to `cerulean`
2. **Database connection errors**: Ensure PostgreSQL database is connected
3. **CORS errors**: Add your frontend domain to `CORS_ALLOWED_ORIGINS`
4. **Static files not loading**: Ensure `whitenoise` is in `MIDDLEWARE`

### Checking Logs

- Go to your service → "Logs" tab
- Look for Django startup messages
- Check for any error messages during deployment

### Environment Variables

Make sure these are set in Render:
- `SECRET_KEY` (**REQUIRED** - app will not start without this)
- `DEBUG=False`
- `ALLOWED_HOSTS`
- `DATABASE_URL` (auto-set by Render when you connect a PostgreSQL database)
- `CORS_ALLOWED_ORIGINS`

**If you see "SECRET_KEY environment variable is required" error**: You must set the SECRET_KEY environment variable in your Render service settings.

## Updating Your API

To deploy updates:
1. Push changes to your GitHub repository
2. Render will automatically redeploy
3. Check logs to ensure successful deployment

## Security Notes

- Never commit `.env` files with real secrets
- Use strong, unique `SECRET_KEY`
- Keep `DEBUG=False` in production
- Regularly update dependencies
- Monitor your Render logs for suspicious activity

## Support

- **Render Documentation**: https://render.com/docs
- **Django Documentation**: https://docs.djangoproject.com/
- **Django REST Framework**: https://www.django-rest-framework.org/

Your Hocus Focus API should now be live and ready to serve your client applications!