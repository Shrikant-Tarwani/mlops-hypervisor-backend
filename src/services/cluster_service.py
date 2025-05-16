from typing import List, Dict

class Cluster:
    def __init__(self, name: str, ram: int, cpu: int, gpu: int):
        self.name = name
        self.ram = ram
        self.cpu = cpu
        self.gpu = gpu
        self.available_resources = {
            'ram': ram,
            'cpu': cpu,
            'gpu': gpu
        }
        self.deployments = []

    def allocate_resources(self, ram: int, cpu: int, gpu: int) -> bool:
        if self.available_resources['ram'] >= ram and \
           self.available_resources['cpu'] >= cpu and \
           self.available_resources['gpu'] >= gpu:
            self.available_resources['ram'] -= ram
            self.available_resources['cpu'] -= cpu
            self.available_resources['gpu'] -= gpu
            return True
        return False

    def release_resources(self, ram: int, cpu: int, gpu: int):
        self.available_resources['ram'] += ram
        self.available_resources['cpu'] += cpu
        self.available_resources['gpu'] += gpu

    def add_deployment(self, deployment: Dict):
        self.deployments.append(deployment)

class ClusterService:
    def __init__(self):
        self.clusters: Dict[str, Cluster] = {}

    def create_cluster(self, name: str, ram: int, cpu: int, gpu: int) -> Cluster:
        cluster = Cluster(name, ram, cpu, gpu)
        self.clusters[name] = cluster
        return cluster

    def get_cluster(self, name: str) -> Cluster:
        return self.clusters.get(name)

    def allocate_resources(self, cluster_name: str, ram: int, cpu: int, gpu: int) -> bool:
        cluster = self.get_cluster(cluster_name)
        if cluster:
            return cluster.allocate_resources(ram, cpu, gpu)
        return False

    def release_resources(self, cluster_name: str, ram: int, cpu: int, gpu: int):
        cluster = self.get_cluster(cluster_name)
        if cluster:
            cluster.release_resources(ram, cpu, gpu)

    def list_clusters(self) -> List[Cluster]:
        return list(self.clusters.values())