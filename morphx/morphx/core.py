from typing import Any
from pydantic import BaseModel
import pandas as pd

from .types import MorphTarget
from .adapters import find_adapter


def morph(data: Any, *, to: MorphTarget = None, from_: str | None = None) -> Any:
    """
    Универсальный преобразователь данных.
    morph(data, to=dict)
    morph(data, to=MyModel)
    morph(data, to="pandas")

    В версии 2.0 добавлены:
        - from_="csv"/"json"
        - система адаптеров
    """
    # Если нет преобразования — вернуть как есть
    if to is None:
        return data

    target = to
    if isinstance(target, str):
        target = target.lower().strip()

    # ==========================
    # from_ обработка (csv/json)
    # ==========================
    if from_:
        source_type = from_.lower().strip()

        if source_type == "json":
            import json
            data = json.loads(data)

        elif source_type == "csv":
            import csv
            rows = []
            reader = csv.DictReader(data.splitlines())
            for row in reader:
                rows.append(dict(row))
            data = rows

    # ========================================
    # Адаптеры кастомные (главный механизм v2)
    # ========================================
    # попытка адаптера: data_class → target
    adapter = find_adapter(type(data), target)
    if adapter:
        return adapter(data)

    # ==============
    # Pydantic
    # ==============
    if isinstance(target, type) and issubclass(target, BaseModel):
        if isinstance(data, list):
            return [target.model_validate(item) for item in data]
        return target.model_validate(data)

    # ==============
    # pandas DataFrame
    # ==============
    if target in ("pandas", "df", "dataframe"):
        if isinstance(data, pd.DataFrame):
            return data
        if isinstance(data, list) and data and isinstance(data[0], BaseModel):
            return pd.DataFrame([item.model_dump() for item in data])
        return pd.DataFrame(data)

    # ==============
    # dict/json
    # ==============
    if target in (dict, "dict", "json"):
        if isinstance(data, BaseModel):
            return data.model_dump()
        if isinstance(data, list) and data and isinstance(data[0], BaseModel):
            return [item.model_dump() for item in data]
        if isinstance(data, pd.DataFrame):
            return data.to_dict("records")
        if isinstance(data, (dict, list)):
            return data
        return {"data": data}

    raise ValueError(f"Не поддерживается to={to}")
