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
from src.auth.router import router as auth_router
from src.core.router import router as page_router
from src.recipients.router import router as recipients_router
from src.email.router import router as smtp_router
from src.db.database import create_recipients_table

app = FastAPI()
# Connecting static files
app.mount("/static", StaticFiles(directory="src/static"), name="static")
# Creating a table at the start of the application
create_recipients_table()
# Connecting routers
app.include_router(recipients_router)
app.include_router(smtp_router)
app.include_router(page_router)
app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run("src.main:app", host='127.0.0.1', port=8000, reload=True)
