from email import message
from email.mime import application
from re import X
from tkinter import dialog
from PyQt5 import QtWidgets, QtCore
from numpy import diag
from Game import Game
from User import User
from mainwindow import Ui_MainWindow  
from PyQt5.QtGui import QPixmap, QIcon
import sys
import GameController
import additionController
import datetime
import functionalController
import enterDialog
import registerDialog
import UserController
import updateDialog

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
        self.ui.enterAction.triggered.connect(self.Login)
        self.ui.regiseterAction.triggered.connect(self.Register)
        self.ui.deleteAction.triggered.connect(self.deleteUser)
        self.ui.exitAction.triggered.connect(self.exitUser)
        self.ui.action.triggered.connect(self.updateUser)

        #фигня


        #выключаем дизайн
        self.ui.addButton.setVisible(False)
        self.ui.editButton.setVisible(False)
        self.ui.deleteButton.setVisible(False)

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
        flag = True
        self.isAdmin = flag

        #выключаем дизайн
        self.ui.addButton.setVisible(flag)
        self.ui.editButton.setVisible(flag)
        self.ui.deleteButton.setVisible(flag)

    def turnOffAdmin(self):

        flag = False
        self.isAdmin = flag

        #выключаем дизайн
        self.ui.addButton.setVisible(flag)
        self.ui.editButton.setVisible(flag)
        self.ui.deleteButton.setVisible(flag)


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

    def Login(self):
        
        dialog = EnterDialog(self)
        dialog.exec_()
        self.user_id = dialog.user_id
        print("user_id:")
        print(self.user_id)
        self.ui.libraryTable.setRowCount(0)

        if (self.user_id != 0):
            self.makeLibrary()

    def Register(self):
        dialog = RegisterDialog(self)
        dialog.exec_()
        self.user_id = dialog.user_id
        print("user_id:")
        print(self.user_id)
        self.ui.libraryTable.setRowCount(0)
    
    def exitUser(self):
        self.user_id = 0
        self.ui.libraryTable.setRowCount(0)

    def deleteUser(self):
        
        if (self.user_id == 0):
            return
        
        
        UserController.delete(self.user_id)

        messageBox = QtWidgets.QMessageBox(self)
        messageBox.setText('Пользователь удален')
        messageBox.exec()

        self.user_id = 0

    def updateUser(self):
        if (self.user_id == 0):
            return

        dialog = UpdateDialog(userId= self.user_id)

        dialog.exec_()

    def makeLibrary(self):

        games, tags = functionalController.getLibrary(self.user_id)

        for i in range(len(games)):
            self.ui.libraryTable.insertRow(self.ui.libraryTable.rowCount())
            index = self.ui.libraryTable.rowCount() - 1   
            print('index {}'.format(index))
            self.fillLibraryTableRow(games[i], tags[i], index)

    def fillLibraryTableRow(self,game,tag,index):
       
        game_id = game.id
        name = game.name
        release_date = game.release_date
        price = game.price
        
        publisher = self.ui.publisherBox.itemText(self.reverse_publisher_box[game.publisher_id])
        developer = self.ui.developerBox.itemText(self.reverse_developer_box[game.developer_id])

        print('{} {} {} {} {}'.format(name, release_date, price, publisher, developer))
        
        #заполнение таблицы
        self.ui.libraryTable.setItem(index, 0, QtWidgets.QTableWidgetItem(name))
        self.ui.libraryTable.setItem(index, 1, QtWidgets.QTableWidgetItem(str(release_date)))
        self.ui.libraryTable.setItem(index, 2, QtWidgets.QTableWidgetItem(str(price)))
        self.ui.libraryTable.setItem(index, 3, QtWidgets.QTableWidgetItem(developer))
        self.ui.libraryTable.setItem(index, 4, QtWidgets.QTableWidgetItem(publisher))
        self.ui.libraryTable.setItem(index, 5, QtWidgets.QTableWidgetItem(tag))

class EnterDialog(QtWidgets.QDialog):
    
    user_id = 0

    def __init__(self, parent = None):
        super(EnterDialog, self).__init__(parent)
        self.ui = enterDialog.Ui_Dialog()
        self.ui.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.ui.pushButton.clicked.connect(self.login)
  
    def login(self):
        
        login = self.ui.loginEdit.text()
        password = self.ui.passwordEdit.text()

        user = UserController.getByLogin(login)

        if (user == None or user.password != password):
            print('error')
            messageBox = QtWidgets.QMessageBox(self)
            messageBox.setWindowTitle('Неправильный логин или пароль')
            messageBox.setText('Неправильный логин или пароль. Попробуйте попытку снова')
            messageBox.exec()

        else:
            self.user_id = user.id
            self.close()


class RegisterDialog(QtWidgets.QDialog):
    
    user_id = 0

    def __init__(self, parent = None):
        super(RegisterDialog, self).__init__(parent)
        self.ui = registerDialog.Ui_Dialog()
        self.ui.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.ui.pushButton.clicked.connect(self.register)

        

    def register(self):
        
        login = self.ui.loginEdit.text()
        password = self.ui.passwordEdit.text()
        nickname = self.ui.nicknameEdit.text()

        user = UserController.getByLogin(login)
        
        if (user != None):
            print('error')
            messageBox = QtWidgets.QMessageBox(self)
            messageBox.setText('Пользователь уже существует')
            messageBox.exec()
        
        else:
            user = User(1,login,password, nickname)
            user = UserController.add(user)
            self.user_id = user.id
            self.close()

class UpdateDialog(QtWidgets.QDialog):
    
    user_id = 0

    def __init__(self, parent = None,  userId = 1):
        super(UpdateDialog, self).__init__(parent)
        self.ui = registerDialog.Ui_Dialog()
        self.ui.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        user = UserController.getById(userId)

        self.ui.loginEdit.setText(user.login)
        self.ui.passwordEdit.setText(user.password)
        self.ui.nicknameEdit.setText(user.nickname)

        UpdateDialog.user_id = userId
        self.ui.pushButton.clicked.connect(self.update)

    def update(self):
        
        id = UpdateDialog.user_id 
        login = self.ui.loginEdit.text()
        password = self.ui.passwordEdit.text()
        nickname = self.ui.nicknameEdit.text()

        user = UserController.getByLogin(login)
        
        if (user != None):
            print('error')
            messageBox = QtWidgets.QMessageBox(self)
            messageBox.setText('Логин уже существует')
            messageBox.exec()
        
        else:
            user = User(id,login,password, nickname)
            user = UserController.update(user)
            self.user_id = user.id
            self.close()



app = QtWidgets.QApplication([])
application = Window()
application.setWindowIcon(QIcon("./image/icon.jpg"))
application.show()
 

sys.exit(app.exec())