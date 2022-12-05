from fastapi import FastAPI, HTTPException, Depends, Request, Form, Request, Response, status
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from typing import Union
import requests
import json
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets


security = HTTPBasic()

Base = declarative_base()

templates = Jinja2Templates(directory="templates/")


class Endpoint(Base):
    __tablename__ = "Endpoints"
    id = Column(Integer, primary_key=True, index=True)
    endpoint = Column(String)
    ip = Column(String)
    port = Column(String)


engine = create_engine(
    "sqlite:///./gatewayway.db", connect_args={"check_same_thread": False}
)

app = FastAPI()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "Habiba")
    correct_password = secrets.compare_digest(
        credentials.password, "habiba@12")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/users/me")
def read_current_user(username: str = Depends(get_current_username)):
    return {"username": username}


@app.delete("/gateway/{endpoint}/{param}")
def delete_api(endpoint: str, param: str, response: Response,  request: Request, db: Session = Depends(get_db), username: str = Depends(get_current_username)):
    print(username)

    endpoint_obj = db.query(Endpoint).filter_by(endpoint=endpoint).first()
    if endpoint_obj is None:
        raise HTTPException(status_code=404, detail="Endpoint not found")

    db.delete(endpoint_obj)
    db.commit()
    return True


@app.post("/gateway/{endpoint}/{param}")
@app.post("/gateway/{endpoint}")
async def post_gateway(
    endpoint: str,
    response: Response,
    request: Request,
    param: Union[str, None] = None,
    db: Session = Depends(get_db),
    username: str = Depends(get_current_username)
):
    print(username)

    body = await request.body()
    body = json.loads(body)

    endpoint_obj = db.query(Endpoint).filter_by(endpoint=endpoint).first()

    if endpoint_obj is None:
        raise HTTPException(status_code=404, detail="Endpoint not found")

    ip = endpoint_obj.ip
    port = endpoint_obj.port

    if param:
        api_url = "http://{}:{}/{}".format(ip, port, param)
    else:
        api_url = "http://{}:{}".format(ip, port)
    print(api_url)

    api_response = requests.post(api_url, json=body)
    response.status_code = api_response.status_code
    return api_response.json()


@app.get("/gateway/{endpoint}/{param}")
@app.get("/gateway/{endpoint}")
def read_api(
    endpoint: str,
    response: Response,
    param: Union[str, None] = None,
    db: Session = Depends(get_db),
    username: str = Depends(get_current_username)
):
    print(username)

    print(endpoint)
    endpoint_obj = db.query(Endpoint).filter_by(endpoint=endpoint).first()

    if endpoint_obj is None:
        raise HTTPException(status_code=404, detail="Endpoint not found")

    ip = endpoint_obj.ip
    port = endpoint_obj.port
    endpoint = endpoint_obj.endpoint

    if param:
        api_url = "http://{}:{}/{}".format(ip, port, param)
    else:
        api_url = "http://{}:{}".format(ip, port)
    print(api_url)

    api_response = requests.get(api_url)
    response.status_code = api_response.status_code
    return api_response.json()


@app.put("/gateway/{endpoint}/{param}")
@app.put("/gateway/{endpoint}")
async def update_api(
    endpoint: str,
    request: Request,
    response: Response,
    param: Union[str, None] = None,
    db: Session = Depends(get_db),
    username: str = Depends(get_current_username)
):
    print(username)

    body = await request.body()
    body = json.loads(body)

    endpoint_obj = db.query(Endpoint).filter_by(endpoint=endpoint).first()

    if endpoint_obj is None:
        raise HTTPException(status_code=404, detail="Endpoint not found")

    ip = endpoint_obj.ip
    port = endpoint_obj.port

    if param:
        api_url = "http://{}:{}/{}".format(ip, port, param)
    else:
        api_url = "http://{}:{}".format(ip, port)
    print(api_url)

    api_response = requests.put(api_url, json=body)
    response.status_code = api_response.status_code
    return api_response.json()


@app.get("/")
@app.get("/index")
def index(request: Request, db: Session = Depends(get_db), username: str = Depends(get_current_username)):
    print(username)

    return get_all_endpoint(request, db)


@app.post("/add")
def add(
    request: Request,
    endpoint: str = Form(...),
    ip: str = Form(...),
    port: str = Form(...),
    db: Session = Depends(get_db),
    username: str = Depends(get_current_username)
):
    print(username)

    endpoint = Endpoint(endpoint=endpoint, ip=ip, port=port)
    db.add(endpoint)
    db.commit()
    return get_all_endpoint(request, db)


@app.delete("/delete/{id}")
def delete(
    id: int,
    request: Request,
    db: Session = Depends(get_db),
    username: str = Depends(get_current_username)
):
    print(username)

    endpoint = db.query(Endpoint).filter_by(id=id).first()
    db.delete(endpoint)
    db.commit()
    return get_all_endpoint(request, db)


def get_all_endpoint(
    request: Request,
    db: Session,
    username: str = Depends(get_current_username)
):
    print(username)

    endpoints = db.query(Endpoint).all()
    return templates.TemplateResponse(
        "index.html", context={"request": request, "endpoints": endpoints}
    )
