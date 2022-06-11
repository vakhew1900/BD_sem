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
        self.isAdmin = False

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

        self.fillDevelopers()
        self.fillPublishers()
        self.fillShop()
       

        #коннекторы
        self.ui.shopTable.selectionModel().selectionChanged.connect(self.viewGame)
        self.ui.editButton.clicked.connect(self.updateGame)
        self.ui.findButton.clicked.connect(self.findByName)
        self.ui.pushButton.clicked.connect(self.findByDeveloper)
        self.ui.pushButton_3.clicked.connect(self.findByPublisher)
        self.ui.addButton.clicked.connect(self.addGame)
        self.ui.deleteButton.clicked.connect(self.deleteGame)

        #коннекторы для экшена
        self.ui.turnOnAction.triggered.connect(self.turnOnAdmin)
        self.ui.turnOffAction.triggered.connect(self.turnOffAdmin)

    def viewGame(self, selected, deselected):

            self.ui.widget.setVisible(True)

            print('aslafsaghfg{}'.format(selected))

            print(self.ui.shopTable.rowCount())
            rows = selected.indexes()
            if (len(rows) < 1):
                return
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

        self.table_id_relation = []

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
        print('Вход')
        self.ui.shopTable.setRowCount(0)
        print('Выход')
        self.table_id_relation = []

        if(str==''):
            self.fillShop()
        
        else:
            games, tags = GameController.getByName(str)
            
            if (games == None):
                return

            for i in range(len(games)):
                index = self.ui.shopTable.rowCount()
                self.ui.shopTable.insertRow(index)
                self.fillTableRow(games[i],tags[i],index)
            
            self.ui.widget.setVisible(False)

    def findByPublisher(self):
        
        index = self.ui.shopTable.currentRow()
        publisher_id = self.table_id_relation[index][2]
        self.table_id_relation = []

        self.ui.shopTable.setRowCount(0)
        self.ui.widget.setVisible(False)
        games, tags = GameController.getByPublisher(publisher_id)
        
        if (games == None):
            return

        for i in range(len(games)):
            index = self.ui.shopTable.rowCount()
            self.ui.shopTable.insertRow(index)
            self.fillTableRow(games[i],tags[i],index)
        
        self.ui.widget.setVisible(False)

    def findByDeveloper(self):
        
        index = self.ui.shopTable.currentRow()
        developer_id = self.table_id_relation[index][1]
        self.table_id_relation = []
        
        self.ui.widget.setVisible(False)
        self.ui.shopTable.setRowCount(0)
        games, tags = GameController.getByDeveloper(developer_id)
        
        if (games == None):
            return

        for i in range(len(games)):
            index = self.ui.shopTable.rowCount()
            self.ui.shopTable.insertRow(index)
            self.fillTableRow(games[i],tags[i],index)
        
        self.ui.widget.setVisible(False)

    def turnOnAdmin(self):
        self.isAdmin = True

    def turnOffAdmin(self):
        self.isAdmin = False               

    def addGame(self):

        name = self.ui.nameEdit.text()
        release_date =self.ui.release_dateEdit.date().toPyDate()
        price = self.ui.spinBox.value()
        description = self.ui.descriptionEdit.toPlainText()

        publisher_id = self.publisher_box[self.ui.publisherBox.currentIndex()]
        developer_id = self.developers_box[self.ui.developerBox.currentIndex()]
        
        game = Game(1, name, release_date, price, description, developer_id, publisher_id)

        game = GameController.add(game)
        tag = 'Игра'

        row = self.ui.shopTable.rowCount()
        self.ui.shopTable.insertRow(row)

        self.fillTableRow(game, tag, row)
        
    def deleteGame(self):
        row = self.ui.shopTable.currentRow()
        id = self.table_id_relation[row][0]
        self.ui.shopTable.removeRow(row)
        print(row)
        print(self.table_id_relation)
        self.table_id_relation.pop(row)

        GameController.delete(id)


app = QtWidgets.QApplication([])
application = Window()
application.setWindowIcon(QIcon("./image/icon.jpg"))
application.show()
 
sys.exit(app.exec())