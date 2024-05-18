from datetime import datetime

import requests
from pydantic import BaseModel, Field, NonNegativeInt, field_validator, model_validator
from pandas import DataFrame


API_ENDPOINT = 'https://api.gazprombank.ru/very/important/docs'
MOCK_RESPONSE = '''
{
"Columns": ["key1", "key2", "key3"],
"Description": "Банковское API каких-то важных документов",
"RowCount": 2,
"Rows": [
[2, "2024-05-18T14:50:55.943531", "value3"],
[3, "2024-05-18T14:50:55.943531", "value6"]
]
}
'''
RENAME_MAP = {
    'key1': 'document_id',
    'key2': 'document_dt',
    'key3': 'document_name'
}

def request_api(document_date: datetime, mock: bool = False) -> str | bytes:
    if mock:
        return MOCK_RESPONSE
    response = requests.get(
        API_ENDPOINT, params={
            'document_date': document_date.timestamp()
        }
    )
    if response.status_code >= 400:
        raise Exception(f'Error {response.status_code} on request. Content: {response.content}')
    return response.content

class APIRespoonse(BaseModel):
    colums: list[str] = Field(validation_alias='Columns')
    description: str = Field(validation_alias='Description')
    row_count: NonNegativeInt = Field(validation_alias='RowCount')
    rows: list[list[datetime | int | str]] = Field(validation_alias='Rows')

    @field_validator('colums')
    @classmethod
    def validate_colums(cls, value: list[str]):
        fields = ['key1', 'key2', 'key3']
        if len(value) != 3 or any([el not in value for el in fields]):
            raise ValueError('Unrecognizale column names')
        return value
    
    @model_validator(mode='after')
    def validate_rows(self) -> 'APIRespoonse':
        if self.row_count != len(self.rows):
            raise ValueError('Rows amount differs from expected amount')
        for row in self.rows:
            if len(row) != len(self.colums):
                raise ValueError('Rows length differs from expected')
            if type(row[0]) is not int:
                raise ValueError('Col 0 must be int type')
            if type(row[1]) is not datetime:
                raise ValueError('Col 1 must be datetime type')
            if type(row[2]) is not str:
                raise ValueError('Col 2 must be str type')
        return self

if __name__ == '__main__':
    document_date = datetime.now()
    response = request_api(document_date, mock=True)
    res = APIRespoonse.model_validate_json(response)
    data = DataFrame(res.rows, columns=res.colums)
    data.rename(columns=RENAME_MAP, inplace=True)
    data.insert(len(data.columns), 'load_dt', [document_date] * len(data))
    print(data)
