import Scraper
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class MainWidget(QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 저장 경로 라벨
        pathLabel = QLabel('저장경로')
        pathLabel.setAlignment(Qt.AlignRight)
        # 저장 경로 출력 QLineEdit
        self.savingPathLine = QLineEdit(self)
        self.savingPathLine.setReadOnly(True)
        
        # 경로 설정 버튼
        self.pathSetButton = QToolButton(self)
        self.pathSetButton.setText('경로 설정')
        
        # 스크래핑 설정 버튼
        self.scrapeButton = QToolButton(self)
        self.scrapeButton.setText('스크래핑!')
        
        # 스크롤 회수 설정 라벨
        scrollLabel = QLabel('스크롤 횟수')
        scrollLabel.setAlignment(Qt.AlignRight)
        # 스크롤 회수 설정
        self.scrollSpinBox = QSpinBox(self)
        self.scrollSpinBox.setRange(1,20)
        
        # 검색할 태그 설정 라벨
        tagLabel = QLabel('검색할 태그')
        tagLabel.setAlignment(Qt.AlignRight)
        # 검색할 태그 설정 QLineEdit
        self.tagLine = QLineEdit(self)


        directionLayout = QHBoxLayout()
        directionLayout.addWidget(pathLabel, 0)
        directionLayout.addWidget(self.savingPathLine, 1)
        directionLayout.addWidget(self.pathSetButton, 2)


        userSettingLayout = QHBoxLayout()
        userSettingLayout.addWidget(scrollLabel, 0)
        userSettingLayout.addWidget(self.scrollSpinBox, 1)
        userSettingLayout.addWidget(tagLabel, 2)
        userSettingLayout.addWidget(self.tagLine, 3)
        userSettingLayout.addWidget(self.scrapeButton, 4)
        

        outerBox = QVBoxLayout()
        outerBox.addLayout(directionLayout)
        outerBox.addLayout(userSettingLayout)

        self.setLayout(outerBox)

class mainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.title = '크롤링 도구'
        self.initUI()
    
    def initUI(self):
        #Scraper 클래스 선언
        self.scraper = Scraper.Scraper()
        
        self.setWindowTitle(self.title)
        self.mainWidget = MainWidget()
        self.setCentralWidget(self.mainWidget)
        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)
        self.show()
        self.mainWidget.pathSetButton.clicked.connect(self.openFileNameDialog)
        self.openFileNameDialog()
        
        # 스크래핑 버튼에 스크래핑 함수 연결
        self.mainWidget.scrapeButton.clicked.connect(self.scrape)
    
    def openFileNameDialog(self):
        options = QFileDialog.Options()
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.mainWidget.savingPathLine.setText(file)
        print(file)
    
    def showError(self, exceptionContent):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("에러가 발생했습니다.")
        msg.setText(exceptionContent)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
    
    def scrape(self):
        try:
            self.scraper.scrape(
                                self.mainWidget.scrollSpinBox.value(),
                                self.mainWidget.tagLine.text(),
                                self.mainWidget.savingPathLine.text()
                                )
        except Exception as e:
            self.showError(str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gameWindow = mainWindow()
    gameWindow.show()
    sys.exit(app.exec_())
