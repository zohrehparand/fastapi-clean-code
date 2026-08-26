from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from core.app.database import Base


class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(250), unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)

    costs = relationship("CostModel", back_populates="user")
