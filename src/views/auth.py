from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="src/views/templates")

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get(
    "/reset-password/{token}", response_class=HTMLResponse, include_in_schema=False
)
async def reset_password_form(request: Request, token: str):
    return templates.TemplateResponse(
        "reset_password.html", {"request": request, "token": token}
    )
