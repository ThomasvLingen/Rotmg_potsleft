from urllib.request import *
import math
import xml.etree.ElementTree as ET
import time
from colorama import *

#NOTE THAT THIS ONLY RUNS ON WINDOWS BECAUSE REASONS.
__author__ = 'Muffin'

EMAIL = "YOUR EMAIL"
PASSWORD = "YOUR PASS"
ERRORPOSY = 15
FAMEPOSY = 13

def cursorPos(x, y):
    return('\x1b[' + str(y) + ";" + str(x) + "H")

class Player:
    def __init__(self):
        self.name = ""
        self.classID = -1
        self.hp = -1
        self.mp = -1
        self.atk = -1
        self.defen = -1
        self.spd = -1
        self.dex = -1
        self.vit = -1
        self.wis = -1
        self.fame = -1

    def fill(self):
        file = urlopen("http://www.realmofthemadgod.com/char/list?guid=" + EMAIL + "&password=" + PASSWORD)
        tree = ET.parse(file)
        file.close()
        root = tree.getroot()

        if(root.tag == "Error"):
            return False
        else:
            self.fillByElement(root.find("Char"))
            return True

    def fillByElement(self, element):
        self.name = element.find("./Account/Name").text
        self.classID = int(element.find("ObjectType").text)
        self.hp = int(element.find("MaxHitPoints").text)
        self.mp = int(element.find("MaxMagicPoints").text)
        self.atk = int(element.find("Attack").text)
        self.defen = int(element.find("Defense").text)
        self.spd = int(element.find("Speed").text)
        self.dex = int(element.find("Dexterity").text)
        self.vit = int(element.find("HpRegen").text)
        self.wis = int(element.find("MpRegen").text)
        self.fame = int(element.find("CurrentFame").text)

class ClassStats():
    def __init__(self):
        self.name = ""
        self.maxHp = -1
        self.maxMp = -1
        self.maxAtk = -1
        self.maxDef = -1
        self.maxSpd = -1
        self.maxDex = -1
        self.maxVit = -1
        self.maxWis = -1

    def printStats(self):
        print("\nStats for class: " + self.name)
        print("Max Hp: " + str(self.maxHp))
        print("Max Mp: " + str(self.maxMp))
        print("Max Attack: " + str(self.maxAtk))
        print("Max Defense: " + str(self.maxDef))
        print("Max Speed: " + str(self.maxSpd))
        print("Max Dexterity: " + str(self.maxDex))
        print("Max Vitality: " + str(self.maxVit))
        print("Max Wisdom: " + str(self.maxWis))

class ClassList():
    classNames = ["Archer", "Wizard", "Priest", "Warrior", "Knight", "Paladin", "Assassin", "Necromancer", "Huntress", "Mystic", "Trickster", "Sorcerer", "Ninja"]
    classList = {}

    def __init__(self, url):
        file = urlopen(url)
        tree = ET.parse(file)
        file.close()

        root = tree.getroot()

        for obj in root:
            if(obj.attrib["id"] in self.classNames):
                self.addToList(obj)

    def addToList(self, element):
        classIDString = element.attrib["type"]
        classID = int(classIDString, 16)

        self.classList[classID] = ClassStats()
        self.classList[classID].name = element.attrib["id"]
        self.classList[classID].maxHp = int(element.find("MaxHitPoints").attrib["max"])
        self.classList[classID].maxMp = int(element.find("MaxMagicPoints").attrib["max"])
        self.classList[classID].maxAtk = int(element.find("Attack").attrib["max"])
        self.classList[classID].maxDef = int(element.find("Defense").attrib["max"])
        self.classList[classID].maxSpd = int(element.find("Speed").attrib["max"])
        self.classList[classID].maxDex = int(element.find("Dexterity").attrib["max"])
        self.classList[classID].maxVit = int(element.find("HpRegen").attrib["max"])
        self.classList[classID].maxWis = int(element.find("MpRegen").attrib["max"])

def printPotsWindow():
    print("Displaying pots left for player: \n")
    print("/=====================")
    print("| Life pots left:    |")
    print("| Mana pots left:    |")
    print("| ATK  pots left:    |")
    print("| DEF  pots left:    |")
    print("| SPD  pots left:    |")
    print("| DEX  pots left:    |")
    print("| VIT  pots left:    |")
    print("| WIS  pots left:    |")
    print("=====================/")
    print(cursorPos(1, FAMEPOSY+1) + Fore.RED + "[                    ]" + Style.RESET_ALL)

def printFameBar(player):
    #Draw fame amount
    fameAmountString = "Fame: " + str(player.fame) + "/" + str(getFameQuest(player.fame))
    fameAmountStringX = int((20 - len(fameAmountString)) / 2) + 1
    print(cursorPos(1, FAMEPOSY) + "                    ")
    print(cursorPos(1+fameAmountStringX, FAMEPOSY) + Fore.RED + fameAmountString + Style.RESET_ALL)

    #Draw fame bar
    barAmount = round(player.fame / getFameQuest(player.fame) * 100 / 5)
    bars = "="
    bars *= barAmount
    print(cursorPos(2, FAMEPOSY+1) + "                    ")
    print(cursorPos(2, FAMEPOSY+1) + Fore.RED + bars + Style.RESET_ALL)

def getFameQuest(fame):
    fameQuests = [20, 150, 400, 800, 2000]
    for i in range(0, 5):
        if(fame < fameQuests[i]):
            return fameQuests[i]

def printPotsLeft(classList, player):
    #contains all values which we will shove in the PotsWindow
    potsLeftValues = [str(int(math.ceil(classList.classList[player.classID].maxHp/5 - player.hp/5))),
                      str(int(math.ceil(classList.classList[player.classID].maxMp/5 - player.mp/5))),
                      str(classList.classList[player.classID].maxAtk - player.atk),
                      str(classList.classList[player.classID].maxDef - player.defen),
                      str(classList.classList[player.classID].maxSpd - player.spd),
                      str(classList.classList[player.classID].maxDex - player.dex),
                      str(classList.classList[player.classID].maxVit - player.vit),
                      str(classList.classList[player.classID].maxWis - player.wis)]

    #print name
    print(cursorPos(34, 1) + player.name)

    #print stats
    for i in range(0, 8):
        print(cursorPos(19, 4+i) + "  ")
        print(cursorPos(19, 4+i) + potsLeftValues[i])

if __name__ == '__main__':
    #init for colorama
    init()
    #Grab class information
    classes = ClassList("http://static.drips.pw/rotmg/production/current/xmlc/Objects.xml")

    #Grab information from the player
    player = Player()
    player.fill()

    printPotsWindow()

    while(1):
        successfulFill = player.fill()

        if(successfulFill):
            printPotsLeft(classes, player)
            printFameBar(player)
            print(cursorPos(1, ERRORPOSY) + "                      ", end="")#Removes the error message if it was there
        else:
            print(cursorPos(1, ERRORPOSY) + "    Please log out    ", end="")#Error message
        time.sleep(1)