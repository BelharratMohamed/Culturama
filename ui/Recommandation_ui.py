'''
-----------------------------
10/04/2025

Membre qui travaille dessus : Belharrat Mohamed

Que fait le code ? 
Recommandations de l'écran d'accueil

Changement par rapport à la version précédente : Ajoute une image par défaut quand les oeuvres n'ont pas de couverture.
-----------------------------
'''
import os
from function_python.final import rechercher_oeuvre_par_id
from PyQt5 import QtWidgets, QtCore, QtGui

db_path = "culutrama.db"

class Recommandation(QtWidgets.QScrollArea):
    def __init__(self,conn, recoList: list[str], parent=None):
        """
        Affiche les recommandations sur l'écran d'accueil
        
        Args:
            recoList : liste des id des oeuvres dans cette section"""
        super().__init__()

        self.parent = parent

        # Create a group box
        group_box = QtWidgets.QGroupBox()
        group_layout = QtWidgets.QHBoxLayout()

        for id in recoList:
            info = rechercher_oeuvre_par_id(id,conn,db_path)        # List with artwork information
            label = QtWidgets.QLabel()                 # Add label
            label.id = id                              # Save id
            label.setMinimumWidth(300)                 # set Size
            label.setMinimumHeight(300)
            label.setStyleSheet("""
                QLabel {
                    background-color: transparent;
                }
                QLabel:hover {
                    background-color : #339DFF;
                }
            """)
            base_dir = os.path.dirname(os.path.abspath(__file__))           # Found the path for this file on the system
            relative_path = os.path.join(base_dir, "../Cache", str(id)+".jpg")          # Found the .jpg
            if os.path.exists(relative_path):
                img_path = os.path.normpath(relative_path)                      # Normalize the path
                img = QtGui.QPixmap(img_path)                                   # Add the .jpg to a Pixmap to add it to the label
            else:
                relative_path = os.path.join(base_dir, "../Cache", "pas_disponible.jpg")          # Put a default image
                img_path = os.path.normpath(relative_path)                      # Normalize the path
                img = QtGui.QPixmap(img_path)                                   # Add the .jpg to a Pixmap to add it to the label
            img = img.scaled(label.minimumWidth(), label.minimumHeight(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)        # Scale the .jpg to fit 
            label.setPixmap(img)
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setCursor(QtCore.Qt.PointingHandCursor)               # Change hover
            label.mousePressEvent = lambda event, l = label : self.labelClicked(l)      # Action when clicked, l=label to not lose the label

            titre_brut = info[1]                        # Wrap the title
            if len(titre_brut) > 30:
                titre_affiche = titre_brut[:24] + "..."
            else:
                titre_affiche = titre_brut

            title = QtWidgets.QLabel(titre_affiche)      # Title under img   
            title.setAlignment(QtCore.Qt.AlignCenter)       # Center the title
            title.setStyleSheet("font-size: 25px;font-family: 'Times New Roman';")
            title.setCursor(QtCore.Qt.IBeamCursor)  # Added IBeam cursor on the title    
            title.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse) # Selectable text)

            container = QtWidgets.QWidget()                 # Containe img + text
            layout = QtWidgets.QVBoxLayout(container)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(5)
            layout.addWidget(label)
            layout.addWidget(title)

            group_layout.addWidget(container)                                # Add to widget
        group_box.setLayout(group_layout)                               # Add to the main layout of the ScrollArea

        # Set the group box as the widget for the scroll area
        self.setWidget(group_box)
        self.setWidgetResizable(True)
        self.setMaximumHeight(500)
        self.setAutoFillBackground(False)
    
    def labelClicked(self,label):
        '''
        Action when one label is clicked
        '''
        label.setStyleSheet("QLabel { border: 1px solid green; }")
        self.parent.changeToFicheOeuvre(label.id)

        print(label.id)
