from __future__ import annotations


def summarize_vegetation(*, region, start_date, end_date, sources) -> dict:
    _ = (region, start_date, end_date, sources)
    return {"summary": "Vegetation conditions summary for the last 24 months.", "metrics": {}}
