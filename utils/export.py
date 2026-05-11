"""Data export utilities"""

import json
import csv
import io


def to_json(data):
    """Convert data to JSON string"""
    return json.dumps(data, indent=2, ensure_ascii=False)


def to_csv(rows, fields):
    """Convert data to CSV string"""
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)
    return buf.getvalue()
