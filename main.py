from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
import os
from app import datactl  


app = FastAPI()

origins = [
    "http://localhost:8080",
    "http://localhost:8000"
    # 추가로 허용할 도메인들
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def getTest():
    message = "hello"
    return{"message": message}

@app.get("/product")
async def getProduct(company=None, start_date="2004-01-16", end_date="2020-07-10"):
    data = datactl.get_product(company, start_date, end_date)

    return {"data": data}

@app.get("/ingredient")
async def getIngredient(company=None, start_date="2004-01-16", end_date="2020-07-10"):
    data = datactl.get_ingredient(company, start_date, end_date)

    return {"data": data}

@app.get("/all")
async def getAll(start_date="2004-01-16", end_date="2020-07-10"):
    data = datactl.get_all(start_date, end_date)

    return {"data": data}

@app.get("/company_column")
async def geCompanyColumn():
    data = datactl.get_company_columns()

    return {"data": data}

if __name__ == "__main__":
   #inner_ip = os.popen("hostname -I").read()
    port = str(input("insert port: "))
    run = f"sudo uvicorn main:app --reload --host=localhost --port={port}"
    os.system(run.replace("\n",""))