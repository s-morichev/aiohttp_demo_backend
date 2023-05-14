from typing import Any, Callable, Sequence

import orjson
from pydantic import BaseModel


def orjson_dumps(
    dump_value: Any, *, default: Callable[[Any], Any] | None
) -> str:
    return orjson.dumps(dump_value, default=default).decode()


class BaseSchema(BaseModel):
    class Config(object):
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        allow_population_by_field_name = True
        orm_mode = True


def dump_schemas_sequence(
    models: Sequence[BaseSchema],
    default: Callable[[Any], Any] = BaseSchema.__json_encoder__,
) -> bytes:
    return orjson.dumps(models, default=default)


def dump_schema(
    model: BaseSchema,
    default: Callable[[Any], Any] = BaseSchema.__json_encoder__,
) -> bytes:
    return orjson.dumps(model, default=default)
