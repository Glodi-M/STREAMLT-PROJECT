import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Configuration de base
st.set_page_config(page_title="Dashboard Nutrition", layout="wide")
st.title("🍏 Dashboard Nutrition - Analyse des aliments")
st.markdown("Groupe de Glodi MIETETE,Destiné BEHANZIN, Arnold Boly LEGRE")

# Chargement des données
df = pd.read_csv("openfoodfacts_nettoyage copie.csv")


# Nettoyage rapide (on garde les colonnes utiles)
colonnes_utiles = ['product_name', 'pnns_groups_1','pnns_groups_2', 'energy_100g', 'fat_100g', 'fiber_100g', 'sugars_100g', 'proteins_100g']
df = df[colonnes_utiles].dropna()

# Sidebar - Filtres
st.sidebar.header("🎯 Filtres")
categories = df['pnns_groups_2'].unique()
selected_category = st.sidebar.selectbox("Catégorie", categories)

# Filtrage
df_filtered = df[df['pnns_groups_2'] == selected_category]

# 1. Aperçu des données
st.subheader(f"📋 Données filtrées - {selected_category}")
st.dataframe(df_filtered.head())

# 2. Histogramme de l’énergie
st.subheader("🔥 Distribution de l'énergie (kcal/100g)")
fig1, ax1 = plt.subplots()
sns.histplot(df_filtered["energy_100g"], kde=True, color="orange", ax=ax1)
st.pyplot(fig1)

# 3. Scatterplot Gras vs Sucres
st.subheader("🥯 Scatterplot : matières grasses vs sucres")
fig2, ax2 = plt.subplots()
sns.scatterplot(data=df_filtered, x="fat_100g", y="sugars_100g", alpha=0.6, ax=ax2)
st.pyplot(fig2)

# 4. Boxplot de chaque nutriment
st.subheader("📦 Boxplot des nutriments")
nutriments = ["energy_100g", "fat_100g", "sugars_100g", "proteins_100g"]
selected_nutriment = st.selectbox("Choisis un nutriment :", nutriments)

fig3, ax3 = plt.subplots()
sns.boxplot(data=df, x="pnns_groups_2", y=selected_nutriment, ax=ax3)
plt.xticks(rotation=90)
st.pyplot(fig3)

# 5. Heatmap de corrélation
st.subheader("🧪 Corrélation entre les nutriments")
corr = df_filtered[nutriments].corr()

fig4, ax4 = plt.subplots()
sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax4)
st.pyplot(fig4)

st.header("📂 Analyse des variables catégorielles")



# Choix d'une variable catégorielle
selected_cat_var = st.selectbox("Choisis une variable catégorielle :", ['pnns_groups_1', 'pnns_groups_2'])

# Top catégories
st.subheader(f"🔢 Répartition des produits selon : {selected_cat_var}")
top_cats = df[selected_cat_var].value_counts().head(10)
st.bar_chart(top_cats)

# Sélection multiple de catégories
selected_categories = st.multiselect(
    f"Sélectionne des catégories dans {selected_cat_var}",
    options=df[selected_cat_var].dropna().unique(),
    default=top_cats.index.tolist()
)

# Filtrage par catégories sélectionnées
df_cat_filtered = df[df[selected_cat_var].isin(selected_categories)]

# Moyenne des nutriments par catégorie sélectionnée
st.subheader("📊 Moyenne des nutriments par catégorie sélectionnée")
mean_by_cat = df_cat_filtered.groupby(selected_cat_var)[["energy_100g", "fat_100g", "sugars_100g", "proteins_100g"]].mean()
st.dataframe(mean_by_cat.style.format("{:.1f}"))

# Boxplot comparatif
st.subheader("📦 Comparaison par boxplot")
selected_nutrient = st.selectbox("Nutriment à afficher :", ['energy_100g', 'fat_100g', 'sugars_100g', 'proteins_100g'])

fig_box, ax_box = plt.subplots(figsize=(10, 5))
sns.boxplot(data=df_cat_filtered, x=selected_cat_var, y=selected_nutrient, ax=ax_box)
plt.xticks(rotation=45)
st.pyplot(fig_box)


# SYSTEME DE RECOMMANDATION

st.header("🍽️ Recommandations pour un repas équilibré")

# 1. Sélection d'un produit
product_selected = st.selectbox("🔍 Choisis un produit de base", df["product_name"].dropna().unique())

# 2. Récupération des données du produit
product_info = df[df["product_name"] == product_selected].iloc[0]

# 3. Analyse nutritionnelle simple
st.subheader("🔬 Analyse nutritionnelle du produit sélectionné")
st.write(product_info[["energy_100g", "fat_100g", "sugars_100g", "proteins_100g", "fiber_100g"]])

# 4. Recommandations personnalisées
st.subheader("🤖 Suggestions complémentaires")

recommendations = []

# Analyse simple
if product_info["proteins_100g"] < 5:
    recommendations.append("🟢 Ajoute une source de **protéines** : œufs, poisson, légumineuses, tofu.")
if product_info["sugars_100g"] > 15:
    recommendations.append("🍓 Ajoute des aliments **pauvres en sucre** : légumes, yaourt nature, noix.")
if product_info["fat_100g"] > 17:
    recommendations.append("🥗 Équilibre avec des aliments **pauvres en matières grasses** : crudités, fruits.")
if product_info["fiber_100g"] < 2.5:
    recommendations.append("🌾 Ajoute des aliments **riches en fibres** : légumes, céréales complètes, graines.")

if not recommendations:
    st.success("✅ Ce produit est déjà assez équilibré pour un repas léger.")
else:
    for rec in recommendations:
        st.markdown(rec)
