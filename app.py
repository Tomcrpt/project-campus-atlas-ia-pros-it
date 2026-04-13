import plotly.express as px
import pandas as pd

données = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSC4KusfFzvOsr8WJRgozzsCxrELW4G4PopUkiDbvrrV2lg0S19-zeryp02MC9WYSVBuzGCUtn8ucZW/pub?output=csv')

#figure = px.pie(données, values='qte', names='region', title='quantité vendue par région')

#figure.write_html('ventes-par-region.html')

#print('ventes-par-région.html généré avec succès !')

# 5. Chiffre d'affaire
données["ca"] = données["prix"] * données["qte"]

# 5.a Chiffre d'affaire et volume de vente par produit
grouped = données.groupby("produit").agg({
    "ca": ["mean", "median"],
    "qte": ["mean", "median"]
})

print(grouped)

# 5.b Ecart-type et variance pour le volume de vente par produit
stats_qte = données.groupby("produit")["qte"].agg(["std", "var"])

print(stats_qte)

# 6. Produit le plus vendu et le moins vendu en nombre d'unités vendues
totaux = {} # création d'un dictionnaire de données. Structure adaptée pour la recherche de min / max

for ligne in données.to_dict("records"):
    produit = ligne["produit"]
    qte = ligne["qte"]
    
    if produit not in totaux:
        totaux[produit] = 0
    
    totaux[produit] += qte # mise à jour du cumul

# Trouver max et min
produit_max = max(totaux, key=totaux.get) # détermination du maximum
produit_min = min(totaux, key=totaux.get) # détermination du minimum

print("Produit le plus vendu ", produit_max, totaux[produit_max])
print("Produit le moins vendu ", produit_min, totaux[produit_min])

# 7.a Graphique des ventes par produit 
ventes = données.groupby("produit")["qte"].sum().reset_index()

fig1 = px.pie(ventes, values='qte', names='produit', title='Ventes par produit')
fig1.write_html("ventes-par-produit.html")

# 7.b Graphique du chiffre d'affaire par produit
ca = données.groupby("produit")["ca"].sum().reset_index()

fig2 = px.pie(ca, values='ca', names='produit', title='Chiffre d affaires par produit')
fig2.write_html("ca-par-produit.html")