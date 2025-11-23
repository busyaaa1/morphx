import pandas as pd
from pydantic import BaseModel
from morphx import morph


class User(BaseModel):
    name: str
    age: int


def test_dict_to_df():
    data = [{"name": "A", "age": 10}]
    df = morph(data, to="pandas")
    assert isinstance(df, pd.DataFrame)
    assert df.loc[0, "name"] == "A"


def test_dict_to_model():
    data = {"name": "A", "age": 10}
    user = morph(data, to=User)
    assert user.name == "A"


def test_list_model_to_dict():
    users = [User(name="A", age=10)]
    result = morph(users, to=dict)
    assert isinstance(result, list)
    assert result[0]["name"] == "A"
