
from src.common.schema import SchemaBase


class BankAddRequest(SchemaBase):
    name: str
    logo_url:str 
    website: str 

class BankGetResponse(SchemaBase):
    id: int
    name: str
    logo_url:str 
    website: str 

class CardRelation(SchemaBase):
    id: int
    name: str
    bank_id: int
    description: str
    annual_fee: int
    reward_desc: str
    interest_rate: int
    min_credit_score: int 

class BankGetRelationResponse(SchemaBase):
    id: int
    name: str
    logo_url:str 
    website: str 
    cards: list[CardRelation]
    