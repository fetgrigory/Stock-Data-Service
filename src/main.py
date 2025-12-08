'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 23/09/2025
Ending //

'''
# Installing the necessary libraries
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqladmin import Admin
from src.db.database import sync_engine, init_db
from src.admin_panel.views import RecipientAdmin, UserAdmin, SmtpSettingAdmin
from src.auth.user_router import router as auth_router
from src.core.router import router as page_router
from src.email.router import router as smtp_router


def create_app():
    """AI is creating summary for create_app

    Returns:
        FastAPI: [description]
    """
    fastapi_app = FastAPI()

    # Connecting static files
    fastapi_app.mount("/static", StaticFiles(directory="src/static"), name="static")

    # Connecting routers
    fastapi_app.include_router(smtp_router)
    fastapi_app.include_router(page_router)
    fastapi_app.include_router(auth_router)

    # Initializing the database
    init_db()
    # Configuring SQLAdmin
    admin = Admin(fastapi_app, sync_engine)
    admin.add_view(RecipientAdmin)
    admin.add_view(UserAdmin)
    admin.add_view(SmtpSettingAdmin)
    return fastapi_app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("src.main:app", host='127.0.0.1', port=8000, reload=True)
