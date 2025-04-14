"""Application helpers functions"""

import re


def filter_normalize(query: str) -> str:
    """Replace all '*' with '%' in any __like parameter values."""
    return re.sub(
        r"(__like=)([^&]*)", lambda m: m.group(1) + m.group(2).replace("*", "%"), query
    )
