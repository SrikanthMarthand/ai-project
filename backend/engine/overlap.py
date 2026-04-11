from typing import Any, Dict, List


def _get_value(source: Any, key: str):
    if isinstance(source, dict):
        return source.get(key)
    return getattr(source, key, None)


def _ranges_overlap(start_a: int, end_a: int, start_b: int, end_b: int) -> bool:
    return start_a <= end_b and start_b <= end_a


def _overlap_range(start_a: int, end_a: int, start_b: int, end_b: int) -> str:
    low = max(start_a, start_b)
    high = min(end_a, end_b)
    return f"{low}-{high}" if low <= high else "none"


def detect_overlaps(activities: List[Dict]) -> List[Dict]:
    overlaps = []
    by_file: Dict[str, List[Any]] = {}
    for entry in activities:
        key = _get_value(entry, "file_name")
        if key is None:
            continue
        by_file.setdefault(key, []).append(entry)

    for file_name, file_activities in by_file.items():
        for i in range(len(file_activities)):
            for j in range(i + 1, len(file_activities)):
                a = file_activities[i]
                b = file_activities[j]
                same_file = _get_value(a, "file_name") == _get_value(b, "file_name")
                lines_overlap = _ranges_overlap(
                    _get_value(a, "start_line"),
                    _get_value(a, "end_line"),
                    _get_value(b, "start_line"),
                    _get_value(b, "end_line"),
                )
                if same_file and lines_overlap:
                    overlaps.append({
                        "developer_ids": [_get_value(a, "developer_id"), _get_value(b, "developer_id")],
                        "file_name": file_name,
                        "overlap_type": "line-level",
                        "overlap_range": _overlap_range(
                            _get_value(a, "start_line"),
                            _get_value(a, "end_line"),
                            _get_value(b, "start_line"),
                            _get_value(b, "end_line"),
                        ),
                        "severity": "HIGH",
                        "reason_tags": ["overlapping_lines", "shared_file"],
                    })
                elif same_file:
                    overlaps.append({
                        "developer_ids": [_get_value(a, "developer_id"), _get_value(b, "developer_id")],
                        "file_name": file_name,
                        "overlap_type": "file-level",
                        "overlap_range": "file",
                        "severity": "MEDIUM",
                        "reason_tags": ["same_file"],
                    })
    return overlaps
