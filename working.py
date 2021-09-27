from fastapi import FastAPI, Path, Query, HTTPException, status
from typing import Optional
from pydantic import BaseModel

app = FastAPI() #create an API object that will initialize the API

#An API endpoint is the point of entry in a communication channel when two system are interacting. 
# It refers to touch points of the communication betwee an aPI and a server.


class Item(BaseModel): 
    name: str
    price: float
    brand: Optional[str] = None

class UpdateItem(BaseModel): 
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None

@app.get("/")
def home():
    return {"Data": "Testing"}
#to run this localhost, type in the terminal: uvicorn working:app --reload

@app.get("/about")
def about():
    return {"Data": "About"}

inventory = {}

@app.get("/get-item/{item_id}")
def get_item(item_id: int = Path(None, description="The ID of the item you would like to view", gt = 0)):
    return inventory[item_id]

# if you only want Query parameters
# @app.get("/get-by-name")
# def get_item(*, name: Optional[str] = None, test: int): #you can have a required parameters after a optional one, you move the test to the beginning or add the * as the first one)
#     for item_id in inventory:
#         if inventory[item_id]["name"] == name:
#             return inventory[item_id]
#     return {"Data": "Not found"}

#query and path parameters together

@app.get("/get-by-name/{item_id}")
def get_item(*, item_id: int, name: Optional[str] = None, test: int): #you can have a required parameters after a optional one, you move the test to the beginning or add the * as the first one)
    for item_id in inventory:
        if inventory[item_id].name == name:
            return inventory[item_id]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item name not found")
    #you could also have raise HTTPException(status_code=404)

@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item): 
    if item_id in inventory: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item ID already exist")

    inventory[item_id] = item
    return inventory[item_id]

@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem): 
    if item_id not in inventory: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item ID not found")

    if item.name != None: 
        inventory[item_id].name = item.name

    if item.price != None: 
        inventory[item_id].price = item.price

    if item.brand != None: 
        inventory[item_id].brand = item.brand

    return inventory[item_id]

@app.delete("/delete-item")
def delete_item(item_id: int = Query(..., description="The ID of the item to delete", gt=0)): 
    if item_id  not in inventory: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item ID not found")

    del inventory[item_id]

    return {"Success:" "Item deleted"}