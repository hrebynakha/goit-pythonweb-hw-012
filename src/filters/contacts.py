"""Contact filtering configuration module.

This module defines the filtering rules for contact queries using fastapi-sa-orm-filter.
It specifies which operators are allowed for each contact field, enabling flexible
query filtering in the API.

Available filters:
Text fields (first_name, last_name, email, phone):
    - eq: Exact match
    - in_: Match any in list
    - like: SQL LIKE pattern matching
    - startswith: Prefix matching
    - contains: Substring matching

Date/Time fields (updated_at, created_at, birthday):
    - between: Range query
    - eq: Exact match
    - gt: Greater than
    - lt: Less than
    - in_: Match any in list
"""

from fastapi_sa_orm_filter.operators import Operators as ops


contact_filter = {
    # Text field filters
    "first_name": [ops.eq, ops.in_, ops.like, ops.startswith, ops.contains],
    "last_name": [ops.eq, ops.in_, ops.like, ops.startswith, ops.contains],
    "email": [ops.eq, ops.in_, ops.like, ops.startswith, ops.contains],
    "phone": [ops.eq, ops.in_, ops.like, ops.startswith, ops.contains],
    
    # Date/Time field filters
    "updated_at": [ops.between, ops.eq, ops.gt, ops.lt, ops.in_],
    "created_at": [ops.between, ops.eq, ops.gt, ops.lt, ops.in_],
    "birthday": [ops.between, ops.eq, ops.gt, ops.lt, ops.in_],
}
