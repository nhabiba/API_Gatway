from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy import Column,  Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./Book.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Books(Base):
    __tablename__ = "Books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    description = Column(String)
    rating = Column(Integer)


app = FastAPI()
Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Book(BaseModel):
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(it=101)


@app.get("/")
def read_api(db: Session = Depends(get_db)):
    return db.query(Books).all()


@app.post("/")
def create_book(book: Book, db: Session = Depends(get_db)):
    book_model = Books()
    book_model.title = book.title
    book_model.author = book.author
    book_model.description = book.description
    book_model.rating = book.rating
    db.add(book_model)
    db.commit()
    return book


@app.delete("/{book_id}")
async def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Books).filter_by(id=book_id).first()
    db.delete(book)
    db.commit()
    return True


@app.put("/{book_id}")
async def update_book(book_id: int, new_book: Book, db: Session = Depends(get_db)):
    book = db.query(Books).filter_by(id=book_id).first()

    if book is None:
        raise HTTPException(
            status_code=404, detail=f"Id {book_id} :Does not exist")

    book.title = new_book.title
    book.author = new_book.author
    book.description = new_book.description
    book.rating = new_book.rating

    db.commit()
    book = db.query(Books).filter_by(id=book_id).first()
    return book
