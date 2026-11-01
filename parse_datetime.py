import time

def parse_datetime(s: str) -> int:
    """Convert a timestamp like `2026-10-30T10:05:00+0100` to unix."""

    parts = (
        int(s[0:4]), int(s[5:7]), int(s[8:10]),
        int(s[11:13]), int(s[14:16]), int(s[17:19]),
        0, 0
    )

    offset = (
        (1 if s[19] == "+" else -1)
        * (int(s[20:22]) * 60 + int(s[22:24]))
        * 60
    )

    return int(time.mktime(parts) - offset)


if __name__ == "__main__":
    timestamp = parse_datetime("2026-10-30T10:05:00+0100")
    print(timestamp)  
