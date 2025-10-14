'''
-----------------------------
10/04/2025

Membre qui travaille dessus : Belharrat Mohamed

Que fait le code ? 
Interfaçage de l'écran d'accueil, importé via PyQt5 depuis Qt designer :
    - Searchbox depuis searchbox.py
    - Ajout du titre : title
    - Ajout d'un stylesheet qss

Changement par rapport à la version précédente : Ajout des méthodes permettant le bouton retour de fonctionner
-----------------------------
'''
# Created by: PyQt5 UI code generator 5.15.11

import os
from function_python.final import get_resource_path, parcours_categories, get_ids_recommandation_par_type
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy
from SearchBox import SearchBox  
from Recommandation_ui import Recommandation 
from IntermediateSearchScreen import IntermediateSearchScreen
from FicheOeuvre import FicheOeuvre


class Ui_homeScreen(object):

    def setupUi(self, homeScreen, conn):

        self.homeScreen = homeScreen
        self.conn = conn


        homeScreen.setObjectName("homeScreen")
        
        homeScreen.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)

        stylesheet_path = get_resource_path("homeScreen.txt")
        # Load the QSS file to apply styles to the interface
        if not os.path.exists(stylesheet_path):
            stylesheet_path = "ui/homeScreen.txt"
        with open(stylesheet_path, "r") as file:
            homeScreen.setStyleSheet(file.read())

        self.centralwidget = QtWidgets.QWidget(homeScreen)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setMaximumSize(QtCore.QSize(5000, 10000))
        self.centralwidget.setContextMenuPolicy(QtCore.Qt.NoContextMenu)

        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget) # Use a grid layout to make the window responsive
        self.gridLayout.setObjectName("gridLayout")

        # Add a scroll area to enable scrolling when content exceeds window size
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setMinimumSize(QtCore.QSize(800, 300))
        self.scrollArea.setWidgetResizable(True)

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1883, 5000))
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(800, 5000))

        self.gridLayout_scrollArea = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)   # Use a grid layout to make the window responsive
        self.gridLayout_scrollArea.setObjectName("gridLayout_scrollArea")

        self.verticalSpacerTopTitle = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout_scrollArea.addItem(self.verticalSpacerTopTitle, 0, 0, 1, 1) # Add spacer to the grid to ensure responsiveness

        # Create the label for the title
        self.title = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.title.setObjectName("title")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(3)   # Set horizontal resizing ratio
        sizePolicy.setVerticalStretch(0)
        self.title.setSizePolicy(sizePolicy)
        self.title.setMinimumSize(QtCore.QSize(0, 100)) # Set minimum title size
        self.title.setAlignment(QtCore.Qt.AlignCenter)  # Center alignment
        self.gridLayout_scrollArea.addWidget(self.title, 1, 0, 1, 1)    # Add title to the grid to ensure responsiveness

        self.verticalSpacerBetweenTitleAndSearchBox = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)   # Add a spacer between title and search box
        self.gridLayout_scrollArea.addItem(self.verticalSpacerBetweenTitleAndSearchBox, 2, 0, 1, 1) # Add spacer to the grid


        # Create the search box using the SearchBox class
        self.searchBox = SearchBox(self.scrollAreaWidgetContents,parcours_categories(conn,start_category=None))
        self.searchBox.searchSubmitted.connect(self.changeIntermediateScreen) # Waiting for the signal to change the window
        self.gridLayout_scrollArea.addWidget(self.searchBox, 3, 0, 1, 1)

        # Add title for recommandation section
        self.recommandationText = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.recommandationText.setObjectName("recommandationText")
        self.gridLayout_scrollArea.addWidget(self.recommandationText, 5, 0, 1, 1)
        

        # Add title for film section
        self.recommandationFilmText = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.recommandationFilmText.setObjectName("recommandationFilmText")
        self.gridLayout_scrollArea.addWidget(self.recommandationFilmText, 6, 0, 1, 1)

        # Add film section
        film_ids = get_ids_recommandation_par_type("Film",conn)
        self.filmSection = Recommandation(conn,film_ids,parent=self)
        self.filmSection.setObjectName("serieSection")
        self.gridLayout_scrollArea.addWidget(self.filmSection, 7, 0, 1, 1)

        # Add title for serie section
        self.recommandationSerieText = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.recommandationSerieText.setObjectName("recommandationSerieText")
        self.gridLayout_scrollArea.addWidget(self.recommandationSerieText, 8, 0, 1, 1)

        # Add serie section
        serie_ids = get_ids_recommandation_par_type("Série",conn)
        self.serieSection = Recommandation(conn,serie_ids,parent=self)
        self.serieSection.setObjectName("serieSection")
        self.gridLayout_scrollArea.addWidget(self.serieSection, 9, 0, 1, 1)

        # Add title for livre section
        self.recommandationLivreText = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.recommandationLivreText.setObjectName("recommandationLivreText")
        self.gridLayout_scrollArea.addWidget(self.recommandationLivreText, 10, 0, 1, 1)

        # Add livre section
        livre_ids = get_ids_recommandation_par_type("Livre",conn)
        self.livreSection = Recommandation(conn,livre_ids,parent=self)
        self.livreSection.setObjectName("livreSection")
        self.gridLayout_scrollArea.addWidget(self.livreSection, 11, 0, 1, 1)

        # Add title for musique section
        self.recommandationMusiqueText = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.recommandationMusiqueText.setObjectName("recommandationMusiqueText")
        self.gridLayout_scrollArea.addWidget(self.recommandationMusiqueText, 12, 0, 1, 1)

        # Add musique section
        musique_ids = get_ids_recommandation_par_type("Musique",conn)
        self.musiqueSection = Recommandation(conn,musique_ids,parent=self)
        self.musiqueSection.setObjectName("musiqueSection")
        self.gridLayout_scrollArea.addWidget(self.musiqueSection, 13, 0, 1, 1)

        # Add title for peinture section
        self.recommandationPeintureText = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.recommandationPeintureText.setObjectName("recommandationPeintureText")
        self.gridLayout_scrollArea.addWidget(self.recommandationPeintureText, 14, 0, 1, 1)

        # Add peinture section
        peinture_ids = get_ids_recommandation_par_type("Peinture et Sculpture",conn)
        self.peintureSection = Recommandation(conn,peinture_ids,parent=self)
        self.peintureSection.setObjectName("peintureSection")
        self.gridLayout_scrollArea.addWidget(self.peintureSection, 15, 0, 1, 1)

        # Add title for jv section
        self.recommandationJVText = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.recommandationJVText.setObjectName("recommandationJVText")
        self.gridLayout_scrollArea.addWidget(self.recommandationJVText, 16, 0, 1, 1)

        # Add jv section
        jv_ids = get_ids_recommandation_par_type("Jeu-vidéo",conn)
        self.jvSection = Recommandation(conn,jv_ids,parent=self)
        self.jvSection.setObjectName("jvSection")
        self.gridLayout_scrollArea.addWidget(self.jvSection, 17, 0, 1, 1)

        # Add bottom logo
        self.bottomLogo = QtWidgets.QLabel()
        self.bottomLogo.setObjectName("bottomLogo")
        self.logo_path = get_resource_path("images/appIcon.png")
        self.bottomLogo.setPixmap(QtGui.QPixmap(self.logo_path))
        self.bottomLogo.setScaledContents(True)
        self.bottomLogo.setMaximumSize(350,250)
        
        self.gridLayout_scrollArea.addWidget(self.bottomLogo, 18, 0, 1, 1, QtCore.Qt.AlignCenter)


        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)

        pRecoText = 3; # Proportion Recommandation Type text
        pRecoScroll = 8; # Proportion Recommandation Scroll

        # Proportion of elements on the screen
        self.gridLayout_scrollArea.setRowStretch(0, 1)  # Spacer above title
        self.gridLayout_scrollArea.setRowStretch(1, 1)  # Title
        self.gridLayout_scrollArea.setRowStretch(2, 1)  # Spacer between searchbox and title 
        self.gridLayout_scrollArea.setRowStretch(3, 1)  # Search box
        self.gridLayout_scrollArea.setRowStretch(4, 1)  # Spacer between recommandation text and search box
        self.gridLayout_scrollArea.setRowStretch(5, 2)  # Recommandation text
        self.gridLayout_scrollArea.setRowStretch(6, pRecoText)  # Film text
        self.gridLayout_scrollArea.setRowStretch(7, pRecoScroll)  # Film section
        self.gridLayout_scrollArea.setRowStretch(8, pRecoText)  # Serie text
        self.gridLayout_scrollArea.setRowStretch(9, pRecoScroll)  # Serie section
        self.gridLayout_scrollArea.setRowStretch(10, pRecoText)  # Livre text
        self.gridLayout_scrollArea.setRowStretch(11, pRecoScroll)  # Livre section
        self.gridLayout_scrollArea.setRowStretch(12, pRecoText)  # Musique text
        self.gridLayout_scrollArea.setRowStretch(13, pRecoScroll)  # Musique section
        self.gridLayout_scrollArea.setRowStretch(14, pRecoText)  # Peinture text
        self.gridLayout_scrollArea.setRowStretch(15, pRecoScroll)  # Peinture section
        self.gridLayout_scrollArea.setRowStretch(16, pRecoText)  # JV text
        self.gridLayout_scrollArea.setRowStretch(17, pRecoScroll)  # JV section
        self.gridLayout_scrollArea.setRowStretch(18, 0) # Spacer bottom screen
        homeScreen.setCentralWidget(self.centralwidget)  # Set the central widget


        self.retranslateUi(homeScreen)
        QtCore.QMetaObject.connectSlotsByName(homeScreen)

    def retranslateUi(self, homeScreen):
        homeScreen.setWindowTitle("Culturama")
        homeScreen.setWindowIcon(QtGui.QIcon(self.logo_path))
        self.title.setText("CULTURAMA")  # Set the title text
        self.searchBox.searchBar.setPlaceholderText("Recherche...")  # Placeholder text for the search bar
        self.recommandationText.setText("Recommandations")  # Recommandation title text
        self.recommandationFilmText.setText("Films")
        self.recommandationSerieText.setText("Series")
        self.recommandationLivreText.setText("Livres")
        self.recommandationMusiqueText.setText("Musiques")
        self.recommandationPeintureText.setText("Peintures / Sculptures")
        self.recommandationJVText.setText("Jeux-Vidéos")

    def changeIntermediateScreen(self,dataSearch):
        self.clearLayout(self.gridLayout)  # Clear the Screen
        self.searchBox.setParent(None)  # Delete the searchbar
        
        # Change to new Layout
        self.resultWidget = IntermediateSearchScreen(self.conn,data = dataSearch,parentWidget=self)
        self.gridLayout.addWidget(self.resultWidget, 0, 0)

    def changeToHomeScreen(self):
        self.clearLayout(self.gridLayout) 
        self.setupUi(self.homeScreen,conn=self.conn)      # Reload homeScreen
    
    def changeToFicheOeuvre(self,id,fromFicheOeuvre = False,fromHomeScreen=True):
        self.clearLayout(self.gridLayout)
        self.searchBox.setParent(None)

        self.resultWidget = FicheOeuvre(id,self.conn,parent=self,fromHomeScreen=fromHomeScreen,fromFicheOeuvre=fromFicheOeuvre)
        self.gridLayout.addWidget(self.resultWidget, 0, 0)

    def clearLayout(self,layout):
        """Clear the window (found on gitHub)"""
        while layout.count():
            item = layout.takeAt(0)  
            if item.widget():
                item.widget().deleteLater()  
            elif item.layout():
                self.clearLayout(item.layout())  

