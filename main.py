from database import *
from fastapi import FastAPI, Depends, Body
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session


Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def main():
    return FileResponse("public/index.html")


@app.get("/api/items")
def get_items(db: Session = Depends(get_db)):
    return db.query(Item).all()


@app.get("/api/items/{id}")
def get_item(id, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == id).first()
    if item == None:
        return JSONResponse(status_code=404, content={"message": "Item not found!"})
    return item


@app.post("/api/items")
def create_item(data=Body(), db: Session = Depends(get_db)):
    item = Item(title=data["title"], description=data["description"], priority=data["priority"])
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.put("/api/items")
def edit_item(data=Body(), db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == data["id"]).first()
    if item == None:
        return JSONResponse(status_code=404, content={"message": "Item not found"})
    item.title = data["title"]
    item.description = data["description"]
    item.priority = data["priority"]
    db.commit()
    db.refresh(item)
    return item


@app.delete("/api/items/{id}")
def delete_item(id, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == id).first()
    if item == None:
        return JSONResponse(status_code=404, content={"message": "Item not found"})
    db.delete(item)
    db.commit()
    return item