from sqlalchemy import Table, Column, ForeignKey, DateTime, String, Integer, MetaData
from sqlalchemy.sql import func
from config.db import engine, meta

meta = MetaData()

users = Table(
    'user', meta,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('email', String(255), unique=True, index=True, nullable=False),
    Column('password', String(255), nullable=False),
)

friend_requests = Table(
    'friend_requests', meta,
    Column('id', Integer, primary_key=True),
    Column('from_user_id', Integer, ForeignKey('user.id')),
    Column('to_user_id', Integer, ForeignKey('user.id')),
    Column('status', String(10), default='pending'),
    Column('created_at', DateTime, server_default=func.now())
)

meta.create_all(engine)
