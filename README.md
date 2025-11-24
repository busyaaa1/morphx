<div align="center">
  <img src="logo.png" width="400"/>
  <h1>morphx</h1>
  <p>Одна строчка — любой формат данных</p>
</div>


```markdown
# morphx

**Одна строчка — любой формат данных**

```python
from morphx import morph

df     = morph(data, to="pandas")     # → pandas.DataFrame
users  = morph(data, to=User)         # → list[User]
json   = morph(users, to="json")      # → str
```

## Установка

```bash
pip install morphx
```

## Как это работает

```python
from morphx import morph
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

# Любые данные из API, JSON, базы
data = [{"name": "Аня", "age": 17}, {"name": "Дима", "age": 19}]

# → в таблицу
df = morph(data, to="pandas")

# → в нормальные объекты
users = morph(data, to=User)

# → обратно в словарь или JSON
result = morph(users, to=dict)
json_string = morph(users, to="json")

# → CSV строка
csv_string = morph(users, to="csv")
```

## Поддерживается

| Из чего       | Во что              | Как писать                  |
|---------------|---------------------|-----------------------------|
| `dict`        | Pydantic модель     | `to=User`                   |
| `list[dict]`  | DataFrame           | `to="pandas"`               |
| Pydantic      | dict / JSON         | `to=dict` или `to="json"`   |
| Pydantic      | CSV строка          | `to="csv"`                  |
| JSON строка   | Pydantic            | через адаптер               |

## Лицензия
MIT License

## Автор
[@busyaaa_1](https://github.com/busyaaa-1)


**Понравилось? Поставь звёздочку — это лучшая благодарность**
