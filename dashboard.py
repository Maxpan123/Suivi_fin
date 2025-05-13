import os
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date
from main import Transaction, Valorisation, Base

# Connexion à la BDD
DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

st.title("📊 Dashboard PEA")

# Récupérer toutes les transactions
transactions = session.query(Transaction).all()
df_transac = pd.DataFrame([{
    "isin": t.isin,
    "ticker": t.ticker,
    "quantite": t.quantite if t.type == "achat" else -t.quantite,
    "prix_unitaire": t.prix_unitaire,
    "frais": t.frais
} for t in transactions])

# Prix moyen d'achat et quantité nette
df_grouped = df_transac.groupby(["isin", "ticker"]).agg(
    quantite_totale=("quantite", "sum"),
    cout_total=("prix_unitaire", lambda x: (x * df_transac["quantite"]).sum())
).reset_index()
df_grouped = df_grouped[df_grouped["quantite_totale"] > 0]
df_grouped["prix_moyen_achat"] = df_grouped["cout_total"] / df_grouped["quantite_totale"]

# Dernières valorisations
latest_valos = session.query(Valorisation).filter_by(date=date.today()).all()
df_valo = pd.DataFrame([{
    "isin": v.isin,
    "ticker": v.ticker,
    "valeur_actuelle": v.prix_unitaire
} for v in latest_valos])

# Fusion
df_merge = pd.merge(df_grouped, df_valo, on=["isin", "ticker"], how="left")
df_merge["plus_value"] = (df_merge["valeur_actuelle"] - df_merge["prix_moyen_achat"]) * df_merge["quantite_totale"]
df_merge["performance (%)"] = ((df_merge["valeur_actuelle"] / df_merge["prix_moyen_achat"]) - 1) * 100

st.subheader("🧾 Synthèse des positions")
st.dataframe(df_merge[[
    "isin", "ticker", "quantite_totale", "prix_moyen_achat", "valeur_actuelle", "plus_value", "performance (%)"
]])

session.close()
