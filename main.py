# from colorama import Fore as fore
# from colorama import Style as style
from random import uniform, choice
from time import sleep
from os import system

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

def stars2color(stars):
  match stars:
    case 3:
      return brown
    case 4:
      return grey
    case 5:
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
    case "3xMF":
      return magenta
    case 'ticketM':
      return magenta
    case "arcSuitFair":
      return yellow
    case "spotlight":
      return brown
    case "mix":
      return red
    case "variety":
      return red
    case "seasonal":
      return green
    case "seasonalRerun":
      return green
    case "costume":
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
  def __init__(self, name, featuredPairs, type, genPool = True, fiveStarOnly = False, mixPool = False, dailyPool = False):
    self.name = type2color(type) + name + reset()
    self.featuredPairs = featuredPairs
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
    elif self.type == "pokeFair":
      self.rates = [2, 10, 30]
    elif self.type == "masterFair":
      self.rates = [1, 12, 32]
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
    elif self.type == "2xSC":
      self.rates = [3, 7, 27]
    elif self.type == "seasonal":
      self.rates = [2, 7, 27]
    elif self.type == "seasonalRerun":
      self.rates = [2, 7, 27]
    elif self.type == "ticket":
      self.rates = [25, 34, 54]
    elif self.type == "ticketM":
      self.rates = [100, 0, 0]
    elif self.type == "gym":
      self.rates = [2, 7, 27]
    elif self.type == "variety":
      self.rates = [2, 7, 27]
    else:
      raise ValueError("Invalid banner type")
    if fiveStarOnly:
      self.rates = [0, 100, 100]

    if mixPool:
      self.pool5 = mixFull
    elif genPool:
      self.pool5 = fiveStarSpotlight
    if dailyPool:
      self.featuredPairs = fiveStarMasterFair + fiveStarArcSuitFair + seasonalFull + fiveStarPokeFair + specialCostume + variety + mixExclusive
      
    self.pairs = self.featuredPairs + self.pool5 + sortByObtain(fourStar,"General") + threeStar
    
  def __str__(self):
    return "\n".join([pair.__str__() for pair in self.featuredPairs]) if not self.dailyPool else "ALL Sync Pairs up to Feb 2025 (3 months prior)"

  def checkPity(self):
    if self.type in ["ticket", "ticketM", "daily", "gym"]:
      return False
    if self.multis * 11 + self.singles >= 300 and self.type == "mix":
      return True
    elif self.multis * 11 + self.singles >= 400 and self.type != "arcSuitFair":
      return True
    elif self.multis * 11 + self.singles >= 500 and self.type == "arcSuitFair":
      return True
    else:
      return False
    
  def single(self):
    factor = uniform(1, 100)
    if factor <= self.rates[0]:
      scouted = choice(self.featuredPairs)
    elif factor <= self.rates[1]:
      scouted = choice(pool5)
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
      sleep(0.1)
    self.singles -= 11
    self.multis += 1
    return scoutMulti

threeStar = [
  Pair(3, False, "General", "Brawly", "Makuhita", []),
  Pair(3, False, "General", "Winona", "Pelipper", []),
  Pair(3, False, "General", "Tate", "Solrock", []),
  Pair(3, False, "General", "Liza", "Lunatone", []),
  Pair(3, False, "General", "Maylene", "Meditite", []),
  Pair(3, False, "General", "Crasher Wake", "Floatzel", []),
  Pair(3, False, "General", "Brycen", "Cryogonal", []),
  Pair(3, False, "General", "Marlon", "Carracosta", []),
  Pair(3, False, "General", "Ramos", "Weepinbell", []),
  Pair(3, False, "General", "Wulfric", "Avalugg", []),
  Pair(3, True, "General", "Lt. Surge", "Voltorb", []),
  Pair(3, True, "General", "Bugsy", "Beedril", []),
  Pair(3, True, "General", "Janine", "Ariados", []),
  Pair(3, True, "General", "Roxanne", "Nosepass", []),
  Pair(3, True, "General", "Roark", "Cranidos", []),
  Pair(3, True, "General", "Candice", "Abomasnow", []),
  Pair(3, True, "General", "Cheryl", "Chansey", []),
  Pair(3, True, "General", "Marley", "Arcanine", []),
  Pair(3, True, "General", "Clan", "Palpitoad", []),
  Pair(3, True, "General", "Mina", "Granbull", [])
]

fourStar = [
  Pair(4, False, "General", "Blaine", "Rapidash", []),
  Pair(4, False, "General", "Lucy", "Seviper", []),
  Pair(4, False, "General", "Grant", "Amaura", []),
  Pair(4, True, "General", "Kahili", "Toucannon", []),
  Pair(4, True, "General", "Lorelei", "Lapras", []),
  Pair(4, True, "General", "Bruno", "Machomp", []),
  Pair(4, True, "General", "Agatha", "Gengar", []),
  Pair(4, True, "General", "Will", "Xatu", []),
  Pair(4, True, "General", "Drake", "Salamence", []),
  Pair(4, True, "General", "Thorton", "Bronzong", []),
  Pair(4, True, "General", "Shauntal", "Chandelure", []),
  Pair(4, True, "General", "Wikstrom", "Aegislash", []),
  Pair(4, True, "General", "Sophocles", "Togedemaru", []),
  Pair(4, True, "Fair-Exclusive", "Rachel", "Umbreon", []),
  Pair(4, True, "Fair-Exclusive", "Sawyer", "Honchkrow", []),
  Pair(4, True, "Fair-Exclusive", "Tina", "Flareon", []),
  Pair(4, False, "General", "Whitney", "Miltank", []),
  Pair(4, False, "General", "Gardenia", "Roserade", []),
  Pair(4, False, "General", "Roxie", "Scolipede", []),
  Pair(4, False, "General", "Siebold", "Clawitzer", []),
  Pair(4, False, "General", "Noland", "Pinsir", []),
  Pair(4, False, "General", "Marshal", "Conkeldurr", [])
]

fiveStarSpotlight = [
  Pair(5, True, "General", "Blue", "Pidgeot", []),
  Pair(5, True, "General", "Leaf", "Eevee", []),
  Pair(5, True, "General", "Sygna Suit Misty", "Vaporeon", ["SS Misty", "ss misty"]),
  Pair(5, True, "General", "Sygna Suit Erika", "Leafeon", ["SS Erika", "ss erika"]),
  Pair(5, True, "General", "Sabrina", "Alakazam", []),
  Pair(5, True, "General", "Ethan", "Cyndaquil", []),
  Pair(5, True, "General", "Lyra", "Chikorita", []),
  Pair(5, True, "General", "Kris", "Totodile", []),
  Pair(5, True, "General", "Falkneer", "Swellow", []),
  Pair(5, True, "General", "Morty", "Drifblim", []),
  Pair(5, True, "General", "Chuck", "Poliwrath", []),
  Pair(5, True, "General", "Jasmine", "Steelix", []),
  Pair(5, True, "General", "Karen", "Houndoom", []),
  Pair(5, True, "General", "Brendan", "Treecko", []),
  Pair(5, True, "General", "May", "Mudkip", []),
  Pair(5, True, "General", "Wally", "Gallade", []),
  Pair(5, True, "General", "Wallace", "Milotic", []),
  Pair(5, True, "General", "Sidney", "Absol", []),
  Pair(5, True, "General", "Phoebe", "Dusclops", []),
  Pair(5, True, "General", "Glacia", "Glalie", []),
  Pair(5, True, "General", "Lisia", "Altaria", []),
  Pair(5, True, "General", "Courtney", "Camerupt", []),
  Pair(5, True, "General", "Dawn", "Turtwig", []),
  Pair(5, True, "General", "Fantina", "Mismagius", []),
  Pair(5, True, "General", "Volkneer", "Luxray", []),
  Pair(5, True, "General", "Aaron", "Vespiquen", []),
  Pair(5, True, "General", "Bertha", "Hippowdon", []),
  Pair(5, True, "General", "Lucian", "Girafarig", []),
  Pair(5, True, "General", "Darach", "Staraptor", []),
  Pair(5, True, "General", "Hilbert", "Oshawott", []),
  Pair(5, True, "General", "Hilda", "Tepig", []),
  Pair(5, True, "General", "Bianca", "Musharna", []),
  Pair(5, True, "General", "Nate", "Braviary", []),
  Pair(5, True, "General", "Hugh", "Buffalant", []),
  Pair(5, True, "General", "Lenora", "Watchog", []),
  Pair(5, True, "General", "Burgh", "Leavanny", []),
  Pair(5, True, "General", "Elesa", "Zebstrika", []),
  Pair(5, True, "General", "Sygna Suit Elesa", "Rotom", ["SS Elesa","ss elesa"]),
  Pair(5, True, "General", "Caitlin", "Reuniclus", []),
  Pair(5, True, "General", "Grimsley", "Liepard", []),
  Pair(5, True, "General", "Sygna Suit Grimsley", "Sharpedo", ["SS Grimsley","ss grimsley"]),
  Pair(5, True, "General", "Colress", "Klinklang", []),
  Pair(5, True, "General", "Serena", "Fennekin", []),
  Pair(5, True, "General", "Tierno", "Crawdaunt", []),
  Pair(5, True, "General", "Trevor", "Florges", []),
  Pair(5, True, "General", "Shauna", "Chesnaught", []),
  Pair(5, True, "General", "Clemont", "Heliolisk", []),
  Pair(5, True, "General", "Olympia", "Sigilyph", []),
  Pair(5, True, "General", "Malva", "Talonflame", []),
  Pair(5, True, "General", "Drasna", "Dragalge", []),
  Pair(5, True, "General", "Looker", "Croagunk", []),
  Pair(5, True, "General", "Elio", "Popplio", []),
  Pair(5, True, "General", "Selene", "Rowlet", []),
  Pair(5, True, "General", "Lillie", "Clefairy", []),
  Pair(5, True, "General", "Gladion", "Silvally", []),
  Pair(5, True, "General", "Ilima", "Gumshoos", []),
  Pair(5, True, "General", "Lana", "Araquanid", []),
  Pair(5, True, "General", "Kiawe", "Marowak-Alola", []),
  Pair(5, True, "General", "Mallow", "Tsareena", []),
  Pair(5, True, "General", "Hala", "Crabominable", []),
  Pair(5, True, "General", "Olivia", "Lycanroc-Midnight", []),
  Pair(5, True, "General", "Grimsley (Kimono)", "Bisharp", ["Grimsley Kimono","Grimsley Alt", "AltGrimsley", "KimonoGrimsley", "kimonoGrimsley", "AGrimsley"]),
  Pair(5, True, "General", "Ryuki", "Turtnator", []),
  Pair(5, True, "General", "Lusamine", "Pheromosa", []),
  Pair(5, True, "General", "Plumeria", "Salazzle", []),
  Pair(5, True, "General", "Guzma", "Golisopod", []),
  Pair(5, True, "General", "Kukui", "Lycanroc-Midday", []),
  Pair(5, True, "General", "The Masked Royal", "Incineroar", ["AltKukui", "AKukui", "MaskedRoyal", "MaskKukui", "Masked Royal"]),
  Pair(5, True, "General", "Nessa", "Drednaw", []),
  Pair(5, True, "General", "Bea", "Sirfetch'd", []),
  Pair(5, True, "General", "Allister", "Gengar", []),
  Pair(5, True, "General", "Gordie", "Coalossal", []),
  Pair(5, True, "General", "Melony", "Lapras", []),
  Pair(5, True, "General", "Piers", "Obstagoon", []),
  Pair(5, True, "General", "Sonia", "Yamper", [])
]

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
  "C. Iris": Pair(5, True, "Fair-Exclusive", "Iris (Alt.)", "Hydreigon", ["C.Iris", "AltIris", "Alt Iris", "A.Iris","Iris alt", "Iris Alt", "Champion Iris", "Iris (Champion)"]),
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
  "Stakataka": Pair(5, True, "Fair-Exclusive", "Elio (Alt.)", "Stakataka", ["Alt Elio", "alt elio", "A.Elio"]),
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
  "SS Leaf": Pair(5, True, "Fair-Exclusive", "Sygna Suit Leaf", "Venusaur", ["SS Leaf", "ss leaf"])
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
  "SS Lear": Pair(5, True, "Master Fair", "Sygna Suit Lear", "Gholdengo", ["SS Lear", "ss lear"])
}

fiveStarMasterFair = list(fiveStarMasterFairDict.values())

fiveStarArcSuitFairDict = {
  "ASL": Pair(5, True, "Arc Suit Fair", "Arc Suit Lance", "Dragonite", ["AS Lance", "as lance", "ASL"]),
  "ASC": Pair(5, True, "Arc Suit Fair", "Arc Suit Cynthia", "Garchomp", ["AS Cynthia", "as cynthia", "ASC"]),
  "ASS": Pair(5, True, "Arc Suit Fair", "Arc Suit Steven", "Metagross", ["AS Steven", "as steven", "ASS"]),
  "ASLe": Pair(5, True, "Arc Suit Fair", "Arc Suit Leon", "Charizard", ["AS Leon", "as leon", "ASLe"]),
  "ASN": Pair(5, True, "Arc Suit Fair", "Arc Suit N", "Zoroark", ["AS N", "as n", "ASN"]),
  "ASA": Pair(5, True, "Arc Suit Fair", "Arc Suit Alder", "Volcarona", ["AS Alder", "as alder", "ASA"])
}

fiveStarArcSuitFair = list(fiveStarArcSuitFairDict.values())

mixExclusiveDict = {
  "mix Red": Pair(5, True, "Mix", "Red", "Venosaur", ["Mix Red", "mix red"], True),
  "mix Blue": Pair(5, True, "Mix", "Blue", "Charizard", ["Mix Blue", "mix blue"], True),
  "mix Leaf": Pair(5, True, "Mix", "Leaf", "Blastoise", ["Mix Leaf", "mix leaf"], True),
  "mix Lucas": Pair(5, True, "Mix", "Lucas", "Torterra", ["Mix Lucas", "mix lucas"], True),
  "mix Dawn": Pair(5, True, "Mix", "Dawn", "Empoleom", ["Mix Dawn", "mix dawn"], True)
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
  "h!Syncamore": Pair(5, True, "Seasonal", "Syncamore (Holiday 2023)", "Gogoat", ["Holi Syncamore", "holi syncamore"]),
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
  "SC Sonia": Pair(5, True, "Costume", "Sonia (Special Costume)", "Tsareena", ["SC Sonia", "sc sonia"])
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
  "V.Falkneer": Pair(5, True, "Variety", "Falkneer", "Noctowl", ["V.Falkneer", "v.falkneer"], True),
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
  "V.Ball Guy": Pair(5, True, "Variety", "Ball Guy", "Amoonguss", ["V.Ball Guy", "v.ball guy"], True),
  "V.Rachel": Pair(5, True, "Variety", "Rachel", "Gimmighoul-Roaming", ["V.Rachel", "v.rachel"], True),
  "V.Sawyer": Pair(5, True, "Variety", "Sawyer", "Gimmighoul-Chest", ["V.Sawyer", "v.sawyer"], True),
  "V.Grimsley": Pair(5, True, "Variety", "Grimsley", "Absol", ["V.Grimsley", "v.grimsley"], True)
}

gymDict = {
  "Gym Brock": Pair(5, True, "Gym", "Brock", "Kabutops", ["Gym Brock", "gym brock"], True),
  "Gym Winona": Pair(5, True, "Gym", "Winona", "Altaria", ["Gym Winona", "gym winona"], True),
  "Gym Grusha": Pair(5, True, "Gym", "Grusha", "Beartic", ["Gym Grusha", "gym grusha"], True),
  "Gym Whitney": Pair(5, True, "Gym", "Whitney", "Wigglytuff", ["Gym Whitney", "gym whitney"], True),
  "Gym Korrina": Pair(5, True, "Gym", "Korrina", "Hawlucha", ["Gym Korrina", "gym korrina"], True),
  "Gym Kabu": Pair(5, True, "Gym", "Kabu", "Ninetales", ["Gym Kabu", "gym kabu"], True)
}

gymList = list(gymDict.values())

variety = list(varietyDict.values())

seasonalFull = seasonalHoliday + seasonalNewYear + seasonalSpring + seasonalPalentines + seasonalSummer + seasonalFall

mixFull = mixExclusive + fiveStarPokeFair + seasonalFull + specialCostume + variety

# -----------

action = ""

def searchForPair(text, banner):
  if not nonick:
    if text in [pair.name for pair in banner.pairs]:
      return pair
  for i in range(len(banner.pairs)):
    if text in banner.pairs[i].nick:
      return banner.pairs[i]
  if text in list(banner.pairs.keys()):
    return banner.pairs[text]
  return None

def bannerSelect(banner: Banner):
  print("----------------------------------------")
  print(f"Scouting on {banner.name}...")
  print()
  print(f"Gems spent: {banner.singles*300} (Singles) + {banner.multis*3000} (Multis) = {banner.singles*300 + banner.multis*3000}")
  print()
  print("Featured Pair(s):")
  print(banner.__str__())
  print()
  if banner.checkPity():
    print(blue, "(ENTER) Choose a sync pair", reset())
  else:
    print("(x) Single")
    print("(3) Single x3")
    print("(5) Single x5")
  
  if not banner.type in ["mix", "ticket", "ticketM"]:
    print("(a) Multi")
    print("(z) Straight to Pity", "(Multi x12 + Single x2)" if not banner.type == "arcSuitFair" else "(Multi x15 + Single x2)")
  print("(b) Back")
  if banner.checkPity():
    print("\n".join([pair.__str__() for pair in self.pairs]))
    print()
    pairChosen = input("Sync pair to pity: >")
    pairChosen = searchForPair(pairChosen, banner) 
    if pairChosen == None:
      print("Invalid input.")
    else:
      print(rainbow(pairChosen.literal()))
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
  "SS Bede": Banner("Sygna Suit Bede Poke Fair Scout", [fiveStarPokeFairDict["SS Bede"]], "pokeFair"),
  "ASA": Banner("Arc Suit Alder Arc Suit Fair Scout", [fiveStarArcSuitFairDict["ASA"]], "arcSuitFair"),
  "Benga": Banner("Benga Poke Fair Scout", [fiveStarPokeFairDict["Benga"]], "pokeFair"),
  "SS Iono": Banner("Sygna Suit Iono Poke Fair Scout", [fiveStarPokeFairDict["SS Iono"]], "pokeFair"),
  "SSA Elesa": Banner("Sygna Suit (Alt.) Elesa Poke Fair Scout", [fiveStarPokeFairDict["SSA Elesa"]], "pokeFair"),
  "NC Rosa": Banner("Rosa (Champion) Master Fair Scout", [fiveStarMasterFairDict["NC Rosa"]], "masterFair"),
  "may_3xPF": Banner("Triple Feature Poke Fair Scout", [fiveStarPokeFairDict["Red"], fiveStarPokeFairDict["Gloria"], fiveStarPokeFairDict["Marnie"]], "3xPF"),
  "may_2xSC": Banner("Double Feature Costume Scout", [specialCostumeDict["SC Adaman"], specialCostumeDict["SC Irida"]], "2xSC"),
  "SS Gladion": Banner("Sygna Suit Gladion Master Fair Scout", [fiveStarMasterFairDict["SS Gladion"]], "masterFair"),
  "V.Grimsley": Banner("Grimsley Variety Scout", [varietyDict["V.Grimsley"]], "variety"),
  "vol33": Banner("Vol. 33 Monthly Poke Fair Scout (Larry)", [fiveStarPokeFairDict["Larry"]], "pokeFair"),
  "SC Rei": Banner("Rei Costume Scout",[specialCostumeDict["SC Rei"]], "costume"),
  "Lacey": Banner("Lacey Poke Fair Scout", [fiveStarPokeFairDict["Lacey"]], "pokeFair"),
  "Ilima": Banner("Ilima Spotlight Scout", [Pair(5, True, "General", "Ilima", "Gumshoos", [])], "spotlight"), # dictionary added later
  "apr_2xPF": Banner("Double Feature Poke Fair Scout", [fiveStarPokeFairDict["Rei"], fiveStarPokeFairDict["Akari"]], "2xPF"),
  "SC Marnie": Banner("Marnie Costume Scout",[specialCostumeDict['SC Marnie']], "costume"),
  "SC Morty": Banner("Morty Costume Scout",[specialCostumeDict["SC Morty"]], "costume"),
  "vol32": Banner("Vol. 32 Monthly Poke Fair Scout (Volo)", [fiveStarPokeFairDict["Volo"]],"pokeFair"),
  "mar_3xMF": Banner("Triple Feature Master Fair Scout", [fiveStarMasterFairDict["Maxie"], fiveStarMasterFairDict["Archie"], fiveStarMasterFairDict["Leon"]], "3xMF"),
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
  "palRerun": Banner("Super Spotlight Seasonal Scout (Palentines')", seasonalPalentines, "seasonalRerun"),
  "feb_3xPF": Banner("Triple Feature Poke Fair Scout", [fiveStarPokeFairDict["SS Korrina"], fiveStarPokeFairDict["Eusine"], fiveStarPokeFairDict["Ingo"]], "3xPF"),
  "feb_superScout": Banner("One-Time-Only Fair-Exclusive Guaranteed Scout", [fiveStarPokeFairDict["C.Elesa"], fiveStarPokeFairDict["SS Giovanni"], fiveStarPokeFairDict["Bede"], fiveStarPokeFairDict["Akari"], fiveStarPokeFairDict["Larry"]], "superScout"),
  "feb_superSpotlight": Banner("Super Spotlight Poke Fair Scout", [fiveStarPokeFairDict["SS Diantha"], fiveStarPokeFairDict["SS Lysandre"], fiveStarPokeFairDict["Anabel"], fiveStarPokeFairDict["Emma"]], "superScout"),
  "Juliana": Banner("Juliana Master Fair Scout", [fiveStarMasterFairDict["Juliana"]], "masterFair"),
  "Florian": Banner("Florian Master Fair Scout", [fiveStarMasterFairDict["Florian"]], "masterFair"),
  "vol30": Banner("Vol. 30 Monthly Poke Fair Scout (Klara)", [fiveStarPokeFairDict["Klara"]], "pokeFair"),
  "SSA Giovanni": Banner("Sygna Suit (Alt.) Giovanni Master Fair Scout", [fiveStarMasterFairDict["SSA Giovanni"]], "masterFair"),
  "NY Raihan": Banner("Raihan (New Year's 2025) Seasonal Scout", [seasonalNewYearDict["NY Raihan"]], "seasonal"),
  "NY Poppy": Banner("Poppy (New Year's 2025) Seasonal Scout", [seasonalNewYearDict["NY Poppy"]], "seasonal"),
  "NYRerun": Banner("Super Spotlight Seasonal Scout (New Year's)", seasonalNewYear, "seasonalRerun"),
  "rocketVariety": Banner("Team Rocket Variety Scout", [varietyDict["V.Archer"], varietyDict["V.Ariana"], varietyDict["V.Petrel"], varietyDict["V.Proton"], varietyDict["V.Giovanni"]], "variety"),
  "jan_3xPF": Banner("Triple Feature Poke Fair Scout", [fiveStarPokeFairDict["Grusha"], fiveStarPokeFairDict["Paulo"], fiveStarPokeFairDict["SS Blue"]], "3xPF"),
  "Mela": Banner("Mela Poke Fair Scout", [fiveStarPokeFairDict["Mela"]], "pokeFair"),
  "Atticus": Banner("Atticus Poke Fair Scout", [fiveStarPokeFairDict["Atticus"]], "pokeFair"),
  "jan_2xPF": Banner("Double Feature Poke Fair Scout", [fiveStarPokeFairDict["SS Piers"], fiveStarPokeFairDict["SS Roxie"]], "2xPF"),
  "anni N": Banner("N (Anniversary 2021) Master Fair Scout", [fiveStarMasterFairDict["anni N"]], "masterFair"),
  "vol29": Banner("Vol. 29 Monthly Poke Fair Scout (Iono)", [fiveStarPokeFairDict["Iono"]], "pokeFair")
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
  "e": Banner("Dawn Mix Scout", [mixExclusiveDict["mix Dawn"]], "mix")
}

def gymScout():
  print("----------------------------------------")
  print("Choose the gym scout you want to scout on:")
  print("--- MAY 2025 ---")
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
  print("--- MAY 2025 ---")
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
  print()
  print("--- MISC ---")
  print(f"(#) {cyan}Gym Scout(s){reset()}")
  print(f"(!) {red}Mix Scout(s){reset()}")
  print(f"(@) {cyan}Daily Scout{reset()}")
  print(f"($) {brown}5* Guaranteed Ticket Scout{reset()}")
  print()
  print("Due to technical limitations, a banner will have a pool as if it was reran at the present time. It is not possible to simulate the pool of the banner at the time of its release (yet).")
  return dummyDict

def startSim():
  print("----------------------------------------")
  print("Choose the banner you want to scout on:")
  print("--- MAY 2025 ---")
  dummyDict = loopBanners(banners, {"SC Rei": "Apr 2025", "mar_3xMF": "Mar 2025 (5.5th Anni)", "pal Marley": "Feb 2025 (Pre-anni 5.5th) (Palentines' 2025)", "SSA Giovanni": "Jan 2025 (New Years' 2025)"}, "2025")
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
      case _:
        print("Invalid input. Please try again.")
    

def menu():
  print(rainbow("Pokemon Masters EX - Pull Simulator Reborn"))
  print("Version: v1.0.0")
  print()
  print()
  print(bold + "(a) Start Simulation", reset())
  print()
  print("(s) Settings")
  print("(x) Sync Pair Addition Progress")
  print("(l) Update Log")
  print("(q) Quit")
  action = input("> ")
  match action:
    case "a":
      startSim()
    case "s":
      print("----------------------------------------")
      print("This is a work in progress. Please come back later.")
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
      print("5* Arc Suit Fair: 6/6 [COMPLETED]")
      print("Gym Scout: 6/6 [COMPLETED]")
    case "l":
      print("----------------------------------------")
      print("[WILL ADD IN v2.1.0]")
      print("v1.0.0")
      print("- Initial release")
    case _:
      print("----------------------------------------")
      print("Invalid input. Please try again.") 
  print()
  awaitEnter()
  clear()

while action != "q":
  menu()