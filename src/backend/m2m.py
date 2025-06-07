from sqlalchemy import Column, ForeignKey, Integer, Table
from src.common.model import MappedBase

user_cards = Table(
    'user_cards', 
    MappedBase.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('card_id', Integer, ForeignKey('card.id'), primary_key=True)
)