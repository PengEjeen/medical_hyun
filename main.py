from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app import datactl
from starlette.requests import Request

import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

origins = [
    "http://localhost:8080",
    "http://localhost:8000",
    "*"
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

# 제품 데이터 페이지
@app.get("/product_page", response_class=HTMLResponse)
async def get_product_page(request: Request):
    return templates.TemplateResponse("product.html", {"request": request})

# 성분 데이터 페이지
@app.get("/ingredient_page", response_class=HTMLResponse)
async def get_ingredient_page(request: Request):
    return templates.TemplateResponse("ingredient.html", {"request": request})

# 전체 데이터 페이지
@app.get("/all_page", response_class=HTMLResponse)
async def get_all_page(request: Request):
    return templates.TemplateResponse("all.html", {"request": request})

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
