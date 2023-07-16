import pyautogui
import pytesseract
from PIL import ImageEnhance, Image
import time
from autolocke.fuzzyCheck import fuzzChecker
from autolocke.pytessGrayscaletest import *
import json
import os

# Define the region of the screen to capture
x, y, width, height = 242, 47, 745, 121

# Take a screenshot of the region and save it as an image file
#screenshot = pyautogui.screenshot(region=(x, y, width, height))
#screenshot.save('screenshot.png')

# Load the image file and extract text from it

cordsDictionary = {
    'Emerald Route':[1, 1, 1920,1080],
    'Emerald Caught':[1, 1, 745, 121],
    'Fire Red Route':[242, 47, 745, 121],
    'Fire Red Caught':[270, 800, 380, 207]
}

"""
TODO - change reference check for fuzzywuzzy for appropriate txt route, right now
it only checks fireredroutes no matter which gen is selected.

"""

#cordsDictionary removed from here, now only in file where ImageDiscover is called
class ImageDiscover:
    def __init__(self, cordsDictionary, routeDict):
        self.dict = cordsDictionary
        self.oldtext = ''
        self.currentPokemon = ''
        self.currentRoute = ''
        self.routeDictionary = routeDict
    

    def takeScreenshot(self, section_name, currentGenScreenshot):
        #grabs the coords for the screenshot TODO: instead of multiple small screenshots, it should be just one big screenshot where the functions take snippets FROM, thereby halving the amount of screenshots.
        self.file_path_route = ("autolocke/Images/RouteImage.png")
        self.file_path_caught = ("autolocke/Images/CaughtImage.png")
        self.section = cordsDictionary[f'{currentGenScreenshot} {section_name}']
        x, y, width, height = self.section[0], self.section[1], self.section[2], self.section[3]
        print(f'{section_name} {currentGenScreenshot} {self.section}')
        screenshot = pyautogui.screenshot(region=(x, y, width, height))
        script_directory = os.path.dirname(os.path.abspath(__file__))
        if section_name == 'Route':
            screenshot.save(self.file_path_route)
        else:
            screenshot.save(self.file_path_caught)


    def appendRoutePokeDict(self, CurrentRoute, CaughtPokemon):
        self.dict[CurrentRoute] = CaughtPokemon
        print(self.dict[CurrentRoute])


    def screenshotAnalyze(self, requestedImage, currentDirectory, analyzedGen=None):
        ia = fuzzChecker
        print(currentDirectory)
        if analyzedGen == "Emerald":
            if requestedImage == 'autolocke/Images/RouteImage.png':
                text = imageEnhancer.emeraldFunction(requestedImage)
            elif requestedImage == 'autolocke/Images/CaughtImage.png':
                text = imageEnhancer.enhanceFunction(requestedImage)
            else:
                return
        else:
            text = imageEnhancer.enhanceFunction(requestedImage)
        if requestedImage == 'autolocke/Images/RouteImage.png':
            stripText = text.strip()
            routeFuzz = ia.checkList(currentDirectory, stripText, minScore=95)
            print(self.currentRoute + "CURRENT ROUTE SELF")
            
            if routeFuzz in self.routeDictionary:
                print("in dict")
                routeFuzzFinal = routeFuzz
                self.currentRoute = routeFuzzFinal
        elif requestedImage == 'autolocke/Images/CaughtImage.png':
            if "Gotcha" in text:
                print("if caught")
                if "!" in text:
                    gotchaOrNot, pokemonName = text.split("!\n")
                elif "|\n" in text:
                    gotchaOrNot, pokemonName = text.split("|\n")
                else:
                    print("CAUGHT ERROR89 tC.p")
                fuzz_pokemonName = ia.checkList('autolocke/Data/NatDexPokemonG3.txt', pokemonName)
                print(gotchaOrNot, pokemonName)
                print(fuzz_pokemonName)
                
                if gotchaOrNot == 'Gotcha ':
                    print(f"Caught {fuzz_pokemonName} in {self.currentRoute}")
                    if fuzz_pokemonName:
                        self.routeDictionary[self.currentRoute] = fuzz_pokemonName
                    else:
                        # Handle the case when the value is empty
                        self.routeDictionary.pop(self.currentRoute, None)
                    print(self.routeDictionary[self.currentRoute])
                    json_string = json.dumps(self.routeDictionary)
                    with open("autolocke/Data/data.json", "w") as f:
                        f.write(json_string)
                else:
                    return
            else:
                return

            

