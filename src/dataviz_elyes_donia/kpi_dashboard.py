import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from dataviz_elyes_donia.data_pipeline import load_data, normalize_data, transform_variables
from dataviz_elyes_donia.utils import display_dataframe_overview

def display_kpi_dashboard(file):
    st.title("📈 Tableau de Bord des KPI en Temps Réel")

    # Chargement et préparation des données
    df = load_data(file)
    if df is None:
        return

    # Affichage de l'aperçu des données
    display_dataframe_overview(df)

    # Normalisation et transformation des variables
    df_normalized = normalize_data(df)
    df_transformed = transform_variables(df_normalized)

    st.sidebar.header("⚙️ Paramètres des KPI")
    numeric_cols = df_transformed.select_dtypes(include=[np.number]).columns.tolist()
    selected_kpis = st.sidebar.multiselect("Sélectionnez les KPI à suivre", numeric_cols, default=numeric_cols[:2])

    st.subheader("📊 KPI en Direct")
    cols = st.columns(len(selected_kpis))

    for i, kpi in enumerate(selected_kpis):
        current_value = df_transformed[kpi].iloc[-1]
        delta = current_value - df_transformed[kpi].iloc[-2] if len(df_transformed) > 1 else 0

        cols[i].metric(label=kpi, value=f"{current_value:.2f}", delta=f"{delta:+.2%}")

    st.subheader("📈 Tendances des KPI")
    for kpi in selected_kpis:
        fig = px.line(df_transformed, y=kpi, title=f"Évolution de {kpi} dans le temps")
        st.plotly_chart(fig, use_container_width=True)

    st.success("✅ Tableau de bord des KPI mis à jour avec succès.")
