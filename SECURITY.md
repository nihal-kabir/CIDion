# 🔒 Security Notice for CIDion AI

## ⚠️ Important Security Information

### API Key Protection
Your Gemini API key is a sensitive credential that should be protected:

1. **Never commit API keys to git repositories**
2. **Use environment variables** (`.env` file) for local development
3. **Use secure environment variables** for production deployments
4. **Never share API keys** in public channels or documentation

### What We've Done to Protect You

✅ **`.gitignore` file** - Excludes `.env` and other sensitive files from git  
✅ **`.env.example`** - Template file with placeholder values  
✅ **Environment variables** - Secure configuration management  
✅ **Documentation** - Clear security guidelines  

### If You've Already Committed an API Key

1. **🚨 Immediately revoke the key** at [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **Generate a new API key**
3. **Update your `.env` file** with the new key
4. **Remove from git history** (optional but recommended):
   ```bash
   git filter-branch --force --index-filter \
     'git rm --cached --ignore-unmatch .env' \
     --prune-empty --tag-name-filter cat -- --all
   ```

### Best Practices

- **Local Development**: Use `.env` files (excluded from git)
- **Production**: Use platform environment variables (Render, Railway, etc.)
- **Team Sharing**: Share `.env.example` files, not actual `.env` files
- **Regular Rotation**: Consider rotating API keys periodically

### Getting Your Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and paste it in your `.env` file
5. Keep the key secure and never share it

### Questions?

If you have security concerns or questions:
- Check the [README.md](README.md) for setup instructions
- Review the [DEPLOY.md](DEPLOY.md) for deployment security
- Create an issue on GitHub (without including sensitive information)

---
**Remember**: Security is everyone's responsibility. When in doubt, err on the side of caution! 🛡️
