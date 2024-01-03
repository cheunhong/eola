import duckdb
from pydantic import BaseModel


class Event(BaseModel):
    queries: list[str]
    session: str


def handler(event, context):
    try:
        event = Event(**event)
        for query in event.queries:
            with duckdb.connect(f"/tmp/{event.session}.db") as conn:
                conn.execute(query)

        return {"statusCode": 200}

    except Exception as e:
        return {"statusCode": 400, "body": str(e)}
