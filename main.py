from fastapi import FastAPI
from pydantic import BaseModel
import polars as pl
import tldextract
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Item(BaseModel):
    url: str


@app.post("/check")
async def check(item: Item):
    df = pl.read_parquet('df.parquet')
    response = df.filter(pl.col('url') == item.url)

    domain = tldextract.extract(item.url).domain

    similar = df.filter(pl.col('domain') == domain)

    return {
        'found': response.to_dicts(),
        'similar': similar.to_dicts()
    }
