from PyQt5 import QtWidgets, QtCore
from Game import Game
from mainwindow import Ui_MainWindow  
from PyQt5.QtGui import QPixmap, QIcon
import sys
import GameController
import additionController
import datetime
import functionalController

class Window(QtWidgets.QMainWindow):

    def __init__(self):
        
        self.table_id_relation = []
        self.developers_box = {}
        self.publisher_box = {}
        self.reverse_developer_box = {}
        self.reverse_publisher_box = {}
        self.user_id = 0

        super(Window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.widget.setVisible(False)
        self.ui.widget_2.setVisible(False)
        self.ui.library.setVisible(False)

        #настройка таблицы магазина
        self.ui.shopTable.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.ui.shopTable.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.ui.shopTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        # self.ui.shopTable.insertRow(0)
        self.fillDevelopers()
        self.fillPublishers()
        self.fillShop()
        # print(self.table_id_relation)

        #коннекторы
        self.ui.shopTable.selectionModel().selectionChanged.connect(self.viewGame)
        self.ui.editButton.clicked.connect(self.updateGame)
        self.ui.findButton.clicked.connect(self.findByName)

    def viewGame(self, selected, deselected):

            self.ui.widget.setVisible(True)
            
            rows = selected.indexes()
            index = rows[0].row()

            game_id = self.table_id_relation[index][0]

            game, tag = GameController.getById(game_id)

            game_id = game.id
            name = game.name
            release_date = game.release_date
            price = game.price
            publisher = game.publisher_id
            developer = game.developer_id
            description = game.description

            self.ui.nameEdit.setText(name)
            self.ui.release_dateEdit.setDate(QtCore.QDate(release_date))
            self.ui.spinBox.setValue(price)
            self.ui.descriptionEdit.setText(description)
            self.ui.developerBox.setCurrentIndex(self.reverse_developer_box[developer])
            self.ui.publisherBox.setCurrentIndex(self.reverse_publisher_box[publisher])

            estimation = functionalController.getEstimation(game_id)
            if (estimation == None):
                estimation = 'Данные отсутсвуют'

            estimationStr = 'Средняя оценка: {}'.format(estimation)
            self.ui.scoreLabel.setText(estimationStr)
            
    def fillShop(self):

        games, tags = GameController.getAll()

        for i in range(len(games)):
            self.ui.shopTable.insertRow(self.ui.shopTable.rowCount())
            index = self.ui.shopTable.rowCount() - 1   
            self.fillTableRow(games[i], tags[i], index)

    def fillDevelopers(self):

        id, developers = additionController.getAllDevelopers()

        for i in range(len(developers)):
            index = self.ui.developerBox.count() - 1
            self.ui.developerBox.insertItem(index, developers[i])
            self.developers_box[index] = id[i]
            self.reverse_developer_box[id[i]] = index
            print(self.reverse_developer_box[id[i]])

    def fillPublishers(self):

        id, publishers = additionController.getAllPublishers()

        for i in range(len(publishers)):
            index = self.ui.publisherBox.count() - 1
            self.ui.publisherBox.insertItem(index, publishers[i])
            self.publisher_box[index] = id[i]
            self.reverse_publisher_box[id[i]] = index

    def fillTableRow(self, game, tag, index):
        
        # self.ui.shopTable.insertRow(self.ui.shopTable.rowCount())   
        game_id = game.id
        name = game.name
        release_date = game.release_date
        price = game.price
        # print(self.reverse_publisher_box)
        publisher = self.ui.publisherBox.itemText(self.reverse_publisher_box[game.publisher_id])
        developer = self.ui.developerBox.itemText(self.reverse_developer_box[game.developer_id])

        # print(publisher)
        
        #заполнение таблицы
        self.ui.shopTable.setItem(index, 0, QtWidgets.QTableWidgetItem(name))
        self.ui.shopTable.setItem(index, 1, QtWidgets.QTableWidgetItem(str(release_date)))
        self.ui.shopTable.setItem(index, 2, QtWidgets.QTableWidgetItem(str(price)))
        self.ui.shopTable.setItem(index, 3, QtWidgets.QTableWidgetItem(developer))
        self.ui.shopTable.setItem(index, 4, QtWidgets.QTableWidgetItem(publisher))
        self.ui.shopTable.setItem(index, 5, QtWidgets.QTableWidgetItem(tag))

        self.table_id_relation.append([game_id, game.developer_id, game.publisher_id])

    def updateGame(self):
        
        row = self.ui.shopTable.currentRow()
        id = self.table_id_relation[row][0]

        tag = self.ui.shopTable.item(row, 5)

        name = self.ui.nameEdit.text()
        release_date =self.ui.release_dateEdit.date().toPyDate()
        price = self.ui.spinBox.value()
        description = self.ui.descriptionEdit.toPlainText()

        publisher_id = self.publisher_box[self.ui.publisherBox.currentIndex()]
        developer_id = self.developers_box[self.ui.developerBox.currentIndex()]
        
        game = Game(id, name, release_date, price, description, developer_id, publisher_id)

        GameController.update(game)

        self.fillTableRow(game, tag, row)

    def findByName(self):

        str = self.ui.findEdit.text()
        
        if(str==''):
            self.ui.shopTable.setRowCount(0)
            self.fillShop()
        
        else:
            self.ui.shopTable.setRowCount(0)
            game, tag = GameController.getByName(str)

            if (game != None):
                index = self.ui.shopTable.rowCount()
                self.ui.shopTable.insertRow(index)
                self.fillTableRow(game,tag,index)

    def findByPublisher(self):
        pass

    def findByDeveloper(self):
        pass
                

app = QtWidgets.QApplication([])
application = Window()
application.setWindowIcon(QIcon("./image/icon.jpg"))
application.show()
 
sys.exit(app.exec())