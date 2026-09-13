from enum import Enum
from typing import Annotated

from fastapi import Depends, HTTPException

from models import User
from security import get_current_user


class UserRole(str, Enum):
    VIEWER = "Viewer"
    ANALYST = "Analyst"
    ADMIN = "Admin"


def allow_roles(allowed_roles: UserRole | list[UserRole] | set[UserRole]):
    if isinstance(allowed_roles, UserRole):
        roles_set = {allowed_roles}
    else:
        roles_set = set[UserRole](allowed_roles)

    def dependency(current_user: Annotated[User, Depends(get_current_user)]):
        if current_user.role not in roles_set:
            raise HTTPException(
                status_code=403, detail="Access denied: Insufficient privileges"
            )
        return current_user

    return dependency
