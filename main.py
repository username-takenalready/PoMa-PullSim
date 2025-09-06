# from colorama import Fore as fore
# from colorama import Style as style
from random import uniform, choice
from time import sleep
from os import system
from math import floor

red = "\033[0;31m"
blue = "\033[0;34m"
brown = "\033[0;33m"
green = "\033[0;32m"
yellow = "\033[1;33m"
cyan = "\033[0;36m"
magenta = "\033[0;35m"

bold = "\033[1m"
grey = "\033[1;30m"

rainbowList = [red, yellow, green, blue, cyan, magenta]

pullInt = 0.2

def stars2color(stars):
  if stars == 3:
    return brown
  elif stars == 4:
    return grey
  elif stars == 5:
    return yellow

def type2color(type):
  match type:
    case "pokeFair":
      return blue
    case "2xPF":
      return blue
    case "3xPF":
      return blue
    case "ticket":
      return blue
    case "masterFair":
      return magenta
    case "EXMF":
      return magenta
    case "3xMF":
      return magenta
    case 'ticketM':
      return magenta
    case "arcSuitFair":
      return yellow
    case "spotlight":
      return brown
    case "3xSP":
      return brown
    case "mix":
      return red
    case "variety":
      return red
    case "2xV":
      return red
    case "3xV":
      return red
    case "superVariety":
      return red
    case "seasonal":
      return green
    case "seasonalRerun":
      return green
    case "2xSE":
      return green
    case "costume":
      return green
    case "superCostume":
      return green
    case "2xSC":
      return green
    case "gym":
      return cyan
    case "daily":
      return cyan
    case _:
      return reset()
    
def rainbow(text):
  str = [bold]
  for i in range(len(text)):
    str.append(rainbowList[i % len(rainbowList)] + text[i] + reset())
  return "".join(str)

def reset(): return "\033[0m"

def sortByObtain(list, obtain): return [pair for pair in list if pair.obtain == obtain]

def awaitEnter(): input("Press Enter to continue...")

def clear(): system("clear")
  
class Pair:
  def __init__(self, stars, ex, obtain, name, pkmn, nick, nonick = False):
    self.stars = stars
    self.ex = ex
    self.obtain = obtain
    self.name = name
    self.nick = nick
    self.pkmn = pkmn
    self.nonick = nonick
    self.featured = False
    
  def __str__(self):
    return f"{stars2color(self.stars)}{self.stars}★{'EX' if self.ex else ''} {self.name + ' & '+ self.pkmn}{reset()}"
  
  def literal(self):
    return f"{self.stars}★{'EX' if self.ex else ''} {self.name + ' & '+ self.pkmn}"

class Banner:
  def __init__(self, name, featuredPairs, type, genPool = True, fiveStarOnly = False, mixPool = False, dailyPool = False, featured2 = []):
    self.name = type2color(type) + name + reset()
    self.featuredPairs = featuredPairs
    self.featured2 = featured2
    self.type = type
    self.genPool = genPool
    self.fiveStarOnly = fiveStarOnly
    self.mixPool = mixPool
    self.dailyPool = dailyPool
    self.pity = False 
    self.singles = 0
    self.multis = 0
    
    if self.type == "spotlight":
      self.rates = [2, 7, 27]
    elif self.type == "3xSP":
      self.rates = [4.5, 7, 27]
    elif self.type == "pokeFair":
      self.rates = [2, 10, 30]
    elif self.type == "masterFair":
      self.rates = [1, 12, 32]
    elif self.type == "EXMF":
      self.rates = [1, 2, 3, 12, 32]
    elif self.type == "arcSuitFair":
      self.rates = [1, 12, 32]
    elif self.type == "mix":
      self.rates = [2, 7, 27]
    elif self.type == "daily":
      self.rates = [0.02, 1, 5]
    elif self.type == "gym":
      self.rates = [2, 7, 27]
    elif self.type == "2xPF":
      self.rates = [3, 10, 27]
    elif self.type == "3xPF":
      self.rates = [4.5, 10, 26]
    elif self.type == "3xMF":
      self.rates = [1, 12, 32]
    elif self.type == "superScout":
      self.rates = [2, 10, 30] # maybe?
    elif self.type == "costume":
      self.rates = [2, 7, 27]
    elif self.type == "superCostume":
      self.rates = [2, 7, 27]
    elif self.type == "2xSC":
      self.rates = [3, 7, 27]
    elif self.type == "seasonal":
      self.rates = [2, 7, 27]
    elif self.type == "2xSE":
      self.rates = [3, 7, 27]
    elif self.type == "seasonalRerun":
      self.rates = [2, 7, 27]
    elif self.type == "ticket":
      self.rates = [25, 34, 54]
    elif self.type == "10ticket":
      self.rates = [2, 7, 27]
    elif self.type == "fairTicket":
      self.rates = [2, 7, 27]
    elif self.type == "anniTicket":
      self.rates = [0, 7, 27]
    elif self.type == "ticketM":
      self.rates = [100, 0, 0]
    elif self.type == "gym":
      self.rates = [2, 7, 27]
    elif self.type == "variety":
      self.rates = [2, 7, 27]
    elif self.type == "2xV":
      self.rates = [3, 7, 27]
    elif self.type == "3xV":
      self.rates = [4.5, 7, 27]
    elif self.type == "superVariety":
      self.rates = [2, 7, 27]
    else:
      raise ValueError("Invalid banner type")
    if fiveStarOnly:
      self.rates = [0, 100, 100]

    if mixPool:
      self.pool5 = mixFull
    elif genPool:
      self.pool5 = fiveStarSpotlight
    if self.type == "anniTicket":
      self.pool5 = fiveStarPokeFair + seasonalFull + specialCostume + variety
    if dailyPool:
      self.featuredPairs = fiveStarMasterFair + fiveStarArcSuitFair + seasonalFull + fiveStarPokeFair + specialCostume + variety + mixExclusive

    self.pokefairs = [item for item in fiveStarPokeFair if item not in self.featured2]
    self.pairs = self.featuredPairs + self.pool5 + sortByObtain(fourStar,"General") + threeStar
    
  def __str__(self):
    return "\n".join([pair.__str__() for pair in self.featuredPairs]) if not self.dailyPool else "ALL Sync Pairs up to Feb 2025 (3 months prior)"

  def featuredtwo(self):
    return "\n".join([pair.__str__() for pair in self.featured2]) if not self.dailyPool else "ALL Sync Pairs up to Feb 2025 (3 months prior)"

  def checkPity(self):
    if self.type in ["ticket", "ticketM", "daily", "gym", "anniTicket", "10ticket"]:
      return False
    if self.multis * 33 + self.singles * 3 >= 300 and self.type == "mix":
      return True
    elif self.multis * 33 + self.singles * 3 >= 400 and self.type != "arcSuitFair":
      return True
    elif self.multis * 33 + self.singles * 3 >= 500 and self.type == "arcSuitFair":
      return True
    else:
      return False
    
  def single(self):
    factor = floor(uniform(1, 100))
    if self.type == "EXMF":
      if factor <= self.rates[0]:
        scouted = choice(self.featuredPairs)
      elif factor <= self.rates[1]:
        scouted = choice(self.featured2)
      elif factor <= self.rates[2]:
        scouted = choice(self.pokefairs)
      elif factor <= self.rates[3]:
        scouted = choice(self.pool5)
      elif factor <= self.rates[4]:
        scouted = choice(sortByObtain(fourStar, "General"))
      else:
        scouted = choice(sortByObtain(threeStar, "General"))
      self.singles += 1
      return scouted
    if self.type == "fairTicket":
      return choice(self.pokefairs)
    if factor <= self.rates[0]:
      scouted = choice(self.featuredPairs)
    elif factor <= self.rates[1]:
      scouted = choice(self.pool5)
    elif factor <= self.rates[2]:
      scouted = choice(sortByObtain(fourStar, "General"))
    else:
      scouted = choice(sortByObtain(threeStar, "General"))
    self.singles += 1
    return scouted # the variable is useless as of now

  def multi(self):
    scoutMulti = []
    for i in range(11):
      scouted = self.single()
      print(rainbow(scouted.literal()) if scouted in self.featuredPairs else scouted.__str__())
      scoutMulti.append(scouted)
      sleep(pullInt)
    self.singles -= 11
    self.multis += 1
    return scoutMulti

threeStarDict = {
  "Brawly": Pair(3, True, "General", "Brawly", "Makuhita", []),
  "Winona": Pair(3, True, "General", "Winona", "Pelipper", []),
  "Tate": Pair(3, True, "General", "Tate", "Solrock", []),
  "Liza": Pair(3, True, "General", "Liza", "Lunatone", []),
  "Maylene": Pair(3, True, "General", "Maylene", "Meditite", []),
  "Crasher Wake": Pair(3, True, "General", "Crasher Wake", "Floatzel", []),
  "Brycen": Pair(3, True, "General", "Brycen", "Cryogonal", []),
  "Marlon": Pair(3, True, "General", "Marlon", "Carracosta", []),
  "Ramos": Pair(3, True, "General", "Ramos", "Weepinbell", []),
  "Wulfric": Pair(3, True, "General", "Wulfric", "Avalugg", []),
  "Lt. Surge": Pair(3, True, "General", "Lt. Surge", "Voltorb", []),
  "Bugsy": Pair(3, True, "General", "Bugsy", "Beedril", []),
  "Janine": Pair(3, True, "General", "Janine", "Ariados", []),
  "Roxanne": Pair(3, True, "General", "Roxanne", "Nosepass", []),
  "Roark": Pair(3, True, "General", "Roark", "Cranidos", []),
  "Candice": Pair(3, True, "General", "Candice", "Abomasnow", []),
  "Cheryl": Pair(3, True, "General", "Cheryl", "Chansey", []),
  "Marley": Pair(3, True, "General", "Marley", "Arcanine", []),
  "Clan": Pair(3, True, "General", "Clan", "Palpitoad", []),
  "Mina": Pair(3, True, "General", "Mina", "Granbull", [])
}

threeStar = list(threeStarDict.values())

fourStarDict = {
  "Blaine": Pair(4, True, "General", "Blaine", "Rapidash", []),
  "Lucy": Pair(4, True, "General", "Lucy", "Seviper", []),
  "Grant": Pair(4, True, "General", "Grant", "Amaura", []),
  "Kahili": Pair(4, True, "General", "Kahili", "Toucannon", []),
  "Lorelei": Pair(4, True, "General", "Lorelei", "Lapras", []),
  "Bruno": Pair(4, True, "General", "Bruno", "Machomp", []),
  "Agatha": Pair(4, True, "General", "Agatha", "Gengar", []),
  "Will": Pair(4, True, "General", "Will", "Xatu", []),
  "Drake": Pair(4, True, "General", "Drake", "Salamence", []),
  "Thorton": Pair(4, True, "General", "Thorton", "Bronzong", []),
  "Shauntal": Pair(4, True, "General", "Shauntal", "Chandelure", []),
  "Wikstrom": Pair(4, True, "General", "Wikstrom", "Aegislash", []),
  "Sophocles": Pair(4, True, "General", "Sophocles", "Togedemaru", []),
  "Rachel": Pair(4, True, "Fair-Exclusive", "Rachel", "Umbreon", []),
  "Honchkrow": Pair(4, True, "Fair-Exclusive", "Sawyer", "Honchkrow", []),
  "Tina": Pair(4, True, "Fair-Exclusive", "Tina", "Flareon", []),
  "Whitney": Pair(4, True, "General", "Whitney", "Miltank", []),
  "Gardenia": Pair(4, True, "General", "Gardenia", "Roserade", []),
  "Roxie": Pair(4, True, "General", "Roxie", "Scolipede", []),
  "Siebold": Pair(4, True, "General", "Siebold", "Clawitzer", []),
  "Noland": Pair(4, True, "General", "Noland", "Pinsir", []),
  "Marshal": Pair(4, True, "General", "Marshal", "Conkeldurr", [])
}

fourStar = list(fourStarDict.values())

fiveStarSpotlightDict = {
  "Blue": Pair(5, True, "General", "Blue", "Pidgeot", []),
  "Leaf": Pair(5, True, "General", "Leaf", "Eevee", []),
  "SS Misty": Pair(5, True, "General", "Sygna Suit Misty", "Vaporeon", ["SS Misty", "ss misty"]),
  "SS Erika": Pair(5, True, "General", "Sygna Suit Erika", "Leafeon", ["SS Erika", "ss erika"]),
  "Sabrina": Pair(5, True, "General", "Sabrina", "Alakazam", []),
  "Ethan": Pair(5, True, "General", "Ethan", "Cyndaquil", []),
  "Lyra": Pair(5, True, "General", "Lyra", "Chikorita", []),
  "Kris": Pair(5, True, "General", "Kris", "Totodile", []),
  "Falkneer": Pair(5, True, "General", "Falkneer", "Swellow", []),
  "Morty": Pair(5, True, "General", "Morty", "Drifblim", []),
  "Chuck": Pair(5, True, "General", "Chuck", "Poliwrath", []),
  "Jasmine": Pair(5, True, "General", "Jasmine", "Steelix", []),
  "Karen": Pair(5, True, "General", "Karen", "Houndoom", []),
  "Brendan": Pair(5, True, "General", "Brendan", "Treecko", []),
  "May": Pair(5, True, "General", "May", "Mudkip", []),
  "Wally": Pair(5, True, "General", "Wally", "Gallade", []),
  "Wallace": Pair(5, True, "General", "Wallace", "Milotic", []),
  "Sidney": Pair(5, True, "General", "Sidney", "Absol", []),
  "Phoebe": Pair(5, True, "General", "Phoebe", "Dusclops", []),
  "Glacia": Pair(5, True, "General", "Glacia", "Glalie", []),
  "Lisia": Pair(5, True, "General", "Lisia", "Altaria", []),
  "Courtney": Pair(5, True, "General", "Courtney", "Camerupt", []),
  "Dawn": Pair(5, True, "General", "Dawn", "Turtwig", []),
  "Fantina": Pair(5, True, "General", "Fantina", "Mismagius", []),
  "Volkneer": Pair(5, True, "General", "Volkneer", "Luxray", []),
  "Aaron": Pair(5, True, "General", "Aaron", "Vespiquen", []),
  "Bertha": Pair(5, True, "General", "Bertha", "Hippowdon", []),
  "Lucian": Pair(5, True, "General", "Lucian", "Girafarig", []),
  "Darach": Pair(5, True, "General", "Darach", "Staraptor", []),
  "Hilbert": Pair(5, True, "General", "Hilbert", "Oshawott", []),
  "Hilda": Pair(5, True, "General", "Hilda", "Tepig", []),
  "Bianca": Pair(5, True, "General", "Bianca", "Musharna", []),
  "Nate": Pair(5, True, "General", "Nate", "Braviary", []),
  "Hugh": Pair(5, True, "General", "Hugh", "Buffalant", []),
  "Lenora": Pair(5, True, "General", "Lenora", "Watchog", []),
  "Burgh": Pair(5, True, "General", "Burgh", "Leavanny", []),
  "Elesa": Pair(5, True, "General", "Elesa", "Zebstrika", []),
  "SS Elesa":  Pair(5, True, "General", "Sygna Suit Elesa", "Rotom", ["SS Elesa","ss elesa"]),
  "Caitlin": Pair(5, True, "General", "Caitlin", "Reuniclus", []),
  "Grimsley": Pair(5, True, "General", "Grimsley", "Liepard", []),
  "SS Grimsley": Pair(5, True, "General", "Sygna Suit Grimsley", "Sharpedo", ["SS Grimsley","ss grimsley"]),
  "Colress": Pair(5, True, "General", "Colress", "Klinklang", []),
  "Serena": Pair(5, True, "General", "Serena", "Fennekin", []),
  "Tierno": Pair(5, True, "General", "Tierno", "Crawdaunt", []),
  "Trevor": Pair(5, True, "General", "Trevor", "Florges", []),
  "Shauna": Pair(5, True, "General", "Shauna", "Chesnaught", []),
  "Clemont": Pair(5, True, "General", "Clemont", "Heliolisk", []),
  "Olympia": Pair(5, True, "General", "Olympia", "Sigilyph", []),
  "Malva": Pair(5, True, "General", "Malva", "Talonflame", []),
  "Drasna": Pair(5, True, "General", "Drasna", "Dragalge", []),
  "Looker": Pair(5, True, "General", "Looker", "Croagunk", []),
  "Elio": Pair(5, True, "General", "Elio", "Popplio", []),
  "Selene": Pair(5, True, "General", "Selene", "Rowlet", []),
  "Lillie": Pair(5, True, "General", "Lillie", "Clefairy", []),
  "Gladion": Pair(5, True, "General", "Gladion", "Silvally", []),
  "Ilima": Pair(5, True, "General", "Ilima", "Gumshoos", []),
  "Lana": Pair(5, True, "General", "Lana", "Araquanid", []),
  "Kiawe": Pair(5, True, "General", "Kiawe", "Marowak-Alola", []),
  "Mallow": Pair(5, True, "General", "Mallow", "Tsareena", []),
  "Hala": Pair(5, True, "General", "Hala", "Crabominable", []),
  "Olivia": Pair(5, True, "General", "Olivia", "Lycanroc-Midnight", []),
  "K.Grimsley": Pair(5, True, "General", "Grimsley (Kimono)", "Bisharp", ["Grimsley Kimono","Grimsley Alt", "AltGrimsley", "KimonoGrimsley", "kimonoGrimsley", "AGrimsley"]),
  "Ryuki": Pair(5, True, "General", "Ryuki", "Turtnator", []),
  "Lusamine": Pair(5, True, "General", "Lusamine", "Pheromosa", []),
  "Plumeria": Pair(5, True, "General", "Plumeria", "Salazzle", []),
  "Guzma": Pair(5, True, "General", "Guzma", "Golisopod", []),
  "Kukui": Pair(5, True, "General", "Kukui", "Lycanroc-Midday", []),
  "A.Kukui": Pair(5, True, "General", "The Masked Royal", "Incineroar", ["AltKukui", "AKukui", "MaskedRoyal", "MaskKukui", "Masked Royal"]),
  "Nessa": Pair(5, True, "General", "Nessa", "Drednaw", []),
  "Bea": Pair(5, True, "General", "Bea", "Sirfetch'd", []),
  "Allister": Pair(5, True, "General", "Allister", "Gengar", []),
  "Gordie": Pair(5, True, "General", "Gordie", "Coalossal", []),
  "Melony": Pair(5, True, "General", "Melony", "Lapras", []),
  "Piers": Pair(5, True, "General", "Piers", "Obstagoon", []),
  "Sonia": Pair(5, True, "General", "Sonia", "Yamper", [])
}

fiveStarSpotlight = list(fiveStarSpotlightDict.values())

fiveStarPokeFairDict = {
  "Red": Pair(5, True, "Fair-Exclusive", "Red", "Snorlax", []),
  "Chase": Pair(5, True, "Fair-Exclusive", "Chase", "Pikachu", []),
  "Elaine": Pair(5, True, "Fair-Exclusive", "Elaine", "Eevee", []),
  "Lance": Pair(5, True, "Fair-Exclusive", "Lance", "Dragonite", []),
  "C.Blue": Pair(5, True, "Fair-Exclusive", "Blue (Classic)", "Aerodactyl", ["ClassicBlue", "Classic Blue", "CBlue"]),
  "SS Silver": Pair(5, True, "Fair-Exclusive", "Sygna Suit Silver", "Sneasel", ["SS Silver", "ss silver"]),
  "SS Morty": Pair(5, True, "Fair-Exclusive", "Sygna Suit Morty", "Ho-Oh", ["SS Morty", "ss morty"]),
  "Eusine": Pair(5, True, "Fair-Exclusive", "Eusine", "Suicune", []),
  "SS Giovanni": Pair(5, True, "Fair-Exclusive", "Sygna Suit Giovanni", "Nidoking", ["SS Giovanni", "ss giovanni"]),
  "SS Brendan": Pair(5, True, "Fair-Exclusive", "Sygna Suit Brendan", "Latios", ["SS Brendan", "ss brendan"]),
  "anni May": Pair(5, True, "Fair-Exclusive", "May (Anniversary 2022)", "Latias", ["anni may", "Anni May", "anniMay","AnniMay", "anni May"]),
  "SS May": Pair(5, True, "Fair-Exclusive", "Sygna Suit May", "Blaziken", ["SS May", "ss may"]),
  "SS Wally": Pair(5, True, "Fair-Exclusive", "Sygna Suit Wally", "Gardevoir", ["SS Wally", "ss wally"]),
  "Steven": Pair(5, True, "Fair-Exclusive", "Steven", "Metagross", []),
  "SS Steven": Pair(5, True, "Fair-Exclusive", "Sygna Suit Steven", "Deoxys", ["SS Steven", "ss steven", "SSS"]),
  "Greta": Pair(5, True, "Fair-Exclusive", "Greta", "Breloom", []),
  "Lucas": Pair(5, True, "Fair-Exclusive", "Lucas", "Dialga", []),
  "SS Dawn": Pair(5, True, "Fair-Exclusive", "Sygna Suit Dawn", "Cresselia", ["SS Dawn", "ss dawn"]),
  "Cynthia": Pair(5, True, "Fair-Exclusive", "Cynthia", "Garchomp", []),
  "SS Cynthia": Pair(5, True, "Fair-Exclusive", "Sygna Suit Cynthia", "Kommo-o", ["SS Cynthia", "ss cynthia"]),
  "Dahlia": Pair(5, True, "Fair-Exclusive", "Dahlia", "Ludicolo", []),
  "Palmer": Pair(5, True, "Fair-Exclusive", "Palmer", "Regigigas", []),
  "Argenta": Pair(5, True, "Fair-Exclusive", "Argenta", "Skarmory", []),
  "SS Cyrus": Pair(5, True, "Fair-Exclusive", "Sygna Suit Cyrus", "Darkrai", ["SS Cyrus", "ss cyrus"]),
  "Rei": Pair(5, True, "Fair-Exclusive", "Rei", "Decidueye-Hisui", []),
  "Akari": Pair(5, True, "Fair-Exclusive", "Akari", "Samurott-Hisui", []),
  "Volo": Pair(5, True, "Fair-Exclusive", "Volo", "Togepi", []),
  "SS Hilbert": Pair(5, True, "Fair-Exclusive", "Sygna Suit Hilbert", "Genesect", ["SS Hilbert", "ss hilbert"]),
  "SS Hilda": Pair(5, True, "Fair-Exclusive", "Sygna Suit Hilda", "Victini", ["SS Hilda", "ss hilda"]),
  "C.Elesa": Pair(5, True, "Fair-Exclusive", "Elesa (Classic)", "Emolga", ["CElesa", "ClassicElesa", "Classic Elesa", "classicElesa", "AltElesa"]),
  "SSA Elesa": Pair(5, True, "Fair-Exclusive", "Sygna Suit (Alt.) Elesa", "Thundurus-Therian", ["SSA Elesa", "ssa elesa"]),
  "anni Skyla": Pair(5, True, "Fair-Exclusive", "Skyla (Anniversary 2022)", "Tornadus-Therian", ["anni skyla", "Anni Skyla", "anni Skyla", "anniSkyla", "AnniSkyla"]),
  "C.Iris": Pair(5, True, "Fair-Exclusive", "Iris (Alt.)", "Hydreigon", ["C.Iris", "AltIris", "Alt Iris", "A.Iris","Iris alt", "Iris Alt", "Champion Iris", "Iris (Champion)"]),
  "SS Roxie": Pair(5, True, "Fair-Exclusive", "Sygna Suit Roxie", "Toxtricity", ["SS Roxie", "ss roxie"]),
  "Alder": Pair(5, True, "Fair-Exclusive", "Alder", "Volcarona", []),
  "Ingo": Pair(5, True, "Fair-Exclusive", "Ingo", "Excadrill", ["submas 1", "submas white"]),
  "SS Ingo": Pair(5, True, "Fair-Exclusive", "Sygna Suit Ingo", "Chandelure", ["SS Ingo", "ss ingo"]),
  "Emmet": Pair(5, True, "Fair-Exclusive", "Emmet", "Archeops", ["submas 2", "submas black"]),
  "SS Emmet": Pair(5, True, "Fair-Exclusive", "Sygna Suit Emmet", "Eelektross", ["SS Emmet", "ss emmet"]),
  "Benga": Pair(5, True, "Fair-Exclusive", "Benga", "Volcarona", []),
  "N": Pair(5, True, "Fair-Exclusive", "N", "Zekrom", []),
  "SS N": Pair(5, True, "Fair-Exclusive", "Sygna Suit N", "Kyurem-Black", ["SS N", "ss n"]),
  "Sina": Pair(5, True, "Fair-Exclusive", "Sina", "Glaceon", []),
  "Dexio": Pair(5, True, "Fair-Exclusive", "Dexio", "Espeon", []),
  "SS Korrina": Pair(5, True, "Fair-Exclusive", "Sygna Suit Korrina", "Marshadow", ["SS Korrina", "ss korrina"]),
  "Diantha": Pair(5, True, "Fair-Exclusive", "Diantha", "Gardevoir", []),
  "SS Diantha": Pair(5, True, "Fair-Exclusive", "Sygna Suit Diantha", "Diancie", ["SS Diantha", "ss diantha"]),
  "Emma": Pair(5, True, "Fair-Exclusive", "Emma", "Crobat", []),
  "Lysandre": Pair(5, True, "Fair-Exclusive", "Lysandre", "Yveltal", []),
  "SS Lysandre": Pair(5, True, "Fair-Exclusive", "Sygna Suit Lysandre", "Volcanion", ["SS Lysandre", "ss lysandre"]),
  "A.Elio": Pair(5, True, "Fair-Exclusive", "Elio (Alt.)", "Stakataka", ["Alt Elio", "alt elio", "A.Elio"]),
  "A.Selene": Pair(5, True, "Fair-Exclusive", "Selene (Alt.)", "Nihilego", ["Alt Selene", "alt selene", "A.Selene"]),
  "SS Hau": Pair(5, True, "Fair-Exclusive", "Sygna Suit Hau", "Tapu Koko", ["SS Hau", "ss hau"]),
  "SS Lana": Pair(5, True, "Fair-Exclusive", "Sygna Suit Lana", "Tapu Lele", ["SS Lana", "ss lana"]),
  "SS Mina": Pair(5, True, "Fair-Exclusive", "Sygna Suit Mina", "Tapu Bulu", ["SS Mina", "ss mina"]),
  "SS Acerola": Pair(5, True, "Fair-Exclusive", "Sygna Suit Acerola", "Tapu Fini", ["SS Acerola", "ss acerola"]),
  "Anabel": Pair(5, True, "Fair-Exclusive", "Anabel", "Snorlax", []),
  "Victor": Pair(5, True, "Fair-Exclusive", "Victor", "Rillaboom", []),
  "Gloria": Pair(5, True, "Fair-Exclusive", "Gloria", "Zacian-Crowned", []),
  "D.Gloria": Pair(5, True, "Fair-Exclusive", "Gloria (Dojo Uniform)", "Urshifu", ["A.Gloria", "D.Gloria", "Dojo Gloria", "DojoGloria", "dojoGloria","DU Gloria", "Alt Gloria", "AltGloria","A1 Gloria"]),
  "A2Gloria": Pair(5, True, "Fair-Exclusive", "Gloria (Alt. 2)", "Cinderace", ["A.2. Gloria", "Alt 2 Gloria", "Alt2 Gloria","alt 2 gloria", "alt2 gloria", "A2 Gloria"]),
  "Marnie": Pair(5, True, "Fair-Exclusive", "Marnie", "Morpeko", []),
  "Bede": Pair(5, True, "Fair-Exclusive", "Bede", "Hatterene", []),
  "SS Bede": Pair(5, True, "Fair-Exclusive", "Sygna Suit Bede", "Iron Valiant", ["SS Bede", "ss bede"]),
  "Milo": Pair(5, True, "Fair-Exclusive", "Milo", "Eldegoss", []),
  "Kabu": Pair(5, True, "Fair-Exclusive", "Kabu", "Centiskorch", []),
  "SS Piers": Pair(5, True, "Fair-Exclusive", "Sygna Suit Piers", "Toxtricity-Low-Key", ["SS Piers", "ss piers"]),
  "Raihan": Pair(5, True, "Fair-Exclusive", "Raihan", "Duraludon", []),
  "anni Raihan": Pair(5, True, "Fair-Exclusive", "Raihan (Anniversary 2022)", "Flygon", ["anni raihan", "Anni Raihan", "anniRaihan", "AnniRaihan", "anni Raihan"]),
  "Klara": Pair(5, True, "Fair-Exclusive", "Klara", "Slowbro-Galar", []),
  "Avery": Pair(5, True, "Fair-Exclusive", "Avery", "Slowking-Galar", []),
  "SS Leon": Pair(5, True, "Fair-Exclusive", "Sygna Suit Leon", "Eternatus", ["SS Leon", "ss leon"]),
  "A.Leon": Pair(5, True, "Fair-Exclusive", "Leon (Alt.)", "Dragapult", ["Alt Leon", "alt leon", "leon alt", "Leon Alt", "A. Leon"]),
  "Rose": Pair(5, True, "Fair-Exclusive", "Rose", "Copperajah", []),
  "Oleana": Pair(5, True, "Fair-Exclusive", "Oleana", "Garbodor", []),
  "Nemona": Pair(5, True, "Fair-Exclusive", "Nemona", "Pawmot", []),
  "Penny": Pair(5, True, "Fair-Exclusive", "Penny", "Sylveon", []),
  "Arven": Pair(5, True, "Fair-Exclusive", "Arven", "Mabosstiff", []),
  "Iono": Pair(5, True, "Fair-Exclusive", "Iono", "Bellibolt", []),
  "SS Iono": Pair(5, True, "Fair-Exclusive", "Sygna Suit Iono", "Raging Bolt", ["SS Iono", "ss iono"]),
  "Grusha": Pair(5, True, "Fair-Exclusive", "Grusha", "Cetitan", []),
  "Larry": Pair(5, True, "Fair-Exclusive", "Larry", "Dudunsparce", []),
  "Rika": Pair(5, True, "Fair-Exclusive", "Rika", "Clodsire", []),
  "Poppy": Pair(5, True, "Fair-Exclusive", "Poppy", "Tinkaton", []),
  "Clavell": Pair(5, True, "Fair-Exclusive", "Clavell", "Quaquaval", []),
  "Jacq": Pair(5, True, "Fair-Exclusive", "Jacq", "Farigiraf", []),
  "Giacomo": Pair(5, True, "Fair-Exclusive", "Giacomo", "Kingambit", []),
  "Eri": Pair(5, True, "Fair-Exclusive", "Eri", "Annihilape", []),
  "Mela": Pair(5, True, "Fair-Exclusive", "Mela", "Armarouge", []),
  "Atticus": Pair(5, True, "Fair-Exclusive", "Atticus", "Revavroom", []),
  "Ortega": Pair(5, True, "Fair-Exclusive", "Ortega", "Dachsbun", []),
  "Lacey": Pair(5, True, "Fair-Exclusive", "Lacey", "Granbull", []),
  "Lear": Pair(5, True, "Fair-Exclusive", "Lear", "Hoopa", []),
  "Paulo": Pair(5, True, "Fair-Exclusive", "Paulo", "Lycanroc-Dusk", []),
  "SS Red": Pair(5, True, "Fair-Exclusive", "Sygna Suit Red", "Charizard", ["SS Red", "ss red"]),
  "SS Blue": Pair(5, True, "Fair-Exclusive", "Sygna Suit Blue", "Blastoise", ["SS Blue", "ss blue"]),
  "SS Leaf": Pair(5, True, "Fair-Exclusive", "Sygna Suit Leaf", "Venusaur", ["SS Leaf", "ss leaf"]),
  "Carmine": Pair(5, True, "Fair-Exclusive", "Carmine", "Sinistcha", [])
}

fiveStarPokeFair = list(fiveStarPokeFairDict.values())

fiveStarMasterFairDict = {
  "SST Red": Pair(5, True, "Master Fair", "Sygna Suit (Thunderbolt) Red", "Pikachu", ["SST Red", "sst red"]),
  "NC Red": Pair(5, True, "Master Fair", "Red (Champion)", "Articuno", ["NC Red", "nc red"]),
  "NC Leaf": Pair(5, True, "Master Fair", "Leaf (Champion)", "Moltres", ["NC Leaf", "nc leaf"]),
  "NC Blue": Pair(5, True, "Master Fair", "Blue (Champion)", "Zapdos", ["NC Blue", "nc blue"]),
  "SS Ethan": Pair(5, True, "Master Fair", "Sygna Suit Ethan", "Lugia", ["SS Ethan", "ss ethan"]),
  "SS Lyra": Pair(5, True, "Master Fair", "Sygna Suit Lyra", "Celebi", ["SS Lyra", "ss lyra"]),
  "SS Kris": Pair(5, True, "Master Fair", "Sygna Suit Kris", "Suicune", ["SS Kris", "ss kris"]),
  "NC Silver": Pair(5, True, "Master Fair", "Silver (Champion)", "Tyranitar", ["NC Silver", "nc silver"]),
  "SSA Giovanni": Pair(5, True, "Master Fair", "Sygna Suit (Alt.) Giovanni", "Guzzlord", ["SSA Giovanni", "ssa giovanni"]),
  "NC Brendan": Pair(5, True, "Master Fair", "Brendan (Champion)", "Groudon", ["NC Brendan", "nc brendan"]),
  "NC May": Pair(5, True, "Master Fair", "May (Champion)", "Kyogre", ["NC May", "nc may"]),
  "anni Steven": Pair(5, True, "Master Fair", "Steven (Anniversary 2021)", "Rayquaza", ["Anni Steven", "anni steven", "anniSteven", "AnniSteven"]),
  "Maxie": Pair(5, True, "Master Fair", "Maxie", "Groudon", []),
  "Archie": Pair(5, True, "Master Fair", "Archie", "Kyogre", []),
  "SSR Cynthia": Pair(5, True, "Master Fair", "Sygna Suit (Renegade) Cynthia", "Giratina", ["SSR Cynthia", "ssr cynthia"]),
  "SSA Cynthia": Pair(5, True, "Master Fair", "Sygna Suit (Aura) Cynthia", "Lucario", ["SSA Cynthia", "ssa cynthia"]),
  "Adaman": Pair(5, True, "Master Fair", "Adaman", "Leafeon", []),
  "Irida": Pair(5, True, "Master Fair", "Irida", "Glaceon", []),
  "NC Cheren": Pair(5, True, "Master Fair", "Cheren (Champion)", "Tornadus", ["NC Cheren", "nc cheren"]),
  "NC Bianca": Pair(5, True, "Master Fair", "Bianca (Champion)", "Virizion", ["NC Bianca", "nc bianca"]),
  "NC Nate": Pair(5, True, "Master Fair", "Nate (Champion)", "Haxorus", ["NC Nate", "nc nate"]),
  "NC Rosa": Pair(5, True, "Master Fair", "Rosa (Champion)", "Meloetta", ["NC Rosa", "nc rosa"]),
  "anni N": Pair(5, True, "Master Fair", "N (Anniversary 2021)", "Reshiram", ["Anni N", "anni n", "AnniN", "anniN", "N anni"]),
  "NC Calem": Pair(5, True, "Master Fair", "Calem (Champion)", "Greninja", ["NC Calem", "nc calem"]),
  "SS Serena": Pair(5, True, "Master Fair", "Sygna Suit Serena", "Zygarde", ["SS Serena", "ss serena", "Zerena", "zerena"]),
  "NC Serena": Pair(5, True, "Master Fair", "Serena (Champion)", "Greninja", ["NC Serena", "nc serena"]),
  "anni Lillie": Pair(5, True, "Master Fair", "Lillie (Anniversary 2021)", "Lunala", ["Anni Lillie", "anni lillie", "anniLillie", "AnniLillie", "Lillie anni"]),
  "SS Lusamine": Pair(5, True, "Master Fair", "Sygna Suit Lusamine", "Necrozma-Dusk-Mane", ["SS Lusamine", "ss lusamine"]),
  "SS Gladion": Pair(5, True, "Master Fair", "Sygna Suit Gladion", "Magearna", ["SS Gladion", "ss gladion"]),
  "NC Hop": Pair(5, True, "Master Fair", "Hop (Champion)", "Zapdos-Galar", ["NC Hop", "nc hop"]),
  "NC Marnie": Pair(5, True, "Master Fair", "Marnie (Champion)", "Moltres-Galar", ["NC Marnie", "nc marnie"]),
  "NC Bede": Pair(5, True, "Master Fair", "Bede (Champion)", "Articuno-Galar", ["NC Bede", "nc bede"]),
  "Leon": Pair(5, True, "Master Fair", "Leon", "Charizard", []),
  "SS Nemona": Pair(5, True, "Master Fair", "Sygna Suit Nemona", "Scream Tail", ["SS Nemona", "ss nemona"]),
  "Juliana": Pair(5, True, "Master Fair", "Juliana", "Koraidon", []),
  "Florian": Pair(5, True, "Master Fair", "Florian", "Miraidon", []),
  "Geeta": Pair(5, True, "Master Fair", "Geeta", "Glimmora", []),
  "Ash": Pair(5, True, "Master Fair", "Ash", "Pikachu", []),
  "SS Lear": Pair(5, True, "Master Fair", "Sygna Suit Lear", "Gholdengo", ["SS Lear", "ss lear"]),
  "NC Elio": Pair(5, True, "Master Fair", "Elio (Champion)", "Necrozma-Dusk-Mane", ["NC Elio", "nc elio"]),
  "NC Selene": Pair(5, True, "Master Fair", "Selene (Champion)", "Necrozma-Dawn-Wings", ["NC Selene", "nc selene"]),
  "Kieran": Pair(5, True, "Master Fair", "Kieran", "Hydrapple", []),
  "A25 Red": Pair(5, True, "Master Fair", "Red (Anniversary 2025)", "Charizard", ["A25 Red", "a25 red"]),
  "A25 Irida": Pair(5, True, "Master Fair", "Irida (Anniversary 2025)", "Typhlosion-Hisui", ["A25 Irida", "a25 irida"]),
  "A25 Gloria": Pair(5, True, "Master Fair", "Gloria (Anniversary 2025)", "Cinderace", ["A25 Gloria", "a25 gloria"]),
  "A.Volo": Pair(5, True, "Master Fair", "Volo (Alt.)", "Giratina", ["A.Volo", "a.volo", "Alt Volo", "alt volo"])
}

fiveStarMasterFair = list(fiveStarMasterFairDict.values())

fiveStarArcSuitFairDict = {
  "ASL": Pair(5, True, "Arc Suit Fair", "Arc Suit Lance", "Dragonite", ["AS Lance", "as lance", "ASL"]),
  "ASC": Pair(5, True, "Arc Suit Fair", "Arc Suit Cynthia", "Garchomp", ["AS Cynthia", "as cynthia", "ASC"]),
  "ASS": Pair(5, True, "Arc Suit Fair", "Arc Suit Steven", "Metagross", ["AS Steven", "as steven", "ASS"]),
  "ASLe": Pair(5, True, "Arc Suit Fair", "Arc Suit Leon", "Charizard", ["AS Leon", "as leon", "ASLe"]),
  "ASN": Pair(5, True, "Arc Suit Fair", "Arc Suit N", "Zoroark", ["AS N", "as n", "ASN"]),
  "ASA": Pair(5, True, "Arc Suit Fair", "Arc Suit Alder", "Volcarona", ["AS Alder", "as alder", "ASA"]),
  "ASE": Pair(5, True, "Arc Suit Fair", "Arc Suit Ethan", "Lugia", ["AS Ethan", "as ethan", "ASE"]),
  "ASSi": Pair(5, True, "Arc Suit Fair", "Arc Suit Silver", "Ho-Oh", ["AS Silver", "as silver", "ASSi"])
}

fiveStarArcSuitFair = list(fiveStarArcSuitFairDict.values())

mixExclusiveDict = {
  "mix Red": Pair(5, True, "Mix", "Red", "Venosaur", ["Mix Red", "mix red"], True),
  "mix Blue": Pair(5, True, "Mix", "Blue", "Charizard", ["Mix Blue", "mix blue"], True),
  "mix Leaf": Pair(5, True, "Mix", "Leaf", "Blastoise", ["Mix Leaf", "mix leaf"], True),
  "mix Lucas": Pair(5, True, "Mix", "Lucas", "Torterra", ["Mix Lucas", "mix lucas"], True),
  "mix Dawn": Pair(5, True, "Mix", "Dawn", "Empoleom", ["Mix Dawn", "mix dawn"], True),
  "mix Barry": Pair(5, True, "Mix", "Barry", "Infernape", ["Mix Barry", "mix barry"], True)
}

mixExclusive = list(mixExclusiveDict.values())

seasonalHolidayDict = {
  "h!Rosa": Pair(5, True, "Seasonal", "Rosa (Holiday 2019)", "Greninja", ["Holi Rosa", "holi rosa"]),
  "h!Siebold": Pair(5, True, "Seasonal", "Siebold (Holiday 2019)", "Octillery", ["Holi Siebold", "holi siebold"]),
  "h!Erika": Pair(5, True, "Seasonal", "Erika (Holiday 2020)", "Comfey", ["Holi Erika", "holi erika"]),
  "h!Skyla": Pair(5, True, "Seasonal", "Skyla (Holiday 2020)", "Togekiss", ["Holi Skyla", "holi skyla"]),
  "h!Nessa": Pair(5, True, "Seasonal", "Nessa (Holiday 2021)", "Eiscue", ["Holi Nessa", "holi nessa"]),
  "h!Leon": Pair(5, True, "Seasonal", "Leon (Holiday 2021)", "Calyrex", ["Holi Leon", "holi leon"]),
  "h!Whitney": Pair(5, True, "Seasonal", "Whitney (Holiday 2022)", "Sawsbuck-Winter", ["Holi Whitney", "holi whitney"]),
  "h!Jasmine": Pair(5, True, "Seasonal", "Jasmine (Holiday 2022)", "Ampharos", ["Holi Jasmine", "holi jasmine"]),
  "h!Viola": Pair(5, True, "Seasonal", "Viola (Holiday 2023)", "Vivillon", ["Holi Viola", "holi viola"]),
  "h!Sycamore": Pair(5, True, "Seasonal", "Sycamore (Holiday 2023)", "Gogoat", ["Holi Sycamore", "holi sycamore"]),
  "h!Lillie": Pair(5, True, "Seasonal", "Lillie (Holiday 2024)", "Primarina", ["Holi Lillie", "holi lillie"]),
  "h!Bugsy": Pair(5, True, "Seasonal", "Bugsy (Holiday 2024)", "Kricketune", ["Holi Bugsy", "holi bugsy"])
}

seasonalHoliday = list(seasonalHolidayDict.values())

seasonalNewYearDict = {
  "NY Lance": Pair(5, True, "Seasonal", "Lance (New Year's 2021)", "Gyarados", ["NY Lance", "ny lance"]),
  "NY Lillie": Pair(5, True, "Seasonal", "Lillie (New Year's 2021)", "Ribombee", ["NY Lillie", "ny lillie"]),
  "NY Sabrina": Pair(5, True, "Seasonal", "Sabrina (New Year's 2022)", "Chingling", ["NY Sabrina", "ny sabrina"]),
  "NY Volkneer": Pair(5, True, "Seasonal", "Volkneer (New Year's 2022)", "Electivire", ["NY Volkneer", "ny volkneer"]),
  "NY Lisia": Pair(5, True, "Seasonal", "Lisia (New Year's 2023)", "Rapidash-Galar", ["NY Lisia", "ny lisia"]),
  "NY Dawn": Pair(5, True, "Seasonal", "Dawn (New Year's 2023)", "Oricorio-Sensu", ["NY Dawn", "ny dawn"]),
  "NY Clair": Pair(5, True, "Seasonal", "Clair (New Year's 2024)", "Drampa", ["NY Clair", "ny clair"]),
  "NY Wallace": Pair(5, True, "Seasonal", "Wallace (New Year's 2024)", "Blacephalon", ["NY Wallace", "ny wallace"]),
  "NY Raihan": Pair(5, True, "Seasonal", "Raihan (New Year's 2025)", "Sandaconda", ["NY Raihan", "ny raihan"]),
  "NY Poppy": Pair(5, True, "Seasonal", "Poppy (New Year's 2025)", "Steelix", ["NY Poppy", "ny poppy"])
}

seasonalNewYear = list(seasonalNewYearDict.values())

seasonalSpringDict = {
  "sp May": Pair(5, True, "Seasonal", "May (Spring 2021)", "Lopunny", ["sp May", "sp may"]),
  "sp Burgh": Pair(5, True, "Seasonal", "Burgh (Spring 2021)", "Togepi", ["sp Burgh", "sp burgh"])
}

seasonalSpring = list(seasonalSpringDict.values())

seasonalPalentinesDict = {
  "pal Dawn": Pair(5, True, "Seasonal", "Dawn (Palentine's 2021)", "Alcremie", ["pal Dawn", "pal dawn"]),
  "pal Serena": Pair(5, True, "Seasonal", "Serena (Palentine's 2021)", "Whimsicott", ["pal Serena", "pal serena"]),
  "pal Marnie": Pair(5, True, "Seasonal", "Marnie (Palentine's 2022)", "Mawile", ["pal Marnie", "pal marnie"]),
  "pal Bea": Pair(5, True, "Seasonal", "Bea (Palentine's 2022)", "Vanilluxe", ["pal Bea", "pal bea"]),
  "pal Elesa": Pair(5, True, "Seasonal", "Elesa (Palentine's 2023)", "Togetic", ["Pal Elesa", "pal elesa"]),
  "pal Mallow": Pair(5, True, "Seasonal", "Mallow (Palentine's 2023)", "Appletun", ["pal Mallow", "pal mallow"]),
  "pal Candice": Pair(5, True, "Seasonal", "Candice (Palentine's 2024)", "Darmanitan-Galar", ["pal Candice", "pal candice"]),
  "pal Victor": Pair(5, True, "Seasonal", "Victor (Palentine's 2024)", "Greedent", ["pal Victor", "pal victor"]),
  "pal Erika": Pair(5, True, "Seasonal", "Erika (Palentine's 2025)", "Lurantis", ["pal Erika", "pal erika"]),
  "pal Marley": Pair(5, True, "Seasonal", "Marley (Palentine's 2025)", "Shaymin", ["pal Marley", "pal marley"])
}

seasonalPalentines = list(seasonalPalentinesDict.values())

seasonalSummerDict = {
  "sum Lyra": Pair(5, True, "Seasonal", "Lyra (Summer 2020)", "Jigglypuff", ["sum Lyra", "sum lyra"]),
  "sum Steven": Pair(5, True, "Seasonal", "Steven (Summer 2020)", "Sandslash-Alola", ["sum Steven", "sum steven"]),
  "sum Gloria": Pair(5, True, "Seasonal", "Gloria (Summer 2021)", "Inteleon", ["sum Gloria", "sum gloria"]),
  "sum Marnie": Pair(5, True, "Seasonal", "Marnie (Summer 2021)", "Grimmsnarl", ["sum Marnie", "sum marnie"]),
  "sum Hilda": Pair(5, True, "Seasonal", "Hilda (Summer 2022)", "Grapploct", ["sum Hilda", "sum hilda"]),
  "sum N": Pair(5, True, "Seasonal", "N (Summer 2022)", "Zoroark", ["sum N", "sum n"]),
  "sum Tate": Pair(5, True, "Seasonal", "Tate (Summer 2023)", "Jirachi", ["sum Tate", "sum tate"]),
  "sum Liza": Pair(5, True, "Seasonal", "Liza (Summer 2023)", "Celesteela", ["sum Liza", "sum liza"]),
  "sum Gardenia": Pair(5, True, "Seasonal", "Gardenia (Summer 2024)", "Dhelmise", ["sum Gardenia", "sum gardenia"]),
  "sum Acerola": Pair(5, True, "Seasonal", "Acerola (Summer 2024)", "Jellicent", ["sum Acerola", "sum acerola"]),
  "sum Cynthia": Pair(5, True, "Seasonal", "Cynthia (Summer 2025)", "Milotic", ["sum Cynthia", "sum cynthia"]),
  "sum Skyla": Pair(5, True, "Seasonal", "Skyla (Summer 2025)", "Jumpluff", ["sum Skyla", "sum skyla"])
}

seasonalSummer = list(seasonalSummerDict.values())

seasonalFallDict = {
  "fa Hilbert": Pair(5, True, "Seasonal", "Hilbert (Fall 2020)", "Mightyena", ["fa Hilbert", "fa hilbert"]),
  "fa Acerola": Pair(5, True, "Seasonal", "Acerola (Fall 2020)", "Mimikyu", ["fa Acerola", "fa acerola"]),
  "fa Morty": Pair(5, True, "Seasonal", "Morty (Fall 2021)", "Banette", ["fa Morty", "fa morty"]),
  "fa Caitlin": Pair(5, True, "Seasonal", "Caitlin (Fall 2021)", "Sableye", ["fa Caitlin", "fa caitlin"]),
  "fa Iris": Pair(5, True, "Seasonal", "Iris (Fall 2022)", "Naganadel", ["fa Iris", "fa iris"]),
  "fa Allister": Pair(5, True, "Seasonal", "Allister (Fall 2022)", "Gourgeist", ["fa Allister", "fa allister"]),
  "fa Roxanne": Pair(5, True, "Seasonal", "Roxanne (Fall 2023)", "Runerigus", ["fa Roxanne", "fa roxanne"]),
  "fa Phoebe": Pair(5, True, "Seasonal", "Phoebe (Fall 2023)", "Cofagrigus", ["fa Phoebe", "fa phoebe"]),
  "fa Shauntal": Pair(5, True, "Seasonal", "Shauntal (Fall 2024)", "Froslass", ["fa Shauntal", "fa shauntal"]),
  "fa Iono": Pair(5, True, "Seasonal", "Iono (Fall 2024)", "Flutter Mane", ["fa Iono", "fa iono"])
}

seasonalFall = list(seasonalFallDict.values())

specialCostumeDict = {
  "SC Lyra": Pair(5, True, "Costume", "Lyra (Special Costume)", "Phanpy", ["SC Lyra", "sc lyra"]),
  "SC Morty": Pair(5, True, "Costume", "Morty (Academy)", "Typhlosion-Hisui", ["SC Morty", "sc morty", "AcaMorty", "acaMorty", "acamorty","Morty Academy"]),
  "SC Jasmine": Pair(5, True, "Costume", "Jasmine (Special Costume)", "Celesteela", ["SC Jasmine", "sc jasmine"]),
  "SC Steven": Pair(5, True, "Costume", "Steven (Special Costume)", "Stoutland", ["SC Steven", "sc steven"]),
  "SC Zinnia": Pair(5, True, "Costume", "Zinnia (Special Costume)", "Theivul", ["SC Zinnia", "sc zinnia"]),
  "SC Barry": Pair(5, True, "Costume", "Barry (Special Costume)", "Heracross", ["SC Barry", "sc barry"]),
  "SC Rei": Pair(5, True, "Costume", "Rei (Academy)", "Braviary-Hisui", ["SC Rei", "sc rei", "AcaRei", "acaRei", "acarei","Rei Academy"]),
  "SC Adaman": Pair(5, True, "Costume", "Adaman (Special Costume)", "Ursaluna", ["SC Adaman", "sc adaman"]),
  "SC Irida": Pair(5, True, "Costume", "Irida (Special Costume)", "Zoroark-Hisui", ["SC Irida", "sc irida"]),
  "SC Hilda": Pair(5, True, "Costume", "Hilda (Special Costume)", "Diancie", ["SC Hilda", "sc hilda"]),
  "SC Rosa": Pair(5, True, "Costume", "Rosa (Special Costume)", "Shaymin-Sky", ["SC Rosa", "sc rosa"]),
  "SC Ingo": Pair(5, True, "Costume", "Ingo (Special Costume)", "Accelgor", ["SC Ingo", "sc ingo"]),
  "SC Emmet": Pair(5, True, "Costume", "Emmet (Special Costume)", "Escavalier", ["SC Emmet", "sc emmet"]),
  "Brycen-Man": Pair(5, True, "Costume", "Brycen-Man", "Zoroark", []),
  "Belleba": Pair(5, True, "Costume", "Belleba", "Swoobat", ["SC Sabrina", "sc sabrina"]),
  "SC Shauna": Pair(5, True, "Costume", "Shauna (Special Costume)", "Klefki", ["SC Shauna", "sc shauna"]),
  "SC Diantha": Pair(5, True, "Costume", "Diantha (Special Costume)", "Keldeo", ["SC Diantha", "sc diantha"]),
  "SC Selene": Pair(5, True, "Costume", "Selene (Special Costume)", "Scizor", ["SC Selene", "sc selene"]),
  "SC Lillie": Pair(5, True, "Costume", "Lillie (Special Costume)", "Polteageist-Antique", ["SC Lillie", "sc lillie"]),
  "SC Guzma": Pair(5, True, "Costume", "Guzma (Special Costume)", "Buzzwole", ["SC Guzma", "sc guzma"]),
  "SC Marnie": Pair(5, True, "Costume", "Marnie (Academy)", "Cyclizar", ["SC Marnie", "sc marnie", "AcaMarnie", "acaMarnie", "acamarnie","Marnie Academy"]),
  "SC Sonia": Pair(5, True, "Costume", "Sonia (Special Costume)", "Tsareena", ["SC Sonia", "sc sonia"]),
  "SC Larry": Pair(5, True, "Costume", "Larry (Special Costume)", "Flamigo}", ["SC Larry", "sc larry"]),
  "Clive": Pair(5, True, "Costume", "Clive", "Amoonguss", []),
  "SC Iris": Pair(5, True, "Costume", "Iris (Academy)", "Lapras", ["SC Iris", "sc iris", "AcaIris", "acaIris", "acairis"]),
  "SC Gladion": Pair(5, True, "Costume", "Gladion (Academy)", "Greninja-Ash", ["SC Gladion", "sc gladion", "AcaGladion", "acaGladion", "acagladion"])
}

specialCostume = list(specialCostumeDict.values())

varietyDict = {
  "V.Lorelei": Pair(5, True, "Variety", "Lorelei", "Cloyster", ["V.Lorelei", "v.lorelei"], True),
  "V.Bruno": Pair(5, True, "Variety", "Bruno", "Onix", ["V.Bruno", "v.bruno"], True),
  "V.Agatha": Pair(5, True, "Variety", "Agatha", "Arbok", ["V.Agatha", "v.agatha"], True),
  "V.Lance": Pair(5, True, "Variety", "Lance", "Dragonair", ["V.Lance", "v.lance"], True),
  "V.Giovanni": Pair(5, True, "Variety", "Giovanni", "Rhydon", ["V.Giovanni", "v.giovanni"], True),
  "V.Ethan": Pair(5, True, "Variety", "Ethan", "Ho-Oh", ["V.Ethan", "v.ethan"], True),
  "V.Lyra": Pair(5, True, "Variety", "Lyra", "Vaporeon", ["V.Lyra", "v.lyra"], True),
  "V.Kris": Pair(5, True, "Variety", "Kris", "Jolteon", ["V.Kris", "v.kris"], True),
  "V.Falkner": Pair(5, True, "Variety", "Falkner", "Noctowl", ["V.Falkner", "v.falkner"], True),
  "V.Archer": Pair(5, True, "Variety", "Archer", "Houndoom", ["V.Archer", "v.archer"], True),
  "V.Ariana": Pair(5, True, "Variety", "Ariana", "Arbok", ["V.Ariana", "v.ariana"], True),
  "V.Petrel": Pair(5, True, "Variety", "Petrel", "Weezing", ["V.Petrel", "v.petrel"], True),
  "V.Proton": Pair(5, True, "Variety", "Proton", "Golbat", ["V.Proton", "v.proton"], True),
  "V.Noland": Pair(5, True, "Variety", "Noland", "Ninjask", ["V.Noland", "v.noland"], True),
  "V.Lucas": Pair(5, True, "Variety", "Lucas", "Flareon", ["V.Lucas", "v.lucas"], True),
  "V.Cynthia": Pair(5, True, "Variety", "Cynthia", "Spiritomb", ["V.Cynthia", "v.cynthia"], True),
  "V.Thorton": Pair(5, True, "Variety", "Thorton", "Magnezone", ["V.Thorton", "v.thorton"], True),
  "V.Hilbert": Pair(5, True, "Variety", "Hilbert", "Glaceon", ["V.Hilbert", "v.hilbert"], True),
  "V.Hilda": Pair(5, True, "Variety", "Hilda", "Leafeon", ["V.Hilda", "v.hilda"], True),
  "V.Calem": Pair(5, True, "Variety", "Calem", "Sylveon", ["V.Calem", "v.calem"], True),
  "V.Elio": Pair(5, True, "Variety", "Elio", "Espeon", ["V.Elio", "v.elio"], True),
  "V.Selene": Pair(5, True, "Variety", "Selene", "Umbreon", ["V.Selene", "v.selene"], True),
  "V.Kiawe": Pair(5, True, "Variety", "Kiawe", "Arcanine", ["V.Wallace", "v.wallace"], True),
  "V.Mallow": Pair(5, True, "Variety", "Mallow", "Shiinotic", ["V.Morty", "v.morty"], True),
  "V.Plumeria": Pair(5, True, "Variety", "Plumeria", "Gengar", ["V.Chuck", "v.chuck"], True),
  "V.Guzma": Pair(5, True, "Variety", "Guzma", "Ariados", ["V.Jasmine", "v.jasmine"], True),
  "V.Hop": Pair(5, True, "Variety", "Hop", "Rillaboom", ["V.Rillaboom", "v.rillaboom"], True),
  "V2.Hop": Pair(5, True, "Variety", "Hop", "Zacian-Crowned", ["V2.Hop", "v2.hop"], True),
  "V.Marnie": Pair(5, True, "Variety", "Marnie", "Cinderace", ["V.Marnie", "v.marnie"], True),
  "V.Bede": Pair(5, True, "Variety", "Bede", "Inteleon", ["V.Bede", "v.bede"], True),
  "Ball Guy": Pair(5, True, "Variety", "Ball Guy", "Amoonguss", ["Ball Guy", "ball guy"]),
  "V.Rachel": Pair(5, True, "Variety", "Rachel", "Gimmighoul-Roaming", ["V.Rachel", "v.rachel"], True),
  "V.Sawyer": Pair(5, True, "Variety", "Sawyer", "Gimmighoul-Chest", ["V.Sawyer", "v.sawyer"], True),
  "V.Grimsley": Pair(5, True, "Variety", "Grimsley", "Absol", ["V.Grimsley", "v.grimsley"], True),
  "Samson Oak": Pair(5, True, "Variety", "Samson Oak", "Exeggutor", ["Samson Oak", "S.Oak", "s.oak", "samson oak"]),
  "V.Gordie": Pair(5, True, "Variety", "Gordie", "Barbaracle", ["V.Gordie", "v.gordie"], True),
  "V.Melony": Pair(5, True, "Variety", "Melony", "Frosmoth", ["V.Melony", "v.melony"], True),
  "V2.Hilda": Pair(5, True, "Variety", "Hilda", "Tornadus", ["V2.Hilda", "v2.hilda"], True),
  "V2.Hilbert": Pair(5, True, "Variety", "Hilbert", "Thundurus", ["V2.Hilbert", "v2.hilbert"], True),
  "V.N": Pair(5, True, "Variety", "N", "Landorus", ["V.N", "v.n", "VN"], True)
}

gymDict = {
  "Gym Brock": Pair(5, True, "Gym", "Brock", "Kabutops", ["Gym Brock", "gym brock"], True),
  "Gym Winona": Pair(5, True, "Gym", "Winona", "Altaria", ["Gym Winona", "gym winona"], True),
  "Gym Grusha": Pair(5, True, "Gym", "Grusha", "Beartic", ["Gym Grusha", "gym grusha"], True),
  "Gym Whitney": Pair(5, True, "Gym", "Whitney", "Wigglytuff", ["Gym Whitney", "gym whitney"], True),
  "Gym Korrina": Pair(5, True, "Gym", "Korrina", "Hawlucha", ["Gym Korrina", "gym korrina"], True),
  "Gym Kabu": Pair(5, True, "Gym", "Kabu", "Ninetales", ["Gym Kabu", "gym kabu"], True),
  "Gym Roxie": Pair(5, True, "Gym", "Roxie", "Garbodor", ["Gym Roxie", "gym roxie"], True),
  "Gym Fantina": Pair(5, True, "Gym", "Fantina", "Dusknoir", ["Gym Fantina", "gym fantina"], True),
  "Gym Lana": Pair(5, True, "Gym", "Lana", "Cloyster", ["Gym Lana", "gym lana"], True)
}

gymList = list(gymDict.values())

variety = list(varietyDict.values())

seasonalFull = seasonalHoliday + seasonalNewYear + seasonalSpring + seasonalPalentines + seasonalSummer + seasonalFall

mixFull = mixExclusive + fiveStarPokeFair + seasonalFull + specialCostume + variety

# -----------

action = ""

def searchForPair(text, banner):
  for i in range(len(banner.pairs)):
    if text == banner.pairs[i].name and banner.pairs[i].nonick:
      return banner.pairs[i]
  for i in range(len(banner.pairs)):
    if text in banner.pairs[i].nick:
      return banner.pairs[i]
  # if text in banner.pairs:
    # return banner.pairs[text]
  return None

def bannerSelect(banner: Banner):
  print("----------------------------------------")
  print(f"Scouting on {banner.name}...")
  print()
  print(f"Gems spent: {banner.singles*300} (Singles) + {banner.multis*3000} (Multis) = {banner.singles*300 + banner.multis*3000}")
  print()
  if len(banner.featuredPairs) <= 10:
    print("Featured Pair(s):")
    print(banner.__str__())
  print()
  if len(banner.featured2) > 0:
    print("Featured Poke Fair(s):")
    print(banner.featuredtwo())
  print()
  if banner.checkPity():
    print(blue, "(ENTER) Choose a sync pair", reset())
  else:
    print("(x) Single")
    print("(3) Single x3")
    print("(5) Single x5")
    print("(10) Single x10")
  
  if banner.type not in ["mix", "ticket", "ticketM"]:
    print("(a) Multi")
    print("(z) Straight to Pity", "(Multi x12 + Single x2)" if not banner.type == "arcSuitFair" else "(Multi x15 + Single x2)")
  print("(b) Back")
  if banner.checkPity():
    print("\n".join([pair.__str__() for pair in banner.pairs]))
    print()
    pairChosen = input("Sync pair to pity: >")
    pairChosen = searchForPair(pairChosen, banner) 
    if pairChosen is None:
      print("Invalid input.")
    else:
      print(rainbow(pairChosen.literal()))
      banner.multis = 0
      banner.singles = 0
    return
  match input('> '):
    case "x":
      scouted = banner.single()
      print(rainbow(scouted.literal()) if scouted in banner.featuredPairs else scouted.__str__())
    case "3":
      for i in range(3):
        scouted = banner.single()
        print(rainbow(scouted.literal()) if scouted in banner.featuredPairs else scouted.__str__())
    case "5":
      for i in range(5):
        scouted = banner.single()
        print(rainbow(scouted.literal()) if scouted in banner.featuredPairs else scouted.__str__())
    case "10":
      for i in range(10):
        scouted = banner.single()
        print(rainbow(scouted.literal()) if scouted in banner.featuredPairs else scouted.__str__())
    case "a":
      banner.multi()
    case "b":
      pass
    case "z":
      for i in range(12 if not banner.type == "arcSuitFair" else 15):
        banner.multi()
      scouted = banner.single()
      print(rainbow(scouted.literal()) if scouted in banner.featuredPairs else scouted.__str__())
      scouted = banner.single()
      print(rainbow(scouted.literal()) if scouted in banner.featuredPairs else scouted.__str__())
    case _:
      print("Invalid input. ")
  awaitEnter()
  if input("Do you want to scout again on this banner? (y/n) \n> ") == "y":
    bannerSelect(banner)
  else:
    pass

bannersDict = {
  "A25 Red": Banner("Red (Anniversary 2025) EX Master Fair", [fiveStarMasterFairDict["A25 Red"]], "EXMF", featured2 = [fiveStarPokeFairDict["SS Leon"], fiveStarPokeFairDict["SS Brendan"]]),
  "A25 Irida": Banner("Irida (Anniversary 2025) EX Master Fair", [fiveStarMasterFairDict["A25 Irida"]], "EXMF", featured2 = [fiveStarPokeFairDict["SS Roxie"], fiveStarPokeFairDict["Atticus"]]),
  "A25 Gloria": Banner("Gloria (Anniversary 2025) EX Master Fair", [fiveStarMasterFairDict["A25 Gloria"]], "EXMF", featured2 = [fiveStarPokeFairDict["A.Selene"], fiveStarPokeFairDict["C.Blue"]]),
  "vol37": Banner("Vol. 37 Monthly Poke Fair Scout (Marnie)", [fiveStarPokeFairDict["Marnie"]], "pokeFair"),
  "sep25_3xV": Banner("Triple Feature Variety Scout", [varietyDict["V2.Hilda"], varietyDict["V2.Hilbert"], varietyDict["V.N"]], "3xV"),
  "A.Volo": Banner("Volo (Alt.) EX Master Fair", [fiveStarMasterFairDict["A.Volo"]], "EXMF", featured2 = [fiveStarPokeFairDict["Rei"], fiveStarPokeFairDict["Akari"]]),
  # Rei (Academy) rerun
  # Lacey rerun
  "sep25_3xMF": Banner("Triple Feature Master Fair Scout", [fiveStarMasterFairDict["SSR Cynthia"], fiveStarMasterFairDict["NC Bede"], fiveStarMasterFairDict["SS Nemona"]], "3xMF"),
  "Carmine": Banner("Carmine Poke Fair Scout", [fiveStarPokeFairDict["Carmine"]], "pokeFair"),
  "vol36": Banner("Vol. 36 Monthly Poke Fair Scout (Arven)", [fiveStarPokeFairDict["Arven"]], "pokeFair"),
  "SC Iris": Banner("Iris Costume Scout", [specialCostumeDict["SC Iris"]], "costume"),
  "SC Gladion": Banner("Gladion Costume Scout", [specialCostumeDict["SC Gladion"]], "costume"),
  "aug25_3xPF": Banner("Triple Feature Poke Fair Scout", [fiveStarPokeFairDict["C.Elesa"], fiveStarPokeFairDict["Lucas"], fiveStarPokeFairDict["Milo"]], "3xPF"),
  "aug25_2xV": Banner("Double Feature Variety Scout", [varietyDict["V.Plumeria"], varietyDict["V.Guzma"]], "2xV"),
  "Kieran": Banner("Kieran Master Fair Scout", [fiveStarMasterFairDict["Kieran"]], "masterFair"),
  # bikes rerun
  "sum Cynthia": Banner("Cynthia (Summer 2025) Seasonal Scout", [seasonalSummerDict["sum Cynthia"]], "seasonal"),
  "vol35": Banner("Vol. 35 Monthly Poke Fair Scout (Kabu)", [fiveStarPokeFairDict["Kabu"]], "pokeFair"),
  "sum Skyla": Banner("Skyla (Summer 2025) Seasonal Scout", [seasonalSummerDict["sum Skyla"]], "seasonal"),
  # seasonal rerun
  "AS Ethan": Banner("Arc Suit Ethan Arc Suit Fair Scout", [fiveStarArcSuitFairDict["ASE"]], "arcSuitFair"),
  "AS Silver": Banner("Arc Suit Silver Arc Suit Fair Scout", [fiveStarArcSuitFairDict["ASSi"]], "arcSuitFair"),
  "jul25_2xV": Banner("Double Feature Variety Scout", [varietyDict["V.Thorton"], varietyDict["V.Noland"]], "2xV"),
  # NC Silver rerun
  "NC Elio": Banner("Elio (Champion) Master Fair Scout", [fiveStarMasterFairDict["NC Elio"]], "masterFair"),
  "NC Selene": Banner("Selene (Champion) Master Fair Scout", [fiveStarMasterFairDict["NC Selene"]], "masterFair"),
  "jun25_superCostume": Banner("Super Spotlight Costume Scout", [specialCostumeDict["SC Barry"], specialCostumeDict["SC Selene"], specialCostumeDict["Belleba"], specialCostumeDict["Brycen-Man"]], "superCostume"),
  "jun25_3xPF": Banner("Triple Feature Poke Fair Scout", [fiveStarPokeFairDict["C.Blue"], fiveStarPokeFairDict["SS Ingo"], fiveStarPokeFairDict["SS Dawn"]], "3xPF"),
  "SC Larry": Banner("Larry Costume Scout", [specialCostumeDict["SC Larry"]], "costume"),
  "Clive": Banner("Clive Costume Scout", [specialCostumeDict["Clive"]], "costume"),
  "Samson Oak": Banner("Samson Oak Variety Scout", [varietyDict["Samson Oak"]], "variety"),
  "V.Gordie": Banner("Gordie Variety Scout", [varietyDict["V.Gordie"]], "variety"),
  "V.Melony": Banner("Melony Variety Scout", [varietyDict["V.Melony"]], "variety"),
  "Geeta": Banner("Geeta Master Fair Scout", [fiveStarMasterFairDict["Geeta"]], "masterFair"),
  "vol34": Banner("Vol. 34 Monthly Poke Fair Scout (Rika)", [fiveStarPokeFairDict["Rika"]], "pokeFair"),
  "SS Bede": Banner("Sygna Suit Bede Poke Fair Scout", [fiveStarPokeFairDict["SS Bede"]], "pokeFair"),
  "ASA": Banner("Arc Suit Alder Arc Suit Fair Scout", [fiveStarArcSuitFairDict["ASA"]], "arcSuitFair"),
  "Benga": Banner("Benga Poke Fair Scout", [fiveStarPokeFairDict["Benga"]], "pokeFair"),
  "SS Iono": Banner("Sygna Suit Iono Poke Fair Scout", [fiveStarPokeFairDict["SS Iono"]], "pokeFair"),
  "SSA Elesa": Banner("Sygna Suit (Alt.) Elesa Poke Fair Scout", [fiveStarPokeFairDict["SSA Elesa"]], "pokeFair"),
  "NC Rosa": Banner("Rosa (Champion) Master Fair Scout", [fiveStarMasterFairDict["NC Rosa"]], "masterFair"),
  "may25_3xPF": Banner("Triple Feature Poke Fair Scout", [fiveStarPokeFairDict["Red"], fiveStarPokeFairDict["Gloria"], fiveStarPokeFairDict["Marnie"]], "3xPF"),
  "may25_2xSC": Banner("Double Feature Costume Scout", [specialCostumeDict["SC Adaman"], specialCostumeDict["SC Irida"]], "2xSC"),
  "SS Gladion": Banner("Sygna Suit Gladion Master Fair Scout", [fiveStarMasterFairDict["SS Gladion"]], "masterFair"),
  "V.Grimsley": Banner("Grimsley Variety Scout", [varietyDict["V.Grimsley"]], "variety"),
  "vol33": Banner("Vol. 33 Monthly Poke Fair Scout (Larry)", [fiveStarPokeFairDict["Larry"]], "pokeFair"),
  "SC Rei": Banner("Rei Costume Scout",[specialCostumeDict["SC Rei"]], "costume"),
  "Lacey": Banner("Lacey Poke Fair Scout", [fiveStarPokeFairDict["Lacey"]], "pokeFair"),
  "Ilima": Banner("Ilima Spotlight Scout", [fiveStarSpotlightDict["Ilima"]], "spotlight"),
  "apr_2xPF": Banner("Double Feature Poke Fair Scout", [fiveStarPokeFairDict["Rei"], fiveStarPokeFairDict["Akari"]], "2xPF"),
  "SC Marnie": Banner("Marnie Costume Scout",[specialCostumeDict['SC Marnie']], "costume"),
  "SC Morty": Banner("Morty Costume Scout",[specialCostumeDict["SC Morty"]], "costume"),
  "vol32": Banner("Vol. 32 Monthly Poke Fair Scout (Volo)", [fiveStarPokeFairDict["Volo"]],"pokeFair"),
  "mar25_3xMF": Banner("Triple Feature Master Fair Scout", [fiveStarMasterFairDict["Maxie"], fiveStarMasterFairDict["Archie"], fiveStarMasterFairDict["Leon"]], "3xMF"),
  "NC May": Banner("May (Champion) Master Fair Scout", [fiveStarMasterFairDict["NC May"]], "masterFair"),
  "NC Brendan": Banner("Brendan (Champion) Master Fair Scout", [fiveStarMasterFairDict["NC Brendan"]], "masterFair"),
  "anni Steven": Banner("Steven (Anniversary 2021) Master Fair Scout", [fiveStarMasterFairDict["anni Steven"]], "masterFair"),
  "ASN": Banner("Arc Suit N Arc Suit Fair Scout", [fiveStarArcSuitFairDict["ASN"]], "arcSuitFair"),
  "Ortega": Banner("Ortega Poke Fair Scout", [fiveStarPokeFairDict["Ortega"]], "pokeFair"),
  "teamStar": Banner("Team Star Assemble! Super Spotlight Poke Fair Scout", [fiveStarPokeFairDict["Penny"], fiveStarPokeFairDict["Atticus"], fiveStarPokeFairDict["Ortega"], fiveStarPokeFairDict["Mela"], fiveStarPokeFairDict["Eri"], fiveStarPokeFairDict["Giacomo"]], "superScout"),
  "NC Nate": Banner("Nate (Champion) Master Fair Scout", [fiveStarMasterFairDict["NC Nate"]], "masterFair"),
  "vol31": Banner("Vol. 31 Monthly Poke Fair Scout (Raihan)", [fiveStarPokeFairDict["Raihan"]], "pokeFair"),
  "pal Marley": Banner("Marley (Palentines' 2025) Seasonal Scout", [seasonalPalentinesDict["pal Marley"]], "seasonal"),
  "pal Erika": Banner("Erika (Palentines' 2025) Seasonal Scout", [seasonalPalentinesDict["pal Erika"]], "seasonal"),
  "feb25_3xPF": Banner("Triple Feature Poke Fair Scout", [fiveStarPokeFairDict["SS Korrina"], fiveStarPokeFairDict["Eusine"], fiveStarPokeFairDict["Ingo"]], "3xPF"),
  "feb25_superScout": Banner("One-Time-Only Fair-Exclusive Guaranteed Scout", [fiveStarPokeFairDict["C.Elesa"], fiveStarPokeFairDict["SS Giovanni"], fiveStarPokeFairDict["Bede"], fiveStarPokeFairDict["Akari"], fiveStarPokeFairDict["Larry"]], "superScout"),
  "feb25_superSpotlight": Banner("Super Spotlight Poke Fair Scout", [fiveStarPokeFairDict["SS Diantha"], fiveStarPokeFairDict["SS Lysandre"], fiveStarPokeFairDict["Anabel"], fiveStarPokeFairDict["Emma"]], "superScout"),
  "Juliana": Banner("Juliana Master Fair Scout", [fiveStarMasterFairDict["Juliana"]], "masterFair"),
  "Florian": Banner("Florian Master Fair Scout", [fiveStarMasterFairDict["Florian"]], "masterFair"),
  "vol30": Banner("Vol. 30 Monthly Poke Fair Scout (Klara)", [fiveStarPokeFairDict["Klara"]], "pokeFair"),
  "SSA Giovanni": Banner("Sygna Suit (Alt.) Giovanni Master Fair Scout", [fiveStarMasterFairDict["SSA Giovanni"]], "masterFair"),
  "NY Raihan": Banner("Raihan (New Year's 2025) Seasonal Scout", [seasonalNewYearDict["NY Raihan"]], "seasonal"),
  "NY Poppy": Banner("Poppy (New Year's 2025) Seasonal Scout", [seasonalNewYearDict["NY Poppy"]], "seasonal"),
  "rocketVariety": Banner("Team Rocket Variety Scout", [varietyDict["V.Archer"], varietyDict["V.Ariana"], varietyDict["V.Petrel"], varietyDict["V.Proton"], varietyDict["V.Giovanni"]], "variety"),
  "jan25_3xPF": Banner("Triple Feature Poke Fair Scout", [fiveStarPokeFairDict["Grusha"], fiveStarPokeFairDict["Paulo"], fiveStarPokeFairDict["SS Blue"]], "3xPF"),
  "Mela": Banner("Mela Poke Fair Scout", [fiveStarPokeFairDict["Mela"]], "pokeFair"),
  "Atticus": Banner("Atticus Poke Fair Scout", [fiveStarPokeFairDict["Atticus"]], "pokeFair"),
  "jan25_2xPF": Banner("Double Feature Poke Fair Scout", [fiveStarPokeFairDict["SS Piers"], fiveStarPokeFairDict["SS Roxie"]], "2xPF"),
  "anni N": Banner("N (Anniversary 2021) Master Fair Scout", [fiveStarMasterFairDict["anni N"]], "masterFair"),
  "vol29": Banner("Vol. 29 Monthly Poke Fair Scout (Iono)", [fiveStarPokeFairDict["Iono"]], "pokeFair"),
  "ASLe": Banner("Arc Suit Leon Arc Suit Fair Scout", [fiveStarArcSuitFairDict["ASLe"]], "arcSuitFair"),
  "Arven": Banner("Arven Poke Fair Scout", [fiveStarPokeFairDict["Arven"]], "pokeFair"),
  "dec24_3xPF_A": Banner("Triple Feature Poke Fair Scout A", [fiveStarPokeFairDict["Chase"], fiveStarPokeFairDict["SS May"], fiveStarPokeFairDict["SS Cynthia"]], "3xPF"),
  "dec24_3xPF_B": Banner("Triple Feature Poke Fair Scout B", [fiveStarPokeFairDict["Rika"], fiveStarPokeFairDict["anni May"], fiveStarPokeFairDict["N"]], "3xPF"),
  "Milo": Banner("Milo Poke Fair Scout", [fiveStarPokeFairDict["Milo"]], "pokeFair"),
  "dec24_3xV": Banner("Triple Feature Variety Scout", [varietyDict["V.Hop"], varietyDict["V.Marnie"], varietyDict["V.Bede"]], "3xV"),
  "dec24_superCostume": Banner("Super Spotlight Costume Scout", [specialCostumeDict["SC Hilda"], specialCostumeDict["SC Diantha"], specialCostumeDict["SC Guzma"], specialCostumeDict["SC Jasmine"]], "superCostume"),
  "h!Lillie": Banner("Lillie (Holiday 2024) Seasonal Scout", [seasonalHolidayDict["h!Lillie"]], "seasonal"),
  "h!Bugsy": Banner("Bugsy (Holiday 2024) Seasonal Scout", [seasonalHolidayDict["h!Bugsy"]], "seasonal"),
  "NC Red": Banner("Red (Champion) Master Fair Scout", [fiveStarMasterFairDict["NC Red"]], "masterFair"),
  "NC Leaf": Banner("Leaf (Champion) Master Fair Scout", [fiveStarMasterFairDict["NC Leaf"]], "masterFair"),
  "NC Blue": Banner("Blue (Champion) Master Fair Scout", [fiveStarMasterFairDict["NC Blue"]], "masterFair"),
  "dec24_2xPF": Banner("Double Feature Poke Fair Scout", [fiveStarPokeFairDict["A.Elio"], fiveStarPokeFairDict["A.Selene"]], "2xPF"),
  "SS Red": Banner("Sygna Suit Red Poke Fair Scout", [fiveStarPokeFairDict["SS Red"]], "pokeFair"),
  "SS Blue": Banner("Sygna Suit Blue Poke Fair Scout", [fiveStarPokeFairDict["SS Blue"]], "pokeFair"),
  "SS Leaf": Banner("Sygna Suit Leaf Poke Fair Scout", [fiveStarPokeFairDict["SS Leaf"]], "pokeFair"),
  "vol28": Banner("Vol. 28 Monthly Poke Fair Scout (Gloria)", [fiveStarPokeFairDict["Gloria"]], "pokeFair"),
  "SS Ingo": Banner("Sygna Suit Ingo Poke Fair Scout", [fiveStarPokeFairDict["SS Ingo"]], "pokeFair"),
  "SS Emmet": Banner("Sygna Suit Emmet Poke Fair Scout", [fiveStarPokeFairDict["SS Emmet"]], "pokeFair"),
  "nov24_2xPF": Banner("Double Feature Poke Fair Scout", [fiveStarPokeFairDict["Ingo"], fiveStarPokeFairDict["Emmet"]], "2xPF"),
  "Eri": Banner("Eri Poke Fair Scout", [fiveStarPokeFairDict["Eri"]], "pokeFair"),
  "Sina": Banner("Sina Poke Fair Scout", [fiveStarPokeFairDict["Sina"]], "pokeFair"),
  "Dexio": Banner("Dexio Poke Fair Scout", [fiveStarPokeFairDict["Dexio"]], "pokeFair"),
  "nov24_3xV": Banner("Triple Feature Variety Scout", [varietyDict["V.Hilbert"], varietyDict["V.Hilda"], varietyDict["V.Calem"]], "3xV"),
  "Adaman": Banner("Adaman Master Fair Scout", [fiveStarMasterFairDict["Adaman"]], "pokeFair"),
  "nov24_superVariety": Banner("Super Spotlight Variety Scout", [varietyDict["V.Kris"], varietyDict["V.Lyra"], varietyDict["V.Lucas"], varietyDict["V.Selene"], varietyDict["V.Elio"]], "superVariety"),
  "Irida": Banner("Irida Master Fair Scout", [fiveStarMasterFairDict["Irida"]], "pokeFair"),
  "nov24_superScout": Banner("Super Spotlight Poke Fair Scout", [fiveStarPokeFairDict["Penny"], fiveStarPokeFairDict["Elaine"], fourStarDict["Tina"], fourStarDict["Rachel"]], "superScout"),
  "vol27": Banner("Vol. 27 Monthly Poke Fair Scout (Steven)", [fiveStarPokeFairDict["Steven"]], "pokeFair"),
  "Giacomo": Banner("Giacomo Poke Fair Scout", [fiveStarPokeFairDict["Giacomo"]], "pokeFair"),
  "Clavell": Banner("Clavell Poke Fair Scout", [fiveStarPokeFairDict["Clavell"]], "pokeFair"),
  "oct24_superScout": Banner("Super Spotlight Poke Fair Scout", [fiveStarPokeFairDict["SS Hau"], fiveStarPokeFairDict["SS Mina"], fiveStarPokeFairDict["SS Acerola"], fiveStarPokeFairDict["SS Lana"]], "superScout"),
  "oct24_3xPF_A": Banner("Triple Feature Poke Fair Scout A", [fiveStarPokeFairDict["SS Roxie"], fiveStarPokeFairDict["SS N"], fiveStarPokeFairDict["Kabu"]], "3xPF"),
  "oct24_3xPF_B": Banner("Triple Feature Poke Fair Scout B", [fiveStarPokeFairDict["SS Lysandre"], fiveStarPokeFairDict["Volo"], fiveStarPokeFairDict["Raihan"]], "3xPF"),
  "oct24_3xPF_C": Banner("Triple Feature Poke Fair Scout C", [fiveStarPokeFairDict["Jacq"], fiveStarPokeFairDict["SS Silver"], fiveStarPokeFairDict["SS Leon"]], "3xPF"),
  "oct24_3xPF": Banner("Triple Feature Poke Fair Scout", [fiveStarPokeFairDict["Iono"], fiveStarPokeFairDict["Dahlia"], fiveStarPokeFairDict["Diantha"]], "3xPF"),
  "fa Iono": Banner("Iono (Fall 2024) Seasonal Scout", [seasonalFallDict["fa Iono"]], "seasonal"),
  "fa Shauntal": Banner("Shauntal (Fall 2024) Seasonal Scout", [seasonalFallDict["fa Shauntal"]], "seasonal"),
  "oct24_2xPF": Banner("Double Feature Poke Fair Scout", [fiveStarPokeFairDict["Palmer"], fiveStarPokeFairDict["Argenta"]], "2xPF"),
  "SS Serena": Banner("Sygna Suit Serena Master Fair Scout", [fiveStarMasterFairDict["SS Serena"]], "masterFair"),
  "vol26": Banner("Vol. 26 Monthly Poke Fair Scout (Lear)", [fiveStarPokeFairDict["Lear"]], "pokeFair"),
  "ASC": Banner("Arc Suit Cynthia Arc Suit Fair Scout", [fiveStarArcSuitFairDict["ASC"]], "arcSuitFair"),
  "ASS": Banner("Arc Suit Steven Arc Suit Fair Scout", [fiveStarArcSuitFairDict["ASS"]], "arcSuitFair"),
  "ASL": Banner("Arc Suit Lance Arc Suit Fair Scout", [fiveStarArcSuitFairDict["ASL"]], "arcSuitFair"),
  "sep24_3xPF": Banner("Triple Feature Poke Fair Scout", [fiveStarPokeFairDict["Rika"], fiveStarPokeFairDict["A.Leon"], fiveStarPokeFairDict["anni Raihan"]], "3xPF"),
  "Malva": Banner("Malva Spotlight Scout", [fiveStarSpotlightDict["Malva"]], "spotlight"),
  "Chuck": Banner("Chuck Spotlight Scout", [fiveStarSpotlightDict["Chuck"]], "spotlight"),
  "Trevor": Banner("Trevor Spotlight Scout", [fiveStarSpotlightDict["Trevor"]], "spotlight"),
  "SS Lear": Banner("Sygna Suit Lear Master Fair Scout", [fiveStarMasterFairDict["SS Lear"]], "masterFair"),
  "sep24_2xV": Banner("Double Feature Variety Scout", [varietyDict["V.Sawyer"], varietyDict["V.Rachel"]], "2xV"),
  "Lear": Banner("Lear Poke Fair Scout", [fiveStarPokeFairDict["Lear"]], "pokeFair"),
  "SS Kris": Banner("Sygna Suit Kris Master Fair Scout", [fiveStarMasterFairDict["SS Kris"]], "masterFair"),
  "vol25": Banner("Vol. 25 Monthly Poke Fair Scout (Lance)", [fiveStarPokeFairDict["Lance"]], "pokeFair"),
  "A.Elio": Banner("Elio (Alt.) Poke Fair Scout", [fiveStarPokeFairDict["A.Elio"]], "pokeFair"),
  "A.Selene": Banner("Selene (Alt.) Poke Fair Scout", [fiveStarPokeFairDict["A.Selene"]], "pokeFair"),
  "aug24_3xPF": Banner("Triple Feature Poke Fair Scout", [fiveStarPokeFairDict["C.Iris"], fiveStarPokeFairDict["SS Diantha"], fiveStarPokeFairDict["Emma"]], "3xPF"),
  "aug24_2xPF": Banner("Double Feature Poke Fair Scout", [fiveStarPokeFairDict["SS Dawn"], fiveStarPokeFairDict["Lucas"]], "2xPF"),
  # "Arven": Banner("Arven Poke Fair Scout", [fiveStarPokeFairDict["Arven"]], "pokeFair"),
  "Penny": Banner("Penny Poke Fair Scout", [fiveStarPokeFairDict["Penny"]], "pokeFair"),
  "SS Nemona": Banner("Sygna Suit Nemona Master Fair Scout", [fiveStarMasterFairDict["SS Nemona"]], "masterFair"),
  "NC Marnie": Banner("Marnie (Champion) Master Fair Scout", [fiveStarMasterFairDict["NC Marnie"]], "masterFair"),
  "NC Hop": Banner("Hop (Champion) Master Fair Scout", [fiveStarMasterFairDict["NC Hop"]], "masterFair"),
  "NC Bede": Banner("Bede (Champion) Master Fair Scout", [fiveStarMasterFairDict["NC Bede"]], "masterFair"),
  "vol24": Banner("Vol. 24 Monthly Poke Fair Scout (N)", [fiveStarPokeFairDict["N"]], "pokeFair"),
  "sum Gardenia": Banner("Gardenia (Summer 2024) Seasonal Scout", [seasonalSummerDict["sum Gardenia"]], "seasonal"),
  "sum Acerola": Banner("Acerola (Summer 2024) Seasonal Scout", [seasonalSummerDict["sum Acerola"]], "seasonal"),
  "jul24_2xPF_A": Banner("Double Feature Poke Fair Scout", [fiveStarPokeFairDict["SS Cyrus"], fiveStarPokeFairDict["Akari"]], "2xPF"),
  "Klara": Banner("Klara Poke Fair Scout", [fiveStarPokeFairDict["Klara"]], "pokeFair"),
  "Avery": Banner("Avery Poke Fair Scout", [fiveStarPokeFairDict["Avery"]], "pokeFair"),
  "Greta": Banner("Greta Poke Fair Scout", [fiveStarPokeFairDict["Greta"]], "pokeFair"),
  "jul24_2xPF_B": Banner("Double Feature Poke Fair Scout", [fiveStarPokeFairDict["SS Brendan"], fiveStarPokeFairDict["SS Steven"]], "2xPF"),
  "SS Lyra": Banner("Sygna Suit Lyra Master Fair Scout", [fiveStarMasterFairDict["SS Lyra"]], "masterFair"),
  "vol23": Banner("Vol. 23 Monthly Poke Fair Scout (Cynthia)", [fiveStarPokeFairDict["Cynthia"]], "pokeFair"),
  "NC Cheren": Banner("Cheren (Champion) Master Fair Scout", [fiveStarMasterFairDict["NC Cheren"]], "masterFair"),
  "NC Bianca": Banner("Bianca (Champion) Master Fair Scout", [fiveStarMasterFairDict["NC Bianca"]], "masterFair"),
  "Ball Guy": Banner("Ball Guy Variety Scout", [varietyDict["Ball Guy"]], "variety"),
  "jun24_3xPF_A": Banner("Triple Feature Poke Fair Scout", [fiveStarPokeFairDict["SS Korrina"], fiveStarPokeFairDict["SS Lana"], fiveStarPokeFairDict["Argenta"]], "3xPF"),
  "Larry": Banner("Larry Poke Fair Scout", [fiveStarPokeFairDict["Larry"]], "pokeFair"),
  "Kabu": Banner("Kabu Poke Fair Scout", [fiveStarPokeFairDict["Kabu"]], "pokeFair"),
  "jun24_3xPF_B": Banner("Triple Feature Poke Fair Scout", [fiveStarPokeFairDict["Red"], fiveStarPokeFairDict["Anabel"], fiveStarPokeFairDict["Elaine"]], "3xPF"),
  "SS Ethan": Banner("Sygna Suit Ethan Master Fair Scout", [fiveStarMasterFairDict["SS Ethan"]], "masterFair"),
  "vol22": Banner("Vol. 22 Monthly Poke Fair Scout (Marnie)", [fiveStarPokeFairDict["Marnie"]], "pokeFair"),
  "Archie": Banner("Archie Master Fair Scout", [fiveStarMasterFairDict["Archie"]], "masterFair"),
  "Rika": Banner("Rika Poke Fair Scout", [fiveStarPokeFairDict["Rika"]], "pokeFair"),
  "may24_3xPF_A": Banner("Triple Feature Poke Fair Scout A", [fiveStarPokeFairDict["anni Skyla"], fiveStarPokeFairDict["SS Hilbert"], fiveStarPokeFairDict["SS Hau"]], "3xPF"),
  "may24_3xPF_B": Banner("Triple Feature Poke Fair Scout B", [fiveStarPokeFairDict["C.Blue"], fiveStarPokeFairDict["Palmer"], fiveStarPokeFairDict["SS Lysandre"]], "3xPF"),
  "may24_3xPF_C": Banner("Triple Feature Poke Fair Scout C", [fiveStarPokeFairDict["Emmet"], fiveStarPokeFairDict["SS Giovanni"], fiveStarPokeFairDict["D.Gloria"]], "3xPF"),
  "Brycen-Man": Banner("Brycen-Man Costume Scout", [specialCostumeDict["Brycen-Man"]], "costume"),
  "Belleba": Banner("Belleba Costume Scout", [specialCostumeDict["Belleba"]], "costume"),
  "SS Morty": Banner("Sygna Suit Morty Poke Fair Scout", [fiveStarPokeFairDict["SS Morty"]], "pokeFair"),
  "may24_2xPF_A": Banner("Double Feature Poke Fair Scout", [fiveStarPokeFairDict["SS Wally"], fiveStarPokeFairDict["Bede"]], "2xPF"),
  "V.Guzma": Banner("Guzma Variety Scout", [varietyDict["V.Guzma"]], "variety"),
  "V.Plumeria": Banner("Plumeria Variety Scout", [varietyDict["V.Plumeria"]], "variety"),
  "Poppy": Banner("Poppy Poke Fair Scout", [fiveStarPokeFairDict["Poppy"]], "pokeFair"),
  "may24_2xPF_B": Banner("Double Feature Poke Fair Scout", [fiveStarPokeFairDict["SS Silver"], fiveStarPokeFairDict["Eusine"]], "2xPF"),
  "Maxie": Banner("Maxie Master Fair Scout", [fiveStarMasterFairDict["Maxie"]], "masterFair"),
  "vol21": Banner("Vol. 21 Monthly Poke Fair Scout (Raihan)", [fiveStarPokeFairDict["Raihan"]], "pokeFair"),
  "Volo": Banner("Volo Poke Fair Scout", [fiveStarPokeFairDict["Volo"]], "pokeFair"),
  "Jacq": Banner("Jacq Poke Fair Scout", [fiveStarPokeFairDict["Jacq"]], "pokeFair"),
  "apr24_3xPF_A": Banner("Triple Feature Poke Fair Scout", [fiveStarPokeFairDict["C.Elesa"], fiveStarPokeFairDict["Lysandre"], fiveStarPokeFairDict["Emma"]], "3xPF"),
  "apr24_3xPF_B": Banner("Triple Feature Poke Fair Scout", [fiveStarPokeFairDict["SS Red"], fiveStarPokeFairDict["SS Hilda"], fiveStarPokeFairDict["SS May"]], "3xPF"),
  "SC Barry": Banner("Barry Costume Scout", [specialCostumeDict["SC Barry"]], "costume"),
  "SC Selene": Banner("Selene Costume Scout", [specialCostumeDict["SC Selene"]], "costume"),
  "apr24_superVariety": Banner("Super Spotlight Variety Scout", [varietyDict["V.Lorelei"], varietyDict["V.Bruno"], varietyDict["V.Agatha"], varietyDict["V.Lance"]], "superVariety"),
  "vol20": Banner("Vol. 20 Monthly Poke Fair Scout (Gloria)", [fiveStarPokeFairDict["Gloria"]], "pokeFair"),
  # geeta debut here
  "NC Silver": Banner("Silver (Champion) Master Fair Scout", [fiveStarMasterFairDict["NC Silver"]], "masterFair"),
  "mar24_2xPF_A": Banner("Double Feature Poke Fair Scout", [fiveStarPokeFairDict["SS Dawn"], fiveStarPokeFairDict["anni May"]], "2xPF"),
  "SC Adaman": Banner("Adaman Costume Scout", [specialCostumeDict["SC Adaman"]], "costume"),
  "SC Irida": Banner("Irida Costume Scout", [specialCostumeDict["SC Irida"]], "costume"),
  "Tierno": Banner("Tierno Spotlight Scout", [fiveStarSpotlightDict["Tierno"]], "spotlight"),
  "mar24_2xPF_B": Banner("Double Feature Poke Fair Scout", [fiveStarPokeFairDict["Rose"], fiveStarPokeFairDict["Oleana"]], "2xPF"),
  "Dahlia": Banner("Dahlia Poke Fair Scout", [fiveStarPokeFairDict["Dahlia"]], "pokeFair"),
  "SSR Cynthia": Banner("Sygna Suit (Renegade) Cynthia Master Fair Scout", [fiveStarMasterFairDict["SSR Cynthia"]], "masterFair"),
  "vol19": Banner("Vol. 19 Monthly Poke Fair Scout (Steven)", [fiveStarPokeFairDict["Steven"]], "pokeFair"),
  "Chase": Banner("Chase Poke Fair Scout", [fiveStarPokeFairDict["Chase"]], "pokeFair"),
  "vol18": Banner("Vol. 18 Monthly Poke Fair Scout (N)", [fiveStarPokeFairDict["N"]], "pokeFair"),
  "feb24_3xPF": Banner("Triple Feature Poke Fair Scout", [fiveStarPokeFairDict["SS Brendan"], fiveStarPokeFairDict["SS Red"], fiveStarPokeFairDict["Alder"]], "3xPF"),
  "V.Falkner": Banner("Falkner Variety Scout", [varietyDict["V.Falkner"]], "variety"),
  "pal Victor": Banner("Victor (Palentines' 2024) Seasonal Scout", [seasonalPalentinesDict["pal Victor"]], "seasonal"),
  "pal Candice": Banner("Candice (Palentines' 2024) Seasonal Scout", [seasonalPalentinesDict["pal Candice"]], "seasonal"),
  # SS Gladion debut
  "anni Lillie": Banner("Lillie (Anniversary 2021) Master Fair Scout", [fiveStarMasterFairDict["anni Lillie"]], "masterFair"),
  "SS Lusamine": Banner("Sygna Suit Lusamine Master Fair Scout", [fiveStarMasterFairDict["SS Lusamine"]], "masterFair"),
  "SS Steven": Banner("Sygna Suit Steven Poke Fair Scout", [fiveStarPokeFairDict["SS Steven"]], "pokeFair"),
  "SSA Cynthia": Banner("Sygna Suit (Aura) Cynthia Master Fair Scout", [fiveStarMasterFairDict["SSA Cynthia"]], "masterFair"),
  "SST Red": Banner("Sygna Suit (Thunderbolt) Red Master Fair Scout", [fiveStarMasterFairDict["SST Red"]], "masterFair"),
  "NY Clair": Banner("Clair (New Year's 2024) Seasonal Scout", [seasonalNewYearDict["NY Clair"]], "seasonal"),
  "NY Wallace": Banner("Wallace (New Year's 2024) Seasonal Scout", [seasonalNewYearDict["NY Wallace"]], "seasonal"),
  "vol17": Banner("Vol. 17 Monthly Poke Fair Scout (Cynthia)", [fiveStarPokeFairDict["Cynthia"]], "pokeFair"),
  "jan24_2xPF": Banner("Double Feature Poke Fair Scout", [fiveStarPokeFairDict["SS Leaf"], fiveStarPokeFairDict["Victor"]], "2xPF"),
  "Iono": Banner("Iono Poke Fair Scout", [fiveStarPokeFairDict["Iono"]], "pokeFair"),
  "jan24_3xPF": Banner("Triple Feature Poke Fair Scout", [fiveStarPokeFairDict["SS Cynthia"], fiveStarPokeFairDict["SS Leon"], fiveStarPokeFairDict["Lucas"]], "3xPF"),
  "Grusha": Banner("Grusha Poke Fair Scout", [fiveStarPokeFairDict["Grusha"]], "pokeFair"),
  "Leon": Banner("Leon Master Fair Scout (mid)", [fiveStarMasterFairDict["Leon"]], "masterFair"),
  "jan24_3xSP": Banner("Triple Feature Spotlight Scout", [fiveStarSpotlightDict["K.Grimsley"], fiveStarSpotlightDict["SS Elesa"], fiveStarSpotlightDict["Phoebe"]], "3xSP"),
  # NC Nate debut
  "vol16": Banner("Vol. 16 Monthly Poke Fair Scout (Marnie)", [fiveStarPokeFairDict["Marnie"]], "pokeFair"),
  "dec23_3xPF": Banner("Triple Feature Poke Fair Scout", [fiveStarPokeFairDict["SS Korrina"], fiveStarPokeFairDict["SS Blue"], fiveStarPokeFairDict["Emma"]], "3xPF"),
  "h!Viola": Banner("Viola (Holiday 2023) Seasonal Scout", [seasonalHolidayDict["h!Viola"]], "seasonal"),
  "h!Sycamore": Banner("Sycamore (Holiday 2023) Seasonal Scout", [seasonalHolidayDict["h!Sycamore"]], "seasonal"),
  # NC Rosa debut
  "SS Roxie": Banner("Sygna Suit Roxie Poke Fair Scout", [fiveStarPokeFairDict["SS Roxie"]], "pokeFair"),
  "vol15": Banner("Vol. 15 Monthly Poke Fair Scout (Raihan)", [fiveStarPokeFairDict["Raihan"]], "pokeFair"),
  "SS Piers": Banner("Sygna Suit Piers Poke Fair Scout", [fiveStarPokeFairDict["SS Piers"]], "pokeFair"),
  "Ryuki": Banner("Ryuki Spotlight Scout", [fiveStarSpotlightDict["Ryuki"]], "spotlight"),
  "C.Iris": Banner("Iris (Alt.) Poke Fair Scout", [fiveStarPokeFairDict["C.Iris"]], "pokeFair"),
  "nov23_2xPF": Banner("Double Feature Poke Fair Scout", [fiveStarPokeFairDict["SS Morty"], fiveStarPokeFairDict["SS May"]], "2xPF"),
  # Penny debut
  "Elaine": Banner("Elaine Poke Fair Scout", [fiveStarPokeFairDict["Elaine"]], "pokeFair"),
  "nov23_2xV": Banner("Double Feature Variety Scout", [varietyDict["V.Selene"], varietyDict["V.Elio"]], "2xV"),
  "nov23_3xV": Banner("Triple Feature Variety Scout", [varietyDict["V.Lyra"], varietyDict["V.Kris"], varietyDict["V.Lucas"]], "3xV"),
  "nov23_2xPF_2": Banner("Double Feature Poke Fair Scout", [fiveStarPokeFairDict["SS Diantha"], fiveStarPokeFairDict["Anabel"]], "2xPF"),
  "NC Serena": Banner("Serena (Champion) Master Fair Scout (NC SERENA RERUN WHEN)", [fiveStarMasterFairDict["NC Serena"]], "masterFair"),
  "Akari": Banner("Akari Poke Fair Scout", [fiveStarPokeFairDict["Akari"]], "pokeFair"),
  "Rei": Banner("Rei Poke Fair Scout", [fiveStarPokeFairDict["Rei"]], "pokeFair"),
  "vol14": Banner("Vol. 14 Monthly Poke Fair Scout (Steven)", [fiveStarPokeFairDict["Steven"]], "pokeFair"),
  "V.Thorton": Banner("Thorton Variety Scout", [varietyDict["V.Thorton"]], "variety"),
  "V.Noland": Banner("Noland Variety Scout", [varietyDict["V.Noland"]], "variety"),
  "oct23_3xPF": Banner("Triple Feature Poke Fair Scout", [fiveStarPokeFairDict["SS Hau"], fiveStarPokeFairDict["Red"], fiveStarPokeFairDict["Lance"]], "3xPF"),
  "fa Phoebe": Banner("Phoebe (Fall 2023) Seasonal Scout", [seasonalFallDict["fa Phoebe"]], "seasonal"),
  "fa Roxanne": Banner("Roxanne (Fall 2023) Seasonal Scout", [seasonalFallDict["fa Roxanne"]], "seasonal"),
  "oct23_3xPF_2": Banner("Triple Feature Poke Fair Scout", [fiveStarPokeFairDict["SS Hilda"], fiveStarPokeFairDict["SS Hilbert"], fiveStarPokeFairDict["SS N"]], "3xPF"),
  "NC Calem": Banner("Calem (Champion) Master Fair Scout", [fiveStarMasterFairDict["NC Calem"]], "masterFair"),
  # NC Red debut
  # NC Leaf debut
  # NC Blue debut
  "vol13": Banner("Vol. 13 Monthly Poke Fair Scout (Gloria)", [fiveStarPokeFairDict["Gloria"]], "pokeFair"),
  "sep23_2xPF": Banner("Double Feature Poke Fair Scout", [fiveStarPokeFairDict["SS Cyrus"], fiveStarPokeFairDict["SS Lysandre"]], "2xPF"),
  "sep23_superVariety": Banner("Team Rocket Variety Scout", [varietyDict["V.Giovanni"], varietyDict["V.Archer"], varietyDict["V.Ariana"], varietyDict["V.Petrel"], varietyDict["V.Proton"]], "superVariety"),
  "SC Rosa": Banner("Rosa Costume Scout", [specialCostumeDict["SC Rosa"]], "costume"),
  "C.Elesa": Banner("Elesa (Alt.) Poke Fair Scout", [fiveStarPokeFairDict["C.Elesa"]], "pokeFair"),
  "Palmer": Banner("Palmer Poke Fair Scout", [fiveStarPokeFairDict["Palmer"]], "pokeFair"),
  "Argenta": Banner("Argenta Poke Fair Scout", [fiveStarPokeFairDict["Argenta"]], "pokeFair"),
  "Bede": Banner("Bede Poke Fair Scout", [fiveStarPokeFairDict["Bede"]], "pokeFair"),
  # SS Serena rerun (they really like rerunning her)
  "A.Leon": Banner("Leon (Alt.) Poke Fair Scout", [fiveStarPokeFairDict["A.Leon"]], "pokeFair"),
  "vol12": Banner("Vol. 12 Monthly Poke Fair Scout (N)", [fiveStarPokeFairDict["N"]], "pokeFair"),
  "A2Gloria": Banner("Gloria (Alt. 2) Poke Fair Scout", [fiveStarPokeFairDict["A2Gloria"]], "pokeFair"),
  "Olympia": Banner("Olympia Spotlight Scout", [fiveStarSpotlightDict["Olympia"]], "spotlight"),
  "Drasna": Banner("Drasna Spotlight Scout", [fiveStarSpotlightDict["Drasna"]], "spotlight"),
  "Nemona": Banner("Nemona Poke Fair Scout", [fiveStarPokeFairDict["Nemona"]], "pokeFair"),
  "aug23_3xPF": Banner("Triple Feature Poke Fair Scout", [fiveStarPokeFairDict["Ingo"], fiveStarPokeFairDict["Red"], fiveStarPokeFairDict["Diantha"]], "3xPF"),
  # SS Kris debut
  # SS Lyra debut
  # SS Ethan debut
  "sum Tate": Banner("Tate (Summer 2023) Seasonal Scout", [seasonalSummerDict["sum Tate"]], "seasonal"),
  "vol11": Banner("Vol. 11 Monthly Poke Fair Scout (Cynthia)", [fiveStarPokeFairDict["Cynthia"]], "pokeFair"),
  "sum Liza": Banner("Liza (Summer 2023) Seasonal Scout", [seasonalSummerDict["sum Liza"]], "seasonal"),
  "jul23_2xPF": Banner("Double Feature Poke Fair Scout", [fiveStarPokeFairDict["D.Gloria"], fiveStarPokeFairDict["SS Lysandre"]], "2xPF"),
  "Rose": Banner("Rose Poke Fair Scout", [fiveStarPokeFairDict["Rose"]], "pokeFair"),
  "Oleana": Banner("Oleana Poke Fair Scout", [fiveStarPokeFairDict["Oleana"]], "pokeFair"),
  "V.Kiawe": Banner("Kiawe Variety Scout", [varietyDict["V.Kiawe"]], "variety"),
  "V.Mallow": Banner("Mallow Variety Scout", [varietyDict["V.Mallow"]], "variety"),
  # Maxie rerun
  "SS Wally": Banner("Sygna Suit Wally Poke Fair Scout", [fiveStarPokeFairDict["SS Wally"]], "pokeFair"),
  # Adaman debut
  "vol10": Banner("Vol. 10 Monthly Poke Fair Scout (Marnie)", [fiveStarPokeFairDict["Marnie"]], "pokeFair"),
  # Irida debut
  # SS Morty debut
  "Eusine": Banner("Eusine Poke Fair Scout", [fiveStarPokeFairDict["Eusine"]], "pokeFair"),
  "SS Silver": Banner("Sygna Suit Silver Poke Fair Scout", [fiveStarPokeFairDict["SS Silver"]], "pokeFair"),
  "SS May": Banner("Sygna Suit May Poke Fair Scout", [fiveStarPokeFairDict["SS May"]], "pokeFair"),
  # Archie rerun
  "SS N": Banner("Sygna Suit N Poke Fair Scout", [fiveStarPokeFairDict["SS N"]], "pokeFair"),
  "SS Hau": Banner("Sygna Suit Hau Poke Fair Scout", [fiveStarPokeFairDict["SS Hau"]], "pokeFair"),
  "SS Mina": Banner("Sygna Suit Mina Poke Fair Scout", [fiveStarPokeFairDict["SS Mina"]], "pokeFair"),
  "vol9": Banner("Vol. 9 Monthly Poke Fair Scout (Raihan)", [fiveStarPokeFairDict["Raihan"]], "pokeFair"),
  # Fashion week banner - WIP
  # 50M download banner - WIP
  "V.Agatha": Banner("Agatha Variety Scout", [varietyDict["V.Agatha"]], "variety"),
  "V.Lance": Banner("Lance Variety Scout", [varietyDict["V.Lance"]], "variety"),
  "SS Acerola": Banner("Sygna Suit Acerola Poke Fair Scout", [fiveStarPokeFairDict["SS Acerola"]], "pokeFair"),
  "SS Lana": Banner("Sygna Suit Lana Poke Fair Scout", [fiveStarPokeFairDict["SS Lana"]], "pokeFair"),
  "may23_3xPF": Banner("Triple Feature Poke Fair Scout", [fiveStarPokeFairDict["Alder"], fiveStarPokeFairDict["SS Blue"], fiveStarPokeFairDict["SS Red"]], "3xPF"),
  # SSR cynthia rerun
  "SC Steven": Banner("Steven Costume Scout", [specialCostumeDict["SC Steven"]], "costume"),
  "vol8": Banner("Vol. 8 Monthly Poke Fair Scout (Steven)", [fiveStarPokeFairDict["Steven"]], "pokeFair"),
  "SC Shauna": Banner("Shauna Costume Scout", [specialCostumeDict["SC Shauna"]], "costume"),
  "apr23_2xSE": Banner("Seasonal Super Spotlight Scout", [seasonalSpringDict["sp May"], seasonalSpringDict["sp Burgh"]], "2xSE"),
  "Victor": Banner("Victor Poke Fair Scout", [fiveStarPokeFairDict["Victor"]], "pokeFair"),
  "SC Zinnia": Banner("Zinnia Costume Scout", [specialCostumeDict["SC Zinnia"]], "costume"),
  "SC Lyra": Banner("Lyra Costume Scout", [specialCostumeDict["SC Lyra"]], "costume"),
  "V.Lorelei": Banner("Lorelei Variety Scout", [varietyDict["V.Lorelei"]], "variety"),
  "apr23_superCostume": Banner("Special Costume Seasonal Scout", [specialCostumeDict["SC Lillie"], specialCostumeDict["SC Sonia"], specialCostumeDict["SC Ingo"], specialCostumeDict["SC Emmet"]], "superCostume"),
  "V.Bruno": Banner("Bruno Variety Scout", [varietyDict["V.Bruno"]], "variety"),
  # SS Lusamine rerun
  # NC Marnie debut
  "vol7": Banner("Vol. 7 Monthly Poke Fair Scout (Gloria)", [fiveStarPokeFairDict["Gloria"]], "pokeFair"),
  # NC Hop debut
  # NC Bede debut
  "mar23_3xPF": Banner("Triple Feature Charming Poke Fair Scout", [fiveStarPokeFairDict["anni Raihan"], fiveStarPokeFairDict["Red"], fiveStarPokeFairDict["Lucas"]], "3xPF"),
  "mar23_3xPF_2": Banner("Triple Feature Poke Fair Scout", [fiveStarPokeFairDict["SS Cynthia"], fiveStarPokeFairDict["Emmet"], fiveStarPokeFairDict["Lysandre"]], "3xPF"),
  # Ball Guy rerun/debut idk
  "Lance": Banner("Lance Poke Fair Scout", [fiveStarPokeFairDict["Lance"]], "pokeFair"),
  "mar23_2xPF": Banner("Double Feature Poke Fair Scout (Eon Duo Banner)", [fiveStarPokeFairDict["anni May"], fiveStarPokeFairDict["SS Brendan"]], "2xPF"),
  # SEASONAL RERUNS VVV
  "holiRerun": Banner("Super Spotlight Seasonal Scout (Holiday)", seasonalHoliday, "seasonalRerun"),
  "fallRerun": Banner("Super Spotlight Seasonal Scout (Fall)", seasonalFall, "seasonalRerun"),
  "sumRerun": Banner("Super Spotlight Seasonal Scout (Summer)", seasonalSummer, "seasonalRerun"),
  "palRerun": Banner("Super Spotlight Seasonal Scout (Palentines')", seasonalPalentines, "seasonalRerun"),
  "NYRerun": Banner("Super Spotlight Seasonal Scout (New Year's)", seasonalNewYear, "seasonalRerun")
}

gymBannersDict = {
  "A": Banner("Gym Scout (A)", gymList[:3], "gym"),
  "B": Banner("Gym Scout (B)", gymList[3:], "gym")
}

mixBannersDict = {
  "a": Banner("Red Mix Scout", [mixExclusiveDict["mix Red"]], "mix"),
  "b": Banner("Blue Mix Scout", [mixExclusiveDict["mix Blue"]], "mix"),
  "c": Banner("Leaf Mix Scout", [mixExclusiveDict["mix Leaf"]], "mix"),
  "d": Banner("Lucas Mix Scout", [mixExclusiveDict["mix Lucas"]], "mix"),
  "e": Banner("Dawn Mix Scout", [mixExclusiveDict["mix Dawn"]], "mix"),
  "f": Banner("Barry Mix Scout", [mixExclusiveDict["mix Barry"]], "mix")
}

def gymScout():
  print("----------------------------------------")
  print("Choose the gym scout you want to scout on:")
  # print("--- MAY 2025 ---")
  print("(A) Brock, Winona & Grusha")
  print("(B) Whitney, Korrina & Kabu")
  print("Due to technical limitations, a gym scout will have a pool as if it was reran at the present time. It is not possible to simulate the pool of the gym scout at the time of its release (yet).")
  match input("Which gym scout do you want to scout on? \n> "):
    case "A":
      bannerSelect(gymBannersDict["A"])
    case "B":
      bannerSelect(gymBannersDict["B"])

def mixScout():
  print("----------------------------------------")
  print("Choose the mix scout you want to scout on:")
  # print("--- MAY 2025 ---")
  print("(a) Red")
  print("(b) Blue")
  print("(c) Leaf")
  print("(d) Lucas")
  print("(e) Dawn")
  print("Due to technical limitations, a mix scout will have a pool as if it was reran at the present time. It is not possible to simulate the pool of the mix scout at the time of its release (yet).")
  match input("Which mix scout do you want to scout on? \n> "):
    case "a":
      bannerSelect(mixBannersDict["a"])
    case "b":
      bannerSelect(mixBannersDict["b"])
    case "c":
      bannerSelect(mixBannersDict["c"])
    case "d":
      bannerSelect(mixBannersDict["d"])
    case "e":
      bannerSelect(mixBannersDict["e"])
    case "f":
      bannerSelect(mixBannersDict["f"])
    case _:
      print("Invalid input. Please try again.")
banners = list(bannersDict.values())
bannerNames = list(bannersDict.keys())

def loopBanners(bannerList: list, newMonth: dict, oldest: str):
  dummyDict = {}
  for i in range(len(bannerList)):
    if bannerNames[i] in list(newMonth.keys()):
      print(f"--- {newMonth[bannerNames[i]]} ---")
    dummyDict[str(i+1)] = bannerList[i]
    print(f"({i+1}) {bannerList[i].name}")
  print("BANNERS OLDER THAN " + oldest + " ARE YET TO BE AVAILABLE")
  print("Select Scouts in Anniversary and Type-Exclusive Poke Fairs (which will act as Regular PF banners if they have featured PFs) are yet to be available.")
  print("If a banner appears multiple times in the span of the included dates, it will open appear ONCE in the most recent reran month in the list.")
  print("If any banners are missing, feel free to message me on Discord (miraidon_the_motorbike) / Reddit (u/notsusimpostor), or create a GitHub issue. Do include the featured pair(s), banner month, release month, and the banner type (if possible, include the rates of pulling the featured or 5*s).")
  print()
  print("--- MISC ---")
  print(f"(#) {cyan}Gym Scout(s){reset()}")
  print(f"(!) {red}Mix Scout(s){reset()}")
  print(f"(@) {cyan}Daily Scout{reset()}")
  print(f"($) {brown}5* Guaranteed Ticket Scout{reset()}")
  print(f"(&) {blue}Fair-Guaranteed Ticket Scout{reset()}")
  print(f"(%) {blue}Fair-exclusive pairs included! 10-pair Scout{reset()}")
  print(f"(^) {brown}Six-Year Anniversary Ticket Scout{reset()}")
  print()
  print("Due to technical limitations, a banner will have a pool as if it was reran at the present time. It is not possible to simulate the pool of the banner at the time of its release (yet).")
  print("Note: The fair guaranteed/included ticket will include all limiteds, despite it excluding the ones that debuted in the last three versions in the game, due to technical limitations.")
  return dummyDict

def startSim():
  print("----------------------------------------")
  print("Choose the banner you want to scout on:")
  print("--- SEP 2025 (6th anni) ---")
  dummyDict = loopBanners(banners, {
    "Carmine": "AUG 2025 (Pre-anni 6th)",
    "sum Cynthia": "JUL 2025 (Summer 2025)",
    "NC Elio": "JUN 2025",
    "SS Bede": "MAY 2025",
    "SC Rei": "APR 2025",
    "mar_3xMF": "MAR 2025 (5.5th Anni)",
    "pal Marley": "FEB 2025 (Pre-anni 5.5th) (Palentines' 2025)",
    "SSA Giovanni": "JAN 2025 (New Years' 2025)",
    "ASLe": "DEC 2024 (Holiday 2024)",
    "SS Ingo": "NOV 2024",
    "Giacomo": "OCT 2024 (Fall 2024)",
    "ASC": "SEP 2024 (5th Anni)",
    "A.Elio": "AUG 2024 (Pre-anni 5th)",
    "sum Gardenia": "JUL 2024 (Summer 2024)",
    "NC Cheren": "JUN 2024",
    "Archie": "MAY 2024",
    "Volo": "APR 2024",
    "NC Silver": "MAR 2024 (4.5th Anni)",
    "Chase": "FEB 2024 (Pre-anni 4.5th)",
    "SSA Cynthia": "JAN 2024 (New Years' 2024)",
    "vol16": "DEC 2023 (Holiday 2023)",
    "SS Roxie": "NOV 2023",
    "Akari": "OCT 2023 (Fall 2023)",
    "vol13": "SEP 2023 (4th anni)",
    "A.Leon": "AUG 2023 (Pre-anni 4th)",
    "sum Tate": "JUL 2023 (Summer 2023)",
    "vol10": "JUN 2023",
    "SS Hau": "MAY 2023",
    "SC Steven": "APR 2023",
    "vol7": "MAR 2023 (3.5th anni)",
    "holiRerun": f"{green}SEASONAL RERUNS{reset()}"
  }, "3.5th Anni")
  print(red + "NOTE - There is not enough data for the 'Fifty million downloads Poke Fair Scout' or 'Fashion Week Limited Scout' to be included in the list" + reset())
  target = input("Which banner do you want to scout on? \n> ")
  if target in list(dummyDict.keys()):
    bannerSelect(dummyDict[target])
  else:
    match target:
      case "#":
        gymScout()
      case "!":
        mixScout()
      case "@":
        bannerSelect(Banner("Daily Scout", [], "daily", dailyPool = True))
      case "$":
        bannerSelect(Banner("5* Guaranteed Ticket Scout", [], "pokeFair", fiveStarOnly = True))
      case "&":
        bannerSelect(Banner("Fair-Guaranteed Ticket Scout", [], "fairTicket"))
      case "%":
        bannerSelect(Banner("Fair-exclusive pairs included! 10-pair Scout", [fiveStarPokeFair], "10ticket"))
      case "^":
        bannerSelect(Banner("Six-Year Anniversary Ticket Scout", [], "anniTicket"))
      case _:
        print("Invalid input. Please try again.")
    

def menu():
  print(rainbow("Pokemon Masters EX - Pull Simulator Reborn"))
  print("Version: v3.0.0")
  print()
  print()
  print(bold + "(a) Start Simulation", reset())
  print()
  print("(s) Settings")
  print("(x) Sync Pair Addition Progress")
  print("(l) Update Log")
  print("(q) Quit")
  print()
  print("Tip: Scouting is too slow/fast? Change it in settings!")
  action = input("> ")
  match action:
    case "a":
      startSim()
    case "s":
      global pullInt
      print("----------------------------------------")
      print("The current interval between singles is", pullInt, "seconds.")
      print("Enter the new value: (only positive numbers are accepted)")
      try:
        pullInt = float(input("> "))
      except ValueError:
        print("Invalid input.")
    case "x":
      print("----------------------------------------")
      print("3* General Pool: 20/20 [COMPLETED]")
      print("3* Story: 0/?? ")
      print("4* General Pool: 19/19")
      print("4* Story: 0/??")
      print("4* Poke Fair: 3/3 [COMPLETED]")
      print("5* General Pool: 75/75 [COMPLETED]")
      print("5* Story: 0/??")
      print("5* Poke Fair: 97/97 [COMPLETED]")
      print("5* Event Exclusive: 0/??")
      print("5* BP: 0/??")
      print("5* Variety: 34/34 [COMPLETED]")
      print("5* Damage Challenge: 0/??")
      print("5* Seasonal: 54/54 [COMPLETED]")
      print("5* Mix: 5/5 [COMPLETED]")
      print("5* Special Costume: 22/22 [COMPLETED]")
      print("5* Master Fair: 39/39 [COMPLETED]")
      print("5* Arc Suit Fair: 8/8 [COMPLETED]")
      print("5* EX Master Fair: 4/4 [COMPLETED]")
      print("Gym Scout: 6/6 [COMPLETED]")
    case "l":
      print("----------------------------------------")
      print(f"""
      {bold}v3.0.0 - Sixth Anniversary Returning Update [2025-09-06] {red}(LATEST){reset()}
      - {rainbow("Long time no see, and I'm back!")}
      - Added pairs and scouts from game version v2.58.0 to v2.60.0 (July to September 2025).
      - Added scouts from March 2023 to February 2024. (Yes you heard that right. 12 MONTHS, 100+ BANNERS.)
      - New banner type: EX Master Fair.
      - Every scoutable pair now has EX (since the anniversary update)
      - Seasonal Reruns are now separate from other banners for more convenience.
      - Fixed spelling mistakes ("Syncamore" -> "Sycamore") ("Falkneer" -> "Falkner")
      - Added Fair-included ticket scout and sixth anni ticket scout.

      v2.2.0 - June Datamine Update [2025-05-29]
      - Added pairs and scouts from game version v2.57.0 (June 2025).
      - Added scouts from March to September 2024.
      - Fixed bug of being unable to change settings.
      
      v2.1.0 - Past Banners Patch 1 [2025-05-22]
      - Added scouts from September to December 2024.
      - Changed storage of the remaining spotlight pairs that remain stored in lists before this update, to dictionaries.
      - Added the update log (which you're reading now).
      - Changed the interval between singles from 0.1s to 0.2s. They are now customizable via Settings.
      - Added settings.
      - Fixed the bug of being unable to quit the software via the input "q".
      - Fixed the issue of Selene (Alt.) being mistakenly named "Stakataka" in dictionary keys.
      - Fixed the issue with pair searching when pitying.
      - {rainbow("Happy Line 1000!")}{reset()} The simulator has reached 1000 lines of code!
      
      v2.0.2 - Emergency Patch 2 [2025-05-21]
      - Fixed the issue of the rates of pulling an MF/AS.
      - Fixed the issue of scout points not cleared after pitying.

      v2.0.1 - Emergency Patch 1 [2025-05-19]
      - Fixed the bug of being unable to pull any 5*s.
      - Fixed pitying functionality.
      - Fixed the but of being unable to pity.

      v2.0.0 - The Supplementary Update (Not Disclosed) [2025-05-19]
      - Changed storage of banners, now they are created only once, hence they have the memory of gem count.
      - Added Mix Scout and Gym Scout.
      - Added Variety sync pairs.
      - Temporarily changed the interval between singles from 1s to 0.1s.
      - Fixed Major Bug of “NC Rosa / SC Marnie / SC Morty” being referenced incorrectly as “SS Rosa / Marnie / Morty”.

      v1.9.0 - The Special Costume Update [2025-05-18]
      - Added SC pairs.
      - Changed the storage type of sync pairs, from lists to dictionaries.
      - Added scouts for February 2025.
      - Fixed the Pokemon of the PF Victor being incorrect.

      v1.0.0 - Release [2025-05-17]
      - Initial release.
      """)
    case "q":
      exit(0)
    case _:
      print("----------------------------------------")
      print("Invalid input. Please try again.") 
  print()
  awaitEnter()
  clear()

while action != "q":
  menu()