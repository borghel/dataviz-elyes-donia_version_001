import streamlit as st
import pandas as pd
import logging
import matplotlib.pyplot as plt
import re  # ✅ Ajout de l'importation pour l'extraction du code

# Importation des modules développés
from kpi_dashboard import display_kpi_dashboard

# Chargement de la clé API depuis le fichier .env
from dotenv import load_dotenv
import os
load_dotenv()
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise ValueError("Clé API manquante. Veuillez la définir dans le fichier .env")

# Configuration du journal de logs
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def main():
    st.set_page_config(page_title="📊 DataViz Project", layout="wide")
    st.sidebar.title("🚀 Menu de Navigation")

    pages = {
        "🏠 Accueil": "home",
        "📈 Tableau de Bord des KPI": "kpi_dashboard"
    }

    selected_page = st.sidebar.radio("Choisissez une page :", list(pages.keys()))

    if selected_page == "🏠 Accueil":
        st.title("📊 DataViz Project Elyes-Donia")
        st.markdown("""
            **Cette application vous permet de :**
            - Suivre vos **KPI en temps réel**.
            - Explorer les **relations cachées** entre les variables.
        """)

    elif selected_page == "📈 Tableau de Bord des KPI":
        uploaded_file = st.file_uploader("📂 Téléchargez votre fichier de données (CSV, Excel) :", type=["csv", "xlsx"])
        if uploaded_file:
            display_kpi_dashboard(uploaded_file)

if __name__ == "__main__":
    main()
