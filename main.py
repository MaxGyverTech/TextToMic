import sys
import os
import time
import threading
from PySide2 import QtWidgets, QtCore, QtGui, QtMultimedia
from PyUI import ui_main

import pyttsx3
import sounddevice as sd
import soundfile as sf
import keyboard


def play(data, fs, device=None, id=0):
    if device is None:
        sd.play(data, fs)
    else:
        sd.play(data, fs, device=device)
    print(f'process {id}')


class Player(threading.Thread):
    def __init__(self, data, fs, device=None, id=0):
        threading.Thread.__init__(self)
        self.data = data
        self.fs = fs
        self.device = device
        self.id = id

    def run(self):
        if self.device is None:
            sd.play(self.data, self.fs)
        else:
            sd.play(self.data, self.fs, device=self.device)
        print(f'process {self.id}')

# pyinstaller --hidden-import=pyttsx3.drivers --hidden-import=pyttsx3.drivers.dummy --hidden-import=pyttsx3.drivers.espeak --hidden-import=pyttsx3.drivers.nsss --hidden-import=pyttsx3.drivers.sapi5 --onefile --noconsole --icon=icon.ico --name="Text to Mic by MaxGyverTech" main.py
# pyside2-uic UI/main.ui -o PyUI/ui_main.py
class MainWindow(QtWidgets.QMainWindow, ui_main.Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.ui = ui_main.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('TextToMic by MaxGyver')
        self.setWindowIcon(QtGui.QIcon('res/icon.ico'))
        self.setStyleSheet(open('res/main.qss', 'r').read())
        # classes
        self.engine = pyttsx3.init()

        self.settings = QtCore.QSettings('PySoundpad', 'Settings')
        self.ao = QtMultimedia.QAudioOutput(QtMultimedia.QAudioDeviceInfo().defaultOutputDevice())
        self.soundfile = QtCore.QFile()
        self.s = QtMultimedia.QSound('')

        self.proc1 = None
        self.proc2 = None
        # self.a1 = QtMultimedia.QAudioOutput(QtMultimedia.QAudioDeviceInfo.defaultOutputDevice())
        # self.a2 = QtMultimedia.QAudioOutput(QtMultimedia.QAudioDeviceInfo.availableDevices(QtMultimedia.QAudio.AudioInput)[4])

        # sett
        self.sounds_dir = 'sounds/'
        self.key_bind_dir = 'sound_keys/'
        self.var_dir = 'var/'

        self.device = self.settings.value(f'{self.var_dir}device', 9)
        self.voice = self.settings.value(f'{self.var_dir}voice', None)
        self.debug = self.settings.value(f'{self.var_dir}debug', True)

        # var
        self.error_w = None
        self.change_voice_window = None
        # triggers
        self.ui.playButt.clicked.connect(self.ev_play)
        self.ui.saveButt.clicked.connect(self.ev_play_save)
        self.ui.set_output.triggered.connect(self.change_output)
        self.ui.set_voice.triggered.connect(self.change_voice)
        self.ui.textEdit.textChanged.connect(self.ev_text_updated)

        # init
        os.makedirs('sounds', exist_ok=True)
        self.update_list()
        self.apply_voice(self.voice)

    def ev_play(self):
        text = self.ui.textEdit.toPlainText()
        if not text == '':
            self.record_text(self.ui.textEdit.toPlainText())
            self.play_sound()
        else:
            self.play_sound()

    def ev_play_save(self):
        if self.ui.textEdit.toPlainText() == '':
            return
        file = self.ui.saveLine.text()
        if file == '':
            file = self.ui.textEdit.toPlainText()[:20]
        self.record_text(self.ui.textEdit.toPlainText(), file=file)
        self.play_sound(file=file)
        self.update_list()

    def ev_text_updated(self):
        text = self.ui.textEdit.toPlainText()
        if '\n' in text:
            self.ev_play()
            self.ui.textEdit.clear()

    def play_sound(self, file=None):
        if file is None:
            file = 'sound.wav'
        else:
            file = f'{self.sounds_dir}{file}.wav'
        data, fs = sf.read(file)
        # self.my_sd.stop()
        # self.my_sd.play(file)

        # self.tr1, self.tr2 = None, None
        # self.tr1 = Player(data, fs, 9)
        # self.tr2 = Player(data, fs, id=1)
        # self.tr1.start()
        # self.tr2.start()

        # sd.play(data, fs)
        # sd.wait()
        sd.play(data,fs,device=self.device)
        self.s.play(file)
        # self.soundfile.setFileName(file)
        # self.soundfile.open(QtCore.QIODevice.ReadOnly)
        # self.ao.start(self.soundfile)

    def record_text(self, text, file=None):
        if file is None:
            file = 'sound.wav'
        else:
            file = f'{self.sounds_dir}{file}.wav'
        self.engine.save_to_file(text, file)
        # self.engine.say(text)
        self.engine.runAndWait()

    def change_output(self):
        # items = [str(i)+self.p.get_device_info_by_index(device_index=i).get('name') for i in range(
        # self.p.get_device_count()) if self.p.get_device_info_by_index(device_index=i).get('maxOutputChannels') !=
        # 0] print(items) devices = [] for i in range(self.p.get_device_count()): dev =
        # self.p.get_device_info_by_index(device_index=i) if dev.get('maxOutputChannels') and dev.get('name') not in
        # devices: devices.append(dev.get('name'))
        devices = list(set(
            [i.deviceName() for i in QtMultimedia.QAudioDeviceInfo.availableDevices(QtMultimedia.QAudio.AudioInput)]))
        # devices = [i['name'] for i in sd.query_devices()]

        item, ok = QtWidgets.QInputDialog().getItem(self, "Настройка выхода", "Выберите устройство", devices, 0, False)
        if ok:
            device = sd.query_devices(item)[0]
            self.device = device.hostapi()

    def change_voice(self):
        voices = self.engine.getProperty('voices')
        index = 0
        if self.voice is not None:
            for i in range(len(voices)):
                if voices[i].id == self.voice:
                    index = i
                    break

        self.change_voice_window = VoiceSettings(voices, index, parent=self)
        self.change_voice_window.show()

    def apply_voice(self, voice):
        if voice is not None:
            self.engine.setProperty('voice', voice)
            self.settings.setValue(f'{self.var_dir}voice', voice)

    def update_list(self):
        self.ui.soundList.clear()
        files = [file for file in os.listdir('sounds/') if
                 os.path.isfile(os.path.join('sounds/', file)) and file.split('.')[len(file.split('.')) - 1] == 'wav']
        for file in files:
            key = self.settings.value(f'{self.key_bind_dir}{file.split(".")[0]}')
            item = SoundItemWidget(file.split('.')[0], key, parent=self)
            listItem = QtWidgets.QListWidgetItem(self.ui.soundList)
            listItem.setSizeHint(item.sizeHint())
            self.ui.soundList.addItem(listItem)
            self.ui.soundList.setItemWidget(listItem, item)

    def upd_shortcut(self, file, key):
        self.settings.setValue(f'{self.key_bind_dir}{file}', key)

    def debug_err(self, error, text):
        if self.debug:
            self.error_w = ErrorWindow(error, text)
            self.error_w.show()
        else:
            print(error, text)

    def closeEvent(self, event):
        self.error_w = None
        self.close()


class SoundItemWidget(QtWidgets.QWidget):
    def __init__(self, filename: str, key=None, parent: MainWindow = None):
        super(SoundItemWidget, self).__init__(parent)
        self.parent = parent
        self.filename = filename
        self.key = None
        self.setObjectName('SoundItemWidget')

        self.keyEdit = QtWidgets.QPushButton(key if key is not None else 'Задать сочетание клавиш')
        self.keyEdit.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.keyEdit.adjustSize()

        self.clear_but = QtWidgets.QPushButton(QtGui.QIcon('res/close.png'), '')
        self.clear_but.clicked.connect(self.clear_key)
        self.clear_but.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.clear_but.setToolTip('очистить осчетание клавиш')

        self.delete_but = QtWidgets.QPushButton(QtGui.QIcon('res/delete.png'), '')
        self.delete_but.clicked.connect(self.delete_key)
        self.delete_but.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.delete_but.setToolTip('удалить звук/текст')

        self.key_layout = QtWidgets.QHBoxLayout()
        self.key_layout.addWidget(self.keyEdit)
        self.key_layout.addWidget(self.clear_but)
        self.key_layout.addWidget(self.delete_but)

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(QtWidgets.QLabel(filename if len(filename)<20 else filename[:19]+'...'))
        self.layout.addLayout(self.key_layout)
        self.setLayout(self.layout)

        self.setToolTip('даблкликни на меня')

        if key is not None:
            self.key = key
            keyboard.add_hotkey(self.key, self.play_sound)

        self.keyEdit.clicked.connect(self.key_change)

    def clear_key(self):
        self.keyEdit.setText('Задать сочетание клавиш')
        if self.key is not None:
            keyboard.remove_hotkey(self.key)
        self.key = None
        self.parent.settings.remove(f'{self.parent.key_bind_dir}{self.filename}')

    def delete_key(self):
        os.remove(f'sounds/{self.filename}.wav')
        self.parent.settings.remove(f'{self.parent.key_bind_dir}{self.filename}')
        if self.key is not None:
            keyboard.remove_hotkey(self.key)
        self.parent.update_list()

    def key_change(self):
        if self.key is not None:
            keyboard.remove_hotkey(self.key)
        self.keyEdit.setText('...')
        self.keyEdit.setStyleSheet('border-width: 2px;')
        self.key = keyboard.read_hotkey(suppress=False)
        self.keyEdit.setStyleSheet('border-width: 0px;')
        self.keyEdit.setText(self.key)
        print(self.key)
        keyboard.add_hotkey(self.key, SoundItemWidget.play_sound, args=[self])
        self.parent.upd_shortcut(self.filename, self.key)

    def play_sound(self):
        self.parent.play_sound(self.filename)

    def mouseDoubleClickEvent(self, event):
        self.play_sound()

class VoiceSettings(QtWidgets.QWidget):
    def __init__(self, voices, current_voice=0, parent=None):
        super(VoiceSettings, self).__init__()
        self.setStyleSheet(open('res/main.qss', 'r').read())
        self.parent = parent
        self.voices = voices

        voice_list = [i.name for i in voices]

        self.timer = QtCore.QTimer()

        self.box = QtWidgets.QComboBox()
        self.box.addItems(voice_list)
        self.box.setCurrentIndex(current_voice)

        self.play_butt = QtWidgets.QPushButton(QtGui.QIcon('res/play.png'), '')

        self.box_layout = QtWidgets.QHBoxLayout()
        self.box_layout.addWidget(self.box)
        self.box_layout.addWidget(self.play_butt)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addLayout(self.box_layout)

        self.setLayout(self.layout)
        self.setGeometry(500, 500, 300, 100)
        self.adjustSize()
        self.setFixedSize(self.size())
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowCloseButtonHint)

        self.box.currentIndexChanged.connect(self.save)
        self.play_butt.clicked.connect(self.test_play)
        self.timer.timeout.connect(self.return_title)

        self.return_title()

    def test_play(self):
        self.parent.apply_voice(self.voices[self.box.currentIndex()].id)
        self.parent.record_text('Привет это небольшой пример этого голоса')
        data, fs = sf.read('sound.wav')
        sd.stop()
        sd.play(data, fs)

    def save(self):
        self.timer.start(2000)
        self.setWindowTitle('Настройки голоса(сохранено)')

    def return_title(self):
        self.setWindowTitle('Настройки голоса')


class ErrorWindow(QtWidgets.QWidget):
    def __init__(self, error, content):
        super(ErrorWindow, self).__init__()
        # TODO: set img

        title = str(error)[8:len(str(error)) - 2]
        text = str(content)
        self.setFocus(QtCore.Qt.FocusReason.PopupFocusReason)

        self.text_field = QtWidgets.QLabel(text)
        self.text_field.setGeometry(0, 0, 300, 100)
        self.text_field.setAlignment(QtCore.Qt.AlignTop)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.text_field)

        self.setLayout(self.layout)
        self.setGeometry(500, 500, 300, 100)
        self.setWindowTitle(title)
        self.adjustSize()
        self.setFixedSize(self.size())
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowCloseButtonHint)


def excepthook(exc_type, exc_value, exc_tb):
    window.debug_err(exc_type, exc_value)

def key_loop():
    keyboard.wait()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    key_tr = threading.Thread(target=key_loop)
    key_tr.start()
    # sys.excepthook = excepthook
    app.exec_()


