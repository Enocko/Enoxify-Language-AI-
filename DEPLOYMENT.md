# 🚀 Deployment Guide for Enoxify

This guide will help you safely deploy Enoxify to various platforms while protecting your sensitive information.

## 🔐 Security First!

### Critical Security Checklist
- ✅ `.env` file is in `.gitignore` (already done)
- ✅ Never commit API keys to Git
- ✅ Use environment variables in production
- ✅ Keep your OpenAI API key private

## 🌐 Deployment Options

### 1. **Backend Deployment**

#### Option A: Railway (Recommended for beginners)
```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login to Railway
railway login

# 3. Initialize project
railway init

# 4. Set environment variables
railway variables set OPENAI_API_KEY=your_actual_key_here

# 5. Deploy
railway up
```

#### Option B: Heroku
```bash
# 1. Install Heroku CLI
# 2. Login
heroku login

# 3. Create app
heroku create your-enoxify-app

# 4. Set environment variables
heroku config:set OPENAI_API_KEY=your_actual_key_here

# 5. Deploy
git push heroku main
```

#### Option C: Docker
```bash
# 1. Build image
docker build -t enoxify-backend ./backend

# 2. Run container
docker run -d \
  -p 8000:8000 \
  -e OPENAI_API_KEY=your_actual_key_here \
  --name enoxify-backend \
  enoxify-backend
```

### 2. **Frontend Deployment**

#### Option A: Vercel (Recommended)
```bash
# 1. Install Vercel CLI
npm install -g vercel

# 2. Deploy
cd frontend
vercel

# 3. Update API endpoint in production
# Change localhost:8000 to your backend URL
```

#### Option B: Netlify
```bash
# 1. Build the project
cd frontend
npm run build

# 2. Drag and drop the 'build' folder to Netlify
# 3. Update API endpoints for production
```

#### Option C: GitHub Pages
```bash
# 1. Add to package.json
{
  "homepage": "https://yourusername.github.io/enoxify",
  "scripts": {
    "predeploy": "npm run build",
    "deploy": "gh-pages -d build"
  }
}

# 2. Install gh-pages
npm install --save-dev gh-pages

# 3. Deploy
npm run deploy
```

## 🔧 Environment Configuration

### Production Environment Variables
```bash
# Backend (.env file or platform environment variables)
OPENAI_API_KEY=your_actual_openai_api_key
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
LOG_LEVEL=INFO

# Frontend (update in code)
REACT_APP_API_URL=https://your-backend-url.com
```

### Update Frontend API Endpoints
In `frontend/src/services/api.ts` or similar:
```typescript
// Development
const API_BASE_URL = 'http://localhost:8000';

// Production
const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://your-backend-url.com';
```

## 📱 Platform-Specific Instructions

### Railway
- **Pros**: Easy, free tier, automatic deployments
- **Cons**: Limited resources on free tier
- **Best for**: Prototypes and small projects

### Heroku
- **Pros**: Reliable, good free tier, easy scaling
- **Cons**: Free tier discontinued, paid plans
- **Best for**: Production applications

### Vercel
- **Pros**: Excellent for frontend, automatic deployments
- **Cons**: Backend requires serverless functions
- **Best for**: Frontend deployment

### Docker
- **Pros**: Consistent environment, easy scaling
- **Cons**: More complex setup
- **Best for**: Production deployments

## 🚨 Common Deployment Issues

### 1. **CORS Errors**
```python
# In backend/main.py, update CORS origins
origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "https://your-frontend-domain.com"  # Add your production domain
]
```

### 2. **API Key Not Found**
- Check environment variables are set correctly
- Verify the variable name matches exactly
- Restart the application after setting variables

### 3. **Port Conflicts**
- Ensure the port you're using is available
- Check if another service is using the same port
- Use platform-specific port configuration

### 4. **File Upload Issues**
- Check file size limits
- Verify upload directory permissions
- Ensure temporary directories exist

## 🔍 Testing Your Deployment

### Backend Health Check
```bash
curl https://your-backend-url.com/health
# Should return: {"status": "healthy"}
```

### Frontend API Connection
1. Open your deployed frontend
2. Try the text simplification feature
3. Check browser console for errors
4. Verify API calls are going to the right URL

## 📊 Monitoring & Maintenance

### Logs
- **Railway**: `railway logs`
- **Heroku**: `heroku logs --tail`
- **Docker**: `docker logs enoxify-backend`

### Performance
- Monitor API response times
- Check OpenAI API usage and costs
- Monitor server resource usage

### Updates
- Keep dependencies updated
- Monitor security advisories
- Regular backups of configuration

## 🆘 Troubleshooting

### Backend Won't Start
```bash
# Check logs
railway logs  # or heroku logs

# Verify environment variables
railway variables  # or heroku config

# Test locally
cd backend
python main.py
```

### Frontend Can't Connect to Backend
1. Check CORS configuration
2. Verify backend URL is correct
3. Ensure backend is running
4. Check network requests in browser dev tools

### API Key Issues
1. Verify the key is correct
2. Check if the key has expired
3. Ensure sufficient OpenAI credits
4. Test the key with a simple curl request

## 🎯 Next Steps

1. **Choose your deployment platform**
2. **Set up environment variables**
3. **Deploy backend first**
4. **Update frontend API endpoints**
5. **Deploy frontend**
6. **Test all functionality**
7. **Monitor performance and logs**

## 📞 Need Help?

- Check the main README.md
- Review platform-specific documentation
- Create an issue on GitHub
- Check deployment platform support

---

**Happy Deploying! 🚀✨**

Remember: Keep your API keys secure and never commit them to version control! 