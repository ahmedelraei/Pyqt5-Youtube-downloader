from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import os
from os import path
import sys
import urllib
import urllib.request
import pafy
import humanize
import multiprocessing
import getpass
import random
import time

Form_Class,_ = loadUiType(path.join(path.dirname(__file__), "main.ui"))

class mainapp(QMainWindow, Form_Class):

	def __init__(self, parent=None):
		super(mainapp,self).__init__(parent)
		QMainWindow.__init__(self)
		self.setupUi(self)
		self.handle_UI()
		self.buttons()
		self.textboxes()
		self.themes()
		self.tabWidget.tabBar().setVisible(False)
		self.dockWidget.hide()


	def handle_UI(self):
		self.setFont(QFont('Segoe UI'))
		user = getpass.getuser()
		msg1 = "Hello " + user
		msg2 = "Hi %s, We hope you appreciate our Program :D" %(user)
		msg3 = "Hi %s, I forgot to mention myself, i am mr.GETIT :) , I came to help you download anything :P" %(user)
		msgs = [msg1,msg2,msg3]
		randomMsg = random.choice(msgs)
		self.setWindowTitle(randomMsg)
		self.setFixedSize(1019,707)


	def textboxes(self):
		self.lineEdit_4.setPlaceholderText("Press Enter after adding url")
		self.lineEdit_4.setFocus()
		self.lineEdit_14.setFocus()

	def buttons(self):
		self.lineEdit_4.returnPressed.connect(self.yt_get_vid)
		self.pushButton_13.clicked.connect(self.browse3)
		self.pushButton_3.clicked.connect(self.browse2)
		self.pushButton_4.clicked.connect(self.yt_download_vid)
		self.pushButton_14.clicked.connect(self.playlist_dl)
		self.pushButton_6.clicked.connect(self.tab1)
		self.pushButton_7.clicked.connect(self.tab2)
		self.lineEdit_15.returnPressed.connect(self.yt_analyzer)
		self.pushButton_9.clicked.connect(self.themesApply)
		self.pushButton_8.clicked.connect(self.thumbnail)
		#self.pushButton_5.clicked.connect(self.Browser)

		###### Menu Triggers ######
		self.actionSettings.triggered.connect(self.tabSettings)
		self.actionExit.triggered.connect(lambda: sys.exit())


	def themes(self):
		try:
			if not os.path.exists("Themes"):
				os.mkdir("Themes")
			if os.path.exists("Themes/.defaultTheme/.default.css"):
				f = open("Themes/.defaultTheme/.default.css","r")
				default = f.read() 
				self.setStyleSheet('')
				self.setStyleSheet(default)

			if not os.path.exists("Themes/.defaultTheme/"):
				os.mkdir("Themes/.defaultTheme/")

			Themes = os.listdir("Themes")
			for theme in Themes:
				if os.path.isfile("Themes/"+theme):
					addedTheme = theme.split('.')[0]
					self.comboBox_2.addItem(addedTheme)
		except Exception:
			QMessageBox.warning(self,"Process Error" , "Restart The Program . if the problem not solved contact The Support")

	def themesApply(self):
		try:
			theme = self.comboBox_2.currentText()
			f = open("Themes/"+theme+".css" , "r")
			appliedTheme = f.read()
			self.setStyleSheet('')
			self.setStyleSheet(appliedTheme)
			f.close()
			self.update()

			if not os.path.exists("Themes"):
				os.mkdir("Themes")

			if not os.path.exists("Themes/.defaultTheme/"):
				os.mkdir("Themes/.defaultTheme/")

			f = open("Themes/.defaultTheme/.default.css" , "w")
			f.write(appliedTheme)
			f.close()
		except FileNotFoundError:
			pass

	def tab1(self):
		self.tabWidget.setCurrentIndex(0)

	def tab2(self):
		self.tabWidget.setCurrentIndex(1)

	def tabSettings(self):
		self.tabWidget.setCurrentIndex(2)

	def browse(self):
		save_place = QFileDialog.getSaveFileName(self,caption="Download Location" , directory=".", filter="All Files(*.*)")
		s = str(save_place)
		b_path = s.split(",")[0][2:-1]
		self.lineEdit_2.setText(b_path)

	def browse2(self):
		save_place = QFileDialog.getExistingDirectory(self,"Download Location")
		self.lineEdit_3.setText(save_place)

	def browse3(self):
		save_place = QFileDialog.getExistingDirectory(self,"Download Location")
		self.lineEdit_13.setText(save_place)

	def yt_analyzer(self):
		self.dockWidget.show()
		vid_url = self.lineEdit_15.text()
		v = pafy.new(vid_url)
		self.plainTextEdit.appendPlainText(v.description)

		for keyword in v.keywords:
			self.plainTextEdit_2.clear()	
			self.plainTextEdit_2.appendPlainText(keyword+",")

		self.title = v.title
		self.lineEdit_16.setText(v.title)
		self.lineEdit_19.setText(str(v.rating))
		try:
			self.thumburl = v.bigthumbhd
		except Exception:
			self.thumburl = v.bigthumb
		except:
			self.thumburl = v.thumb
		self.lineEdit_17.setText(v.videoid)
		self.lineEdit_18.setText(str(v.viewcount))
		QApplication.processEvents()

	def thumbnail(self):
		save_place = os.path.expanduser('~') + "/Pictures/"
		path = save_place+self.title
		ext = "."+self.thumburl.split(".")[-1]
		print(path)
		f = open(path+ext , 'wb')
		f.write(urllib.request.urlopen(self.thumburl).read())
		f.close()

	def yt_get_vid(self):
		try:
			self.comboBox.clear()
			video_url = self.lineEdit_4.text()
			v = pafy.new(video_url)
			print(v.title)
			print(v.duration)
			print(v.rating)
			print(v.author)
			print(v.length)
			print(v.keywords)
			print(v.thumb)
			print(v.videoid)
			print(v.viewcount)
			st = v.allstreams
			print(st)
			for s in st:
				size = humanize.naturalsize(s.get_filesize())
				data = '{} {} {} {}'.format(s.mediatype , s.extension , s.quality , size)
				self.comboBox.addItem(data)
				QApplication.processEvents()
		except Exception:
			QMessageBox.warning(self,"Error","The Download has Failed")


	def progress1(self,totalsize, recieved, ratio , rate , eta):

		if totalsize > 0:
			p = "{:.0%}".format(ratio)
			percent = int(p.strip("%"))
			self.progressBar_2.setValue(percent)
			QApplication.processEvents()  #not responding partial fix


	def progress2(self, totalsize, recieved, ratio , rate , eta):
		if totalsize > 0:
			p = "{:.0%}".format(ratio)
			percent = int(p.strip("%"))
			self.progressBar_7.setValue(percent)
			QApplication.processEvents()  #not responding partial fix
	

	def yt_download_vid(self):
		url = self.lineEdit_4.text()
		save = self.lineEdit_3.text()
		quality = self.comboBox.currentIndex()
		self.save_url_qual.emit(save,url,quality)
		try:
			v = pafy.new(url)
			st = v.allstreams
			quality = self.comboBox.currentIndex()
			down = st[quality].download(filepath=save,quiet=False,callback=self.progress1)
			QMessageBox.information(self, 'Download is Completed', 'Media has just Downloaded Succesfully')

		except Exception as e:
			print("yt_download_vid: ", e)
			QMessageBox.warning(self,"Error","The Download has Failed")

	def playlist_dl(self):

		try:

			url = self.lineEdit_14.text()
			save_location = self.lineEdit_13.text()
			playlist = pafy.get_playlist(url)
			videos = playlist['items']
			try:
				os.chdir(save_location)
				os.mkdir(str(playlist['title']))
				os.chdir(str(playlist['title']))
			except FileExistsError:
				os.chdir(str(playlist['title']))

			if self.comboBox_4.currentIndex() == 0:

				for v in videos:

					video = v['pafy']
					self.label_19.setText('Current: ' + video.title)
					best = video.getbest(preftype="mp4")
					best.download(quiet=False,callback=self.progress2)

			elif self.comboBox_4.currentIndex() == 1:

				for v in videos:
					audio = v['pafy']
					self.label_19.setText("Current: " + audio.title)
					best = video.getbestaudio(preftype="m4a")
					best.download(quiet=False,callback=self.progress2)

			if self.checkBox.isChecked() == True:
				os.system("shutdown /s")

		except FileExistsError:
			QMessageBox.warning(self,"Error","Change Download Path")

		except Exception:
			print("playlist_dl: ", e)
			QMessageBox.warning(self,"Error","The Download has Failed")


# 	def Browser(self):
# 		self.browse = browse()
# 		self.browse.show()
# 		self.browse.gotURL.connect(self.getURL)
#
# 	def getURL(self,url):
#
# 		self.lineEdit_4.setText(url)
# 		self.yt_get_vid()
#
#
#
# Form_Class2,_ = loadUiType(path.join(path.dirname(__file__),"Browser.ui")
#
# class browse(QMainWindow, Form_Class2):
#
# 	gotURL = pyqtSignal('QString')
#
# 	def __init__(self, parent=None):
# 		super(browsing,self).__init__(parent)
# 		QMainWindow.__init__(self)
# 		self.setupUi(self)
# 		self.handle_UI()
# 		self.pushButton.clicked.connect(self.getURL)
# 		self.url = None
#
#
# 	def handle_UI(self):
# 		self.setWindowTitle("Choose A Video or Playlist to Download")
# 		self.setFixedSize(907,712)
#
# 	def getURL(self):
# 		self.update()
# 		self.url = (str(self.webEngineView.url()).replace("PyQt5.QtCore.QUrl","")
# 		.replace("(","").replace(")","").replace("'",""))
# 		print(self.url)
#
# 		target = "https://www.youtube.com/watch?v"
# 		print(target in self.url)
#
# 		if (target in self.url) == True:
# 			self.gotURL.emit(self.url)
# 		else:
# 			pass



def main():
	app = QApplication(sys.argv)
	window = mainapp()
	window.show()
	sys.exit(app.exec_())



if __name__ == "__main__":
	main()








