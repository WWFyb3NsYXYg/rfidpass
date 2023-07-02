from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo  # Import classes for working with serial port
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu  # Import classes for creating system tray icon and context menu
from PyQt5.QtGui import QIcon, QDesktopServices  # Import classes for working with GUI and opening URLs
from PyQt5.QtCore import QIODevice, QUrl  # Import classes for working with Qt core
from cryptography.fernet import Fernet  # Import class for encryption and decryption
from PyQt5 import QtWidgets, uic  # Import classes for creating GUI
import configparser  # Import class for working with configuration files
import pyautogui  # Import class for emulating keyboard input
import sys  # Import module for system functions and variables
import os  # Import module for working with the operating system

# Instantiating a Configuration Object
config = configparser.ConfigParser()
config_file = 'config.ini'

# Function to access internal file
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Defining paths to interface and icon files
ui_path = resource_path('design.ui')
icon_path = resource_path('icon.png')

# Instantiate the application and load the interface
app = QtWidgets.QApplication([])
ui = uic.loadUi(ui_path)
ui.setWindowTitle("RFID Pass")
ui.setWindowIcon(QIcon(icon_path))  # set file icon

# Instantiate the serial port object
serial = QSerialPort()
serial.setBaudRate(9600)

# Function to display application on double click on tray icon
def trayShow():
    # Create the system tray icon
    tray_icon = QSystemTrayIcon(QIcon(icon_path), app)
    tray_icon.activated.connect(lambda reason: ui.show(
    ) if reason == QSystemTrayIcon.DoubleClick else None)

    # Create a menu for the tray icon
    tray_menu = QMenu()

    # Add an action to restore the applications
    restore_action = tray_menu.addAction("Restore App")
    restore_action.triggered.connect(lambda: ui.show())

    # Add an action to quit the application

    git_action = tray_menu.addAction("Repo on GitHub")
    git_action.setData("https://github.com/WWFyb3NsYXYg/rfidpass")
    git_action.triggered.connect(
        lambda: QDesktopServices.openUrl(QUrl(git_action.data())))

    quit_action = tray_menu.addAction("Quit")
    quit_action.triggered.connect(app.quit)

    # Set the tray menu
    tray_icon.setContextMenu(tray_menu)
    tray_icon.setToolTip("Rfid Pass by Yarestem")
    # Show the tray icon
    tray_icon.show()

# Function to write the updated configuration to a file
def updateConfig():
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

# Function to compare UID with main UID
def compareUid(uid):
    master_uid = config.get('RfidPass', 'uid')
    return uid == master_uid

# Function to get the decrypted password
def getPass():
    encrypted_password = config.get('RfidPass', 'password')
    key = config.get('Service', 'key')
    decrypted_password = decrypt_password(
        encrypted_password.encode('utf-8'), key.encode('utf-8'))
    return decrypted_password

# Function to emulate keyboard input
def emulateKeyboardInput():
    pyautogui.typewrite(getPass())
    if ui.checkEnter.isChecked():
        pyautogui.press('enter')

# Function for reading data from the port
def serialRead():
    if not serial.canReadLine():
        return
    rx = serial.readLine()
    data = str(rx, 'utf-8').strip()
    ui.statusBar().showMessage(data)
    if compareUid(data):
        emulateKeyboardInput()

# Function to encrypt the password
def encryptPassword(password):
    key = Fernet.generate_key()
    f = Fernet(key)
    encrypted_password = f.encrypt(password.encode('utf-8'))
    config.set('RfidPass', 'password', encrypted_password.decode('utf-8'))
    config.set('Service', 'key', key.decode('utf-8'))

# Function to decrypt the password
def decrypt_password(encrypted_password, key):
    # Decrypt the encrypted password using the key
    f = Fernet(key)
    decrypted_password = f.decrypt(encrypted_password)
    return decrypted_password.decode('utf-8')

# Function to open serial port
def serialOpen():
    serial.setPortName(ui.comBox.currentText())
    serial.open(QIODevice.ReadWrite)

# Function to close the serial port
def serialClose():
    serial.close()

# Function to update the list of available ports in the interface and text fields
def updateList():
    portList = []
    ports = QSerialPortInfo().availablePorts()
    for port in ports:
        portList.append(port.portName())
    ui.comBox.clear()
    ui.comBox.addItems(portList)
    uid = config.get('RfidPass', 'uid')
    passwd = config.get('RfidPass', 'password')
    pressenter = True if config.get('RfidPass', 'pressenter') == "True" else False
    ui.UIDLine.setText(uid)
    ui.PassLine.setText(passwd)
    ui.checkEnter.setCheckState(pressenter)

# Function to set new UID
def uidSet():
    newUid = ui.statusBar().currentMessage()
    if newUid != "":
        ui.UIDLine.setText(newUid)
        config.set('RfidPass', 'uid', newUid)
        updateConfig()

# Function to set the state of the checkbox "Pressing Enter"
def stateEnter():
    isChecked = str(ui.checkEnter.isChecked())
    config.set('RfidPass', 'pressEnter', isChecked)
    updateConfig()

# Function to set a new password
def setPass():
    newPass = ui.PassLine.text()
    encryptPassword(newPass)
    updateConfig()
    ui.statusBar().showMessage("Password updated")

# Function to minimize the application to tray
def minimizeToTray(event):
    event.ignore()
    ui.hide()


# start program

# Check if the configuration file exists
if not os.path.exists(config_file):
    # Set default values for parameters
    config['RfidPass'] = {
        'uid': 'None',
        'password': '',
        'pressEnter': 'False'

    }
    config['Service'] = {
        'key': 'None'
    }
    # Write the start configuration to the file
    updateConfig()
else:
    config.read(config_file)

# Display the tray icon and bind the event of reading data from the port with the processing function
trayShow()
serial.readyRead.connect(serialRead)

# Associating interface buttons with their respective functions
ui.openBtn.clicked.connect(serialOpen)
ui.updateBtn.clicked.connect(updateList)
ui.closeBtn.clicked.connect(serialClose)
ui.setUID.clicked.connect(uidSet)
ui.setPass.clicked.connect(setPass)
ui.checkEnter.stateChanged.connect(stateEnter)

# Update the list of ports in the interface and display the interface
ui.closeEvent = minimizeToTray
updateList()
ui.show()

# Run the main application loop
app.exec()
