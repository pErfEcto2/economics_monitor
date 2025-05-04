from graphene import ObjectType, String, Schema, Int, Field, List
from fastapi import FastAPI, Request



users = [
        {
            "id": 1,
            "name": "test 1"
            },
        {
            "id": 2,
            "name": "test 2"
            }
        ]



class User(ObjectType):
    id = Int()
    name = String()


class Query(ObjectType):
    get_user = Field(User, id = Int())
    get_users = List(User)

    def resolve_get_user(self, info, id):
        return list(filter(lambda x: x["id"] == id, users))[0]

    def resolve_get_users(self, info):
        return users


schema = Schema(query=Query)
app = FastAPI()


@app.get("/")
async def index():
    return {"message": "hi"}

@app.get("/query")
async def query(request: Request):
    query = request.query_params.get("query", None)

    if not query:
        return {"message": "nope"}

    return schema.execute(query).data


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
