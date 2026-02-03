from __future__ import annotations

from typing import Any


def dataframe_summary(df: Any) -> dict[str, Any]:
    shape = getattr(df, "shape", None)
    columns = list(getattr(df, "columns", []) or [])

    summary: dict[str, Any] = {
        "shape": shape,
        "columns": columns,
    }

    isnull = getattr(df, "isnull", None)
    if callable(isnull):
        try:
            missing = df.isnull().sum().to_dict()  # type: ignore[attr-defined]
            summary["missing"] = missing
        except Exception:
            pass

    describe = getattr(df, "describe", None)
    if callable(describe):
        try:
            stats = df.describe(include="all").to_dict()  # type: ignore[attr-defined]
            summary["describe"] = stats
        except Exception:
            pass

    return summary
