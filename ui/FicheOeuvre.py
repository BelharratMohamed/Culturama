'''
-----------------------------
30/04/2025

Membre qui travaille dessus : Ilian Deqqaq et Belharrat Mohamed

Que fait le code ? 
Affichage de l'écran final de recherche


Changement par rapport à la version précédente : Résolution des bugs concernant le bouton retour
-----------------------------
'''


import os
from PyQt5 import QtWidgets, QtGui, QtCore
from function_python.final import get_resource_path,recommander_oeuvres

class FicheOeuvre(QtWidgets.QScrollArea):
    tracker = []
    def __init__(self,oeuvre_id,conn,parent = None,fromHomeScreen = False,fromFicheOeuvre = False):
        super().__init__()
        self.parent = parent
        self.fromFicheOeuvre = fromFicheOeuvre
        self.fromHomeScreen = fromHomeScreen
        self.conn = conn
        FicheOeuvre.tracker.append(oeuvre_id)

        self.setWidgetResizable(True)
        self.setStyleSheet("background: transparent; border: none;")

        # Widget that contains all the content
        self.scrollContent = QtWidgets.QWidget()
        self.scrollContent.setStyleSheet("background: transparent;")
        self.setWidget(self.scrollContent)
        
        # Principal Layout for scrollable content
        self.centralLayout = QtWidgets.QVBoxLayout(self.scrollContent)
        self.centralLayout.setContentsMargins(20, 20, 20, 20)
        
        # Create the label for the title
        self.titre = QtWidgets.QLabel("Titre de l'œuvre")
        self.titre.setAlignment(QtCore.Qt.AlignCenter)
        self.titre.setStyleSheet("font-family: 'Lucida Calligraphy';font-size: 90px; font-weight: bold; background-color:transparent;")    
        self.titre.setMaximumHeight(600)
        self.titre.setCursor(QtCore.Qt.IBeamCursor)  # Added IBeam cursor on the label
        self.titre.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse) # Selectable text
        self.titre.setWordWrap(True) # The title adapts to the size of the label
        
        # Create the centralLayout
        self.centralLayout.addWidget(self.titre)
        self.centralLayout.addSpacing(200) # Allow for the title to be quite spaced the rest of the page   

        self.infoLayout = QtWidgets.QHBoxLayout()
        
        # Create the label for the cover
        self.couverture = QtWidgets.QLabel()

        self.couverture.setAlignment(QtCore.Qt.AlignCenter)
        self.couverture.setFixedSize(900,900)
        
        self.infoLayout.addWidget(self.couverture, stretch=2)

        self.infoContainer = QtWidgets.QVBoxLayout()

        
        # Create the label for "Date :"
        self.dateLayout = QtWidgets.QVBoxLayout()
        self.date = QtWidgets.QLabel("Date :")
        self.date.setMaximumHeight(50)
        self.date.setStyleSheet("font-weight: bold;font-size: 30px;background-color:rgba(110, 66, 255,255);border-top-left-radius: 20px;border-top-right-radius: 20px;")
        self.date.setCursor(QtCore.Qt.IBeamCursor)  # Added IBeam cursor on the label
        self.date.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse) # Selectable text
        
        # Create the textBrowser for the date
        self.textBrowser_date = QtWidgets.QTextBrowser()
        self.textBrowser_date.setMaximumHeight(50)
        self.textBrowser_date.setStyleSheet("font-size: 30px; border: none;background-color: rgba(255, 255, 255, 150);border-bottom-left-radius: 20px;border-bottom-right-radius: 20px;")
        self.textBrowser_date.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))  # Added IBeam cursor on the label
        
        # Add each Widget to dateLayout
        self.dateLayout.addWidget(self.date)
        self.dateLayout.addWidget(self.textBrowser_date)
        self.dateLayout.setSpacing(0)

       
        # Create the label for "Score :"
        self.scoreLayout = QtWidgets.QVBoxLayout()
        self.score_evaluation = QtWidgets.QLabel("Score :")
        self.score_evaluation.setMaximumHeight(50)
        self.score_evaluation.setStyleSheet("font-weight: bold;font-size: 30px;background-color:rgba(110, 66, 255,255);border-top-left-radius: 20px;border-top-right-radius: 20px;")
        self.score_evaluation.setCursor(QtCore.Qt.IBeamCursor)  # Added IBeam cursor on the label
        self.score_evaluation.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse) # Selectable text

        # Create the textBrowser for the score
        self.textBrowser_score = QtWidgets.QTextBrowser()
        self.textBrowser_score.setMaximumHeight(50)
        self.textBrowser_score.setStyleSheet("font-size: 30px; border: none;background-color: rgba(255, 255, 255, 150);border-bottom-left-radius: 20px;border-bottom-right-radius: 20px;")
        
        # Add each Widget to scoreLayout
        self.scoreLayout.addWidget(self.score_evaluation)
        self.scoreLayout.addWidget(self.textBrowser_score)
        self.scoreLayout.setSpacing(0)

        
        # Create the label for "Auteur :"
        self.auteurLayout = QtWidgets.QVBoxLayout()
        self.auteur = QtWidgets.QLabel("Auteur :")
        self.auteur.setMaximumHeight(50)
        self.auteur.setStyleSheet("font-weight: bold;font-size: 30px;background-color:rgba(110, 66, 255,255);border-top-left-radius: 20px;border-top-right-radius: 20px;")
        self.auteur.setCursor(QtCore.Qt.IBeamCursor)  # Added IBeam cursor on the label
        self.auteur.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse) # Selectable text

        # Create the textBrowser for the author        
        self.textBrowser_auteur = QtWidgets.QTextBrowser()
        self.textBrowser_auteur.setMaximumHeight(50)
        self.textBrowser_auteur.setStyleSheet("font-size: 30px; border: none;background-color: rgba(255, 255, 255, 150);border-bottom-left-radius: 20px;border-bottom-right-radius: 20px;")
        
        # Add each Widget to auteurLayout
        self.auteurLayout.addWidget(self.auteur)
        self.auteurLayout.addWidget(self.textBrowser_auteur)
        self.auteurLayout.setSpacing(0)

        
        # Create the label for "Type :"
        self.nom_typeLayout = QtWidgets.QVBoxLayout()
        self.nom_type = QtWidgets.QLabel("Type :")
        self.nom_type.setMaximumHeight(50)
        self.nom_type.setStyleSheet("font-weight: bold;font-size: 30px;background-color:rgba(110, 66, 255,255);border-top-left-radius: 20px;border-top-right-radius: 20px;")
        self.nom_type.setCursor(QtCore.Qt.IBeamCursor)  # Added IBeam cursor on the label
        self.nom_type.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse) # Selectable text
        
        # Create the textBrowser for the type        
        self.textBrowser_type = QtWidgets.QTextBrowser()
        self.textBrowser_type.setMaximumHeight(50)
        self.textBrowser_type.setStyleSheet("font-size: 30px; border :none; background-color: rgba(255, 255, 255, 150);border-bottom-left-radius: 20px;border-bottom-right-radius: 20px;")

        # Add each Widget to nom_typeLayout       
        self.nom_typeLayout.addWidget(self.nom_type)
        self.nom_typeLayout.addWidget(self.textBrowser_type)
        self.nom_typeLayout.setSpacing(0)

        
        # Create the label for "Description :"
        self.descriptionLayout = QtWidgets.QVBoxLayout()
        self.description = QtWidgets.QLabel("Description :")
        self.description.setWordWrap(True) # The description adapts to the size of the label
        self.description.setMaximumHeight(50)
        self.description.setStyleSheet("font-weight: bold;font-size: 30px;background-color:rgba(110, 66, 255,255);border-top-left-radius: 20px;border-top-right-radius: 20px;")
        self.description.setCursor(QtCore.Qt.IBeamCursor)  # Added IBeam cursor on the label
        self.description.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse) # Selectable text

        # Create the textBrowser for the description
        self.textBrowser_description = QtWidgets.QTextBrowser()
        self.textBrowser_description.setMinimumHeight(200)  # Hauteur minimale raisonnable
        
        self.textBrowser_description.setStyleSheet("font-size: 30px; border: none;background-color: rgba(255, 255, 255, 150);border-bottom-left-radius: 20px;border-bottom-right-radius: 20px;")
        self.textBrowser_description.verticalScrollBar().setStyleSheet("background-color:rgba(110, 66, 255,255);") # Couleur de la barre de scroll

        # Add each Widget to descriptionLayout
        self.descriptionLayout.addWidget(self.description)
        self.descriptionLayout.addWidget(self.textBrowser_description)
        self.descriptionLayout.setSpacing(0)


        # Create the label for "Catégories : "
        self.categorieLayout = QtWidgets.QVBoxLayout()
        self.categorie = QtWidgets.QLabel("Catégories :")
        self.categorie.setMaximumHeight(50)
        self.categorie.setStyleSheet("font-weight: bold;font-size: 30px;background-color:rgba(110, 66, 255,255);border-top-left-radius: 20px;border-top-right-radius: 20px;")
        self.categorie.setCursor(QtCore.Qt.IBeamCursor)  # Added IBeam cursor on the label
        self.categorie.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse) # Selectable text
        
        self.categorieLayout.addWidget(self.categorie)
        self.categorieLayout.setSpacing(0)


        
        # Add each layout to infoContainer
        self.infoContainer.addLayout(self.dateLayout)
        self.infoContainer.addSpacing(20)
        self.infoContainer.addLayout(self.scoreLayout)
        self.infoContainer.addSpacing(20)
        self.infoContainer.addLayout(self.auteurLayout)
        self.infoContainer.addSpacing(20)
        self.infoContainer.addLayout(self.nom_typeLayout)
        self.infoContainer.addSpacing(20)
        self.infoContainer.addLayout(self.descriptionLayout)
        self.infoContainer.addSpacing(20)
        self.infoContainer.addLayout(self.categorieLayout)

        self.infoLayout.addLayout(self.infoContainer, stretch=2)

        
        # Create the label for the keywords
        self.motsClesLayout = QtWidgets.QVBoxLayout()
        self.label_mots_cles = QtWidgets.QLabel("  Mots-clés :")
        self.label_mots_cles.setMaximumHeight(60)
        self.label_mots_cles.setStyleSheet("font-weight: bold; font-size: 30px;background-color:rgba(110, 66, 255,255);border-top-left-radius: 20px;border-top-right-radius: 20px;")
        self.label_mots_cles.setCursor(QtCore.Qt.IBeamCursor)  # Added IBeam cursor on the label
        self.label_mots_cles.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse) # Selectable text
        
        self.motsClesLayout.addWidget(self.label_mots_cles)
        
        # Add a scroll area to enable scrolling when content exceeds window size
        self.scrollAreaMotsCles = QtWidgets.QScrollArea()
        self.scrollAreaMotsCles.setWidgetResizable(True) # The ScrollArea adapts to the size of the label
        self.scrollAreaMotsCles.setStyleSheet("margin: 0px;background-color: transparent;border-bottom-left-radius: 20px;border-bottom-right-radius: 20px;")
        self.scrollAreaMotsCles.setMinimumHeight(150)  # 	Min Height before scroll
        
        self.scrollAreaMotsCles.verticalScrollBar().setStyleSheet("background-color:rgba(110, 66, 255,255);") # Color of the scroll bar
		
		# Widget containing the grid
        self.gridLayoutWidget = QtWidgets.QWidget()
        self.gridLayoutWidget.setStyleSheet("background-color: rgba(255, 255, 255, 150);border-bottom-left-radius: 20px;border-bottom-right-radius: 20px;")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        
        self.scrollAreaMotsCles.setWidget(self.gridLayoutWidget)  # Adding the widget in the scrollArea

        
        self.motsClesLayout.addWidget(self.scrollAreaMotsCles)
        self.motsClesLayout.setSpacing(0)

        self.infoLayout.addLayout(self.motsClesLayout,stretch=1)

        self.centralLayout.addLayout(self.infoLayout)
		
        self.centralLayout.addSpacing(150)
		
        # Section "Vous aimeriez peut-être" 
        self.recommendationsLayout = QtWidgets.QVBoxLayout()
        self.recommendationsLayout.setContentsMargins(0, 20, 0, 20)  # Marge pour aérer

        # Title of the section
        self.recommendationsTitle = QtWidgets.QLabel("Vous aimeriez peut-être :")
        self.recommendationsTitle.setStyleSheet("font-weight: bold; font-size: 40px; background-color: rgba(110, 66, 255,255); border-radius: 20px; padding: 10px;margin-bottom: 15px;")
        self.recommendationsTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.recommendationsLayout.addWidget(self.recommendationsTitle)

        # ScrollArea horizontale pour les recommandations
        self.scrollAreaRecommandations = QtWidgets.QScrollArea()
        self.scrollAreaRecommandations.setMinimumHeight(600)  # Hauteur fixe pour la zone
        self.scrollAreaRecommandations.setWidgetResizable(True)
        self.scrollAreaRecommandations.setStyleSheet("background: transparent;border: none; padding: 10px 0;")
        self.scrollAreaRecommandations.setStyleSheet("""
        QScrollArea {
            background: transparent;
            border: none;
            }
        """)
        
        

        # Widget pour contenir les recommandations
        self.recommandationsWidget = QtWidgets.QWidget()
        self.recommandationsWidget.setStyleSheet("background: transparent;")
        self.horizontalLayoutRecommandations = QtWidgets.QHBoxLayout(self.recommandationsWidget)
        self.horizontalLayoutRecommandations.setSpacing(30)
        self.horizontalLayoutRecommandations.setContentsMargins(20, 0, 20, 10)
        

        # Use the function to set each recommandation
        recommandations = recommander_oeuvres(oeuvre_id, self.conn)
        if recommandations:
            for reco in recommandations:
                # Creation  of a card
                card = QtWidgets.QFrame()
                
                layout = QtWidgets.QVBoxLayout(card)
                layout.setContentsMargins(5, 5, 5, 5)
                img_label = QtWidgets.QLabel()
                img_label.setMinimumHeight(400)
                img_label.setMinimumWidth(400)
                
                img_label.setStyleSheet("""
                QLabel:hover{
                    background-color:#339DFF;
                }
                """)
                base_dir = os.path.dirname(os.path.abspath(__file__))  # Found the path for this file on the system
                relative_path = os.path.join(base_dir, "../Cache", f"{reco["id"]}.jpg")  # Found the .jpg
                if os.path.exists(relative_path): # Check if the artwork has a cover in "Cache"
                    image_path=os.path.normpath(relative_path) # Normalize the path
                    pixmap = QtGui.QPixmap(image_path)
                else:
                    relative_path = os.path.join(base_dir, "../Cache", "pas_disponible.jpg")
                    image_path=os.path.normpath(relative_path) # Normalize the path
                    pixmap = QtGui.QPixmap(image_path)
                pixmap=pixmap.scaled(img_label.minimumWidth(), img_label.minimumHeight(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation) 
                img_label.setPixmap(pixmap)
                img_label.setAlignment(QtCore.Qt.AlignCenter)
                img_label.setCursor(QtCore.Qt.PointingHandCursor)    # Change hover
                img_label.id=reco["id"]
                img_label.mousePressEvent = lambda event, l = img_label : self.labelClicked(l)       # Action when clicked, l=label to not lose the label
                layout.addWidget(img_label)
                # Title (below the image)
                titre_brut = reco['nom']                        # Wrap the title
                if len(titre_brut) > 30:
                    titre_affiche = titre_brut[:24] + "..."
                else:
                    titre_affiche = titre_brut                
                title = QtWidgets.QLabel(titre_affiche)
                title.setAlignment(QtCore.Qt.AlignCenter)
                title.setStyleSheet("font-size: 25px;font-family: 'Times New Roman';")
                title.setCursor(QtCore.Qt.IBeamCursor)  # Added IBeam cursor on the title 
                title.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse) # Selectable text)
                
                container = QtWidgets.QWidget()                 # Containe img + text
                container.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred) # Not spread the image                
                layout = QtWidgets.QVBoxLayout(container)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.setSpacing(5)
                layout.addWidget(img_label)        
                layout.addWidget(title)   
                # Ajout du container au layout horizontal
                self.horizontalLayoutRecommandations.addWidget(container)


        else:
            lbl_vide = QtWidgets.QLabel("Aucune recommandation disponible")
            lbl_vide.setAlignment(QtCore.Qt.AlignCenter)
            self.horizontalLayoutRecommandations.addWidget(lbl_vide)      
        
        
        
        self.scrollAreaRecommandations.setWidget(self.recommandationsWidget)
        self.recommendationsLayout.addWidget(self.scrollAreaRecommandations)

        # Ajouter au layout principal avec un stretch pour l'espace
        self.centralLayout.addLayout(self.recommendationsLayout)
        self.centralLayout.addStretch(1)  # Espace supplémentaire en bas
        
        # Ajout d'un bouton retour pour fermer la page et revenir à la page précédente
        self.bouton_retour = QtWidgets.QPushButton()
        self.bouton_retour.setObjectName("retour")
        self.bouton_retour.setMinimumSize(QtCore.QSize(100, 50))
        self.bouton_retour.setMaximumSize(QtCore.QSize(100, 50))
        
        self.bouton_retour.clicked.connect(self.retour_en_arriere)
        icon = QtGui.QIcon()
        icon_path = get_resource_path("images/retour-icon.png")
        icon.addPixmap(QtGui.QPixmap(icon_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)  # Add icon
        self.bouton_retour.setIconSize(QtCore.QSize(100, 50))
        self.bouton_retour.setIcon(icon)
        
        self.bouton_retour.setCursor(QtCore.Qt.PointingHandCursor)  # Change the cursor to a hand shape
        
        self.centralLayout.insertWidget(0, self.bouton_retour)  # Add at top of the window

        self.afficher_infos_oeuvre(oeuvre_id,self.conn)

    def recuperer_infos_oeuvre(self, oeuvre_id,conn):
            """
            This function allows to recover informations of an artwork in the databse whith its id in params
            """
            cursor = conn.cursor()
            cursor.execute("SELECT nom, date, description, score_evaluation, mots_cles, nom_type, auteur FROM oeuvre WHERE id=?", (oeuvre_id,))
            row = cursor.fetchone()
            

            return {
                'nom': row[0],
                'date': row[1],
                'description': row[2],
                'score_evaluation': row[3],
                'mots_cles': row[4],
                'nom_type':row[5],
                'auteur':row[6]
            }
        
    def afficher_infos_oeuvre(self, oeuvre_id,conn):
        """
        This function allows to display each information of the artwork in labels and textBrowser.
        """
        oeuvre = self.recuperer_infos_oeuvre(oeuvre_id,conn)
        self.titre.setText(oeuvre['nom'])
        self.date.setText("  Date :")
        self.textBrowser_date.setText(oeuvre['date'])
        self.description.setText("  Description :")
        self.textBrowser_description.setText(oeuvre['description'])
        if (oeuvre['nom_type'] == 'Musique' or oeuvre['nom_type'] == 'Peinture et Sculpture'):   
            self.score_evaluation.deleteLater()
            self.textBrowser_score.deleteLater()
            
        else:    
            self.score_evaluation.setText("  Score :")        
            # Checking for the presence of an evaluation score
            if oeuvre['score_evaluation'] != 0.0:
                self.textBrowser_score.setText(str(oeuvre['score_evaluation'])+"/10")
            else:
                self.textBrowser_score.setText("Non évalué")
        
        if (oeuvre['nom_type'] == 'Film'):
            self.auteur.setText("  Réalisateur :")
        elif (oeuvre['nom_type'] == 'Musique' or oeuvre['nom_type'] == 'Peinture et Sculpture'):
            self.auteur.setText("  Artiste :")
        elif (oeuvre['nom_type'] == 'Jeu-vidéo'):
            self.auteur.setText(" Studio :")
        else :
            self.auteur.setText("  Auteur :")
        self.textBrowser_auteur.setText(oeuvre['auteur'])
        self.nom_type.setText("  Type : ")
        self.textBrowser_type.setText(oeuvre['nom_type'])

        base_dir = os.path.dirname(os.path.abspath(__file__))  # Found the path for this file on the system
        
        relative_path = os.path.join(base_dir, "../Cache", f"{oeuvre_id}.jpg")
        if os.path.exists(relative_path):
            image_path= os.path.normpath(relative_path)   # Normalize the path
            pixmap = QtGui.QPixmap(image_path)
            
        else:
            relative_path = os.path.join(base_dir, "../Cache", "pas_disponible.jpg")
            image_path = os.path.normpath(relative_path)  # Normalize the path
            pixmap = QtGui.QPixmap(image_path)
        pixmap = pixmap.scaled(self.couverture.minimumWidth(), self.couverture.minimumHeight(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)        # Scale the .jpg to fit 
        self.couverture.setPixmap(pixmap)

        self.ajouter_mots_cles(oeuvre['mots_cles'],conn)
        self.ajouter_categories(oeuvre_id, conn)


    def ajouter_mots_cles(self, mots_cles,conn):
            """
            This function allows add keywords 
            """
            # We empty the existing layout
            for i in reversed(range(self.gridLayout.count())):
                widget = self.gridLayout.itemAt(i).widget()
                if widget is not None:
                    widget.setParent(None)

            # Cases where there is no keyword
            if mots_cles.strip().lower() == "aucun":
                label = QtWidgets.QLabel("Aucun mot clé n'est disponible.")
                label.setStyleSheet("font-size: 20px;padding: 5px;background-color:transparent;")
                label.setAlignment(QtCore.Qt.AlignCenter)

                # Horizontal layout to center the label
                wrapper = QtWidgets.QWidget()
                wrapperLayout = QtWidgets.QHBoxLayout()
                wrapperLayout.addStretch()
                wrapperLayout.addWidget(label)
                wrapperLayout.addStretch()
                wrapper.setStyleSheet("background-color:transparent;")
                wrapper.setLayout(wrapperLayout)
                

                self.gridLayout.addWidget(wrapper, 0, 0, 1, -1)  # Span across the board
                return
        
            # Otherwise, we display the keywords normally
            mots = mots_cles.split(", ") # Keywords are stored as text and are separated by commas
            row, col = 0, 0
            for mot in mots:
                label = QtWidgets.QLabel(mot)
                label.setStyleSheet("""
                    QLabel{
                        background-color:rgba(110, 66, 255,255);
                        padding: 5px;
                        border: 2px solid black;
                        border-radius: 20px;
                        font-size: 30px;
                        color:black;
                    }
                    QLabel:hover{
                        color:white;
                    }
                """)
                label.setMaximumWidth(400)
                label.setAlignment(QtCore.Qt.AlignCenter)
                label.setCursor(QtCore.Qt.IBeamCursor)
                label.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse) # Selectable text
                label.setWordWrap(True) # Label adapts to text size
                self.gridLayout.addWidget(label, row, col)
                col += 1
                if col >= 1:
                    col = 0
                    row += 1
            
    
    def ajouter_categories(self, oeuvre_id, conn):
        """
        This function allows to add categories in a GridLayout with 4 labels per line with parent category tooltips
        
        
        """
        # Clear any existing widgets in the categories layout
        for i in reversed(range(self.categorieLayout.count())):
            widget = self.categorieLayout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
        
        
        # Create and add the title label
        title_label = QtWidgets.QLabel("Catégories :")
        title_label.setMaximumHeight(40)
        title_label.setStyleSheet("font-weight: bold;font-size: 30px;background-color: rgba(110, 66, 255, 255);border-top-left-radius: 20px;border-top-right-radius: 20px;padding-left: 10px;")
        title_label.setCursor(QtCore.Qt.IBeamCursor)
        title_label.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.categorieLayout.addWidget(title_label)
        
        
        # Create a scroll area for categories
        scrollAreaCategories = QtWidgets.QScrollArea()
        scrollAreaCategories.setWidgetResizable(True)
        scrollAreaCategories.setStyleSheet("margin: 0px; background-color: transparent; border-bottom-left-radius: 20px; border-bottom-right-radius: 20px;")
        scrollAreaCategories.setMinimumHeight(150)
        scrollAreaCategories.setMaximumHeight(1000)
        
    
        # Widget containing the grid
        gridWidget = QtWidgets.QWidget()
        gridWidget.setStyleSheet("background-color: rgba(255, 255, 255, 150); border-bottom-left-radius: 20px; border-bottom-right-radius: 20px;")
        gridLayout = QtWidgets.QGridLayout(gridWidget)
        gridLayout.setContentsMargins(10, 10, 10, 10)
        gridLayout.setSpacing(15) # Space between category
    
        # Get categories from database
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.nom, p.nom as nom_parent
            FROM categorie c
            LEFT JOIN categorie p ON c.id_parent = p.id
            JOIN oeuvre_categorie oc ON c.id = oc.id_categorie
            WHERE oc.id_oeuvre = ?
        """, (oeuvre_id,))
        categories = cursor.fetchall()
    
        if not categories:
            # No categories case
            label = QtWidgets.QLabel("Aucune catégorie disponible")
            label.setStyleSheet("font-size: 20px; padding: 5px; background-color:transparent;")
            label.setAlignment(QtCore.Qt.AlignCenter)
            gridLayout.addWidget(label, 0, 0, 1, 4)  # Span all 4 columns
        else:
            # Add categories to grid (4 per row)
            row, col = 0, 0
            for nom_categorie, nom_parent in categories:
                # Create category label
                label = QtWidgets.QLabel(nom_categorie)
                label.setStyleSheet("""
                    QLabel{
                        background-color: rgba(110, 66, 255, 255);
                        padding: 5px;
                        border: 2px solid black;
                        border-radius: 20px;
                        font-size: 30px;
                        color:black;
                    }    
                    QLabel:hover{
                        color:white;
                    }
                    
                    QToolTip {
                        background-color: rgba(110, 66, 255, 255);
                        color: white;
                        border: 1px solid black;
                        padding: 5px;
                        border-radius: 10px;
                        font-size: 25px;
                    }
                """)
                label.setMaximumWidth(400)
                label.setAlignment(QtCore.Qt.AlignCenter)
                label.setCursor(QtCore.Qt.IBeamCursor) # Text cursor on hover
                label.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
                label.setWordWrap(True)
                # Add tooltip showing parent category
                if nom_parent :
                    label.setToolTip(f"Catégorie parente: {nom_parent}")
                else:
                    label.setToolTip("Catégorie racine (pas de parent)")
                # Add to grid and manage positioning
                gridLayout.addWidget(label, row, col)
                col += 1
                if col >= 4:  # 4 labels per row
                    col = 0
                    row += 1
    
        # Finalize layout
        scrollAreaCategories.setWidget(gridWidget)
        self.categorieLayout.addWidget(scrollAreaCategories)
        self.categorieLayout.setSpacing(0)
    
    
    
        
    def retour_en_arriere(self):
            """
            This function allows to return to the previous page 
            """
            if self.fromHomeScreen == True:
                self.goBack()
            elif self.fromFicheOeuvre == True:
                self.close()
                self.goBack()
            else :
                self.close()
                self.parent.parent.goBack()
                
                
    def labelClicked(self,label):
        '''
        Action when one label is clicked
        '''
        label.setStyleSheet("QLabel { border: 1px solid green; }")
        self.parent.changeToFicheOeuvre(label.id,fromFicheOeuvre = True,fromHomeScreen = self.fromHomeScreen)
   

    def goBack(self):
        '''
        Come back from another FicheOeuvre
        '''
        if len(FicheOeuvre.tracker) == 1 :
            id = self.tracker.pop()
            self.parent.changeToFicheOeuvre(id)
            FicheOeuvre.tracker = []
            if (self.fromHomeScreen == True):
                self.parent.changeToHomeScreen()
            else :
                self.close()
                self.parent.changeIntermediateScreen(dataSearch = [-1])
        else :
            FicheOeuvre.tracker.pop()
            self.parent.changeToFicheOeuvre(FicheOeuvre.tracker.pop(),fromFicheOeuvre = True,fromHomeScreen = self.fromHomeScreen)
