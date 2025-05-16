from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from src.services.cluster_service import ClusterService

router = APIRouter()
cluster_service = ClusterService()

class ClusterCreate(BaseModel):
    name: str
    ram: int  # in MB
    cpu: int  # number of CPUs
    gpu: int  # number of GPUs

class ClusterResponse(BaseModel):
    id: int
    name: str
    ram: int
    cpu: int
    gpu: int

@router.post("/clusters/", response_model=ClusterResponse)
async def create_cluster(cluster: ClusterCreate):
    created_cluster = cluster_service.create_cluster(cluster.name, cluster.ram, cluster.cpu, cluster.gpu)
    if not created_cluster:
        raise HTTPException(status_code=400, detail="Cluster creation failed")
    return created_cluster

@router.get("/clusters/", response_model=List[ClusterResponse])
async def list_clusters():
    return cluster_service.list_clusters()

@router.get("/clusters/{cluster_id}", response_model=ClusterResponse)
async def get_cluster(cluster_id: int):
    cluster = cluster_service.get_cluster(cluster_id)
    if not cluster:
        raise HTTPException(status_code=404, detail="Cluster not found")
    return cluster

@router.delete("/clusters/{cluster_id}")
async def delete_cluster(cluster_id: int):
    success = cluster_service.delete_cluster(cluster_id)
    if not success:
        raise HTTPException(status_code=404, detail="Cluster not found")
    return {"detail": "Cluster deleted successfully"}