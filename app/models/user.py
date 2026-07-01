from sqlalchemy import Column, Integer, String, Boolean,Table, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

# Association Table
user_role = Table(
    'user_role',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True)
)

# Role Table
class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

# User Table
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    phone_number = Column(String)
    is_verified = Column(Boolean, default=False)
    otp = Column(String, nullable=True)

    # linking user to role
    roles = relationship("Role", secondary=user_role)