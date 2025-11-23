from __future__ import annotations
from typing import Any, Callable, Dict, Tuple, Type

# (from_type, to_type) → function
ADAPTERS: Dict[Tuple[Any, Any], Callable] = {}


def register_adapter(from_type: Any, to_type: Any):
    """
    Декоратор: регистрирует адаптер (преобразователь) в глобальном реестре.

    Пример:
        @register_adapter(dict, "json")
        def dict_to_json(data):
            return json.dumps(data)
    """
    def decorator(func: Callable):
        ADAPTERS[(from_type, to_type)] = func
        return func
    return decorator


def find_adapter(from_type: Any, to_type: Any):
    """
    Поиск адаптера по типам.

    Например:
        from dict → to BaseModel
        from list → to pandas
        from Pydantic → to dict
    """
    # прямое совпадение
    if (from_type, to_type) in ADAPTERS:
        return ADAPTERS[(from_type, to_type)]

    # поиск по предкам классов: issubclass(from_type, registered_from)
    for (registered_from, registered_to), fn in ADAPTERS.items():
        if registered_to == to_type:
            try:
                if isinstance(from_type, type) and isinstance(registered_from, type):
                    if issubclass(from_type, registered_from):
                        return fn
            except TypeError:
                pass

    return None
