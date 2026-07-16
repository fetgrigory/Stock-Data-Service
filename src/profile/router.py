import os
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

# Templates
templates = Jinja2Templates(directory=os.path.join("src", "templates"))


# Profile page route
@router.get("/profile", response_class=HTMLResponse)
def profile(request: Request):
    return templates.TemplateResponse(
        name="profile.html",
        context={},
        request=request
    )
