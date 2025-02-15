import os
import sys

# Ajout du chemin vers src pour que Sphinx trouve les modules Python
sys.path.insert(0, os.path.abspath('../../src'))

project = 'Datavizelyes'
author = 'Elyes Maalel'
release = '1.0'

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx_rtd_theme"
]

autosummary_generate = True  # Génère automatiquement les sommaires
html_theme = 'sphinx_rtd_theme'
