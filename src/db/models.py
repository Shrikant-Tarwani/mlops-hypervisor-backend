from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.db.database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    organization_id = Column(Integer, ForeignKey('organizations.id'))

    organization = relationship("Organization", back_populates="members")

class Organization(Base):
    __tablename__ = 'organizations'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    invite_code = Column(String, unique=True)

    members = relationship("User", back_populates="organization")

class Cluster(Base):
    __tablename__ = 'clusters'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    ram = Column(Integer)  # in MB
    cpu = Column(Integer)  # number of CPUs
    gpu = Column(Integer)  # number of GPUs
    organization_id = Column(Integer, ForeignKey('organizations.id'))

    organization = relationship("Organization")

class Deployment(Base):
    __tablename__ = 'deployments'

    id = Column(Integer, primary_key=True, index=True)
    docker_image = Column(String)
    ram_required = Column(Integer)  # in MB
    cpu_required = Column(Integer)  # number of CPUs
    gpu_required = Column(Integer)  # number of GPUs
    cluster_id = Column(Integer, ForeignKey('clusters.id'))
    priority = Column(Integer)

    cluster = relationship("Cluster")