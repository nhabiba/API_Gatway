from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./user.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class LoginC(Base):
    __tablename__ = "Login"
    id = Column(Integer, primary_key=True, index=True)
    Email_address = Column(String)
    password = Column(String)


app = FastAPI()
Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Login(BaseModel):
    Email_address: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=1, max_length=100)


@app.get("/")
def read_api(db: Session = Depends(get_db)):
    return db.query(LoginC).all()


@app.post("/")
def login(login: Login, db: Session = Depends(get_db)):
    login_model = LoginC()
    login_model.Email_address = login.Email_address
    login_model.password = login.password
    db.add(login_model)
    db.commit()
    return login
