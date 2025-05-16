from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from src.db import models, database
from src.services.organization_service import OrganizationService
from src.db.database import get_db

router = APIRouter()

@router.post("/organizations/")
def create_organization(name: str, invite_code: str, db: Session = Depends(get_db)):
    organization_service = OrganizationService(db)
    organization = organization_service.create_organization(name, invite_code)
    if organization:
        return {"message": "Organization created successfully", "organization": organization}
    raise HTTPException(status_code=400, detail="Failed to create organization")

@router.get("/organizations/{org_id}/members/")
def get_organization_members(org_id: int, db: Session = Depends(get_db)):
    organization_service = OrganizationService(db)
    members = organization_service.get_members(org_id)
    if members is not None:
        return {"members": members}
    raise HTTPException(status_code=404, detail="Organization not found")

@router.post("/organizations/{org_id}/members/")
def add_member_to_organization(org_id: int, user_id: int, db: Session = Depends(get_db)):
    organization_service = OrganizationService(db)
    success = organization_service.add_member(org_id, user_id)
    if success:
        return {"message": "Member added successfully"}
    raise HTTPException(status_code=400, detail="Failed to add member")