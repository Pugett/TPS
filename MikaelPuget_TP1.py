import sys
import json
import os
from PySide6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QMainWindow, QListWidget, QPushButton, QVBoxLayout, QWidget, QLineEdit, QHBoxLayout, QLabel
from PySide6.QtCore import Qt

json_file = sys.argv[1]
print(json_file)

try:
    file = open(json_file)
    data = json.load(file)
    print(data)
except FileNotFoundError:
    print(f"Le Fichier: {json_file} n'existe pas.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Erreur : '{json_file}' n'est pas un JSON valide.")
    sys.exit(1)

# INFOS SUR LE FICHIER JSON
nom_fichier = os.path.basename(json_file)
taille_fichier = os.path.getsize(json_file)  # en octets
nombre_elements = len(data)

# CONVERSION DE LA TAILLE EN UNITE LISIBLE
def formater_taille(octets):
    for unite in ["o", "Ko", "Mo", "Go"]:
        if octets < 1024:
            return f"{octets:.1f} {unite}"
        octets /= 1024
    return f"{octets:.1f} To"

# OUVERTURE DE L'APPLICATION
app = QApplication([])

# CREATION DU LABEL D'INFOS SUR LE FICHIER
label_infos = QLabel(f"Fichier : {nom_fichier}  |  Taille : {formater_taille(taille_fichier)}  |  Éléments : {nombre_elements}")

# CREATION DU TABLEAU UI
tableau = QTableWidget()
tableau.setRowCount(len(data))
#tableau.setColumnCount(6)

# CREATION DE LA BARRE DE RECHERCHE
#
#
#
recherche = QLineEdit()
recherche.setPlaceholderText("Rechercher...")

def filtrer():
    texte = recherche.text().lower()
    for row in range(tableau.rowCount()):
        correspond = False
        for col in range(tableau.columnCount()):
            item = tableau.item(row, col)
            if item and texte in item.text().lower():
                correspond = True
                break
        tableau.setRowHidden(row, not correspond)

recherche.textChanged.connect(filtrer)

# CREATION DU CROISSANT DESCROISSANT
bouton_croissant = QPushButton("Tri croissant")
bouton_decroissant = QPushButton("Tri décroissant")

def trier_croissant():
    tableau.sortItems(0, Qt.AscendingOrder)

def trier_decroissant():
    tableau.sortItems(0, Qt.DescendingOrder)

bouton_croissant.clicked.connect(trier_croissant)
bouton_decroissant.clicked.connect(trier_decroissant)
# RECHERCHER DES NOMS DE COLONNES 
#for i in range(len(data)):
    #tableau.setHorizontalHeaderLabels(
        #[list(data[i].keys())[0], 
        #list(data[i].keys())[1], 
        #list(data[i].keys())[2], 
        #list(data[i].keys())[3], 
        #list(data[i].keys())[4], 
        #list(data[i].keys())[5]])

colonnes = list(data[0].keys())
tableau.setColumnCount(len(colonnes))
tableau.setHorizontalHeaderLabels(colonnes)

# POUR CHAQUE COLONNE, AJOUTER LES VALEURS DANS LE TABLEAU
#for i in range(len(data)):
    #tableau.setItem(i, 0, QTableWidgetItem(str(data[i][list(data[i].keys())[0]])))
    #tableau.setItem(i, 1, QTableWidgetItem(str(data[i][list(data[i].keys())[1]])))
    #tableau.setItem(i, 2, QTableWidgetItem(str(data[i][list(data[i].keys())[2]])))
    #tableau.setItem(i, 3, QTableWidgetItem(str(data[i][list(data[i].keys())[3]])))
    #tableau.setItem(i, 4, QTableWidgetItem(str(data[i][list(data[i].keys())[4]])))
    #tableau.setItem(i, 5, QTableWidgetItem(str(data[i][list(data[i].keys())[5]])))

for i in range(len(data)):
    for j in range(len(colonnes)):
        tableau.setItem(i, j, QTableWidgetItem(str(data[i][colonnes[j]])))

# WINDOW AFFICHER
barre_outils = QHBoxLayout()
barre_outils.addWidget(recherche)
barre_outils.addWidget(bouton_croissant)
barre_outils.addWidget(bouton_decroissant)

appli = QWidget()
layout = QVBoxLayout(appli)
layout.addWidget(label_infos)
layout.addLayout(barre_outils)
layout.addWidget(tableau)

window = QMainWindow()
window.setCentralWidget(appli)
window.show()
# PERMET DE BIEN SORTIR DU PROGRAMME
sys.exit(app.exec())
