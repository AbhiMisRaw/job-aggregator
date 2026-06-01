To implement role and permission-based authorization in FastAPI, you should leverage its native Dependency Injection (Depends) system. The cleanest architecture decouples authentication from authorization: authentication extracts the user's role, while authorization enforces permissions at the endpoint level using a reusable class dependency.Here is a complete, production-ready guide to building a dynamic Role-Based Access Control (RBAC) system.1. Define the User & Role SchemasUse Pydantic to mock your user model, linking specific permissions to structural roles.pythonfrom pydantic import BaseModel
from typing import List, Dict

# Define permissions as granular actions
# Roles are bundles of permissions: "Who you are" vs "What you can do"

```python
ROLE_PERMISSIONS: Dict[str, List[str]] = {
    "admin": ["items:create", "items:read", "items:update", "items:delete"],
    "editor": ["items:read", "items:update"],
    "viewer": ["items:read"]
}

class User(BaseModel):
    username: str
    role: str  # e.g., "admin", "editor", "viewer"
```

Use code with caution.2. Create the Authentication DependencyIn a real application, you would decode a JSON Web Token (JWT) here. For structural simplicity, this mock dependency extracts the current user.pythonfrom fastapi import HTTPException, Security, status
from Use code with caution.pythonfastapi.securityUse code with caution.python import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    # Real app: Decode JWT token and fetch user from database
    # For this snippet, we simulate an authenticated 'editor'
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid token"
        )
    return User(username="johndoe", role="editor")
Use code with caution.3. Build a Reusable Permission GuardCreate a callable class to check if the authenticated user's role contains the required permissions. This approach scales cleanly across hundreds of endpoints.

```python
class PermissionChecker:
    def __init__(self, required_permissions: List[str]):
        self.required_permissions = required_permissions

    def __call__(self, current_user: User = Depends(get_current_user)):
        # Retrieve permissions associated with the user's role
        user_permissions = ROLE_PERMISSIONS.get(current_user.role, [])
        
        # Check if user has all the required permissions for the endpoint
        has_permission = all(perm in user_permissions for perm in self.required_permissions)
        
        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted with your current role clearance."
            )
        return current_user
```
Use code with caution.4. Apply the Guard to FastAPI EndpointsEnforce access restrictions on your route handlers by declaring the PermissionChecker inside the Depends() statement.
```python
from fastapi import FastAPI, Depends

app = FastAPI()

@app.get("/items", dependencies=[Depends(PermissionChecker(["items:read"]))])
async def read_items():
    return {"message": "Success! Anyone with view, edit, or admin access can see this."}

@app.post("/items", dependencies=[Depends(PermissionChecker(["items:create"]))])
async def create_item():
    return {"message": "Success! Only Admins can execute this action."}

@app.put("/items", dependencies=[Depends(PermissionChecker(["items:update"]))])
async def update_item():
    return {"message": "Success! Editors and Admins can update this resource."}

```
Use code with caution.Advanced Considerations for ScaleOAuth2 Scopes: If your system exposes third-party APIs, map your permissions directly into FastAPI OAuth2 Scopes. This automatically displays required access privileges inside your interactive Swagger UI documentation.Database Management: For highly dynamic business environments, avoid hardcoding roles. Persist your roles, permissions, and many-to-many relationship structures using an ORM like SQLAlchemy.Third-Party Engines: If your access policies depend on resource attributes (e.g., User can only edit items they own), utilize structured micro-authorization engines like Permit.io or Cerbos.