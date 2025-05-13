# Form.py
import streamlit as st
from datetime import date
from main import Session, Transaction  # On réutilise la session SQLAlchemy

st.title("Ajouter une transaction")

with st.form("ajout_transaction"):
    isin = st.text_input("ISIN")
    libelle = st.text_input("Libellé")
    type_op = st.selectbox("Type", ["achat", "vente"])
    quantite = st.number_input("Quantité", step=1.0)
    prix_unitaire = st.number_input("Prix unitaire (€)", step=0.01)
    frais = st.number_input("Frais (€)", step=0.01, value=0.0)
    date_op = st.date_input("Date", value=date.today())
    submitted = st.form_submit_button("Ajouter")

    if submitted:
        session = Session()
        nouvelle = Transaction(
            isin=isin,
            libelle=libelle,
            type=type_op,
            quantite=quantite,
            prix_unitaire=prix_unitaire,
            frais=frais,
            date=date_op
        )
        session.add(nouvelle)
        session.commit()
        st.success("Transaction ajoutée !")
