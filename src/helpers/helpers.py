"""Helper functions for common application tasks.

This module provides utility functions that are used across different parts
of the application. Current utilities include:
- Query string normalization for database filtering
- Wildcard character conversion for SQL LIKE queries
"""

import re


def filter_normalize(query: str) -> str:
    """Normalize filter query strings for database operations.

    Converts user-friendly wildcard patterns to SQL-compatible patterns by
    replacing asterisk (*) with percent sign (%) in __like filter parameters.

    Args:
        query (str): Original query string containing filter parameters

    Returns:
        str: Normalized query string with converted wildcards

    Example:
        >>> filter_normalize("name__like=John*Doe")
        'name__like=John%Doe'
        >>> filter_normalize("age=25&name__like=*Smith*")
        'age=25&name__like=%Smith%'
    """
    return re.sub(
        r"(__like=)([^&]*)", lambda m: m.group(1) + m.group(2).replace("*", "%"), query
    )
