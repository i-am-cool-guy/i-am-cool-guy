import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from userbot import DATABASE_URL

engine = create_engine(DATABASE_URL)
Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
try:
  db = SessionLocal()
  print("✅ Connected to PostgreSQL successfully!")
  db.close()
except Exception as e:
  print(f"❌ Failed to connect: {e}")
