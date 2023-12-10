import json
from datetime import datetime

import duckdb


def serialize_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f" Object of type {type(obj)} is not JSON serializable")


def handler(event, context):
    query = event.get("query")
    if not query:
        return {"statusCode": 401, "body": "Invalid request body"}

    try:
        with duckdb.connect() as conn:
            conn.load_extension("httpfs")
            # DuckDB auto-loaded env vars
            conn.execute(
                """
                RESET s3_region;
                RESET s3_access_key_id;
                RESET s3_secret_access_key;
                RESET s3_session_token;
                """
            )
            result = conn.execute(query)
            body = {
                "columns": result.description,
                "rows": json.loads(
                    json.dumps(result.fetchall(), default=serialize_datetime)
                ),
            }

        return {"statusCode": 200, "body": body}

    except Exception as e:
        return {"statusCode": 400, "body": str(e)}
