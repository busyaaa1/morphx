from typing import TypeAlias, Union, Literal, Type
from pydantic import BaseModel

MorphTarget: TypeAlias = Union[
    Type[BaseModel],
    Type[dict],
    Literal[
        "pandas",
        "df",
        "dataframe",
        "dict",
        "json",
        "csv",
        "polars",
    ],
]
