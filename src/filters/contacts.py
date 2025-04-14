"""Contact filter"""

from fastapi_sa_orm_filter.operators import Operators as ops


contact_filter = {
    "first_name": [ops.eq, ops.in_, ops.like, ops.startswith, ops.contains],
    "last_name": [ops.eq, ops.in_, ops.like, ops.startswith, ops.contains],
    "email": [ops.eq, ops.in_, ops.like, ops.startswith, ops.contains],
    "phone": [ops.eq, ops.in_, ops.like, ops.startswith, ops.contains],
    "updated_at": [ops.between, ops.eq, ops.gt, ops.lt, ops.in_],
    "created_at": [ops.between, ops.eq, ops.gt, ops.lt, ops.in_],
    "birthday": [ops.between, ops.eq, ops.gt, ops.lt, ops.in_],
}
