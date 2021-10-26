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
import sys

class VideoWindow(QMainWindow):

    def __init__(self, parent=None):
        super(VideoWindow, self).__init__(parent)
        
        self.setWindowIcon(QtGui.QIcon('Wojak_cropped.jpg'))
        self.setWindowTitle("SImple Media Player (SIMP)") 

        #create media player object
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videoWidget = QVideoWidget()

        #Create Play button
        self.playButton = QPushButton()
        #self.playButton.setEnabled(False)
        self.playButton.setToolTip("Play/Pause Media. Press spacebar to toggle as well.")
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play) #trigger play/pause toggle when clicked
        

        #Use Space to play/pause media
        self.playbackToggle = QShortcut(QKeySequence(' '), self)
        self.playbackToggle.activated.connect(self.play)


        #Create Fullscreen Button
        self.fullScreenButton = QPushButton()
        #self.fullScreenButton.setEnabled(False)
        self.fullScreenButton.setIcon(QIcon('fullscreen.png'))
        self.fullScreenButton.clicked.connect(self.toggleFullScreen)
        self.fullScreenButton.setToolTip("Toggle fullscreen mode. Also try F and F11.")

        #Use 'F' to toggle fullscreen on or off. Source: https://zetcode.com/pyqt/qshortcut/
        self.fullScreenShortcut = QShortcut(QKeySequence('F'), self)
        self.fullScreenShortcut.activated.connect(self.toggleFullScreen)

        #Use 'F11' as well.
        self.fullScreenShortcut2 = QShortcut(QKeySequence('F11'), self) 
        self.fullScreenShortcut2.activated.connect(self.toggleFullScreen)

        #create media slider bar
        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Maximum)

       
        # Create open file action
        openAction = QAction('&Open File', self)        
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open a media file')
        openAction.triggered.connect(self.openFile)

        #Create open folder action (for queueing a playlist)
        openAction = QAction('&Open Folder', self)        
        openAction.setShortcut('Ctrl+D') # D is for Directory
        openAction.setStatusTip('Open a folder containing many media files.')
       #openAction.triggered.connect(self.openFile) #Need to create "Open folder" function that will add all files in a directory to play queue.

       
        # Create exit program action
        exitAction = QAction('&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.exitCall)

        # Create menu bar and add action
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)

        # Create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)

        # Create layouts to place inside widget
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)
        controlLayout.addWidget(self.fullScreenButton)
        
        #Add Text to main window
        #self.label = QLabel("No Media Loaded.\n Use the dropdown menu above or press Ctrl + O to open a file.")


        #create program layout
        layout = QVBoxLayout()
       # layout.addWidget(self.label)
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
        audioFileTypes = ('.mp3', '.flac', '.aac', '.m4a', '.wav')
       
        filePath, _ = QFileDialog.getOpenFileName(self, "Open Media File",
                QDir.homePath())

        if filePath != '':
            self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(filePath)))
            filename = QFileInfo(filePath).fileName()
            
            
            #Check file extension. Want to show generic "music-y" image when playing audio file.
            if filename.lower().endswith(audioFileTypes):
                print("File is an audio file.")

            self.enableButtons()
            self.setWindowTitle("SIMP: Now Playing " + filename)
            self.play()
    

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