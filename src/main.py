'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 23/09/2025
Ending //

'''
# Installing the necessary libraries
import uvicorn
from fastapi import FastAPI
from recipients.router import router as recipients_router
from smtp.router import router as smtp_router
from database import create_recipients_table

app = FastAPI()
# Creating a table at the start of the application
create_recipients_table()
# Connecting routers
app.include_router(recipients_router)
app.include_router(smtp_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)
