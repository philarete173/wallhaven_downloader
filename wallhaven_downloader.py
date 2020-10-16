from PySide2 import QtCore, QtGui, QtWidgets
import gui, sys, os, subprocess, json, lz4.block, requests, shutil, datetime, time
from PIL import Image


def GetBasePath():
    try:
        base_path = sys._MEIPASS
    except:
        base_path = os.path.abspath('.')
    return base_path


class MainWindow(QtWidgets.QMainWindow, gui.Ui_MainWindow):
    def __init__(self):
        QtWidgets.QApplication.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
        QtWidgets.QMainWindow.__init__(self)
        gui.Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.submitbutton.setEnabled(False)
        self.submitbutton.clicked.connect(self.RunDownloader)
        self.folderbutton.clicked.connect(self.ChooseFolder)
        self.OpenSettings()
        if self.apikeyEdit.text() != '' and self.folderfield.text() != '':
            self.submitbutton.setEnabled(True)

    def OpenSettings(self):
        self.settings = QtCore.QSettings('settings.ini', QtCore.QSettings.IniFormat)
        self.settings.setFallbacksEnabled(False)
        self.apikeyEdit.setText(self.settings.value('wallhaven/api_key', ''))
        self.destfoldername = self.settings.value('wallhaven/destfoldername', '')
        self.folderfield.setText(self.destfoldername)

    def SaveSettings(self):
        self.settings.setValue('wallhaven/api_key', self.apikeyEdit.text())
        self.settings.setValue('wallhaven/destfoldername', self.destfoldername)

    def ChooseFolder(self):
        self.destfoldername = os.path.abspath(str(QtWidgets.QFileDialog.getExistingDirectory(self, "Choose destination folder")))
        self.folderfield.setText(self.destfoldername)
        self.submitbutton.setEnabled(True)

    def RecieveTextMessage(self, str):
        self.logarea.appendPlainText(str)

    def RunDownloader(self):
        self.submitbutton.setEnabled(False)
        self.downloadthread = DownloadTread()
        self.downloadthread.dirsig.connect(self.downloadthread.RecieveDirName)
        self.downloadthread.dirsig.emit(self.destfoldername)
        self.downloadthread.apisig.connect(self.downloadthread.RecieveApiKey)
        self.downloadthread.apisig.emit(self.apikeyEdit.text())
        self.downloadthread.logsig.connect(self.RecieveTextMessage)
        self.downloadthread.start()
        self.downloadthread.finished.connect(self.ThreadFinished)

    def ThreadFinished(self):
        self.submitbutton.setEnabled(True)

    def closeEvent(self, *args, **kwargs):
        self.SaveSettings()
        self.close()


class DownloadTread(QtCore.QThread):
    dirsig = QtCore.Signal(str)
    apisig = QtCore.Signal(str)
    logsig = QtCore.Signal(str)

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)

    def run(self):
        self.StartDownload(self.destfoldername, self.apikey)

    def RecieveDirName(self, str):
        self.destfoldername = str

    def RecieveApiKey(self, str):
        self.apikey = str

    def StartDownload(self, dirname, apikey):
        base_path = GetBasePath()
        image_folder = f'{base_path}\\images'
        if os.path.isdir(image_folder) is False:
            os.mkdir(image_folder)

        ratio = 1.7777777777777777

        self.logsig.emit('Preparing...')
        find = 'cd /d %appdata%/Mozilla/Firefox & dir /b /s recovery.jsonlz4'
        cmd = subprocess.run(find, shell=True, stdout=subprocess.PIPE).stdout.strip()

        tabsfiletime = datetime.datetime.utcfromtimestamp(os.path.getmtime(cmd))
        checktime = datetime.datetime.now() - datetime.timedelta(seconds=15)
        if checktime > tabsfiletime:
            time.sleep(5)

        file_tabs = open(cmd, 'rb')
        magic = file_tabs.read(8)
        jdata = json.loads(lz4.block.decompress(file_tabs.read()).decode("utf-8"))
        file_tabs.close()

        self.logsig.emit('Start')

        ids = []
        for win in jdata.get("windows"):
            for tab in win.get("tabs"):
                i = int(tab.get("index")) - 1
                url = tab.get("entries")[i].get("url")
                if 'wallhaven.cc/w/' in url:
                    ids.append(url[-url.find('/'):])

        for image_entry, id in enumerate(ids, 1):
            self.logsig.emit(f'Processing image #{image_entry}...')
            image_url = requests.get(f'https://wallhaven.cc/api/v1/w/{id}?apikey={apikey}').json()['data']['path']
            image_name, _, image_format = image_url.rpartition('/')[2].rpartition('.')
            im = requests.get(image_url, stream=True)
            with open(f'{image_folder}\\{image_name}.{image_format}', 'wb')as image_file:
                self.logsig.emit(f'Downloading image with id {id}...')
                for chunk in im.iter_content(1024):
                    image_file.write(chunk)
                image_file.close()

            image = Image.open(f'{image_folder}\\{image_name}.{image_format}')
            if image.size[0] / image.size[1] != ratio:
                self.logsig.emit(f'Cropping image {image_name}.{image_format}...')
                if image.size[0] / image.size[1] < ratio:
                    box = (0, (image.size[1] - image.size[0] / ratio) / 2, image.size[0],
                           image.size[0] / ratio + ((image.size[1] - image.size[0] / ratio) / 2))
                elif image.size[0] / image.size[1] > ratio:
                    box = ((image.size[0] - image.size[1] * ratio) / 2, 0,
                           image.size[1] * ratio + ((image.size[0] - image.size[1] * ratio) / 2), image.size[1])
                self.cropAndResize(image, box, image_folder, image_name, image_format)
            image.close()

        self.logsig.emit('Copying images...')
        for filename in os.listdir(image_folder):
            self.logsig.emit(f'Copying image {filename}...')
            shutil.copy(f'{image_folder}\\{filename}', dirname)
            os.remove(f'{image_folder}\\{filename}')
            time.sleep(0.2)

        self.logsig.emit('All done!')

    def cropAndResize(self, image, box, image_folder, image_name, image_format):
        crop_image = image.crop(box)
        if 1920 <= int(crop_image.size[0]) < 2560:
            width, height = (1920, 1080)
        elif 2560 <= int(crop_image.size[0]) < 3840:
            width, height = (2560, 1440)
        elif int(crop_image.size[0]) >= 3840:
            width, height = (3840, 2160)
        resize_image = crop_image.resize((width, height))
        resize_image.save(f'{image_folder}\\{image_name}_{width}x{height}.{image_format}')
        image.close()
        os.remove(f'{image_folder}\\{image_name}.{image_format}')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    app.setWindowIcon(QtGui.QIcon(f'{GetBasePath()}\\favicon.ico'))
    window.setWindowIcon(QtGui.QIcon(f'{GetBasePath()}\\favicon.ico'))
    window.show()
    sys.exit(app.exec_())
