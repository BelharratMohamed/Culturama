'''
-----------------------------
30/04/2025

Membre qui travaille dessus : Belharrat Mohamed

Que fait le code ? 
Ecran de recherche intermediaire


Changement par rapport à la version précédente : Résolution des bugs concernant le bouton retour
-----------------------------
'''

from ArtworksIntermediate import ArtworksIntermediate
from SearchBox import SearchBox 
from function_python.final import get_resource_path, parcours_categories,rechercher_oeuvres_return, rechercher_ids_oeuvres_from_searchbox
from PyQt5 import QtWidgets, QtCore, QtGui


class IntermediateSearchScreen(QtWidgets.QWidget):

    tracker = []
    def __init__(self,conn, data: list[str],parentWidget=None):
        if (data[0] == -1):
            self.tracker.pop()
            data = self.tracker.pop()
        """
        Ecran de recherche intermediaire
        Args:
            data (list[str]): Données de le recherche [barre de recherche , catégorie selectionée , type]
        """
        self.conn = conn
        super().__init__()
        self.parentWidget = parentWidget
        self.setWindowTitle("Intermediate")
        self.setMinimumSize(QtCore.QSize(900, 500))

        self.tabResult = rechercher_ids_oeuvres_from_searchbox(data) # Result of the research, it contains ids of artworks

        self.tracker.append(data)      # Save the search information

        # Principal Layout
        self.mainLayout = QtWidgets.QVBoxLayout(self)

        # ScrollArea
        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.mainLayout.addWidget(self.scrollArea)

        # ScrollArea Contens
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.contentLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        # Create the label for the title (same as homeScreen)
        self.title = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.title.setObjectName("title")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(3)   # Set horizontal resizing ratio
        sizePolicy.setVerticalStretch(0)
        self.title.setSizePolicy(sizePolicy)
        self.title.setMinimumSize(QtCore.QSize(0, 100)) # Set minimum title size
        self.title.setMaximumSize(QtCore.QSize(500, 100)) 
        self.title.setAlignment(QtCore.Qt.AlignCenter)  # Center alignment
        self.title.setText("CULTURAMA")
        self.title.setCursor(QtCore.Qt.PointingHandCursor)               # Change hover
        self.title.mousePressEvent = lambda event : self.goHomeScreen()  # Reload homeScreen when title is pressed

        self.contentLayout.addWidget(self.title,1,0,1,1, alignment=QtCore.Qt.AlignHCenter)

        # Create retour Button
        self.retour = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.retour.setObjectName("retour")
        self.retour.setMinimumSize(QtCore.QSize(100, 50))
        self.retour.setMaximumSize(QtCore.QSize(100, 50))
        self.retour.setCursor(QtCore.Qt.PointingHandCursor)
        self.retour.clicked.connect(self.goBack)        # When retour is pressed execute goBack
        icon = QtGui.QIcon()
        icon_path = get_resource_path("images/retour-icon.png")
        icon.addPixmap(QtGui.QPixmap(icon_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)  # Add icon
        self.retour.setIconSize(QtCore.QSize(100, 50))
        self.retour.setIcon(icon)

        self.contentLayout.addWidget(self.retour,0,0,1,1)

        # Add SearchBox
        self.searchBox = SearchBox(self.scrollAreaWidgetContents,categories=[data[1]]+parcours_categories(conn, start_category=data[1]))      
        self.searchBox.searchBar.clear()
        self.searchBox.searchBar.setPlaceholderText(data[0])
        self.searchBox.searchSubmitted.connect(self.changeIntermediateScreen) # Waiting for the signal to change the window

        self.contentLayout.addWidget(self.searchBox,2,0,1,1)

        # Create the scrollArea for artworks
        self.scrollAreaResult = QtWidgets.QScrollArea()
        self.scrollAreaResult.setWidgetResizable(True)

        self.scrollAreaResultWidgetContents = QtWidgets.QWidget()
        self.scrollAreaResult.setWidget(self.scrollAreaResultWidgetContents)

        self.contentLayoutResult = QtWidgets.QGridLayout(self.scrollAreaResultWidgetContents)

        # Add artworks
        i = 0
        for id in self.tabResult :
            artwork = ArtworksIntermediate(id, self.conn, parent=self)
            self.contentLayoutResult.addWidget(artwork,i,0,1,1)
            i += 1

        self.contentLayout.addWidget(self.scrollAreaResult,3,0,1,1)



    def changeIntermediateScreen(self, dataSearch):
        """
        Ne cree pas de nouvel écran, ne fait que modifier l'écran actuel
        """
        # Save search info
        self.tracker.append(dataSearch)

        # Clear old layout
        self.clearLayout(self.contentLayoutResult)

        # clear old searchbox for the new one
        self.searchBox.deleteLater()
        self.searchBox = SearchBox(self.scrollAreaWidgetContents,categories=[dataSearch[1]]+parcours_categories(self.conn,start_category=dataSearch[1]))
        self.searchBox.searchBar.setPlaceholderText(dataSearch[0])
        self.searchBox.searchSubmitted.connect(self.changeIntermediateScreen)
        self.contentLayout.addWidget(self.searchBox, 2, 0, 1, 1)

        # New results
        self.tabResult = rechercher_ids_oeuvres_from_searchbox(dataSearch)

        # Change the new list of artworks
        i = 0
        for id in self.tabResult:
            artwork = ArtworksIntermediate(id, self.conn, parent=self)
            self.contentLayoutResult.addWidget(artwork, i, 0, 1, 1)
            i+=1

    def clearLayout(self,layout):
        """Clear the window (found on gitHub)"""
        while layout.count():
            item = layout.takeAt(0)  
            if item.widget():
                item.widget().deleteLater()  
            elif item.layout():
                self.clearLayout(item.layout())  

    def goBack(self):
        """Comeback on the last screen, will be use when the retour button is pressed"""
        self.close()    # Empty the window 
        if len(self.tracker)==1:    # If the last screen was homeScreen
            self.tracker.pop()
            self.parentWidget.changeToHomeScreen()  # Reload homeScreen
        else :      # If the last screen was another IntermediateSearchScreen
            self.tracker.pop()
            self.parentWidget.changeIntermediateScreen(self.tracker.pop())      # Reload the older IntermediateSearchScreen
        
    def goHomeScreen(self):
        """Comeback on the HomeScreen, will be use hen title is pressed"""
        self.tracker.clear() # Reset tracker
        self.parentWidget.changeToHomeScreen()  # Reload homeScreen


    def get_tracker(self):
        return self.tracker[-1]
        
