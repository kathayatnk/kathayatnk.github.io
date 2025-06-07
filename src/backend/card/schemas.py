

from src.common.schema import SchemaBase
    

class CardAddRequest(SchemaBase):
    name: str
    bank_id: int
    description: str
    annual_fee: int
    reward_desc: str
    interest_rate: int
    min_credit_score: int 

class CardGetResponse(SchemaBase):
    id: int
    name: str
    bank_id: int
    description: str
    annual_fee: int
    reward_desc: str
    interest_rate: int
    min_credit_score: int 

class BankRelation(SchemaBase):
    id: int
    name: str
    logo_url:str 
    website: str 

class CardGetRelationResponse(SchemaBase):
    id: int
    name: str
    bank_id: int
    description: str
    annual_fee: int
    reward_desc: str
    interest_rate: int
    min_credit_score: int 
    bank: BankRelation

