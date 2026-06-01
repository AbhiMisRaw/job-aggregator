# app/dependencies.py
from fastapi import Query

class Params:
    def __init__(
        self,
        last_visited_ids: int = Query(None, ge=1, description="Page number"),
        page_size: int = Query(20, ge=1, le=100, description="Page size")
    ):
        self.last_visited_id = last_visited_ids
        self.page_size = page_size
