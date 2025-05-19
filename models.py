from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.now)

class File(Base):
    __tablename__ = "files"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    file_path = Column(String)
    file_type = Column(String)
    file_size = Column(BigInteger)  # Using BigInteger for large file sizes
    upload_date = Column(DateTime, default=datetime.now)
    file_hash = Column(String, unique=True, index=True)  # For deduplication
    description = Column(String, nullable=True)
    tags = Column(String, nullable=True)  # Store as JSON string
    is_favorite = Column(Integer, default=0)  # 0 or 1
    download_count = Column(Integer, default=0)
    last_accessed = Column(DateTime, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Make nullable for now
    is_public = Column(Integer, default=1)  # 1 for public, 0 for private 