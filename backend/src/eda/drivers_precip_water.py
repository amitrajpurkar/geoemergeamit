from __future__ import annotations


def summarize_precip_water(*, region, start_date, end_date, sources) -> dict:
    _ = (region, start_date, end_date, sources)
    return {"summary": "Precipitation and standing-water proxy summary for the last 24 months.", "metrics": {}}
