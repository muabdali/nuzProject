import json
import threading
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore, QtWidgets
from autolocke.textCopy import *
from autolocke.wandr import wandr
from PyQt5.QtCore import QTimer, Qt, QStringListModel
from PyQt5.QtGui import QMovie, QFont, QFontDatabase, QPixmap
from time import sleep
from fractions import Fraction
import csv
import os


cordsDictionary = {
    'Route_Emerald':[242, 47, 745, 121],
    'Pokemon':[300, 110, 450, 121],
    'Caught':[270, 800, 380, 207],
    'Route_Fire Red':[242, 47, 745, 121]
}


with open('autolocke\Data\data.json') as json_filePoke:
    routePokemonDict = json.load(json_filePoke)


ab = ImageDiscover(cordsDictionary=cordsDictionary,routeDict=routePokemonDict)
currentGen = None
currentGenDirectory = None
currentVersion = "23.7.01mi2"
# Format for version = year.month.day.mi/mj.version
# mi = minor update mj = major update.

class WANDR(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.Drawer)
        self.layout = QVBoxLayout(self)
        self.setWindowIcon(QtGui.QIcon('autolocke/UI/logo.png'))
        self.pokemonList = []
        self.convertToCSV(jsonFile='autolocke/Data/data.json', csvOutput='autolocke/Data/wandr.csv')
        self.fillWANDR('autolocke/Data/wandr.csv')
        self.setFixedWidth(370)
        self.setWindowTitle('WANDR')

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Pokemon", "Resistance", "Weakness"])

        self.layout.addWidget(self.table)
        self.weaknessCalculation()
        self.populateTable()

    def showEvent(self, event):
        super().showEvent(event)
        self.populateTable()

    def convertToCSV(self, jsonFile, csvOutput):
        with open(jsonFile, 'r') as file:
            jsonData = json.load(file)

        if not jsonData:
            print("Error: JSON data is empty.")
            return

        values = list(jsonData.values())  # Extract the values

        with open(csvOutput, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Values"])
            writer.writerows([[value] for value in values])
    
    def fillWANDR(self, csvFile):
        with open(csvFile, 'r' , newline="") as file:
            csvData = csv.reader(file)
            for row in csvData:
                row = row[0]
                print(row)
                if row == 'Values':
                    print('rem. values')
                else:
                    self.pokemonList.append(row)
    def weaknessCalculation(self):
        wDR = wandr()
        # Takes wandr.csv inputs from textcopy.py and converts it to a dictionary.
        wDR.csvInputToOutput()
        # Reads each pokemon in new dictionary, and gets typing1 and 2 if needed.
        wDR.getTyping()
        # Finds weaknesses and resistance for given typing from getTyping()
        wDR.pokemonTyping()
        # Multiplies all values to be given the final multiplier between types.
        wDR.isolateType()
        
    def populateTable(self):
        with open('autolocke/Data/wandrTyping.csv') as file:
            csvData = csv.reader(file)
            headers = next(csvData)  # Get the header row
            num_rows = sum(1 for _ in csvData)  # Count the number of rows

            self.table.setRowCount(num_rows)
            self.table.setColumnCount(3)

            # Set the table headers
            self.table.setHorizontalHeaderLabels(["Pokemon", "Weakness", "Resistance"])

            file.seek(0)  # Reset the file reader

            next(csvData)  # Skip the header row

            row = 0
            for line in csvData:
                if line:  # Check if the line is not empty
                    self.table.setItem(row, 0, QTableWidgetItem(line[0]))  # Set the Pokemon name in the first column

                    if len(line) > 1:
                        weakness_resistance = eval(line[1])  # Parse the combined weakness string into a dictionary

                        weakness = []
                        resistance = []

                        for type_, value in weakness_resistance.items():
                            if '/' in value:  # Handle fractions separately
                                value = float(Fraction(value))
                            else:
                                value = float(value)

                            if value > 1:
                                weakness.append(f"{type_}: {value}\n")
                            elif value < 1:
                                resistance.append(f"{type_}: {value}\n")

                        weakness_text = "".join(weakness)
                        resistance_text = "".join(resistance)

                        self.table.setItem(row, 1, QTableWidgetItem(weakness_text))  # Set the weakness value in the second column
                        self.table.setItem(row, 2, QTableWidgetItem(resistance_text))  # Set the resistance value in the third column

                row += 1

        # Resize rows and columns to fit contents
        self.table.resizeRowsToContents()
        self.table.resizeColumnsToContents()


class TutorialSteps(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Tutorial')
        self.setWindowIcon(QtGui.QIcon('autolocke/UI/logo.png'))
        self.layout = QVBoxLayout(self)

        self.gif_label_tut1 = QLabel(self)
        self.layout.addWidget(self.gif_label_tut1)

        self.gif_movie_tut1 = QMovie('autolocke/UI/tut1.gif')
        self.gif_label_tut1.setMovie(self.gif_movie_tut1)
        self.gif_movie_tut1.start()


        self.tutlabel1 = QLabel('1. Adjust your emulator so it is fullscreen on the same monitor in which you launched the application in.')
        self.tutlabel1.setFont(QFont("Verdana"))
        self.layout.addWidget(self.tutlabel1)

        self.nextButton = QPushButton('Next')
        self.layout.addWidget(self.nextButton)
        self.nextButton.clicked.connect(self.gifChange1)

        self.versionLabel = QLabel(f'Version: {currentVersion}')
        self.layout.addWidget(self.versionLabel)

# TODO do all this below better with dictionary

    def gifChange1(self):
        self.gif_movie_tut1 = QMovie('autolocke/UI/tut2.gif')
        self.gif_label_tut1.setMovie(self.gif_movie_tut1)
        self.gif_movie_tut1.start()
        self.tutlabel1.setText("2. Anchor the application to the TOP RIGHT of the emulator.")
        self.nextButton.clicked.connect(self.gifChange2)
    

    def gifChange2(self):
        self.close()
        

class TipsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Tips')
        layout = QVBoxLayout()
        self.setWindowIcon(QtGui.QIcon('autolocke/UI/logo.png'))
        self.clasCurrentGen = None

        # right side layout
        top_layout = QHBoxLayout()

        # labels n widgets

        gif_label = QLabel()
        gif_movie = QMovie('autolocke/UI/479.gif')
        gif_label.setMovie(gif_movie)
        gif_movie.start()
        gif_label.setAlignment(Qt.AlignCenter)

        # Set the stylesheet of the parent widget to position the GIF label absolutely
        self.setLayout(layout)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        # Add the tips label and next button to the main QVBoxLayout layout
        label2 = QLabel('Here are some tips:\n\nTip 1 - Make sure to keep the tracker anchored to the TOP RIGHT of the Emulator.\nTip 2 - So far, the tracker only works for Pokemon Fire Red and Leaf Green\nTip 3 - If you have any issues or suggestions, please open a discussion on https://github.com/muabdali/autoLocke')
        label2.setFont(QFont("Verdana"))
        layout.addWidget(label2)
        next_button = QPushButton('Next')
        next_button.clicked.connect(self.close)  # Close the dialog
        next_button.clicked.connect(self.convertGenJson)
        layout.addWidget(next_button)

        selectLabel = QLabel('Select your game version')
        top_layout.addWidget(selectLabel)
        self.selectGameVersion = QComboBox()
        top_layout.addWidget(self.selectGameVersion)
        layout.addLayout(top_layout)
        self.selectGameVersion.addItem("")        
        self.selectGameVersion.addItem("Fire Red")
        self.selectGameVersion.addItem("Emerald")
        self.selectGameVersion.currentTextChanged.connect(self.changeGen)
        layout.addWidget(gif_label)

        versionLabel = QLabel(f'Version: {currentVersion}')
        layout.addWidget(versionLabel)

    def changeGen(self, value):
        global currentGenDirectory, currentGen
        currentGen = value
        print('DEBUG' + currentGen)
        self.clasCurrentGen = value
        currentGen = value
        if value == "Fire Red":
            print("FR")
            self.clasCurrentGen = 'autolocke/Data/fireredroutes.txt'
            currentGenDirectory = self.clasCurrentGen            
        elif value == "Emerald":
            self.clasCurrentGen = 'autolocke/Data/emeraldroutes.txt'
            currentGenDirectory = self.clasCurrentGen
        print(currentGenDirectory)
        return currentGenDirectory, currentGen
    
    def convertGenJson(self):
        global currentGenDirectory
        currentGenDirectory = self.clasCurrentGen  # Assign returned values to variables
        print("GEN" + currentGenDirectory)
        with open(currentGenDirectory, 'r') as f:
            routes = f.read().splitlines()
        route_dict = {route: None for route in routes}
        json_data = json.dumps(route_dict, indent=4)
        with open('autolocke/Data/data.json', 'w') as file:
            file.write(json_data)




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('autoLocke')
        self.createAction()
        self.createMenu()
        self.table = QTableWidget()
        self.load_button = QPushButton('Load')
        self.save_button = QPushButton('Save')
        self.clear_button = QPushButton('Clear')
        self.edit_button = QRadioButton('Edit')
        self.clear_button.clicked.connect(self.delete_all_values)
        self.load_button.clicked.connect(self.load_json_file)
        self.save_button.clicked.connect(self.doubleSave)
        self.currentRoutelabel = QLabel('')
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.table)
        layout.addWidget(self.load_button)
        layout.addWidget(self.save_button)
        layout.addWidget(self.clear_button)
        layout.addWidget(self.edit_button)
        layout.addWidget(self.currentRoutelabel)
        self.edit_button.setStyleSheet('QRadioButton { text-align: center; }')
        self.setCentralWidget(central_widget)
        self.data = {}
        self.timer = QTimer()
        self.timer.timeout.connect(self.screenshotLoop)
        self.timer.timeout.connect(self.reload_given_json)
        self.timer.start(150)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QtGui.QIcon('autolocke/UI/logo.png'))
        # self.file_path is the current file path for the data.json VERY IMPORTANT FOR NEXT PATCH
        self.file_path = 'autolocke/Data/data.json'
        self.temp_file_path = ""
        versionLabel = QLabel(f'Version: {currentVersion}')
        layout.addWidget(versionLabel)
        print(f'AFTER {currentGenDirectory}')

    
    def createAction(self):
        self.newAction = QAction(self)
        self.newAction.setText("&Weakness and Resistance")
        self.newAction.triggered.connect(self.popUpWANDR)

    def popUpWANDR(self):
        wandrpopup = WANDR()
        wandrpopup.show()
        wandrpopup.exec()

    def createMenu(self):
        menubar = self.menuBar()
        self.setMenuBar(menubar)
        fileMenu  = QMenu("&Tools", self)
        menubar.addMenu(fileMenu)
        fileMenu.addAction(self.newAction)



    def reload_given_json(self):
        if self.edit_button.isChecked():
            return
        with open(self.file_path, 'r') as f:
            self.data = json.load(f)
        self.table.setRowCount(len(self.data))
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['Location', 'Pokemon'])
        row = 0
        print("JSONRE")
        for location, pokemon in self.data.items():
            self.table.setItem(row, 0, QTableWidgetItem(location))
            self.table.setItem(row, 1, QTableWidgetItem(pokemon))
            row += 1


        
    def doubleSave(self):
        self.save_json_file()
        self.save_json_file_buttonFunction()
        


    def load_json_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select JSON File", "", "JSON Files (*.json)", options=options
        )

        if file_path:
            try:
                # Read the contents of the JSON file
                with open(file_path, 'r') as source_file:
                    new_data = json.load(source_file)

                # Check if the loaded data is different from the current data
                if self.data != new_data:
                    self.data = new_data
                    with open('autolocke/Data/data.json', 'w') as destination_file:
                        json.dump(self.data, destination_file, indent=4)
                    print("Data loaded and saved to data.json")
                else:
                    print("Data unchanged. Previous values retained.")

                self.file_path = 'autolocke/Data/data.json'  # Update the file path
                self.reload_given_json()  # Reload the data in the table

            except Exception as e:
                print(f"Error loading and saving data: {e}")
        else:
            print("No file selected. Operation canceled.")

    def save_json_file(self):
        for row in range(self.table.rowCount()):
            location_item = self.table.item(row, 0)
            pokemon_item = self.table.item(row, 1)
            location = location_item.text()
            pokemon = pokemon_item.text()
            self.data[location] = pokemon
            
        with open(self.file_path, 'w') as f:
            json.dump(self.data, f, indent=4)

# i dont know how, i dont want to know how, but for whatever reason adding any type of self variable to this function breaks the overall UI execution and closes the whole application
# DO NOT TOUCH V
    def save_json_file_buttonFunction(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog  # Use the platform-independent dialog
        self.temp_file_path, _ = QFileDialog.getSaveFileName(
            None,
            "Save File",
            "",
            "JSON Files (*.json)",  # Only allow JSON files
            options=options
        )
        
        if self.temp_file_path:
            try:
                with open('autolocke/Data/data.json', 'r') as source_file:
                    data = source_file.read()
                with open(self.temp_file_path, 'w') as destination_file:
                    destination_file.write(data)
                    print("Data saved to:", self.temp_file_path)
                with open(self.file_path, 'w') as dest_file:
                    dest_file.write(data)
            except Exception as e:
                print(f"Error saving data: {e}")
        else:
            print("No file selected. Operation canceled.")

    def delete_all_values(self):
        self.edit_button.setChecked(True)
        with open('autolocke\Data\data.json', 'r') as f:
            self.data = json.load(f)
        self.table.setRowCount(len(self.data))
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['Location', 'Pokemon'])
        row = 0
        for location, pokemon in self.data.items():
            self.table.setItem(row, 0, QTableWidgetItem(location))
            self.table.setItem(row, 1, QTableWidgetItem(None))   
            row += 1
            self.save_json_file

    def screenshotLoop(self):
        route_thread = threading.Thread(target=self.analyzeRoute)
        caught_thread = threading.Thread(target=self.analyzeCaught)
        route_thread.start()
        caught_thread.start()

    def analyzeRoute(self):
        currentRouteSS = ab.takeScreenshot('Route', currentGenScreenshot = currentGen)
        imagePath = os.path.join('autolocke/Images/RouteImage.png')
        currentRouteAN = ab.screenshotAnalyze(imagePath, currentDirectory=currentGenDirectory, analyzedGen=currentGen)
        self.currentRoutelabel.setText(currentRouteAN)
        print(currentRouteAN)
        return currentRouteSS

    def analyzeCaught(self):
        pokemonCaughSS = ab.takeScreenshot('Caught', currentGenScreenshot=currentGen)
        imagePath = os.path.join('autolocke/Images/CaughtImage.png')
        pokemonCaught = ab.screenshotAnalyze(imagePath, currentDirectory=currentGenDirectory)
        if pokemonCaught is not None:
            print(pokemonCaught)
            self.data['Caught'] = pokemonCaught
            self.load_json_file()




if __name__ == '__main__':
    app = QApplication([])
    with open('style.qss', 'r') as f:
        style = f.read()
    app.setStyleSheet(style)
    wandrpopup = TutorialSteps()
    wandrpopup.exec()
    tips_dialog = TipsDialog()
    tips_dialog.exec()
    window = MainWindow()
    window.show()
    app.exec_()
