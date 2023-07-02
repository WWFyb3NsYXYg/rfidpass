<h3 align="right"> <a href="README-ua.md"> <img src="https://user-images.githubusercontent.com/87089735/213570989-5be18f9b-fb96-48ae-bb10-ed0b02ac971b.png" height="20px"> Українська </a></h3>
<p align="center">
        <img src="https://github.com/WWFyb3NsYXYg/Desktop/assets/87089735/925082e8-5a9a-453e-9685-ff1044d42f0e" height="100px">
    </a>
    <h1 align="center">RFID Pass</h1>
</p>


* [Description](#description)
* [Computer Application](#computer-application)
* [Arduino Firmware](#arduino-firmware)
* [Connection](#connection)
* [**For regular users**](#releases)
* [Contributing](#contributing)
* [License](#contributing)
* [Acknowledgments](#acknowledgments)

### Description
RFID Pass is a program developed using the PyQt5 library that allows users to automatically enter a password on their computer by swiping an RFID card or tag. This project consists of two parts: a computer program and an Arduino firmware.


### Computer Application
The computer program provides a convenient interface for configuring and using the functionality of RFID Pass. It is built using the PyQt5 library, which allows for the creation of cross-platform desktop applications in Python. The program communicates with the Arduino board via a serial port to receive RFID card/tag data.

<p align="center">
        <img src="https://github.com/WWFyb3NsYXYg/Desktop/assets/87089735/a7277a72-f93f-4ed2-b0ac-e372af7cf1e6">
</p>

The main features of the computer program include:
1.	**Configuration:** Users can set their desired RFID card/tag UID, password, and choose whether to press Enter after entering the password.
2.	**Serial Communication:** The program establishes a connection with the Arduino board, which is connected to the computer via a serial port. It receives data from the Arduino that contains the UID of the detected RFID card/tag.
3.	**Encryption and Decryption:** The program utilizes a cryptography library for encrypting and decrypting the password. The password is stored in an encrypted form in the program's configuration file to enhance security.
4.	**Keyboard Emulation:** Upon detecting the correct UID of an RFID card/tag, the program emulates keyboard input to automatically enter the configured password into an active program or text field.

### Arduino Firmware
The Arduino firmware is responsible for reading the UID of an RFID card/tag using the MFRC522 RFID module and transmitting it to the computer program via the serial port. The firmware is written in the C++ programming language.
The main functions of the Arduino firmware include:
1.	**RFID Module Initialization:** The embedded software initializes the MFRC522 RFID module and prepares it for reading RFID card/tag data.
2.	**Serial Communication:** The firmware establishes communication with the computer program by sending the UID of the detected RFID card/tag through the serial port. The Arduino continuously scans RFID card/tag data and sends the UID to the computer program whenever a matching card/tag is detected.

### Connection
Here is the connection diagram for the RFID Pass project:

![Sheme](https://github.com/WWFyb3NsYXYg/Desktop/assets/87089735/26cfd8aa-39e7-467d-aa9c-f6bf81f6e393)

The RFID module (MFRC522) is connected to the Arduino board using wires. It is important to ensure proper power supply for the module. In your case, instead of using the usual 3.3V power supply for the module, **you need to connect the module to a 5V power supply as the 7-Byte tags** (e.g., "Gamanets" transportation card or ETicket) you want to use require more power.

### Releases
For regular users, compiled executable files and Arduino firmware are provided in the [**Releases**](https://github.com/WWFyb3NsYXYg/rfidpass/releases) section of this project. The executable file can be run on a Windows computer without any additional dependencies or installations. The Arduino firmware needs to be uploaded to the Arduino board using the Arduino IDE.

### Contributing
Contributions to this project are welcome. To contribute, fork the repository, create a new branch for your changes, make the necessary modifications, and submit a pull request. Please ensure that your contributions align with the project's coding style and guidelines.


### License

This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute the code in accordance with the terms of the license.
Feel free to explore the code and documentation in this project to understand how the RFID Pass application and Arduino firmware work together to provide the automatic password entry functionality using RFID technology.


## Acknowledgments

- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/)
- [cryptography](https://cryptography.io/)
- [pyautogui](https://pyautogui.readthedocs.io/)
