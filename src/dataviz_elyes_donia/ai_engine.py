import anthropic
import streamlit as st
import logging
import base64
import pandas as pd
import matplotlib.pyplot as plt  # ✅ Import manquant
import seaborn as sns            # ✅ Import manquant
import plotly.express as px      # ✅ Import manquant
import numpy as np               # ✅ Import manquant

# ✅ Configuration des logs
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# ✅ Initialisation du client Anthropic
def initialize_ai_client(api_key):
    return anthropic.Anthropic(api_key=api_key)

# ✅ Fonction générique pour envoyer des requêtes à Claude
def send_request_to_claude(client, prompt, max_tokens=2000):
    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except Exception as e:
        logger.error(f"❌ Erreur lors de la requête Claude : {e}")
        st.error(f"Erreur lors de la requête Claude : {str(e)}")
        return None

# ✅ Générer des recommandations IA
def generate_recommendations(df, api_key):
    client = initialize_ai_client(api_key)
    dataset_summary = f"""
    **Aperçu du Jeu de Données :**
    - Colonnes : {', '.join(df.columns)}
    - Statistiques descriptives :
    {df.describe(include='all').to_string()}
    """

    prompt = f"""
    Tu es un expert en analyse de données. À partir des informations suivantes :

    {dataset_summary}

    1. Identifie les principales tendances et anomalies dans les données.
    2. Suggère des actions basées sur ces insights pour améliorer les performances.
    3. Mets en évidence toute relation inattendue entre les variables.

    Génère un rapport concis sous forme de points clés.
    """
    return send_request_to_claude(client, prompt)

# ✅ Détecter des anomalies dans les données
def detect_anomalies(df, api_key):
    client = initialize_ai_client(api_key)
    dataset_summary = f"""
    **Aperçu des Données :**
    - Colonnes : {', '.join(df.columns)}
    - Statistiques descriptives :
    {df.describe(include='all').to_string()}
    """

    prompt = f"""
    Tu es un spécialiste en détection d'anomalies. Sur la base des données suivantes :

    {dataset_summary}

    Identifie les anomalies potentielles, en expliquant pourquoi elles pourraient être considérées comme telles.
    Donne des suggestions sur la manière de gérer ces anomalies.
    """
    return send_request_to_claude(client, prompt)

# ✅ Générer des visualisations personnalisées sans texte explicatif
def call_llm_for_viz(df, user_prompt, api_key):
    client = initialize_ai_client(api_key)
    dataset_summary = f"""
    Colonnes et types :
    {df.dtypes.to_string()}

    Description du jeu de données :
    {df.describe(include='all').to_string()}
    """

    prompt = f"""
    Tu es un expert en visualisation de données avec Python.
    En utilisant le DataFrame suivant nommé `df` :

    {dataset_summary}

    Crée un code Python pour générer la visualisation suivante :
    {user_prompt}

    **Contraintes importantes :**
    - Donne uniquement le code Python sans aucune explication.
    - Le code doit être entouré par des balises ```python et ``` pour faciliter l'extraction.
    - Utilise uniquement `matplotlib`, `seaborn` ou `plotly`.
    - Remplace `plt.show()` par `st.pyplot(plt)` pour Streamlit.
    """
    return send_request_to_claude(client, prompt, max_tokens=1500)

# ✅ Exécuter dynamiquement du code Python généré par l'IA
def exec_generated_code(code: str, df: pd.DataFrame):
    try:
        # ✅ Importation des modules nécessaires pour l'exécution du code généré
        exec_globals = {
            "st": st,
            "pd": pd,
            "plt": plt,   # ✅ Importation correcte de matplotlib.pyplot
            "sns": sns,
            "px": px,
            "np": np,     # ✅ Ajout de numpy pour les calculs mathématiques
            "df": df
        }
        
        # ✅ Compilation du code pour vérifier les erreurs de syntaxe
        compiled_code = compile(code, "<string>", "exec")
        
        # ✅ Exécution du code compilé
        exec(compiled_code, exec_globals)
        
    except SyntaxError as syntax_err:
        error_message = (f"Erreur de syntaxe détectée : "
                         f"Ligne {syntax_err.lineno}, "
                         f"Colonne {syntax_err.offset} -> {syntax_err.text.strip()}")
        logger.error(f"❌ {error_message}")
        st.error(error_message)
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'exécution du code généré : {e}")
        st.error(f"Erreur lors de l'exécution du code généré : {e}")
