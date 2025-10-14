'''
-----------------------------
12/04/2025

Membre qui travaille dessus : Belharrat Mohamed, Takenne Simeon

Que fait le code ? 
Interfaçage de la search box pour l'écran d'accueil
Composé de : 
            - la barre de recherche
            - les menus déroulants des catégories et des types
            - le bouton de recherche


Changement par rapport à la version précédente : integration de la fonction chargerCategories
-----------------------------
'''

from HomeScreen import get_resource_path
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
import sqlite3, os
from function_python.final import parcours_categories

class SearchBox(QtWidgets.QGroupBox):

    searchSubmitted = pyqtSignal(list)

    def __init__(self, parent=None, categories : list[str] = ["Catégories..."], ):
        """
        Args
            categories : Liste des catégories à afficher"""
        super().__init__(parent)
        self.setObjectName("searchBox")
        self.setMinimumSize(QtCore.QSize(800, 80))  # Minimum size
        self.setFlat(False)

        self.searchBoxLayout = QtWidgets.QHBoxLayout(self)  # Horizontal layout for the search box to ensure responsiveness
        self.searchBoxLayout.setObjectName("searchBoxLayout")
        self.searchBoxLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)

        # Search bar
        self.searchBar = QtWidgets.QLineEdit(self)
        self.searchBar.setObjectName("searchBar")
        self.searchBar.setMinimumSize(QtCore.QSize(0, 61))  # Minimum size
        self.searchBar.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))  # Hover effect on search bar
        self.searchBoxLayout.addWidget(self.searchBar)  # Add search field to the layout

        # Dropdown menu for categories
        self.categoriesList = QtWidgets.QComboBox(self)
        self.categoriesList.setObjectName("categoriesList")
        self.categoriesList.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))  # Hover effect on categoriesList
        self.categoriesList.setMinimumSize(QtCore.QSize(200, 61))
        self.categoriesList.setMaximumSize(QtCore.QSize(500, 61))
        self.categoriesList.setFocusPolicy(QtCore.Qt.NoFocus)
        self.categoriesList.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        if(len(categories)==0):
            self.categoriesList.addItem(" ",None)
        elif(categories[0] == 'Histoire et Patrimoine' ):
            self.categoriesList.addItem("Catégories...",None)
        for cat in categories :
            if cat == None :
                self.categoriesList.addItem("Catégories...",None)
            else :
                self.categoriesList.addItem(cat,cat)
        self.searchBoxLayout.addWidget(self.categoriesList)

        # Dropdown menu for types
        self.typesList = QtWidgets.QComboBox(self)
        self.typesList.setObjectName("typesList")
        self.typesList.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))  # Hover effect on typesList
        self.typesList.setMinimumSize(QtCore.QSize(200, 61))
        self.typesList.setMaximumSize(QtCore.QSize(500, 61))
        self.typesList.setFocusPolicy(QtCore.Qt.NoFocus)
        self.typesList.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.typesList.addItem("Types...", None)     # Add types
        self.typesList.addItem("Films", "film")
        self.typesList.addItem("Series", "serie")
        self.typesList.addItem("Musique", "musique")
        self.typesList.addItem("Peintures / Sculptures", "peinturesculpture")
        self.typesList.addItem("Livres", "livre")
        self.typesList.addItem("Jeux-vidéos", "jeuvideo")
        self.searchBoxLayout.addWidget(self.typesList)

        # Search button
        self.searchButton = QtWidgets.QPushButton(self)
        self.searchButton.setObjectName("searchButton")
        self.searchButton.setMinimumSize(QtCore.QSize(61, 61))  
        self.searchButton.setText("")
        self.searchButton.setCursor(QtCore.Qt.PointingHandCursor)
        self.searchButton.clicked.connect(lambda: self.search())
        icon = QtGui.QIcon()
        icon_path = get_resource_path("images/search-icon.png")
        icon.addPixmap(QtGui.QPixmap(icon_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)  # Add icon
        self.searchButton.setIcon(icon)
        self.searchButton.setIconSize(QtCore.QSize(50, 50)) # Icon size
        self.searchBoxLayout.addWidget(self.searchButton)

        # Proportion of elements in the search box
        self.searchBoxLayout.setStretch(0, 5)
        self.searchBoxLayout.setStretch(1, 2)
        self.searchBoxLayout.setStretch(2, 1)

    
    def keyPressEvent(self, event):
        ''' 
        When Return key is pressed, call Searchbox.search()
        '''
        if event.key() == QtCore.Qt.Key_Return:
            self.search()

    def search(self):
        '''
        Return search-related information on an list [text, categories, type]
        '''
        typeSearch = self.typesList.currentData()  # Once the search is triggered, retrieve selected type and category
        categorieSearch = self.categoriesList.currentData()
        textSearch = self.searchBar.text()  
        dataSearch = [textSearch,categorieSearch,typeSearch] 
        self.searchSubmitted.emit(dataSearch) # Return a signal to parent with the search information
    
    
    
