from graphene import ObjectType, Schema, List, DateTime
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import lib
import classes


class Query(ObjectType):
    get_brent_crude_oil = List(classes.EconomicIndicator, startDate=DateTime(), endDate=DateTime())

    # all rows from the db must be no older than date_input
    # date_input format: "year:month:day hour:minute:second"
    # "hour:minute:second" is optional
    def resolve_get_brent_crude_oil(self, _, startDate=None, endDate=None):
        q = f"select * from brent_crude_oil"

        if startDate is not None:
            q += f" where timestamp >= '{startDate}'"
        if endDate is not None:
            q += f" and timestamp <= '{endDate}'"
        
        res = lib.exec_query(q)
        res = lib.query_res_to_dict(res, ["timestamp", "value", "units"])
        return res


schema = Schema(query=Query)
app = FastAPI()
templates = Jinja2Templates(directory="src/frontend")

app.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")
app.mount("/js", StaticFiles(directory="src/frontend/js"), name="js")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# query example:
# http://localhost:8080/query?query=query%20{%20getBrentCrudeOil%20{%20timestamp%20value%20units%20}%20}
# spaces, brackets, etc are url encoded
@app.get("/query")
async def query(request: Request):
    q = request.query_params.get("query", None)

    if not q:
        raise HTTPException(status_code=400, detail="query is not given")

    return schema.execute(q).data


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)

