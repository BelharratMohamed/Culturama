'''
-----------------------------
10/04/2025

Membre qui travaille dessus : Belharrat Mohamed

Que fait le code ? 
Classe pour l'affiche d'une oeuvre dans l'écran de recherche intermediaire


Changement par rapport à la version précédente : 
-----------------------------
'''
import os
from function_python.final import rechercher_oeuvre_par_id
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QGroupBox, QLabel, QGridLayout, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QFont, QCursor
from FicheOeuvre import FicheOeuvre

db_path = "../../trunk/culturama.db"

class ArtworksIntermediate(QGroupBox):
    # Signal personnalisé
    clicked = pyqtSignal(int)  # On émet l'id de l'œuvre

    def __init__(self, id: int,conn,parent):
        """
        Classe pour l'affichage d'une œuvre sur l'écran de recherche intermédiaire.
        Composé d'une image, d'un titre et d'une descirption

        Généré en partie à l'aide de l'outil designer de Qt

        Args:
            id (int): Identifiant de l'œuvre
        """
        super().__init__()
        self.parent = parent
        self.id = id
        self.conn=conn
        if(id == 11):
            id = 22
        self.info_oeuvre = rechercher_oeuvre_par_id(id,conn,db_path)
        self.c = 10
        while(self.info_oeuvre is None or id == 11):
            self.info_oeuvre = rechercher_oeuvre_par_id(id + self.c,conn,db_path)
            self.c+=1

        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setMaximumHeight(350)
        self.setObjectName("artwork")

        # Layout principal
        layout = QGridLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setHorizontalSpacing(20)
        layout.setColumnStretch(0, 0)
        layout.setColumnStretch(1, 1)

        # IMAGE
        self.image = QLabel()
        self.image.setFixedSize(200, 300)  # Taille plus élégante
        base_dir = os.path.dirname(os.path.abspath(__file__))
        relative_path = os.path.join(base_dir, "../Cache", str(id)+".jpg")
        if os.path.exists(relative_path):
            img_path = os.path.normpath(relative_path)
            img = QtGui.QPixmap(img_path)                                   # Add the .jpg to a Pixmap to add it to the label
        else:
            relative_path = os.path.join(base_dir, "../Cache", "pas_disponible.jpg") # Put a default image
            img_path = os.path.normpath(relative_path)                      # Normalize the path
            img = QtGui.QPixmap(img_path)                                   # Add the .jpg to a Pixmap to add it to the label
        img = img.scaled(self.image.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        self.image.setPixmap(img)
        layout.addWidget(self.image, 0, 0, 1, 1, alignment=Qt.AlignTop)

        # Widget contenant le titre et la description
        text_container = QWidget()
        text_layout = QVBoxLayout(text_container)
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(10)

        # TITRE
        self.title = QLabel(self.info_oeuvre[1])
        self.title.setFont(QFont("Arial", 32, QFont.Bold))
        self.title.setWordWrap(True)
        text_layout.addWidget(self.title)

        # DESCRIPTION
        description_text = self.info_oeuvre[2]
        if len(description_text) > 250:
            description_text = description_text[:247] + "..."
        else:
            description_text = description_text

        self.description = QLabel(description_text)
        self.description.setFont(QFont("Arial", 20))
        self.description.setWordWrap(True)
        self.description.setStyleSheet("color: #f0f0f0;")
        text_layout.addWidget(self.description)

        # Ajout du container texte dans le layout principal
        layout.addWidget(text_container, 0, 1, 1, 1)
    def mousePressEvent(self, event):
        """
        Déclenché lorsqu'on clique sur la groupBox.
        """
        if event.button() == Qt.LeftButton:
            self.setStyleSheet("QGroupBox { border: 1px solid green; }")
        self.parent.close()
        
        # Change to new Layout
        self.resultWidget = FicheOeuvre(oeuvre_id=self.id,conn=self.conn,parent=self)
        self.parent.tracker.append([])
        self.parent.parentWidget.gridLayout.addWidget(self.resultWidget, 0, 0)

    def changeToFicheOeuvre(self,id,fromFicheOeuvre,fromHomeScreen):
        self.parent.parentWidget.changeToFicheOeuvre(id,fromFicheOeuvre = fromFicheOeuvre , fromHomeScreen = fromHomeScreen)


    
