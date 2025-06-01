from fastapi import FastAPI
from contextlib import asynccontextmanager
from utils.db_util import lifespan_manager
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, task


# Lifespan event handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    async with lifespan_manager():
        yield


# Create FastAPI instance with lifespan
app = FastAPI(
    version="1.0.0",
    lifespan=lifespan,
    title="Task Manager App API",
    description="A FastAPI application with Prisma & NeonDB",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Include routers
app.include_router(auth.router)
app.include_router(task.router)


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    return {
        "docs": "/docs",
        "status": "running",
        "message": "FastAPI With Prisma & NeonDB",
    }


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy", "message": "API is running successfully"}
