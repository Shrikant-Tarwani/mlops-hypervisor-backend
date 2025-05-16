from typing import List, Dict, Any
from fastapi import HTTPException
from .cluster_service import ClusterService
from src.core.scheduler import Scheduler
from src.db.models import Deployment, Cluster

class DeploymentService:
    def __init__(self, cluster_service: ClusterService, scheduler: Scheduler):
        self.cluster_service = cluster_service
        self.scheduler = scheduler

    def create_deployment(self, cluster_id: str, docker_image: str, resources: Dict[str, Any]) -> Deployment:
        cluster = self.cluster_service.get_cluster(cluster_id)
        if not cluster:
            raise HTTPException(status_code=404, detail="Cluster not found")

        if not self.cluster_service.has_sufficient_resources(cluster, resources):
            raise HTTPException(status_code=400, detail="Insufficient resources in the cluster")

        deployment = Deployment(cluster_id=cluster_id, docker_image=docker_image, resources=resources)
        self.cluster_service.allocate_resources(cluster, resources)
        self.scheduler.schedule_deployment(deployment)
        return deployment

    def queue_deployment(self, deployment: Deployment) -> None:
        self.scheduler.add_to_queue(deployment)

    def get_deployment_status(self, deployment_id: str) -> str:
        deployment = self.scheduler.get_deployment(deployment_id)
        if not deployment:
            raise HTTPException(status_code=404, detail="Deployment not found")
        return deployment.status

    def list_deployments(self, cluster_id: str) -> List[Deployment]:
        return self.scheduler.get_deployments_by_cluster(cluster_id)