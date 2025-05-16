from collections import deque

class Deployment:
    def __init__(self, id, image, ram, cpu, gpu, priority):
        self.id = id
        self.image = image
        self.ram = ram
        self.cpu = cpu
        self.gpu = gpu
        self.priority = priority
        self.status = 'queued'

class Cluster:
    def __init__(self, id, total_ram, total_cpu, total_gpu):
        self.id = id
        self.total_ram = total_ram
        self.total_cpu = total_cpu
        self.total_gpu = total_gpu
        self.available_ram = total_ram
        self.available_cpu = total_cpu
        self.available_gpu = total_gpu
        self.deployments = deque()

    def can_allocate(self, deployment):
        return (self.available_ram >= deployment.ram and
                self.available_cpu >= deployment.cpu and
                self.available_gpu >= deployment.gpu)

    def allocate_resources(self, deployment):
        if self.can_allocate(deployment):
            self.available_ram -= deployment.ram
            self.available_cpu -= deployment.cpu
            self.available_gpu -= deployment.gpu
            deployment.status = 'running'
            return True
        return False

    def release_resources(self, deployment):
        self.available_ram += deployment.ram
        self.available_cpu += deployment.cpu
        self.available_gpu += deployment.gpu
        deployment.status = 'completed'

class Scheduler:
    def __init__(self):
        self.clusters = {}
        self.deployment_queue = deque()

    def add_cluster(self, cluster):
        self.clusters[cluster.id] = cluster

    def queue_deployment(self, deployment):
        self.deployment_queue.append(deployment)

    def schedule_deployments(self):
        while self.deployment_queue:
            deployment = self.deployment_queue.popleft()
            cluster = self.find_best_cluster(deployment)
            if cluster:
                if cluster.allocate_resources(deployment):
                    print(f"Deployment {deployment.id} scheduled on Cluster {cluster.id}.")
                else:
                    self.deployment_queue.append(deployment)  # Requeue if not allocated
            else:
                self.deployment_queue.append(deployment)  # Requeue if no cluster found

    def find_best_cluster(self, deployment):
        # Sort clusters by available resources and prioritize based on deployment priority
        sorted_clusters = sorted(self.clusters.values(), key=lambda c: (c.available_ram, c.available_cpu, c.available_gpu))
        for cluster in sorted_clusters:
            if cluster.can_allocate(deployment):
                return cluster
        return None

    def release_deployment(self, deployment):
        for cluster in self.clusters.values():
            if deployment in cluster.deployments:
                cluster.release_resources(deployment)
                cluster.deployments.remove(deployment)
                print(f"Deployment {deployment.id} completed on Cluster {cluster.id}.")
                break