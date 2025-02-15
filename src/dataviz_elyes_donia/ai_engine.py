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

# ✅ Exécuter dynamiquement du code Python généré

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
