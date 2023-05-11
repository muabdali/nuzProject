import pyautogui
import pytesseract
from PIL import ImageEnhance, Image
import time
from fuzzyCheck import fuzzChecker
from pytessGrayscaletest import *
import json


# Define the region of the screen to capture
x, y, width, height = 242, 47, 745, 121

# Take a screenshot of the region and save it as an image file
#screenshot = pyautogui.screenshot(region=(x, y, width, height))
#screenshot.save('screenshot.png')

# Load the image file and extract text from it

cordsDictionary = {
    'Route':[242, 47, 745, 121],
    'Pokemon':[300, 110, 450, 121],
    'Caught':[270, 800, 380, 207]
}

routePokemonDict = {
    'PALLET TOWN': None,
    'ROUTE 1': None,
    'VIRIDIAN CITY': None,
    'ROUTE 22': None,
    'ROUTE 2': None,
    'VIRIDIAN FOREST': None,
    'ROUTE 3': None,
    'ROUTE 4': None,
    'MT. MOON': None,
    'CERULEAN CITY': None,
    'ROUTE 24': None,
    'ROUTE 25': None,
    'ROUTE 5': None,
    'ROUTE 6': None,
    'VERMILION CITY': None,
    'ROUTE 11': None,
    'DIGLETTS CAVE': None,
    'ROUTE 9': None,
    'ROUTE 10': None,
    'ROCK TUNNEL': None,
    'POKÉMON TOWER': None,
    'ROUTE 12': None,
    'ROUTE 8': None,
    'ROUTE 7': None,
    'CELADON CITY': None,
    'SAFFRON CITY': None,
    'ROUTE 16': None,
    'ONE ISLAND':None,
    'TWO ISLAND':None,
    'THREE ISLAND':None,
    'BERRY FOREST':None,
    'BOND BRIDGE':None,
    'MOUNT EMBER':None,
    'ROUTE 18':None,
    'ROUTE 20':None,
    'KINDLE ROAD':None,
    'ROUTE 18':None,
    'SAFARI ZONE':None,
    'ROUTE 15':None

}


class ImageDiscover:
    def __init__(self, cordsDictionary, routeDict):
        self.dict = cordsDictionary
        self.oldtext = ''
        self.currentPokemon = ''
        self.currentRoute = ''
        self.routeDictionary = routeDict

    def takeScreenshot(self, section_name):
        self.section = cordsDictionary[section_name]
        x, y, width, height = self.section[0], self.section[1], self.section[2], self.section[3]
        screenshot = pyautogui.screenshot(region=(x, y, width, height))
        screenshot.save(f'{section_name}Image.png')


    def appendRoutePokeDict(self, CurrentRoute, CaughtPokemon):
        self.dict[CurrentRoute] = CaughtPokemon
        print(self.dict[CurrentRoute])


    def screenshotAnalyze(self, requestedImage):
        ia = fuzzChecker
        text = imageEnhancer.enhanceFunction(requestedImage)
        if requestedImage == 'routeImage.png':
            text = imageEnhancer.enhanceFunction(requestedImage)
            stripText = text.strip()
            routeFuzz = ia.checkList('fireredroutes.txt',stripText, minScore=76)
            print(routeFuzz)
            print(self.currentRoute + "CURRENT ROUTE SELF")
            
            if routeFuzz in self.routeDictionary:
                print("in dict")
                routeFuzzFinal = routeFuzz
                self.currentRoute = routeFuzzFinal
        elif requestedImage == 'CaughtImage.png':
            text = imageEnhancer.enhanceFunction(requestedImage)
            if "Gotcha" in text:
                print("if caught")
                if "!" in text:
                    gotchaOrNot, pokemonName = text.split("!\n")
                elif "|\n" in text:
                    gotchaOrNot, pokemonName = text.split("|\n")
                fuzz_pokemonName = ia.checkList('NatDexPokemonG3.txt', pokemonName)
                print(gotchaOrNot, pokemonName)
                print(fuzz_pokemonName)
                if gotchaOrNot == 'Gotcha ':
                    print(f"Caught {fuzz_pokemonName} in {self.currentRoute}")
                    self.routeDictionary[self.currentRoute] = fuzz_pokemonName
                    print(self.routeDictionary[self.currentRoute])
                    json_string = json.dumps(self.routeDictionary)
                    with open("data.json", "w") as f:
                        f.write(json_string)

                else:
                    return
            else:
                return

            
# NEED TO CHANGE WHICH JSON FILE GETS CAUGHT UPDATES LINE 117
