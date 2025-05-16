from fastapi import FastAPI
from src.api import auth, organizations, clusters, deployments
from src.core.config import settings

app = FastAPI(title="MLOps Hypervisor Backend")

# Include routers for different API endpoints
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(organizations.router, prefix="/organizations", tags=["Organizations"])
app.include_router(clusters.router, prefix="/clusters", tags=["Clusters"])
app.include_router(deployments.router, prefix="/deployments", tags=["Deployments"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the MLOps Hypervisor Backend"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)