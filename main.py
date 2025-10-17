from fastapi import FastAPI, Response, status
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    desc: str | None = None
    price: float
    tax: float | None = None


mock_item_db = [
    {
        "id": 1,
        "name": "Item One",
        "desc": "The first item",
        "price": 10.5,
        "tax": 0.5,
    },
    {
        "id": 2,
        "name": "Item Two",
        "desc": "The second item",
        "price": 20.0,
        "tax": 1.0,
    },
    {
        "id": 3,
        "name": "Item Three",
        "desc": "The third item",
        "price": 15.75,
        "tax": 0.75,
    },
]
app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "ROOT"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, res: Response):
    filtered_items = [item for item in mock_item_db if item["id"] == item_id]
    if not filtered_items:
        res.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "Item not found"}
    return filtered_items[0]


@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return mock_item_db[skip : skip + limit]


@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.model_dump()
    item_dict.update({"id": len(mock_item_db) + 1})
    if item_dict["tax"] is not None:
        item_dict.update({"taxed_price": item_dict["price"] + item_dict["tax"]})
    mock_item_db.append(item_dict)
    return item_dict


@app.put("/items/{item_id}")
async def update_item(
    item_id: int, item: Item, res: Response, query: str | None = None
):
    for idx, existing_item in enumerate(mock_item_db):
        if existing_item["id"] == item_id:
            item_dict = item.model_dump()
            if query:
                item_dict.update({"query": query})
            if item_dict["tax"] is not None:
                item_dict.update({"taxed_price": item_dict["price"] + item_dict["tax"]})
            mock_item_db[idx] = item_dict
            return item_dict

    res.status_code = status.HTTP_404_NOT_FOUND
    return {"message": "Item not found"}
