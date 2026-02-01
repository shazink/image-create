# AI Image Generator (MVP)

A minimal AI-powered image generator using Stable Diffusion.

## Tech Stack
- FastAPI (backend)
- React + Vite (frontend)
- Hugging Face Inference API

## How it works
1. User enters a prompt
2. Backend sends prompt to Stable Diffusion
3. Generated image is returned and displayed

## Run locally

### Backend
```bash
uvicorn main:app --reload
