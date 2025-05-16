from sqlalchemy.orm import Session
from src.db.models import Organization, User
from src.services.auth_service import AuthService

class OrganizationService:
    def __init__(self, db: Session):
        self.db = db
        self.auth_service = AuthService(db)

    def create_organization(self, name: str, invite_code: str):
        organization = Organization(name=name, invite_code=invite_code)
        self.db.add(organization)
        self.db.commit()
        self.db.refresh(organization)
        return organization

    def add_user_to_organization(self, user_id: int, organization_id: int):
        user = self.auth_service.get_user_by_id(user_id)
        organization = self.db.query(Organization).filter(Organization.id == organization_id).first()
        
        if user and organization:
            organization.members.append(user)
            self.db.commit()
            return organization
        return None

    def get_organizations_for_user(self, user_id: int):
        return self.db.query(Organization).filter(Organization.members.any(id=user_id)).all()