import os
import requests
from datetime import date
from main import Session, Valorisation, Transaction
from sqlalchemy import distinct

# Récupère la clé API EODHD
API_KEY = os.environ.get("EODHD_API_KEY")
session = Session()
today = date.today()

# Récupère tous les tickers distincts de la table transactions
tickers = session.query(distinct(Transaction.ticker)).all()
tickers = [t[0] for t in tickers if t[0]]  # flatten + filtre non null

for ticker in tickers:
    url = f"https://eodhd.com/api/real-time/{ticker}?api_token={API_KEY}&fmt=json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        prix = float(data["close"])

        # Vérifie si déjà présent aujourd'hui
        existing = session.query(Valorisation).filter_by(date=today, ticker=ticker).first()
        if not existing:
            # Trouver l'ISIN correspondant via la table transactions
            isin_entry = session.query(Transaction).filter_by(ticker=ticker).first()
            if isin_entry:
                session.add(Valorisation(
                    date=today,
                    isin=isin_entry.isin,
                    ticker=ticker,
                    prix_unitaire=prix
                ))
                print(f"{ticker} ➜ {prix:.2f} EUR ajouté.")
            else:
                print(f"{ticker} ➜ ISIN introuvable, ignoré.")
        else:
            print(f"{ticker} ➜ déjà valorisé aujourd'hui.")

    except Exception as e:
        print(f"{ticker} ➜ Erreur : {e}")

session.commit()
session.close()
