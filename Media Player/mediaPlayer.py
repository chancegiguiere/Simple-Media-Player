#Note: In order for the player to support more video types you may have to install the K-Lite Codec Pack
#Link: https://www.codecguide.com/download_k-lite_codec_pack_standard.htm


from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import QDir, QFileInfo, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,QPushButton, QShortcut, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction
from PyQt5.QtGui import QIcon, QKeySequence, QPixmap
from lyricsService import *
from tinytag import TinyTag as tt
import sys
import os

class VideoWindow(QMainWindow):

    def __init__(self, parent=None):
        super(VideoWindow, self).__init__(parent)
        self.setWindowIcon(QtGui.QIcon('./Media Player/Wojak_cropped.jpg'))
        self.setWindowTitle("Simple Media Player with Lyrics (SIMP-L)") 

        #create media player object
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        videoWidget = QVideoWidget()

        #Create Play button
        self.playButton = QPushButton()
        self.playButton.setToolTip("Play/Pause Media. Press spacebar to toggle as well.")
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play) #trigger play/pause toggle when clicked
        

        #Use Space to play/pause media
        self.playbackToggle = QShortcut(QKeySequence(' '), self)
        self.playbackToggle.activated.connect(self.play)


        #Create Fullscreen Button
        self.fullScreenButton = QPushButton()
        #self.fullScreenButton.setEnabled(False)
        self.fullScreenButton.setIcon(QIcon('./Media Player/fullscreen.png'))
        self.fullScreenButton.clicked.connect(self.toggleFullScreen)
        self.fullScreenButton.setToolTip("Toggle fullscreen mode. Also try F and F11.")

        #Use 'F' to toggle fullscreen on or off. Source: https://zetcode.com/pyqt/qshortcut/
        self.fullScreenShortcut = QShortcut(QKeySequence('F'), self)
        self.fullScreenShortcut.activated.connect(self.toggleFullScreen)

        #Use 'F11' for fullscreen as well.
        self.fullScreenShortcut2 = QShortcut(QKeySequence('F11'), self) 
        self.fullScreenShortcut2.activated.connect(self.toggleFullScreen)

        #create media slider bar
        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # Create open file action
        openAction = QAction('&Open File', self)        
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open a media file')
        openAction.triggered.connect(self.openFile)

        #create lyrics finder action (For Ken's microservice)
        lyrAction = QAction("&Find Lyrics", self)
        lyrAction.setStatusTip("Find Lyrics for a song")
        lyrAction.triggered.connect(self.findLyrics)

        # Create exit program action
        exitAction = QAction('&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.exitCall)

        # Create menu bar and add file open/ exit actions
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)

        lyrMenu = menuBar.addMenu("&Lyrics")
        lyrMenu.addAction(lyrAction) #add lyrics action to appropriate menu

        visMenu = menuBar.addMenu("&Visualizer")
        
        # Create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)

        # Create layouts to place inside widget
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)
        controlLayout.addWidget(self.fullScreenButton)
        
        #create program layout
        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addLayout(controlLayout)
        layout.addWidget(self.errorLabel)

        # Set widget to contain window contents
        wid.setLayout(layout)
        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)

    def toggleFullScreen(self):
        if self.windowState() & QtCore.Qt.WindowFullScreen:
            self.showNormal()
        else:
            self.showFullScreen()

    def openFile(self):
        global filePath
        global filename
        filePath, _ = QFileDialog.getOpenFileName(self, "Open Media File",
                QDir.homePath())

        if filePath != '':
            print(filePath)
            self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(filePath)))
            filename = QFileInfo(filePath).fileName()
            
            self.enableButtons()
            self.setWindowTitle("SIMP-L - Now Playing: " + filename)
            self.play()
    
   
   
    #Find Lyrics: 
    #This function will check for lyrics matching a given audio file using the Genius API
    #The audio file needs to have title and artist metadata embedded in the file to work properly.
    def findLyrics(self):
        text_file = open("lyrics.txt", "wt")
        audioFileTypes = ('.mp3', '.flac', '.aac', '.m4a', '.wav', '.wma')
        
        if filename.endswith(audioFileTypes):
            song = tt.get(filePath)
            if(song.title):
                songTitle = song.title
                print("song title is: " + songTitle)
            else:
                err = text_file.write("Error searching for lyrics. Make sure that title and artist metadata is present and correct")
                os.startfile("lyrics.txt")
                return

            if(song.artist):
                songArtist = song.artist
                print("song artist is: " + songArtist)
            else:
                err = text_file.write("Error searching for lyrics. Make sure that title and artist metadata is present and correct")
                os.startfile("lyrics.txt")
                return

            lyrics = get_lyrics(songTitle, songArtist)

            #print lyrics to text file (overwrite if already exists)           
            lyr = text_file.write("SONG LYRICS: " + songTitle +" by " + songArtist +"\n \n" + lyrics)
            text_file.close()
            os.startfile("lyrics.txt") #open .txt file in default editor
   
        else:
            err = text_file.write("The file \" " + filename + "\" is not supported by lyrics search. \nSupported file types are mp3, flac, aac, m4a, wma, and wav.")
            os.startfile("lyrics.txt")
            return


    def enableButtons(self):
        self.playButton.setEnabled(True)
        self.fullScreenButton.setEnabled(True)

    def exitCall(self):
        sys.exit(app.exec_())

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoWindow()
    player.resize(640, 480)
    player.show()
    sys.exit(app.exec_())