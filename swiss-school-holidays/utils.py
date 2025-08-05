import gzip
import json


def load_json_gz(path):
    with gzip.open(path, "rt", encoding="utf-8") as f:
        return json.load(f)


def overlap_period(a_start, a_end, b_start, b_end):
    # Return max(start), min(end) or None if no overlap
    start = max(a_start, b_start)
    end = min(a_end, b_end)
    if start > end:
        return None
    return start, end
