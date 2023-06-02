# 1. Import des bibliothèques
import streamlit as st
import plotly.express as px
import pandas as pd


# définition de la fonction de chargement de données
@st.cache_data
def load_data():
    df = pd.read_csv('train.csv').dropna()
    return df
 
# 2. Configuration de la page
st.set_page_config(
    page_title="Dashboard des prêts",
    page_icon="💸",
    layout="wide"
)


# 3. Chargement du jeu de données dans le cache du navigateur
df = load_data()


# Ajout d'un titre
st.title("Dashboard intéractif pour les prêts")

# Ajout d'un subheader
st.subheader("Affichage des données")

# 4. Affichez les données brutes à l'aide d'une checkbox
if st.checkbox("Découvrir les données brutes")==True:
    st.write(df)


# 5. Affichez le l'histogramme des âges avec un titre et un commentaire
st.subheader("Affichage des graphiques")
fig = px.histogram(df.sort_values("age"), x="age",title="Histogramme de l'âges des personnes demandant un prêt")
st.plotly_chart(fig)


# 6. Affichez le diagramme circulaire de la variable job avec un titre et un commentaire
fig = px.pie(df.sort_values("job"), names=df["job"],title="Diagramme circulaire des métiers des personnes demandant un prêt")
fig



# 7. Créez deux colonnes 
st.subheader("Affichage dynamique des données")
col1, col2 = st.columns(2)


# 8. Dans la première colonne, affichez le diagramme en barre de la variable 'y' (accord du crédit) en fonction :
# - De la variable 'marital' (liste déroulant)
# - De la variable 'education' (liste déroulant)
# - De la variale 'age' (slider -> age minimum et age maximum paramétrables)
with col1:
    marital = st.selectbox("Sélectionnez l'état matrimonial",["Single","Married","Divorced"])
    education = st.selectbox("Sélectionnez le niveau d'éducation",["Tertiary","Secondary","Primary","Unknown"])
    agemin = st.selectbox("Sélectionnez l'âge minimum", range(18, 95, 5))
    agemax = st.selectbox("Sélectionnez l'âge maximum", range(agemin, 100, 5))
    data = df[df['marital'] == marital.lower()][df["education"] == education.lower()][df["age"]>=agemin][df["age"]<=agemax]
    fig = px.bar(data, x="y",title="Accord du crédit",labels={"Yes":["crédit accordé","crédit non accordé"]})
    st.plotly_chart(fig,use_container_width=True)


# 9. Dans la seconde colonne, créer un formulaire qui affiche la moyenne d'age des utilisateur en fonction :
# - de la variable 'housing'
# - de la variable 'loan' 
with col2:
    with st.form("moyenne d'age des demandeurs"):
        housing = st.selectbox("Sélectionnez si la personne possède un logement ou non",["Yes","No"])
        loan = st.selectbox("Sélectionnez si la personne a déjà un prêt", ["Yes","No"])
        submit = st.form_submit_button(label="Soumettre")
        
        if submit:
            data_ = df[df["housing"] == housing.lower()][df["loan"]==loan.lower()]
            st.metric(label="moyenne d'age des utilisateur en fonction d'housing et loan",value=data_['age'].mean())

#10. Créez une colonne latérale (sidebar) avec un Sommaire qui renvoie au trois parties suivantes :
# - Affichage des données
# - Affichage des graphiques
# - Affichage dynamique des données
st.sidebar.header("Sommaire")
st.sidebar.markdown("""
    * [Affichage des données](#affichage-des-donn-es)
    * [Affichage des graphiques](#affichage-des-graphiques)
    * [Affichage dynamique des données](#affichage-dynamique-des-donn-es)
""")

# 11. Bonus : 
# - Publiez Créez un conteneur Docker de votre application
# - Déployez votre conteneur sur Docker Hub, noter le nom du conteneur ici : 280720/tp-deploiement:latest
# - Déployer votre application sur Heroku.