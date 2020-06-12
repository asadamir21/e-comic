from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from PIL import Image

import pandas as pd
import numpy as np

import os, sys, patoolib, glob, shutil, ntpath, io

class PicButton(QAbstractButton):
    def __init__(self, pixmap, parent=None):
        super(PicButton, self).__init__(parent)
        self.pixmap = pixmap

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)

    def sizeHint(self):
        return self.pixmap.size()

class Comic:
    def __init__(self):
        self.currentIndex = 0
        self.ComicImageList = []

    def setComicName(self, name):
        self.ComicName = name

    def addComicImage(self, ComicImage):
        self.ComicImageList.append(ComicImage)

    def Next(self):
        self.currentIndex += 1

    def Previous(self):
        self.currentIndex -= 1

    def setCurrentIndex(self, currentIndex):
        self.currentIndex = currentIndex

    def setMainLabel(self, Label):
        self.MainImageLabel = Label

    def setPreviousButton(self, Button):
        self.PreviousButton = Button

    def setNextButton(self, Button):
        self.NextButton = Button

    def setButtonList(self, ButtonList):
        self.ButtonList = ButtonList

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "e-comic version alpha de chez alpha"

        self.width = QDesktopWidget().screenGeometry(0).width()
        self.height = QDesktopWidget().screenGeometry(0).height()

        self.ComicList = []

        self.initWindows()

    # Initiate Windows
    def initWindows(self):
        self.setWindowIcon(QIcon('Images/Logo.png'))
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
        BibliothèqueButton.triggered.connect(self.Library)
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

        # WordAct = QAction(QIcon('Images/Word.png'), 'Word', self)
        # #WordAct.triggered.connect(lambda: self.ImportFileWindow("Word"))
        # self.toolbar.addAction(WordAct)


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

                dummyComic = Comic()
                dummyComic.setComicName(os.path.splitext(ntpath.basename(path[0]))[0])

                if len (next(os.walk('./Dummy/'))[1]) > 0:
                    # Converting Files to Pixmap
                    for ComicImageFileName in glob.glob("Dummy/" + next(os.walk('./Dummy/'))[1][0] + '/*.jpg'):
                        dummyComic.addComicImage(QPixmap(ComicImageFileName.replace(os.sep, '/')))
                else:
                    for ComicImageFileName in glob.glob('Dummy/*.jpg'):
                        dummyComic.addComicImage(QPixmap(ComicImageFileName.replace(os.sep, '/')))

                # Deleting Extracted Content
                if len(next(os.walk('./Dummy/'))[1]) > 0:
                    shutil.rmtree("Dummy/" + next(os.walk('./Dummy/'))[1][0])
                else:
                    for files in glob.glob('Dummy/*'):
                        os.remove(files)

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
                dummyComic.setButtonList(ButtonList)

                for Image in dummyComic.ComicImageList:
                    Button = PicButton(Image.scaled(LeftScrollArea.width(),
                                                    LeftScrollArea.height(),
                                                    Qt.KeepAspectRatio))

                    Button.adjustSize()
                    Button.clicked.connect(lambda: self.ButtonDoubleClick(dummyComic))

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

                # Main Image Label
                MainImageLabel = QLabel()
                MainImageLabel.resize(ComicTab.width()*0.75, ComicTab.height()*0.9)
                RightWidgetLayout.addWidget(MainImageLabel, 90)

                dummyComic.setMainLabel(MainImageLabel)

                # Setting QPixmap in Main Image Label
                MainImageLabel.setPixmap(dummyComic.ComicImageList[dummyComic.currentIndex].scaled(MainImageLabel.width(), MainImageLabel.height(), Qt.KeepAspectRatio))

                # Button Box Widget
                ButtonBox = QWidget()

                # Button Box Layout
                ButtonBoxLayout = QHBoxLayout(ButtonBox)
                ButtonBoxLayout.setAlignment(Qt.AlignVCenter)
                ButtonBoxLayout.setSpacing(50)

                if len(dummyComic.ComicImageList) > 1:
                    # Previous Button
                    PreviousButton = QPushButton("Previous Button")
                    PreviousButton.setDisabled(True)
                    ButtonBoxLayout.addWidget(PreviousButton)

                    # Next Button
                    NextButton = QPushButton("Next Button")
                    ButtonBoxLayout.addWidget(NextButton)

                    dummyComic.setPreviousButton(PreviousButton)
                    dummyComic.setNextButton(NextButton)

                    PreviousButton.clicked.connect(lambda: self.PreviousImage(dummyComic))
                    NextButton.clicked.connect(lambda: self.NextImage(dummyComic))

                self.ComicList.append(dummyComic)
                RightWidgetLayout.addWidget(ButtonBox, 10)

                # Adding ComicTab to TabWidget
                self.tabWidget.addTab(ComicTab, os.path.splitext(ntpath.basename(path[0]))[0])
                self.tabWidget.setCurrentWidget(ComicTab)

        except Exception as e:
            try:
                # Deleting Extracted Content
                if len(next(os.walk('./Dummy/'))[1]) > 0:
                    shutil.rmtree("Dummy/" + next(os.walk('./Dummy/'))[1][0])
                else:
                    for files in glob.glob('Dummy/*'):
                        os.remove(files)

                del dummyComic
            except:
                pass

            QMessageBox.critical(self,
                                 'File Opening Error',
                                 'There were some issue in opening the file',
                                 QMessageBox.Ok)

    # Previous Image Button
    def PreviousImage(self, dummyComic):
        if dummyComic.currentIndex == 1:
            dummyComic.PreviousButton.setDisabled(True)

        dummyComic.Previous()

        if dummyComic.currentIndex == len(dummyComic.ComicImageList) - 2:
            dummyComic.NextButton.setDisabled(False)

        dummyComic.MainImageLabel.setPixmap(dummyComic.ComicImageList[dummyComic.currentIndex].scaled(dummyComic.MainImageLabel.width(), dummyComic.MainImageLabel.height(), Qt.KeepAspectRatio))

    # Next Image Button
    def NextImage(self, dummyComic):
        if dummyComic.currentIndex == 0:
            dummyComic.PreviousButton.setDisabled(False)

        dummyComic.Next()

        if dummyComic.currentIndex == len(dummyComic.ComicImageList)-1:
            dummyComic.NextButton.setDisabled(True)

        dummyComic.MainImageLabel.setPixmap(dummyComic.ComicImageList[dummyComic.currentIndex].scaled(dummyComic.MainImageLabel.width(), dummyComic.MainImageLabel.height(), Qt.KeepAspectRatio))

    # Button Double Click
    def ButtonDoubleClick(self, dummyComic):
        Button = self.sender()
        dummyComic.setCurrentIndex(dummyComic.ButtonList.index(Button))

        if dummyComic.currentIndex == 0:
            dummyComic.PreviousButton.setDisabled(True)

        elif dummyComic.currentIndex == len(dummyComic.ComicImageList)-1:
            dummyComic.NextButton.setDisabled(True)

        else:
            dummyComic.PreviousButton.setDisabled(False)
            dummyComic.NextButton.setDisabled(False)


        dummyComic.MainImageLabel.setPixmap(dummyComic.ComicImageList[dummyComic.currentIndex].scaled(dummyComic.MainImageLabel.width(), dummyComic.MainImageLabel.height(),Qt.KeepAspectRatio))

    # Library
    def Library(self):
        LibraryTabFlag = False

        for tabindex in range(self.tabWidget.count()):
            if self.tabWidget.tabText(tabindex) == 'Bibliothèque':
                LibraryTabFlag = True
                break

        # Library Tab
        LibraryTab = QWidget()
        LibraryTab.setGeometry(QRect(0, 0,
                                     self.tabWidget.width(),
                                     self.tabWidget.height()))

        # Box Layout for Library Tab
        LibraryTabLayout = QHBoxLayout(LibraryTab)
        LibraryTabLayout.setContentsMargins(0, 0, 0, 0)

        # Table for Word Frequency
        LibraryTable = QTableWidget()
        LibraryTable.setColumnCount(8)
        LibraryTable.setGeometry(0, 0,
                                 LibraryTab.width(),
                                 LibraryTab.height())
        LibraryTabLayout.addWidget(LibraryTable)

        LibraryTable.setWindowFlags(LibraryTable.windowFlags() | Qt.MSWindowsFixedSizeDialogHint)

        LibraryTable.setHorizontalHeaderLabels(["Cover", "Title", "Author", "Year", "Tags", "Quality/5", "Edit", "Delete"])
        LibraryTable.horizontalHeader().setStyleSheet("::section {""background-color: grey;  color: white;}")


        for i in range(LibraryTable.columnCount()):
            LibraryTable.horizontalHeaderItem(i).setFont(QFont("Ariel Black", 12))
            LibraryTable.horizontalHeaderItem(i).setFont(QFont(LibraryTable.horizontalHeaderItem(i).text(), weight=QFont.Bold))

        if os.path.exists('Library.pkl'):
            df = pd.read_pickle("Library.pkl")

            for i in range(len(df.index)):
                LibraryTable.insertRow(i)

                for j in range(len(df.columns)):
                    newitem = df.iloc[i, j]

                    # For Cover Picture
                    if j == 0:
                        intItem = QTableWidgetItem()
                        intItem.setData(Qt.DecorationRole, Image.open(io.BytesIO(newitem)).toqpixmap())

                        LibraryTable.setItem(i, j, intItem)
                        LibraryTable.item(i, j).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
                        LibraryTable.item(i, j).setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)

                    else:
                        if isinstance(newitem, (int, np.integer)):
                            newitem = int(newitem)
                        elif isinstance(newitem, (float, np.float)):
                            newitem = float(newitem)

                        intItem = QTableWidgetItem()
                        intItem.setData(Qt.EditRole, QVariant(newitem))
                        LibraryTable.setItem(i, j, intItem)
                        LibraryTable.item(i, j).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
                        LibraryTable.item(i, j).setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)

                EditButton = QPushButton("Edit")
                EditButton.clicked.connect(lambda: self.EditRowDialog(df, LibraryTable))
                LibraryTable.setCellWidget(i, 6, EditButton)

                DeleteButton = QPushButton("Delete")
                DeleteButton.clicked.connect(lambda: self.DeleteRow(df, LibraryTable))
                LibraryTable.setCellWidget(i, 7, DeleteButton)

        LibraryTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        LibraryTable.resizeColumnsToContents()
        LibraryTable.resizeRowsToContents()

        LibraryTable.setSortingEnabled(True)
        LibraryTable.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        for i in range(LibraryTable.columnCount()):
            LibraryTable.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)

        if not LibraryTabFlag:
            self.tabWidget.addTab(LibraryTab, 'Bibliothèque')
            self.tabWidget.setCurrentWidget(LibraryTab)
        else:
            self.tabWidget.removeTab(tabindex)
            self.tabWidget.addTab(LibraryTab, 'Bibliothèque')
            self.tabWidget.setCurrentWidget(LibraryTab)

    # Edit Row
    def EditRowDialog(self, df, Table):
        button = self.sender()
        if button:
            row = Table.indexAt(button.pos()).row()

        EditRowDialogBox = QDialog()
        EditRowDialogBox.setModal(True)
        EditRowDialogBox.setWindowTitle("Editer Mètadonnèes")
        EditRowDialogBox.setParent(self)
        EditRowDialogBox.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint)
        EditRowDialogBox.setFixedWidth(self.width/4)

        EditRowDailogLayout = QVBoxLayout(EditRowDialogBox)
        EditRowDailogLayout.setContentsMargins(50, 50, 50, 50)

        # ****************** Title ********************

        # Title Label
        TitleLabel = QLabel()
        TitleLabel.setText("Titre:")
        TitleLabel.setAlignment(Qt.AlignVCenter)

        EditRowDailogLayout.addWidget(TitleLabel)

        # Title LineEdit
        TitleLineEdit = QLineEdit()
        TitleLineEdit.setText(Table.item(row, 1).text())
        TitleLineEdit.setAlignment(Qt.AlignVCenter)

        EditRowDailogLayout.addWidget(TitleLineEdit)

        # ****************** Author ********************

        # Author Label
        AuthorLabel = QLabel()
        AuthorLabel.setText("Author:")
        AuthorLabel.setAlignment(Qt.AlignVCenter)

        EditRowDailogLayout.addWidget(AuthorLabel)

        # Author LineEdit
        AuthorLineEdit = QLineEdit()
        AuthorLineEdit.setText(Table.item(row, 2).text())
        AuthorLineEdit.setAlignment(Qt.AlignVCenter)

        EditRowDailogLayout.addWidget(AuthorLineEdit)

        # ****************** Year ********************

        # Year Label
        YearLabel = QLabel()
        YearLabel.setText("Year:")
        YearLabel.setAlignment(Qt.AlignVCenter)

        EditRowDailogLayout.addWidget(YearLabel)

        # Year LineEdit
        YearLineEdit = QLineEdit()
        YearLineEdit.setValidator(QIntValidator(1000, 1000, self))
        YearLineEdit.setText(Table.item(row, 3).text())
        YearLineEdit.setAlignment(Qt.AlignVCenter)

        EditRowDailogLayout.addWidget(YearLineEdit)

        # ****************** Tag ********************

        # Tag Label
        TagLabel = QLabel()
        TagLabel.setText("Tags:")
        TagLabel.setAlignment(Qt.AlignVCenter)

        EditRowDailogLayout.addWidget(TagLabel)

        # Tag LineEdit
        TagTextEdit = QTextEdit()
        TagTextEdit.setText(Table.item(row, 4).text())
        TagTextEdit.setAlignment(Qt.AlignVCenter)

        EditRowDailogLayout.addWidget(TagTextEdit)

        # ****************** Quality ********************

        # Quality Label
        QualityLabel = QLabel()
        QualityLabel.setText("Quality:")
        QualityLabel.setAlignment(Qt.AlignVCenter)

        EditRowDailogLayout.addWidget(QualityLabel)

        # Quality LineEdit
        QualityDoubleSpinBox = QDoubleSpinBox()
        QualityDoubleSpinBox.setDecimals(0)
        QualityDoubleSpinBox.setMinimum(1)
        QualityDoubleSpinBox.setMaximum(5)
        QualityDoubleSpinBox.setValue(int(Table.item(row, 5).text()))
        QualityDoubleSpinBox.setAlignment(Qt.AlignVCenter)

        EditRowDailogLayout.addWidget(QualityDoubleSpinBox)

        # Edit Row Button Box
        EditRowbuttonBox = QDialogButtonBox()
        EditRowbuttonBox.setStandardButtons(QDialogButtonBox.Ok)
        EditRowbuttonBox.button(QDialogButtonBox.Ok).setText('Enregistrer')

        EditRowDailogLayout.addWidget(EditRowbuttonBox)

        EditRowbuttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

        TitleLineEdit.textChanged.connect(lambda: self.CurrentTextChanged(TitleLineEdit, AuthorLineEdit, YearLineEdit, TagTextEdit, EditRowbuttonBox))
        AuthorLineEdit.textChanged.connect(lambda: self.CurrentTextChanged(TitleLineEdit, AuthorLineEdit, YearLineEdit, TagTextEdit, EditRowbuttonBox))
        YearLineEdit.textChanged.connect(lambda: self.CurrentTextChanged(TitleLineEdit, AuthorLineEdit, YearLineEdit, TagTextEdit, EditRowbuttonBox))
        TagTextEdit.textChanged.connect(lambda: self.CurrentTextChanged(TitleLineEdit, AuthorLineEdit, YearLineEdit, TagTextEdit, EditRowbuttonBox))
        QualityDoubleSpinBox.valueChanged.connect(lambda: self.CurrentTextChanged(TitleLineEdit, AuthorLineEdit, YearLineEdit, TagTextEdit, EditRowbuttonBox))

        EditRowbuttonBox.accepted.connect(EditRowDialogBox.accept)
        EditRowbuttonBox.rejected.connect(EditRowDialogBox.reject)

        EditRowbuttonBox.accepted.connect(lambda: self.EditRow(TitleLineEdit.text(),
                                                               AuthorLineEdit.text(),
                                                               YearLineEdit.text(),
                                                               TagTextEdit.toPlainText(),
                                                               QualityDoubleSpinBox.value(),
                                                               row,
                                                               df,
                                                               Table))

        EditRowDialogBox.exec_()

    # Enable/Disable Button on Text Change
    def CurrentTextChanged(self, TitleLineEdit, AuthorLineEdit, YearLineEdit, TagTextEdit, EditRowbuttonBox):
        if len(TitleLineEdit.text()) == 0 or len(AuthorLineEdit.text()) == 0 or len(YearLineEdit.text()) == 0 or len(TagTextEdit.toPlainText()) == 0:
            EditRowbuttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        else:
            EditRowbuttonBox.button(QDialogButtonBox.Ok).setEnabled(True)

    # Edit Row
    def EditRow(self, Title, Author, Year, Tag, Quality, row, df, Table):
        df.iloc[row, 1] = Title
        df.iloc[row, 2] = Author
        df.iloc[row, 3] = int(Year)
        df.iloc[row, 4] = Tag
        df.iloc[row, 5] = int(Quality)

        df.to_pickle("Library.pkl")
        self.Library()

    # Delete Row
    def DeleteRow(self, df, Table):
        Deletechoice = QMessageBox.question(self, 'Delete',
                                            'Are you Sure you want to delete this entry?',
                                            QMessageBox.Yes | QMessageBox.No)

        if Deletechoice == QMessageBox.Yes:
            button = self.sender()
            if button:
                df = df[df.Title != Table.item(Table.indexAt(button.pos()).row(), 1).text()]
                df.to_pickle("Library.pkl")
                self.Library()
        else:
            pass

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

    ComicMainWindow = Window()
    ComicMainWindow.show()

    sys.exit(App.exec())