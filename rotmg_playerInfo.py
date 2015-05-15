from urllib.request import *
import xml.etree.ElementTree as ET

__author__ = 'Muffin'


class RotmgPlayerInfo:
    def __init__(self, email, password):
        self.characters = []
        self.email = email
        self.password = password
        self.name = ""
        self.classList = None
        self.classInfoRetrieved = False
        self.ableToUpdate = False

        self.classInfoRetrieved = self.fillClassList()
        # Confirms that we actually have info in our classList
        if (self.classInfoRetrieved):
            self.ableToUpdate = self.updateCharacters()

    def fillClassList(self):
        self.classList = ClassList("http://static.drips.pw/rotmg/production/current/xmlc/Objects.xml")
        return self.classList.success

    def updateCharacters(self):
        try:
            file = urlopen("http://www.realmofthemadgod.com/char/list?guid=" + self.email + "&password=" + self.password)
            tree = ET.parse(file)
            file.close()
            root = tree.getroot()
        except ET.ParseError:
            return False

        if(root.tag == "Error"):
            print("Couldn't retrieve character information!")
            print("Error: " + root.text)
            return(False)
        else:
            self.name = root.find("Char/Account/Name").text
            # Empty the characters list so we won't get any old results
            self.characters.clear()
            for character in root.findall("Char"):
                self.addCharacterByElement(character)
            return(True)


    def addCharacterByElement(self, element):
        char = RotmgCharacter()
        char.classID = int(element.find("ObjectType").text)
        char.hp = int(element.find("MaxHitPoints").text)
        char.mp = int(element.find("MaxMagicPoints").text)
        char.atk = int(element.find("Attack").text)
        char.defen = int(element.find("Defense").text)
        char.spd = int(element.find("Speed").text)
        char.dex = int(element.find("Dexterity").text)
        char.vit = int(element.find("HpRegen").text)
        char.wis = int(element.find("MpRegen").text)
        char.fame = int(element.find("CurrentFame").text)

        self.characters.append(char)

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
    classNames = ["Archer", "Wizard", "Priest", "Warrior", "Knight", "Paladin", "Assassin", "Necromancer", "Huntress",
                  "Mystic", "Trickster", "Sorcerer", "Ninja"]
    classDict = {}

    def __init__(self, objectsURL):
        self.success = True

        try:
            file = urlopen(objectsURL)
            tree = ET.parse(file)
            file.close()

            root = tree.getroot()

            for obj in root:
                if (obj.attrib["id"] in self.classNames):
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

    def printStats(self):
        print("HP: " + str(self.hp))
        print("MP: " + str(self.mp))
        print("ATK: " + str(self.atk))
        print("DEF: " + str(self.defen))
        print("SPD: " + str(self.spd))
        print("DEX: " + str(self.dex))
        print("VIT: " + str(self.vit))
        print("WIS: " + str(self.wis))
        print("FAME: " + str(self.fame))
