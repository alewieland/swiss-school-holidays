import warnings
from datetime import date, datetime
from pathlib import Path

from .utils import load_json_gz, overlap_period

# Default data paths (relative to package)
DATA_DIR = Path(__file__).parent.parent / "data"
ZIP_TO_GROUP_PATH = DATA_DIR / "zip_to_group.json.gz"
SCHOOL_HOLIDAYS_PATH = DATA_DIR / "school_holidays.json.gz"

def get_school_holidays(
    start: datetime | str,
    end: datetime | str,
    zip_codes: int | str | list[int | str],
    mapping_path: Path | None = ZIP_TO_GROUP_PATH,
    canton_holidays_path: Path | None = SCHOOL_HOLIDAYS_PATH
) -> dict[str, list[dict[str, str]]]:
    """Get school holidays for one or more Swiss zip codes in a date range.

    Args:
        start (datetime | str): Start date as datetime or 'YYYY-MM-DD' string.
        end (datetime | str): End date as datetime or 'YYYY-MM-DD' string.
        zip_codes (int | str | list[int | str]): Single zip code (int or str),
                                             or a list of zip codes.
        mapping_path (Path | None): Path to mapping.json.gz. Defaults to ZIP_TO_GROUP_PATH.
        canton_holidays_path (Path | None): Path to canton_holidays.json.gz. 
                                            Defaults to SCHOOL_HOLIDAYS_PATH.

    Returns:
        dict[int | str, list[dict[str, str]]]: 
            Dictionary mapping zip codes to a list of holidays, 
            where each holiday is a dict with keys 'type', 'start', 'end' (all str).
    """
    mapping = load_json_gz(mapping_path)
    canton_holidays = load_json_gz(canton_holidays_path)

    if isinstance(zip_codes, (int, str)):
        zip_codes = [str(zip_codes)]
    else:
        zip_codes = [str(z) for z in zip_codes]

    # Convert start and end to date if needed
    if isinstance(start, str):
        sel_start = datetime.fromisoformat(start).date()
    elif isinstance(start, datetime):
        sel_start = start.date()
    elif isinstance(start, date):
        sel_start = start
    else:
        raise TypeError("start must be a str, datetime, or date")

    if isinstance(end, str):
        sel_end = datetime.fromisoformat(end).date()
    elif isinstance(end, datetime):
        sel_end = end.date()
    elif isinstance(end, date):
        sel_end = end
    else:
        raise TypeError("end must be a str, datetime, or date")
    

    latest_holiday_date = None
    for canton_data in canton_holidays.values():
        for h in canton_data.get("holidays", []):
            if h.get("end"):
                hol_end = datetime.fromisoformat(h["end"]).date()
                if latest_holiday_date is None or hol_end > latest_holiday_date:
                    latest_holiday_date = hol_end

    if latest_holiday_date:
        if sel_start > latest_holiday_date or sel_end > latest_holiday_date:
            warnings.warn(
                f"Selected start ({sel_start}) or end ({sel_end}) is after the \
                 latest holiday in data ({latest_holiday_date}).",
                stacklevel=2
            )

    out = {}
    for zip_code in zip_codes:
        canton = mapping.get(zip_code)
        out[zip_code] = []
        if not canton or canton not in canton_holidays:
            continue
        holidays = canton_holidays[canton].get("holidays", [])
        for h in holidays:
            if not (h.get("start") and h.get("end")):
                continue
            hol_start = datetime.fromisoformat(h["start"]).date()
            hol_end = datetime.fromisoformat(h["end"]).date()
            overlap = overlap_period(sel_start, sel_end, hol_start, hol_end)
            if overlap:
                out[zip_code].append({
                    "type": h["type"],
                    "start": overlap[0].isoformat(),
                    "end": overlap[1].isoformat(),
                })
    return out