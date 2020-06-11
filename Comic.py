from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import os, sys, patoolib, glob, shutil, ntpath

class PicButton(QAbstractButton):
    def __init__(self, pixmap, parent=None):
        super(PicButton, self).__init__(parent)
        self.pixmap = pixmap

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)

    def sizeHint(self):
        return self.pixmap.size()

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "e-comic version alpha de chez alpha"

        self.width = QDesktopWidget().screenGeometry(0).width()
        self.height = QDesktopWidget().screenGeometry(0).height()

        self.initWindows()

    # Initiate Windows
    def initWindows(self):
        #self.setWindowIcon(QIcon(WindowTitleLogo))
        self.setWindowTitle(self.title)
        self.setGeometry(self.width/4, self.height*0.1, self.width/2, self.height*0.8)
        self.setFixedHeight(self.height*0.8)
        self.setFixedWidth(self.width/ 2)

        # ***********************************************************************************
        # *****************************  Menu Item ******************************************
        # ***********************************************************************************

        mainMenu = self.menuBar()
        FichierMenu = mainMenu.addMenu('Fichier')
        EditionMenu = mainMenu.addMenu('Edition')
        AffichageMenu = mainMenu.addMenu('Affichage')
        LireMenu = mainMenu.addMenu('Lire')
        AideMenu = mainMenu.addMenu('Aide')

        # *****************************  FichierMenuItem ***************************************

        # Ouvrir Button
        ouvrirButton = QAction(QIcon("Images/Ouvrir.png"), 'Ouvror...', self)
        ouvrirButton.setShortcut('Ctrl+O')
        ouvrirButton.setStatusTip('Ouvrir')
        ouvrirButton.triggered.connect(self.ouvrir)
        FichierMenu.addAction(ouvrirButton)

        # Imprimer Button
        ImprimerButton = QAction(QIcon("Images/Imprimer.png"), 'Imprimer...', self)
        ImprimerButton.setShortcut('Ctrl+P')
        ImprimerButton.setStatusTip('Imprimer...')
        #ImprimerButton.triggered.connect(self.OpenFileWindow)
        FichierMenu.addAction(ImprimerButton)

        # Bibliothèque Button
        BibliothèqueButton = QAction(QIcon("Images/Bibliothèque.png"), 'Bibliothèque', self)
        BibliothèqueButton.setShortcut('Ctrl+L')
        BibliothèqueButton.setStatusTip('Bibliothèque')
        #BibliothèqueButton.triggered.connect(self.SaveWindow)
        FichierMenu.addAction(BibliothèqueButton)

        # Quitter Button
        QuitterButton = QAction(QIcon("Images/Quitter.png"), 'Quitter', self)
        QuitterButton.setShortcut('Ctrl+Q')
        QuitterButton.setStatusTip('Quitter')
        QuitterButton.triggered.connect(self.close)
        FichierMenu.addAction(QuitterButton)

        # *****************************  AideMenu ***************************************
        # Help Button
        HelpButton = QAction('Help', self)
        HelpButton.setStatusTip('Help')
        HelpButton.triggered.connect(self.AboutWindow)
        AideMenu.addAction(HelpButton)

        # ***********************************************************************************
        # *******************************  ToolBar ******************************************
        # ***********************************************************************************

        self.toolbar = self.addToolBar("Show Toolbar")
        self.toolbar.setToolButtonStyle(Qt.ToolButtonIconOnly | Qt.AlignLeading)  # <= Toolbuttonstyle
        self.toolbar.setMovable(False)

        WordAct = QAction(QIcon('Images/Word.png'), 'Word', self)
        #WordAct.triggered.connect(lambda: self.ImportFileWindow("Word"))
        self.toolbar.addAction(WordAct)

        WordAct2 = QAction(QIcon('Word.png'), 'Word', self)
        # WordAct.triggered.connect(lambda: self.ImportFileWindow("Word"))
        self.toolbar.addAction(WordAct2)

        self.toolbar.addSeparator()
        self.toolbar.setContextMenuPolicy(Qt.PreventContextMenu)

        # ***********************************************************************************
        # *******************************  ToolBar ******************************************
        # ***********************************************************************************

        self.tabWidget = QTabWidget()
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.setElideMode(Qt.ElideRight)
        self.tabWidget.tabBar().setExpanding(True)
        self.tabWidget.setUsesScrollButtons(True)
        self.tabWidget.tabCloseRequested.connect(self.tabCloseHandler)

        self.setCentralWidget(self.tabWidget)

    # Tab Close Handler
    def tabCloseHandler(self, index):
        self.tabWidget.removeTab(index)

    # Open File
    def ouvrir(self):
        try:
            path = QFileDialog.getOpenFileName(self, 'Open Comic File', "", 'Comic File(*.cbz *.cbr)')

            if all(path):
                # Extracting Files
                patoolib.extract_archive(path[0], outdir="Dummy/")

                ComicImageList = []

                # Converting Files to Pixmap
                for ComicImageFileName in glob.glob("Dummy/" + next(os.walk('./Dummy/'))[1][0] + '/*.jpg'):
                    ComicImageList.append(QPixmap(ComicImageFileName.replace(os.sep, '/')))

                # Deleting Extracted Content
                shutil.rmtree("Dummy/" + next(os.walk('./Dummy/'))[1][0])

                # ********************************** Tab *******************************

                # Comic Tab
                ComicTab = QWidget()
                ComicTab.setGeometry(QRect(0, 0, self.tabWidget.width(), self.tabWidget.height()))

                # Horizontal Box Layout for Comic Tab
                HorizontalBoxLayoutComicTab = QHBoxLayout(ComicTab)
                HorizontalBoxLayoutComicTab.setContentsMargins(0, 0, 0, 0)

                # ********************** Left Side Bar **********************

                # Left Widget
                LeftWidget = QWidget()
                LeftWidget.setFixedWidth(ComicTab.width()/4)

                # Left Side Scroll Area
                LeftScrollArea = QScrollArea()
                LeftScrollArea.setWidget(LeftWidget);
                LeftScrollArea.setWidgetResizable(True);
                HorizontalBoxLayoutComicTab.addWidget(LeftScrollArea, 25);

                # Images Vertical Layout
                ImagesLeftBarLayout = QVBoxLayout(LeftWidget)
                ImagesLeftBarLayout.setContentsMargins(LeftScrollArea.width()*0.15,
                                                       LeftScrollArea.height()*0.05,
                                                       LeftScrollArea.width()*0.15,
                                                       LeftScrollArea.height()*0.05)
                ImagesLeftBarLayout.setAlignment(Qt.AlignHCenter)
                ImagesLeftBarLayout.addSpacing(50)

                ButtonList = []

                for Image in ComicImageList:
                    Button = PicButton(Image.scaled(LeftScrollArea.width(),
                                                    LeftScrollArea.height(),
                                                    Qt.KeepAspectRatio))
                    # Button.setStyleSheet(
                    #     """
                    #         border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #86beda, stop: 1 #d4e8f2);
                    #     """
                    # )
                    Button.adjustSize()
                    Button.clicked.connect(lambda e: self.ButtonDoubleClick(e, ButtonList, ComicImageList))

                    ButtonList.append(Button)
                    ImagesLeftBarLayout.addWidget(Button)

                # ********************** Right Side Bar **********************

                # Right Widget
                RightWidget = QWidget()
                RightWidget.setFixedWidth(ComicTab.width()*0.75)
                RightWidget.setFixedHeight(ComicTab.height())
                HorizontalBoxLayoutComicTab.addWidget(RightWidget, 75)

                # Right Widget Layout
                RightWidgetLayout = QVBoxLayout(RightWidget)
                RightWidgetLayout.setContentsMargins(0, RightWidget.height()*0.05, 0, RightWidget.height()*0.05)
                RightWidgetLayout.setAlignment(Qt.AlignHCenter)

                self.CurrentImageIndex = 0

                # Main Image Label
                self.MainImageLabel = QLabel()
                self.MainImageLabel.resize(ComicTab.width()*0.75, ComicTab.height()*0.9)
                RightWidgetLayout.addWidget(self.MainImageLabel, 90)

                # Setting QPixmap in Main Image Label
                self.MainImageLabel.setPixmap(ComicImageList[self.CurrentImageIndex].scaled(self.MainImageLabel.width(), self.MainImageLabel.height(), Qt.KeepAspectRatio))

                # Button Box Widget
                ButtonBox = QWidget()

                # Button Box Layout
                ButtonBoxLayout = QHBoxLayout(ButtonBox)
                ButtonBoxLayout.setAlignment(Qt.AlignVCenter)
                ButtonBoxLayout.setSpacing(50)

                if len(ComicImageList) > 1:
                    # Previous Button
                    self.PreviousButton = QPushButton("Previous Button")
                    self.PreviousButton.setDisabled(True)
                    ButtonBoxLayout.addWidget(self.PreviousButton)

                    # Next Button
                    self.NextButton = QPushButton("Next Button")
                    ButtonBoxLayout.addWidget(self.NextButton)

                    self.PreviousButton.clicked.connect(lambda: self.PreviousImage(ComicImageList))
                    self.NextButton.clicked.connect(lambda: self.NextImage(ComicImageList))

                RightWidgetLayout.addWidget(ButtonBox, 10)

                # Adding ComicTab to TabWidget
                self.tabWidget.addTab(ComicTab, os.path.splitext(ntpath.basename(path[0]))[0])
                self.tabWidget.setCurrentWidget(ComicTab)

        except Exception as e:
            print(str(e))

    # Previous Image Button
    def PreviousImage(self, ComicImageList):
        if self.CurrentImageIndex == 1:
            self.PreviousButton.setDisabled(True)

        self.CurrentImageIndex -= 1

        if self.CurrentImageIndex == len(ComicImageList) - 2:
            self.NextButton.setDisabled(False)

        self.MainImageLabel.setPixmap(ComicImageList[self.CurrentImageIndex].scaled(self.MainImageLabel.width(), self.MainImageLabel.height(), Qt.KeepAspectRatio))

    # Next Image Button
    def NextImage(self, ComicImageList, ):

        if self.CurrentImageIndex == 0:
            self.PreviousButton.setDisabled(False)

        self.CurrentImageIndex += 1

        if self.CurrentImageIndex == len(ComicImageList)-1:
            self.NextButton.setDisabled(True)

        self.MainImageLabel.setPixmap(ComicImageList[self.CurrentImageIndex].scaled(self.MainImageLabel.width(), self.MainImageLabel.height(), Qt.KeepAspectRatio))

    # Button Double Click
    def ButtonDoubleClick(self, ButtonItemName, ButtonList, ComicImageList):
        try:
            Button = self.sender()
            CurrentButtonIndex = ButtonList.index(Button)


            if CurrentButtonIndex == 0:
                self.PreviousButton.setDisabled(True)

            elif CurrentButtonIndex == len(ComicImageList)-1:
                self.NextButton.setDisabled(True)

            else:
                self.PreviousButton.setDisabled(False)
                self.NextButton.setDisabled(False)

            self.CurrentImageIndex = CurrentButtonIndex

            self.MainImageLabel.setPixmap(ComicImageList[self.CurrentImageIndex].scaled(self.MainImageLabel.width(), self.MainImageLabel.height(),Qt.KeepAspectRatio))

        except Exception as e:
            print(str(e))

    # Close Application / Exit
    def closeEvent(self, event):
        ExitWindowChoice = QMessageBox.question(self, 'Exit',
                                                             "Are you sure you want to exit?",
                                                             QMessageBox.Yes | QMessageBox.No)
        if ExitWindowChoice == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    # About Window
    def AboutWindow(self):
        QMessageBox.about(self, "About e-comic version alpha",
                          "Cette Application est une maquette qui sert de preuve de concept à la réalisation d'un projet de fin d'année pour les jeunes pousses de I'ESME Sudria.\nElle utilise des QLabel et des QScrollAreapour afficher des images.Les QLabel servent normalementà afficher du texte mais on peut auss s'en servir pour dispatcher des images.\nLes étudiants devront se servir des ces fonctionnalitéspour créer un lecteur de bandes dessinnées numériques qui devramanipuler des archives aux formats spéciaux .cbr er.cbz")

if __name__ == "__main__":
    App = QApplication(sys.argv)

    TextWizMainwindow = Window()
    TextWizMainwindow.show()

    sys.exit(App.exec())