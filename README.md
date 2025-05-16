# MLOps Hypervisor Backend

## Overview
The MLOps Hypervisor Backend is a service designed to manage user authentication, organization membership, cluster resource allocation, and deployment scheduling for machine learning operations. This service optimizes deployment priority, resource utilization, and maximizes successful deployments.

## Features
- **User Authentication**: Basic authentication mechanism with support for invite codes.
- **Organization Management**: Users can join organizations and manage memberships.
- **Cluster Management**: Create clusters with fixed resources and track resource allocation.
- **Deployment Management**: Create deployments, manage resource allocation, and queue deployments based on availability.
- **Scheduling Algorithm**: Implements a preemption-based scheduling algorithm to prioritize deployments.

## Getting Started

### Prerequisites
- Python 3.11 (or 3.10) 
- SQLite for the database

### Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   cd mlops-hypervisor-backend
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up the environment variables:
   - Copy `.env.example` to `.env` and update the values as needed.

### Running the Service

1. **Make sure you are in the project root directory** (the folder containing `src/`).

2. **(Optional but recommended) Create and activate a Python virtual environment**:
   ```
   python3.11 -m venv venv
   source venv/bin/activate
   ```


3. **Run the application using the Python module syntax** (this ensures imports work correctly):
   ```
   python -m src.main
   ```

   This will start the FastAPI server using your configuration.

4. Access the API at `http://localhost:8000` (or the configured port).

## API Endpoints
- **Authentication**: `/auth`
- **Organizations**: `/organizations`
- **Clusters**: `/clusters`
- **Deployments**: `/deployments`

## Testing
To run the unit tests, use:
```
pytest src/tests
```

## UML Diagram
The UML diagram representing the database schema can be found in `src/db/uml_diagram.puml`.