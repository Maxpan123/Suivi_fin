# main.py
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Enum, Table, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import date
# ----- Configuration de la base -----
DATABASE_URL = "postgresql://DB_SUIFIN_owner:npg_tFPhX8frz0vi@ep-dawn-glade-ab96c3r5-pooler.eu-west-2.aws.neon.tech/DB_SUIFIN?sslmode=require"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

# ----- Définition des tables -----
class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, default=date.today)
    isin = Column(String, nullable=False)
    libelle = Column(String)
    type = Column(Enum('achat', 'vente', name='transaction_type'), nullable=False)
    quantite = Column(Float, nullable=False)
    prix_unitaire = Column(Float, nullable=False)
    frais = Column(Float, default=0.0)
    devise = Column(String, default='EUR')

class Valorisation(Base):
  __tablename__ = 'valorisation'
  date = Column(Date, primary_key=True)
  isin = Column(String, primary_key=True)
  prix_unitaire = Column(Float, nullable=False)

print("Base de données créée avec succès !")
  
