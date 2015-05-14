from urllib.request import *
import xml.etree.ElementTree as ET

__author__ = 'Muffin'


class RotmgPlayerInfo:
    def __init__(self, email, password):
        self.characters = []
        self.classList = None
        self.infoRetrieved = True

        self.fillClassList()
        #Confirms that we actually have info in our classList
        if(self.infoRetrieved):
            self.fillCharactersList(email, password)

    def fillClassList(self):
        self.classList = ClassList("http://static.drips.pw/rotmg/production/current/xmlc/Objects.xml")
        if(not self.classList.success):
            self.infoRetrieved = False

    def fillCharactersList(self, email, password):
        print("Honk honk, still write RotmgPlayerInfo::fillCharactersList.")
        print("It's currently in place but not doing anything!")
        file = urlopen("http://www.realmofthemadgod.com/char/list?guid=" + email + "&password=" + password)
        tree = ET.parse(file)
        file.close()


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
    classDict = {}

    def __init__(self, objectsURL):
        self.success = True

        try:
            file = urlopen(objectsURL)
            tree = ET.parse(file)
            file.close()

            root = tree.getroot()

            for obj in root:
                if(obj.attrib["id"] in self.classNames):
                    self.addToList(obj)
        except Exception:
            self.success = False

    def addToList(self, element):
        classIDString = element.attrib["type"]
        classID = int(classIDString, 16)

        self.classDict[classID] = ClassStats()
        self.classDict[classID].name = element.attrib["id"]
        self.classDict[classID].maxHp = int(element.find("MaxHitPoints").attrib["max"])
        self.classDict[classID].maxMp = int(element.find("MaxMagicPoints").attrib["max"])
        self.classDict[classID].maxAtk = int(element.find("Attack").attrib["max"])
        self.classDict[classID].maxDef = int(element.find("Defense").attrib["max"])
        self.classDict[classID].maxSpd = int(element.find("Speed").attrib["max"])
        self.classDict[classID].maxDex = int(element.find("Dexterity").attrib["max"])
        self.classDict[classID].maxVit = int(element.find("HpRegen").attrib["max"])
        self.classDict[classID].maxWis = int(element.find("MpRegen").attrib["max"])

class RotmgCharacter:
    def __init__(self):
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
