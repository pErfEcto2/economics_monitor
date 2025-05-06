from graphene import ObjectType, Schema, List
from fastapi import FastAPI, HTTPException, Request
import lib
import classes


class Query(ObjectType):
    get_brent_crude_oil = List(classes.BrentCrudeOil)

    def resolve_get_brent_crude_oil(self, info):
        res = lib.exec_query("select * from brent_crude_oil")
        res = lib.query_res_to_dict(res, ["timestamp", "value", "units"])
        return res


schema = Schema(query=Query)
app = FastAPI()


@app.get("/")
async def index():
    return {"message": "hi"}

@app.get("/query")
async def query(request: Request):
    query = request.query_params.get("query", None)

    if not query:
        raise HTTPException(status_code=400, detail="query is not given")

    return schema.execute(query).data


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)

