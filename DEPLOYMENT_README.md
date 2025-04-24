# Deployment Instructions

## FastAPI Backend
You can deploy your FastAPI backend to services like:
- [Render](https://render.com/docs/deploy-fastapi)
- [Railway](https://railway.app/template/Dm1WbL)

## React Frontend
You can deploy the React frontend (built with Vite) to:
- [Vercel](https://vercel.com)
- [Netlify](https://netlify.com)
- GitHub Pages (via `vite.config.js` config)

## Notes
- You can test build locally with `npm run build` inside `frontend/`
- To test FastAPI locally: `uvicorn api.main:app --reload`