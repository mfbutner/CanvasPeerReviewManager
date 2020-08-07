# Peer Review Manager

Peer Review Manager is Python application that helps
 instructors manage and grade Canvas peer reviews automatically.
 The program helps indicate the completion of the peer reviews and grades them. 
 The program also generrates meaningful statistics regarding the scores students give to eacch other. 


## Canvas API Access Key
To use this application you will need to receive your Canvas API 
key. To do so, Follow tho instructions at the [canvas website](https://community.canvaslms.com/t5/Admin-Guide/How-do-I-obtain-an-API-access-token-in-the-Canvas-Data-Portal/ta-p/157).
## Pre Installed Version
A pre-installed GUI version of the program is provided in dist/runGui.
All you have to do is click on it.
## Installation
You can run the pre installed GUI version of the program by just clicking on the provided excutable file: rungui.

If you want to manually install the application download the project files or alternatively run :

```bash
git clone https://github.com/mfbutner/CanvasPeerReviewManager.git
```
After making sure you have python and setup tools installed on your computer 
cd into the project folder and run setup.py to install the program and its dependencies:
```bash
cd CanvasPeerReviewManager/
Python3 setup.py install  
```

## Usage (Manual Installation)
After the installation is complete you can run the terminal version of the program by running this command in a terminal session:
```bash
peer-reviewer-terminal
```
To run the GUI version, run the following command in a terminal session:
```bash
peer-reviewer
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## License
[MIT](https://choosealicense.com/licenses/mit/)

