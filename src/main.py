import os
import sys
import json

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QLineEdit, QPushButton, \
    QRadioButton, QMessageBox, QHBoxLayout, QVBoxLayout, QLabel, QButtonGroup, \
    QTextEdit, QListView, QDialog
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt5.QtCore import pyqtSlot

from boolean_retrieval import query
from corpus_preprocessing import createCSV
from index import Index
from corpus_access import CorpusAccess


# setup some config files
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CORPUS_CSV = CURRENT_DIR + '/../course_corpus.csv'
INDEX = CURRENT_DIR + '/../INDEX'
COURSE_DICT = CURRENT_DIR + '/../courses.json'


# Inspired from https://pythonspot.com/gui/
# Modele 1 - User Interface
class MainWindow(QWidget):
    """
    This is the graphical user interface
    """

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # setup entire layout
        vbox = QVBoxLayout()
        self.setLayout(vbox)

        # default size
        self.resize(640, 480)

        # main window title
        self.setWindowTitle("Vanilla Search Engine")

        # main window icon
        self.setWindowIcon(QIcon(os.path.dirname(
            os.path.abspath(__file__)) + '/icons/vanilla.png'))

        # add query input field
        searchLayout = QHBoxLayout()
        searchLabel = QLabel("Query: ")
        searchLayout.addWidget(searchLabel)
        self.searchField = QLineEdit()
        # self.searchField.move(20, 20)
        # self.searchField.resize(200, 40)
        searchLayout.addWidget(self.searchField)
        vbox.addLayout(searchLayout)

        # add choice of model, Boolean, or VSM
        modelLabel = QLabel("Choice of model: \t\t")
        modelLayout = QHBoxLayout()
        modelGroup = QButtonGroup(self)
        self.modelChoiceButton1 = QRadioButton("Boolean")
        self.modelChoiceButton1.setChecked(True)
        self.modelChoiceButton2 = QRadioButton("VSM")
        self.modelChoiceButton2.setChecked(False)
        self.modelChoiceButton1.toggled.connect(
            lambda: self.changeChoiceState(self.modelChoiceButton1))
        self.modelChoiceButton2.toggled.connect(
            lambda: self.changeChoiceState(self.modelChoiceButton2))
        modelLayout.addWidget(modelLabel)
        modelLayout.addWidget(self.modelChoiceButton1)
        modelGroup.addButton(self.modelChoiceButton1)
        modelLayout.addWidget(self.modelChoiceButton2)
        modelGroup.addButton(self.modelChoiceButton2)
        modelLayout.addStretch(1)
        vbox.addLayout(modelLayout)

        # add choice of collection: UofO catalog, ..
        collectionLabel = QLabel("Choice of collection: \t")
        collectionLayout = QHBoxLayout()
        collectionButtonGroup = QButtonGroup(self)
        self.collectionChoiceButton1 = QRadioButton("UofO catalog")
        self.collectionChoiceButton1.setChecked(True)
        self.collectionChoiceButton1.toggled.connect(
            lambda: self.changeChoiceState(self.collectionChoiceButton1))
        collectionLayout.addWidget(collectionLabel)
        collectionLayout.addWidget(self.collectionChoiceButton1)
        collectionButtonGroup.addButton(self.collectionChoiceButton1)
        collectionLayout.addStretch(1)
        vbox.addLayout(collectionLayout)

        # TODO: the information needed for the spelling correction

        # add a search button
        searchButtonLayout = QHBoxLayout()
        self.searchButton = QPushButton('Search')
        self.searchButton.setToolTip('This is a search button')
        # self.searchButton.move(20, 400)
        self.searchButton.clicked.connect(self.click_search)
        searchButtonLayout.addStretch(1)
        searchButtonLayout.addWidget(self.searchButton)
        vbox.addLayout(searchButtonLayout)

        # add a qeury result listView
        self.doc_ids = []  # record the doc IDs
        queryResultLayout = QHBoxLayout()
        queryResultLabel = QLabel("Query result: \t")
        self.queryResult = QListView()
        self.queryResult.setAcceptDrops(False)
        self.queryResult.setDragDropMode(
            QtWidgets.QAbstractItemView.NoDragDrop)
        self.queryResult.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection)
        self.queryResult.setResizeMode(QListView.Fixed)
        self.queryResult.clicked.connect(self.selectItem)
        queryResultLayout.addWidget(queryResultLabel)
        queryResultLayout.addWidget(self.queryResult)
        # queryResultLayout.addStretch(1)
        vbox.addLayout(queryResultLayout)

        # setup corpus access
        self.courses = CorpusAccess(COURSE_DICT)

        # centerize main window
        self.center()

        self.show()

    # move the window to the center of screen
    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(
            QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    @pyqtSlot()
    def click_search(self):
        # TODO: debugging
        print("Search button clicked.")

        query_string = self.searchField.text().strip()

        # setup QMessageBox
        if query_string == "":
            buttonReplay = self.__create_message_box(
                "The query string cannot be blank")
        else:
            idxf2 = Index.load(INDEX)
            self.doc_ids = query(idxf2, query_string)
            if len(self.doc_ids) == 0:
                msg = self.__create_message_box("Could not find anything.")
            else:
                model = QStandardItemModel()
                for doc in self.doc_ids:
                    item = QStandardItem(doc)
                    model.appendRow(item)
                self.queryResult.setModel(model)
                self.queryResult.show()

    def changeChoiceState(self, button: QPushButton):
        if button.isChecked():
            if button.text() == 'Boolean':
                # TODO: debugging
                print("Radio button '%s' is clicked." % button.text())
            elif button.text() == 'VSM':
                # TODO: debugging
                print("Radio button '%s' is clicked." % button.text())
            elif button.text() == 'UofO catalog':
                # print("Radio button '%s' is clicked." % button.text())
                html_file = "UofO_Courses.html"
                if os.path.exists(CURRENT_DIR + "/../%s" % html_file):
                    setup(html_file=CURRENT_DIR + "/../%s" % html_file)
                else:
                    raise Exception("Could not find '%s'" % html_file)

    def selectItem(self):
        selectedId = self.queryResult.selectedIndexes()[0].row()
        print("id selected: %d" % selectedId)
        print("course: %s" % self.doc_ids[selectedId])
        print("course content: %s" %
              self.courses.get(self.doc_ids[selectedId]))
        self.__display_course_details(
            self.doc_ids[selectedId],
            self.courses.get(self.doc_ids[selectedId])
        )

    def __display_course_details(self, course_id, course_details):
        dialog = QDialog(parent=self)
        dialog.setWindowTitle("%s" % course_id)
        dialog.resize(320, 240)
        vbox = QVBoxLayout()

        hbox1 = QHBoxLayout()
        titelLabel = QLabel("Title: \t")
        title = QLineEdit()
        title.setText(course_details.get('title'))
        title.setReadOnly(True)
        hbox1.addWidget(titelLabel)
        hbox1.addWidget(title)

        hbox2 = QHBoxLayout()
        contentLabel = QLabel("Content: ")
        content = QTextEdit()
        content.setReadOnly(True)
        content.setText(course_details.get('content'))
        hbox2.addWidget(contentLabel)
        hbox2.addWidget(content)

        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)

        dialog.setLayout(vbox)
        dialog.exec_()

    def __create_message_box(self, message):
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Information)
        message_box.setText(message)
        message_box.setWindowTitle("Search result message")
        message_box.setStandardButtons(QMessageBox.Ok)
        message_box.exec_()


def setup(html_file=None, corpus_file=CORPUS_CSV, index_file=INDEX):
    # Preprocessing the html
    createCSV(src_file=html_file)

    # Create index
    idxf2 = Index(corpus=corpus_file)
    if os.path.exists(index_file):
        print("Detected %s exists, removeing ..." % index_file)
        os.remove(index_file)
    idxf2.save(index_file)


if __name__ == "__main__":
    # setup all necessary config files
    # TODO: temporarily disable for testing
    # setup()

    # run GUI
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())
