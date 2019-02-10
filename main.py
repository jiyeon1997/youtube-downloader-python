import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5 import uic
from PyQt5.QtCore import *
import pytube
import os
import re
import subprocess
from ui.Design2 import Ui_MainWindow

class YoutubeDownloader(QMainWindow, Ui_MainWindow) :
    def __init__(self) :
        super().__init__()

        self.setupUi(self)
        self.setWindowTitle('Youtube Downloader v2.0')

        self.comboBox.addItem('mp3')
        self.comboBox.addItem('avi')
        self.comboBox.addItem('mov')
        self.comboBox.addItem('wmv')

        self.extension.addItem('mp3')
        self.extension.addItem('avi')
        self.extension.addItem('mov')
        self.extension.addItem('wmv')
        self.extension.addItem('wav')

        self.initSignal()

        self.statusbar.showMessage('Ready.')

    # 시그널 초기화
    def initSignal(self) :
        self.downloadButton.clicked.connect(self.downloadWork)
        self.toolButton.clicked.connect(self.savePathWork)
        self.fileToolButton.clicked.connect(self.selectFileWork)
        self.toolButton_2.clicked.connect(self.selectPathWork)
        self.convertButton.clicked.connect(self.convertWork)
        self.tabWidget.currentChanged.connect(self.tabClicked)

    # 툴 박스 눌렀을 때
    @pyqtSlot()
    def savePathWork(self) :
        fpath = QFileDialog.getExistingDirectory(self, 'Select the Directory')
        self.saveTextEdit.setText(fpath)

    # 다운로드 버튼 눌렀을 때
    @pyqtSlot()
    def downloadWork(self) :
        # Step #1. url 주소 확인
        url = self.urlTextEdit.text().strip()
        save = self.saveTextEdit.text()
        regex = re.compile('^https://www.youtube.com/watch?')

        if url is None or url == '' or not url :
            QMessageBox.about(self, 'Error', 'Enter the Video Url')
            self.urlTextEdit.setFocus(True)
            return None

        if save is None or save == '' or not save :
            QMessageBox.about(self, 'Error', 'Select the Directory')
            return None

        # Step #2. download 진행
        if regex.match(url) is not None :
            # 동영상 먼저 다운로드
            self.statusbar.showMessage('downloading')

            video = pytube.YouTube(url)
            stream = video.streams.all()
            down_dir = self.saveTextEdit.text()
            stream[0].download(down_dir)

            # Step #3. 체크박스 값 확인
            if self.checkBox.isChecked() :
                oriFiileName = stream[0].default_filename
                newFileName = os.path.splitext(oriFiileName)[0]

                # print(str(self.comboBox.currentText()))
                subprocess.call(['ffmpeg','-i',
                    os.path.join(down_dir, oriFiileName),
                    os.path.join(down_dir, newFileName + '.' + str(self.comboBox.currentText()))
                ])
            self.statusbar.showMessage('Download Finished')

        else :
            QMessageBox.about(self,'Error', '유튜브 url형식이 아닙니다.')

    # tabWidget 눌렀을 때
    @pyqtSlot()
    def tabClicked(self) :
        self.statusbar.showMessage('Ready.')

    # Convert file 눌렀을 때
    @pyqtSlot()
    def selectFileWork(self) :
        self.fname = QFileDialog.getOpenFileName(self, 'select the file')
        self.fileTextEdit.setText(self.fname[0])

    # Convert toolbutton 눌렀을 때
    @pyqtSlot()
    def selectPathWork(self) :
        fpath = QFileDialog.getExistingDirectory(self, 'Select the Directory')
        self.savePathEdit.setText(fpath)

    # Convert file logic
    @pyqtSlot()
    def convertWork(self) :
        file_dir = self.fileTextEdit.text()
        down_dir = self.savePathEdit.text()

        if file_dir is None or file_dir == '' or not file_dir :
            QMessageBox.about(self, 'Error', 'Select the file')
            return None

        if down_dir is None or down_dir == '' or not down_dir :
            QMessageBox.about(self, 'Error', 'Select the Directory')
            return None

        fileName = os.path.basename(file_dir)
        newFileName = os.path.splitext(fileName)[0]

        subprocess.call(['ffmpeg','-i',
            os.path.join(file_dir),
            os.path.join(down_dir, newFileName + '.' + str(self.extension.currentText()))
        ])

        self.statusbar.showMessage('Convert Finished')

if __name__ == '__main__' :
    app = QApplication(sys.argv)
    you_viewer_main = YoutubeDownloader()
    you_viewer_main.show()
    app.exec_()
