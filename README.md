# TextToMic
Простая программа на python для озвучивания звука в виртуальное аудиоустроство
![](screenshot.png)
#### Зависимости:
`pip install -r requirements.txt`

#### Запуск 
`python main.py`
#### Сборка

```cmd
pyinstaller --hidden-import=pyttsx3.drivers --hidden-import=pyttsx3.drivers.dummy --hidden-import=pyttsx3.drivers.espeak --hidden-import=pyttsx3.drivers.nsss --hidden-import=pyttsx3.drivers.sapi5 --onefile --noconsole --icon=icon.ico --name="Text to Mic by MaxGyverTech" main.py
```
