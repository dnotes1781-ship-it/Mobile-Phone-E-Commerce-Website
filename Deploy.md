# Deployment Guide: E-Commerce App on Render

This document describes how to deploy the e-commerce Django application on Render.

---

## **Overview**

The e-commerce application is deployed on **Render** using:
- **Web Server**: Gunicorn (WSGI application server)
- **Framework**: Django with SQLite database
- **Static Files**: WhiteNoise middleware + collectstatic
- **Configuration**: `render.yaml` + environment variables

---

## **Prerequisites**

Before deploying to Render, ensure:
1. Git repository initialized and synced to GitHub/GitLab
2. All changes committed: `git add . && git commit -m "message" && git push`
3. Render account created at [https://render.com](https://render.com)
4. Service connected to your Git repository

---

## **Deployment Files**

The following files are critical for Render deployment:

### **1. `Procfile`**
```
web: gunicorn Eshop.wsgi --bind 0.0.0.0:$PORT
```
- Specifies the command Render executes to start the web service
- Binds to `0.0.0.0` (all interfaces) on the port Render assigns via `$PORT` environment variable

### **2. `render.yaml`**
```yaml
services:
  - type: web
    name: ecommerce-app
    env: python
    buildCommand: pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
    startCommand: gunicorn Eshop.wsgi --bind 0.0.0.0:$PORT
    envVars:
      - key: ALLOWED_HOSTS
        value: mobile-phone-e-commerce-website.onrender.com
      - key: DEBUG
        value: "0"
```
- Infrastructure-as-code configuration for Render
- Defines build steps, start command, and base environment variables
- Render automatically detects and uses this file

### **3. `requirements.txt`**
```
asgiref==3.11.1
Django==5.2.11
gunicorn==21.2.0
whitenoise==6.6.0
pillow==12.1.0
reportlab==4.4.9
pytz==2025.2
sqlparse==0.5.5
tzdata==2025.3
```
- Python dependencies required for the app
- `gunicorn`: WSGI server for production
- `whitenoise`: Middleware to serve static files efficiently

### **4. `Eshop/settings.py` (Key Changes)**
```python
# Allow hosts from environment or default to Render domain
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'mobile-phone-e-commerce-website.onrender.com,localhost,127.0.0.1').split(',')

# Disable debug in production
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

# Use BigAutoField to avoid migration warnings
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# WhiteNoise middleware for static file serving
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # ... other middleware
]
```

---

## **Step-by-Step Deployment Instructions**

### **Step 1: Prepare Your Repository**
```bash
cd /path/to/Ecommerce-v1.1
git add .
git commit -m "Add deployment configuration (Procfile, render.yaml, static files)"
git push origin main
```

### **Step 2: Access Render Dashboard**
1. Go to [https://dashboard.render.com](https://dashboard.render.com)
2. Log in with your account
3. Select your service (e.g., "mobile-phone-e-commerce-website")

### **Step 3: Configure Render Settings**

#### **3a. Build & Deploy Settings**
- Navigate to **Settings** → **Build & Deploy**
- **Start Command**:
  - If using `render.yaml`: Leave blank (Render auto-detects)
  - If manual: Set to `gunicorn Eshop.wsgi --bind 0.0.0.0:$PORT`
- **Build Command**:
  - If using `render.yaml`: Leave blank (auto-configured)
  - If manual: Set to `pip install -r requirements.txt`
- Click **Save Changes**

#### **3b. Environment Variables**
- Navigate to **Environment**
- Add the following variables:

| Key | Value | Notes |
|-----|-------|-------|
| `ALLOWED_HOSTS` | `mobile-phone-e-commerce-website.onrender.com` | Your Render domain |
| `DEBUG` | `0` | Set to 0 for production |
| `DJANGO_SECRET_KEY` | *(your secret key)* | Keep this secret; use a strong value |

- Click **Save** after each addition

### **Step 4: Deploy**
- In the Render dashboard, go to **Deploys**
- Click **Deploy latest commit** (or wait for auto-deploy if enabled)
- Monitor the deployment logs:

**Expected log sequence:**
```
==> Building...
==> Running 'pip install -r requirements.txt'
==> Running 'python manage.py migrate'
==> Running 'python manage.py collectstatic --noinput'
==> Build successful 🎉
==> Starting web service...
==> Listening on 0.0.0.0:$PORT
```

### **Step 5: Verify Deployment**
1. Once deployment completes, open your app URL:
   ```
   https://mobile-phone-e-commerce-website.onrender.com
   ```

2. Check the following:
   - ✅ Homepage loads without errors
   - ✅ Hero carousel displays with Unsplash images
   - ✅ Products load in the grid
   - ✅ Add to cart functionality works
   - ✅ Static assets (CSS, JS, images) load properly
   - ✅ No 500 errors in Render logs

---

## **Environment Variables Explained**

- **`ALLOWED_HOSTS`**: Comma-separated list of domains the app accepts requests from. Must include your Render domain.
- **`DEBUG`**: Set to `0` (False) in production to hide sensitive error details.
- **`DJANGO_SECRET_KEY`**: Secret key for Django security features (sessions, CSRF tokens, etc.). Keep this private.

---

## **Troubleshooting**

### **Issue: `DisallowedHost` Error**
```
Invalid HTTP_HOST header: 'mobile-phone-e-commerce-website.onrender.com'
```
**Solution**: Ensure `ALLOWED_HOSTS` environment variable includes your domain.

### **Issue: `ImproperlyConfigured: WSGI application could not be loaded`**
```
Error importing module
```
**Solution**: 
- Check logs for import errors in `Eshop/settings.py`
- Verify `DJANGO_SETTINGS_MODULE` is set correctly
- Ensure all dependencies in `requirements.txt` are installed

### **Issue: Static Files Not Loading**
**Solution**:
- Verify `collectstatic` ran: check logs for `Running 'python manage.py collectstatic'`
- Ensure `STATIC_ROOT` and `STATICFILES_DIRS` are configured in `settings.py`
- Check WhiteNoise middleware is in the correct position in `MIDDLEWARE`

### **Issue: No Open Ports Detected**
```
Port scan timeout reached, no open ports detected on 0.0.0.0
```
**Solution**: Ensure gunicorn is binding to the port correctly:
```bash
gunicorn Eshop.wsgi --bind 0.0.0.0:$PORT
```

### **Issue: Database Errors**
**Solution**: 
- Run migrations manually via Render shell:
  ```bash
  python manage.py migrate
  ```
- Ensure SQLite database file is in the correct location (`BASE_DIR/db.sqlite3`)

---

## **Monitoring & Maintenance**

### **View Logs**
- Go to **Logs** tab in the Render dashboard
- Filter by recent deployments or errors
- Search for specific error messages

### **Manual Commands**
- Via Render Shell (`/bin/bash` tab):
  ```bash
  python manage.py migrate
  python manage.py createsuperuser
  python manage.py collectstatic --noinput
  ```

### **Redeploy**
- Push changes to Git: `git push`
- Manual redeploy: Click **Deploy latest commit** in Renders dashboard
- Auto-redeploy: Enabled by default on push to main branch

### **Scale the App**
- For paid Render plans, increase instance size or add more workers:
  ```bash
  gunicorn Eshop.wsgi --bind 0.0.0.0:$PORT --workers 4
  ```

---

## **Performance Tips**

1. **Optimize Images**: Use Unsplash CDN URLs or compress local images
2. **Enable Caching**: Add caching headers in `settings.py` (optional)
3. **Database Optimization**: 
   - Use SQLite for dev; consider PostgreSQL for production (upgrade Render plan)
   - Index frequently queried fields

4. **Static Files**: WhiteNoise caches assets aggressively; clear cache if needed

---

## **Rollback**

If deployment breaks the app:
1. Go to **Deploys** tab
2. Find the last working deployment
3. Click **Redeploy** next to it
4. Git will revert to that commit on the server

---

## **Support**

For issues or questions:
- Check Render documentation: [https://render.com/docs](https://render.com/docs)
- Review Django deployment guide: [https://docs.djangoproject.com/en/stable/howto/deployment/](https://docs.djangoproject.com/en/stable/howto/deployment/)
- Check application logs in Render dashboard for detailed error messages

---

**Last Updated**: February 18, 2026  
**App Domain**: `https://mobile-phone-e-commerce-website.onrender.com`  
**Framework**: Django 5.2.11  
**Server**: Gunicorn on Render
