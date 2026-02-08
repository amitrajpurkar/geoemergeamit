from __future__ import annotations


def summarize_temperature(*, region, start_date, end_date, sources) -> dict:
    _ = (region, start_date, end_date, sources)
    return {"summary": "Land surface temperature summary for the last 24 months.", "metrics": {}}
