from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from src.services.deployment_service import DeploymentService
from src.services.cluster_service import ClusterService
from src.core.scheduler import Scheduler

def get_deployment_service():
    cluster_service = ClusterService()
    scheduler = Scheduler()
    return DeploymentService(cluster_service, scheduler)

router = APIRouter()

class DeploymentCreate(BaseModel):
    cluster_id: int
    image_path: str
    ram: int
    cpu: int
    gpu: int
    priority: int

class DeploymentResponse(BaseModel):
    id: int
    cluster_id: int
    image_path: str
    ram: int
    cpu: int
    gpu: int
    priority: int
    status: str
@router.post("/deployments/", response_model=DeploymentResponse)
async def create_deployment(
    deployment: DeploymentCreate,
    deployment_service: DeploymentService = Depends(get_deployment_service)
):
    try:
        return await deployment_service.create_deployment(deployment)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/deployments/", response_model=List[DeploymentResponse])
async def list_deployments(deployment_service: DeploymentService = Depends(get_deployment_service)):
    return await deployment_service.list_deployments()

@router.get("/deployments/{deployment_id}", response_model=DeploymentResponse)
async def get_deployment(deployment_id: int, deployment_service: DeploymentService = Depends(get_deployment_service)):
    deployment = await deployment_service.get_deployment(deployment_id)
    if not deployment:
        raise HTTPException(status_code=404, detail="Deployment not found")
    return deployment