#!/usr/bin/env python3
"""
AI Business Intelligence Automation Platform
FastAPI Main Application

Author: Urja Kotwal
Date: 2026-05-22
Version: 1.0.0
"""

import logging
import os
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZIPMiddleware
import uvicorn

# ========================================
# Configuration
# ========================================
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# ========================================
# Logging Setup
# ========================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ========================================
# Lifespan Events
# ========================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown events
    """
    # Startup
    logger.info("🚀 Starting AI Business Intelligence Automation Platform")
    logger.info(f"Environment: {ENVIRONMENT}")
    logger.info(f"Debug Mode: {DEBUG}")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down application")


# ========================================
# FastAPI Application
# ========================================
app = FastAPI(
    title="AI Business Intelligence Automation Platform",
    description="Production-ready intelligent automation system combining n8n, Milvus, FastAPI, and Power BI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
    debug=DEBUG
)

# ========================================
# CORS Middleware
# ========================================
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:8000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========================================
# GZIP Middleware for compression
# ========================================
app.add_middleware(GZIPMiddleware, minimum_size=1000)

# ========================================
# Health Check Route
# ========================================
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": ENVIRONMENT,
        "version": "1.0.0",
        "services": {
            "api": "running",
            "milvus": "connected",
            "database": "connected"
        }
    }


@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint with API information
    """
    return {
        "name": "AI Business Intelligence Automation Platform",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health"
    }


# ========================================
# Error Handlers
# ========================================
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """
    Handle HTTP exceptions
    """
    logger.error(f"HTTP Exception: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "timestamp": datetime.utcnow().isoformat()}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """
    Handle general exceptions
    """
    logger.error(f"Unhandled Exception: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "timestamp": datetime.utcnow().isoformat()
        }
    )


# ========================================
# Routes (Placeholder - implement in routes/)
# ========================================
@app.post("/api/v1/upload", tags=["Upload"])
async def upload_file():
    """
    Upload and process Excel file
    """
    return {"message": "Upload endpoint - implement in routes/upload.py"}


@app.get("/api/v1/records", tags=["Records"])
async def get_records():
    """
    Get records with pagination
    """
    return {"message": "Records endpoint - implement in routes/records.py"}


@app.post("/api/v1/search", tags=["Search"])
async def semantic_search():
    """
    Semantic search endpoint
    """
    return {"message": "Search endpoint - implement in routes/search.py"}


# ========================================
# Startup Event
# ========================================
@app.on_event("startup")
async def startup_event():
    """
    Run on application startup
    """
    logger.info("✅ FastAPI startup complete")


# ========================================
# Shutdown Event
# ========================================
@app.on_event("shutdown")
async def shutdown_event():
    """
    Run on application shutdown
    """
    logger.info("🛑 FastAPI shutdown")


# ========================================
# Main Entry Point
# ========================================
if __name__ == "__main__":
    host = os.getenv("FASTAPI_HOST", "0.0.0.0")
    port = int(os.getenv("FASTAPI_PORT", 8000))
    reload = os.getenv("FASTAPI_RELOAD", "true").lower() == "true"
    
    logger.info(f"Starting server on {host}:{port}")
    
    uvicorn.run(
        "app:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info",
    )
