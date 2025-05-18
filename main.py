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
    case "seasonal":
      return green
    case "seasonalRerun":
      return green
    case "gym":
      return cyan
    case "daily":
      return cyan
    case _:
      return
    
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
    self.scoutPoint = 0
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
    elif self.type == "seasonal":
      self.rates = [2, 7, 27]
    elif self.type == "seasonalRerun":
      self.rates = [2, 7, 27]
    elif self.type == "ticket":
      self.rates = [25, 34, 54]
    elif self.type == "ticketM":
      self.rates = [100, 0, 0]
    else:
      raise ValueError("Invalid banner type")
    if fiveStarOnly:
      self.rates = [0, 100, 100]

    if mixPool:
      self.pool5 = mixFull
    elif genPool:
      self.pool5 = fiveStarSpotlight
    if dailyPool:
      self.featuredPairs = fiveStarMasterFair + fiveStarArcSuitFair + seasonalFull + fiveStarPokeFair # SC added later
  def __str__(self):
    return "\n".join([pair.__str__() for pair in self.featuredPairs])
  
  def single(self):
    factor = uniform(1, 100)
    if factor <= self.rates[0]:
      scouted = choice(self.featuredPairs)
    elif factor <= self.rates[1]:
      scouted = choice(sortByObtain(fiveStarSpotlight, "General"))
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
      sleep(1)
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

fiveStarPokeFair = [
  Pair(5, True, "Fair-Exclusive", "Red", "Snorlax", []),
  Pair(5, True, "Fair-Exclusive", "Chase", "Pikachu", []),
  Pair(5, True, "Fair-Exclusive", "Elaine", "Eevee", []),
  Pair(5, True, "Fair-Exclusive", "Lance", "Dragonite", []),
  Pair(5, True, "Fair-Exclusive", "Blue (Classic)", "Aerodactyl", ["ClassicBlue", "Classic Blue", "CBlue"]),
  Pair(5, True, "Fair-Exclusive", "Sygna Suit Silver", "Sneasel", ["SS Silver", "ss silver"]),
  Pair(5, True, "Fair-Exclusive", "Sygna Suit Morty", "Ho-Oh", ["SS Morty", "ss morty"]),
  Pair(5, True, "Fair-Exclusive", "Eusine", "Suicune", []),
  Pair(5, True, "Fair-Exclusive", "Sygna Suit Giovanni", "Nidoking", ["SS Giovanni", "ss giovanni"]),
  Pair(5, True, "Fair-Exclusive", "Sygna Suit Brendan", "Latios", ["SS Brendan", "ss brendan"]),
  Pair(5, True, "Fair-Exclusive", "May (Anniversary 2022)", "Latias", ["anni may", "Anni May", "anniMay","AnniMay", "anni May"]),
  Pair(5, True, "Fair-Exclusive", "Sygna Suit May", "Blaziken", ["SS May", "ss may"]),
  Pair(5, True, "Fair-Exclusive", "Sygna Suit Wally", "Gardevoir", ["SS Wally", "ss wally"]),
  Pair(5, True, "Fair-Exclusive", "Steven", "Metagross", []),
  Pair(5, True, "Fair-Exclusive", "Sygna Suit Steven", "Deoxys", ["SS Steven", "ss steven", "SSS"]),
  Pair(5, True, "Fair-Exclusive", "Greta", "Breloom", []),
  Pair(5, True, "Fair-Exclusive", "Lucas", "Dialga", []),
  Pair(5, True, "Fair-Exclusive", "Sygna Suit Dawn", "Cresselia", ["SS Dawn", "ss dawn"]),
  Pair(5, True, "Fair-Exclusive", "Cynthia", "Garchomp", []),
  Pair(5, True, "Fair-Exclusive", "Sygna Suit Cynthia", "Kommo-o", ["SS Cynthia", "ss cynthia"]),
  Pair(5, True, "Fair-Exclusive", "Dahlia", "Ludicolo", []),
  Pair(5, True, "Fair-Exclusive", "Palmer", "Regigigas", []),
  Pair(5, True, "Fair-Exclusive", "Argenta", "Skarmory", []),
  Pair(5, True, "Fair-Exclusive", "Sygna Suit Cyrus", "Darkrai", ["SS Cyrus", "ss cyrus"]),
  Pair(5, True, "Fair-Exclusive", "Rei", "Decidueye-Hisui", []),
  Pair(5, True, "Fair-Exclusive", "Akari", "Samurott-Hisui", []),
  Pair(5, True, "Fair-Exclusive", "Volo", "Togepi", []),
  Pair(5, True, "Fair-Exclusive", "Sygna Suit Hilbert", "Genesect", ["SS Hilbert", "ss hilbert"]),
  Pair(5, True, "Fair-Exclusive", "Sygna Suit Hilda", "Victini", ["SS Hilda", "ss hilda"]),
  Pair(5, True, "Fair-Exclusive", "Elesa (Classic)", "Emolga", ["CElesa", "ClassicElesa", "Classic Elesa", "classicElesa", "AltElesa"]),
  Pair(5, True, "Fair-Exclusive", "Sygna Suit (Alt.) Elesa", "Thundurus-Therian", ["SSA Elesa", "ssa elesa"]),
  Pair(5, True, "Fair-Exclusive", "Skyla (Anniversary 2022)", "Tornadus-Therian", ["anni skyla", "Anni Skyla", "anni Skyla", "anniSkyla", "AnniSkyla"]),
  Pair(5, True, "Fair-Exclusive", "Iris (Alt.)", "Hydreigon", ["C.Iris", "AltIris", "Alt Iris", "A.Iris","Iris alt", "Iris Alt", "Champion Iris", "Iris (Champion)"]),
  Pair(5, True, "Fair-Exclusive", "Sygna Suit Roxie", "Toxtricity", ["SS Roxie", "ss roxie"]),
  Pair(5, True, "Fair-Exclusive", "Alder", "Volcarona", []),
  Pair(5, True, "Fair-Exclusive", "Ingo", "Excadrill", ["submas 1", "submas white"]),
  Pair(5, True, "Fair-Exclusive", "Sygna Suit Ingo", "Chandelure", ["SS Ingo", "ss ingo"]),
  Pair(5, True, "Fair-Exclusive", "Emmet", "Archeops", ["submas 2", "submas black"]),
  Pair(5, True, "Fair-Exclusive", "Sygna Suit Emmet", "Eelektross", ["SS Emmet", "ss emmet"]),
  Pair(5, True, "Fair-Exclusive", "Benga", "Volcarona", []),
  Pair(5, True, "Fair-Exclusive", "N", "Zekrom", []),
  Pair(5, True, "Fair-Exclusive", "Sygna Suit N", "Kyurem-Black", ["SS N", "ss n"]),
  Pair(5, True, "Fair-Exclusive", "Sina", "Glaceon", []),
  Pair(5, True, "Fair-Exclusive", "Dexio", "Espeon", []),
  Pair(5, True, "Fair-Exclusive", "Sygna Suit Korrina", "Marshadow", ["SS Korrina", "ss korrina"]),
  Pair(5, True, "Fair-Exclusive", "Diantha", "Gardevoir", []),
  Pair(5, True, "Fair-Exclusive", "Sygna Suit Diantha", "Diancie", ["SS Diantha", "ss diantha"]),
  Pair(5, True, "Fair-Exclusive", "Emma", "Crobat", []),
  Pair(5, True, "Fair-Exclusive", "Lysandre", "Yveltal", []),
  Pair(5, True, "Fair-Exclusive", "Sygna Suit Lysandre", "Volcanion", ["SS Lysandre", "ss lysandre"]),
  Pair(5, True, "Fair-Exclusive", "Elio (Alt.)", "Stakataka", ["Alt Elio", "alt elio", "A.Elio"]),
  Pair(5, True, "Fair-Exclusive", "Selene (Alt.)", "Nihilego", ["Alt Selene", "alt selene", "A.Selene"]),
  Pair(5, True, "Fair-Exclusive", "Sygna Suit Hau", "Tapu Koko", ["SS Hau", "ss hau"]),
  Pair(5, True, "Fair-Exclusive", "Sygna Suit Lana", "Tapu Lele", ["SS Lana", "ss lana"]),
  Pair(5, True, "Fair-Exclusive", "Sygna Suit Mina", "Tapu Bulu", ["SS Mina", "ss mina"]),
  Pair(5, True, "Fair-Exclusive", "Sygna Suit Acerola", "Tapu Fini", ["SS Acerola", "ss acerola"]),
  Pair(5, True, "Fair-Exclusive", "Anabel", "Snorlax", []),
  Pair(5, True, "Fair-Exclusive", "Victor", "Greninja-Ash", []),
  Pair(5, True, "Fair-Exclusive", "Gloria", "Zacian-Crowned", []),
  Pair(5, True, "Fair-Exclusive", "Gloria (Dojo Uniform)", "Urshifu", ["A.Gloria", "D.Gloria", "Dojo Gloria", "DojoGloria", "dojoGloria","DU Gloria", "Alt Gloria", "AltGloria","A1 Gloria"]),
  Pair(5, True, "Fair-Exclusive", "Gloria (Alt. 2)", "Cinderace", ["A.2. Gloria", "Alt 2 Gloria", "Alt2 Gloria","alt 2 gloria", "alt2 gloria", "A2 Gloria"]),
  Pair(5, True, "Fair-Exclusive", "Marnie", "Morpeko", []),
  Pair(5, True, "Fair-Exclusive", "Bede", "Hatterene", []),
  Pair(5, True, "Fair-Exclusive", "Sygna Suit Bede", "Iron Valiant", ["SS Bede", "ss bede"]),
  Pair(5, True, "Fair-Exclusive", "Milo", "Eldegoss", []),
  Pair(5, True, "Fair-Exclusive", "Kabu", "Centiskorch", []),
  Pair(5, True, "Fair-Exclusive", "Sygna Suit Piers", "Toxtricity-Low-Key", ["SS Piers", "ss piers"]),
  Pair(5, True, "Fair-Exclusive", "Raihan", "Duraludon", []),
  Pair(5, True, "Fair-Exclusive", "Raihan (Anniversary 2022)", "Flygon", ["anni raihan", "Anni Raihan", "anniRaihan", "AnniRaihan", "anni Raihan"]),
  Pair(5, True, "Fair-Exclusive", "Klara", "Slowbro-Galar", []),
  Pair(5, True, "Fair-Exclusive", "Avery", "Slowking-Galar", []),
  Pair(5, True, "Fair-Exclusive", "Sygna Suit Leon", "Eternatus", ["SS Leon", "ss leon"]),
  Pair(5, True, "Fair-Exclusive", "Leon (Alt.)", "Dragapult", ["Alt Leon", "alt leon", "leon alt", "Leon Alt", "A. Leon"]),
  Pair(5, True, "Fair-Exclusive", "Rose", "Copperajah", []),
  Pair(5, True, "Fair-Exclusive", "Oleana", "Garbodor", []),
  Pair(5, True, "Fair-Exclusive", "Nemona", "Pawmot", []),
  Pair(5, True, "Fair-Exclusive", "Penny", "Sylveon", []),
  Pair(5, True, "Fair-Exclusive", "Arven", "Mabosstiff", []),
  Pair(5, True, "Fair-Exclusive", "Iono", "Bellibolt", []),
  Pair(5, True, "Fair-Exclusive", "Sygna Suit Iono", "Raging Bolt", ["SS Iono", "ss iono"]),
  Pair(5, True, "Fair-Exclusive", "Grusha", "Cetitan", []),
  Pair(5, True, "Fair-Exclusive", "Larry", "Dudunsparce", []),
  Pair(5, True, "Fair-Exclusive", "Rika", "Clodsire", []),
  Pair(5, True, "Fair-Exclusive", "Poppy", "Tinkaton", []),
  Pair(5, True, "Fair-Exclusive", "Clavell", "Quaquaval", []),
  Pair(5, True, "Fair-Exclusive", "Jacq", "Farigiraf", []),
  Pair(5, True, "Fair-Exclusive", "Giacomo", "Kingambit", []),
  Pair(5, True, "Fair-Exclusive", "Eri", "Annihilape", []),
  Pair(5, True, "Fair-Exclusive", "Mela", "Armarouge", []),
  Pair(5, True, "Fair-Exclusive", "Atticus", "Revavroom", []),
  Pair(5, True, "Fair-Exclusive", "Ortega", "Dachsbun", []),
  Pair(5, True, "Fair-Exclusive", "Lacey", "Granbull", []),
  Pair(5, True, "Fair-Exclusive", "Lear", "Hoopa", []),
  Pair(5, True, "Fair-Exclusive", "Paulo", "Lycanroc-Dusk", []),
  Pair(5, True, "Fair-Exclusive", "Sygna Suit Red", "Charizard", ["SS Red", "ss red"]),
  Pair(5, True, "Fair-Exclusive", "Sygna Suit Blue", "Blastoise", ["SS Blue", "ss blue"]),
  Pair(5, True, "Fair-Exclusive", "Sygna Suit Leaf", "Venusaur", ["SS Leaf", "ss leaf"])
]

fiveStarMasterFair = [
  Pair(5, True, "Master Fair", "Sygna Suit (Thunderbolt) Red", "Pikachu", ["SST Red", "sst red"]),
  Pair(5, True, "Master Fair", "Red (Champion)", "Articuno", ["NC Red", "nc red"]),
  Pair(5, True, "Master Fair", "Leaf (Champion)", "Moltres", ["NC Leaf", "nc leaf"]),
  Pair(5, True, "Master Fair", "Blue (Champion)", "Zapdos", ["NC Blue", "nc blue"]),
  Pair(5, True, "Master Fair", "Sygna Suit Ethan", "Lugia", ["SS Ethan", "ss ethan"]),
  Pair(5, True, "Master Fair", "Sygna Suit Lyra", "Celebi", ["SS Lyra", "ss lyra"]),
  Pair(5, True, "Master Fair", "Sygna Suit Kris", "Suicune", ["SS Kris", "ss kris"]),
  Pair(5, True, "Master Fair", "Silver (Champion)", "Tyranitar", ["NC Silver", "nc silver"]),
  Pair(5, True, "Master Fair", "Sygna Suit (Alt.) Giovanni", "Guzzlord", ["SSA Giovanni", "ssa giovanni"]),
  Pair(5, True, "Master Fair", "Brendan (Champion)", "Groudon", ["NC Brendan", "nc brendan"]),
  Pair(5, True, "Master Fair", "May (Champion)", "Kyogre", ["NC May", "nc may"]),
  Pair(5, True, "Master Fair", "Steven (Anniversary 2021)", "Rayquaza", ["Anni Steven", "anni steven", "anniSteven", "AnniSteven"]),
  Pair(5, True, "Master Fair", "Maxie", "Groudon", []),
  Pair(5, True, "Master Fair", "Archie", "Kyogre", []),
  Pair(5, True, "Master Fair", "Sygna Suit (Renegade) Cynthia", "Giratina", ["SSR Cynthia", "ssr cynthia"]),
  Pair(5, True, "Master Fair", "Sygna Suit (Aura) Cynthia", "Lucario", ["SSA Cynthia", "ssa cynthia"]),
  Pair(5, True, "Master Fair", "Adaman", "Leafeon", []),
  Pair(5, True, "Master Fair", "Irida", "Glaceon", []),
  Pair(5, True, "Master Fair", "Cheren (Champion)", "Tornadus", ["NC Cheren", "nc cheren"]),
  Pair(5, True, "Master Fair", "Bianca (Champion)", "Virizion", ["NC Bianca", "nc bianca"]),
  Pair(5, True, "Master Fair", "Nate (Champion)", "Haxorus", ["NC Nate", "nc nate"]),
  Pair(5, True, "Master Fair", "Rosa (Champion)", "Meloetta", ["NC Rosa", "nc rosa"]),
  Pair(5, True, "Master Fair", "N (Anniversary 2021)", "Reshiram", ["Anni N", "anni n", "AnniN", "anniN", "N anni"]),
  Pair(5, True, "Master Fair", "Calem (Champion)", "Greninja", ["NC Calem", "nc calem"]),
  Pair(5, True, "Master Fair", "Sygna Suit Serena", "Zygarde", ["SS Serena", "ss serena", "Zerena", "zerena"]),
  Pair(5, True, "Master Fair", "Serena (Champion)", "Greninja", ["NC Serena", "nc serena"]),
  Pair(5, True, "Master Fair", "Lillie (Anniversary 2021)", "Lunala", ["Anni Lillie", "anni lillie", "anniLillie", "AnniLillie", "Lillie anni"]),
  Pair(5, True, "Master Fair", "Sygna Suit Lusamine", "Necrozma-Dusk-Mane", ["SS Lusamine", "ss lusamine"]),
  Pair(5, True, "Master Fair", "Sygna Suit Gladion", "Magearna", ["SS Gladion", "ss gladion"]),
  Pair(5, True, "Master Fair", "Hop (Champion)", "Zapdos-Galar", ["NC Hop", "nc hop"]),
  Pair(5, True, "Master Fair", "Marnie (Champion)", "Moltres-Galar", ["NC Marnie", "nc marnie"]),
  Pair(5, True, "Master Fair", "Bede (Champion)", "Articuno-Galar", ["NC Bede", "nc bede"]),
  Pair(5, True, "Master Fair", "Leon", "Charizard", []),
  Pair(5, True, "Master Fair", "Sygna Suit Nemona", "Scream Tail", ["SS Nemona", "ss nemona"]),
  Pair(5, True, "Master Fair", "Juliana", "Koraidon", []),
  Pair(5, True, "Master Fair", "Florian", "Miraidon", []),
  Pair(5, True, "Master Fair", "Geeta", "Glimmora", []),
  Pair(5, True, "Master Fair", "Ash", "Pikachu", []),
  Pair(5, True, "Master Fair", "Sygna Suit Lear", "Gholdengo", ["SS Lear", "ss lear"])
]

fiveStarArcSuitFair = [
  Pair(5, True, "Arc Suit Fair", "Arc Suit Lance", "Dragonite", ["AS Lance", "as lance", "ASL"]),
  Pair(5, True, "Arc Suit Fair", "Arc Suit Cynthia", "Garchomp", ["AS Cynthia", "as cynthia", "ASC"]),
  Pair(5, True, "Arc Suit Fair", "Arc Suit Steven", "Metagross", ["AS Steven", "as steven", "ASS"]),
  Pair(5, True, "Arc Suit Fair", "Arc Suit Leon", "Charizard", ["AS Leon", "as leon", "ASLe"]),
  Pair(5, True, "Arc Suit Fair", "Arc Suit N", "Zoroark", ["AS N", "as n", "ASN"]),
  Pair(5, True, "Arc Suit Fair", "Arc Suit Alder", "Volcarona", ["AS Alder", "as alder", "ASA"])
]

mixExclusive = [
  Pair(5, True, "Mix", "Red", "Venosaur", ["Mix Red", "mix red"], True),
  Pair(5, True, "Mix", "Blue", "Charizard", ["Mix Blue", "mix blue"], True),
  Pair(5, True, "Mix", "Leaf", "Blastoise", ["Mix Leaf", "mix leaf"], True),
  Pair(5, True, "Mix", "Lucas", "Torterra", ["Mix Lucas", "mix lucas"], True),
  Pair(5, True, "Mix", "Dawn", "Empoleom", ["Mix Dawn", "mix dawn"], True)
]

seasonalHoliday = [
  Pair(5, True, "Seasonal", "Rosa (Holiday 2019)", "Greninja", ["Holi Rosa", "holi rosa"]),
  Pair(5, True, "Seasonal", "Siebold (Holiday 2019)", "Octillery", ["Holi Siebold", "holi siebold"]),
  Pair(5, True, "Seasonal", "Erika (Holiday 2020)", "Comfey", ["Holi Erika", "holi erika"]),
  Pair(5, True, "Seasonal", "Skyla (Holiday 2020)", "Togekiss", ["Holi Skyla", "holi skyla"]),
  Pair(5, True, "Seasonal", "Nessa (Holiday 2021)", "Eiscue", ["Holi Nessa", "holi nessa"]),
  Pair(5, True, "Seasonal", "Leon (Holiday 2021)", "Calyrex", ["Holi Leon", "holi leon"]),
  Pair(5, True, "Seasonal", "Whitney (Holiday 2022)", "Sawsbuck-Winter", ["Holi Whitney", "holi whitney"]),
  Pair(5, True, "Seasonal", "Jasmine (Holiday 2022)", "Ampharos", ["Holi Jasmine", "holi jasmine"]),
  Pair(5, True, "Seasonal", "Viola (Holiday 2023)", "Vivillon", ["Holi Viola", "holi viola"]),
  Pair(5, True, "Seasonal", "Syncamore (Holiday 2023)", "Gogoat", ["Holi Syncamore", "holi syncamore"]),
  Pair(5, True, "Seasonal", "Lillie (Holiday 2024)", "Primarina", ["Holi Lillie", "holi lillie"]),
  Pair(5, True, "Seasonal", "Bugsy (Holiday 2024)", "Kricketune", ["Holi Bugsy", "holi bugsy"])
]

seasonalNewYear = [
  Pair(5, True, "Seasonal", "Lance (New Year's 2021)", "Gyarados", ["NY Lance", "ny lance"]),
  Pair(5, True, "Seasonal", "Lillie (New Year's 2021)", "Ribombee", ["NY Lillie", "ny lillie"]),
  Pair(5, True, "Seasonal", "Sabrina (New Year's 2022)", "Chingling", ["NY Sabrina", "ny sabrina"]),
  Pair(5, True, "Seasonal", "Volkneer (New Year's 2022)", "Electivire", ["NY Volkneer", "ny volkneer"]),
  Pair(5, True, "Seasonal", "Lisia (New Year's 2023)", "Rapidash-Galar", ["NY Lisia", "ny lisia"]),
  Pair(5, True, "Seasonal", "Dawn (New Year's 2023)", "Oricorio-Sensu", ["NY Dawn", "ny dawn"]),
  Pair(5, True, "Seasonal", "Clair (New Year's 2024)", "Drampa", ["NY Clair", "ny clair"]),
  Pair(5, True, "Seasonal", "Wallace (New Year's 2024)", "Blacephalon", ["NY Wallace", "ny wallace"]),
  Pair(5, True, "Seasonal", "Raihan (New Year's 2025)", "Sandaconda", ["NY Raihan", "ny raihan"]),
  Pair(5, True, "Seasonal", "Poppy (New Year's 2025)", "Steelix", ["NY Poppy", "ny poppy"])
]

seasonalSpring = [
  Pair(5, True, "Seasonal", "May (Spring 2021)", "Lopunny", ["sp May", "sp may"]),
  Pair(5, True, "Seasonal", "Burgh (Spring 2021)", "Togepi", ["sp Burgh", "sp burgh"])
]

seasonalPalentines = [
  Pair(5, True, "Seasonal", "Dawn (Palentine's 2021)", "Alcremie", ["pal Dawn", "pal dawn"]),
  Pair(5, True, "Seasonal", "Serena (Palentine's 2021)", "Whimsicott", ["pal Serena", "pal serena"]),
  Pair(5, True, "Seasonal", "Marnie (Palentine's 2022)", "Mawile", ["pal Marnie", "pal marnie"]),
  Pair(5, True, "Seasonal", "Bea (Palentine's 2022)", "Vanilluxe", ["pal Bea", "pal bea"]),
  Pair(5, True, "Seasonal", "Elesa (Palentine's 2023)", "Togetic", ["Pal Elesa", "pal elesa"]),
  Pair(5, True, "Seasonal", "Mallow (Palentine's 2023)", "Appletun", ["pal Mallow", "pal mallow"]),
  Pair(5, True, "Seasonal", "Candice (Palentine's 2024)", "Darmanitan-Galar", ["pal Candice", "pal candice"]),
  Pair(5, True, "Seasonal", "Victor (Palentine's 2024)", "Greedent", ["pal Victor", "pal victor"]),
  Pair(5, True, "Seasonal", "Erika (Palentine's 2025)", "Lurantis", ["pal Erika", "pal erika"]),
  Pair(5, True, "Seasonal", "Marley (Palentine's 2025)", "Shaymin", ["pal Marley", "pal marley"])
]

seasonalSummer = [
  Pair(5, True, "Seasonal", "Lyra (Summer 2020)", "Jigglypuff", ["sum Lyra", "sum lyra"]),
  Pair(5, True, "Seasonal", "Steven (Summer 2020)", "Sandslash-Alola", ["sum Steven", "sum steven"]),
  Pair(5, True, "Seasonal", "Gloria (Summer 2021)", "Inteleon", ["sum Gloria", "sum gloria"]),
  Pair(5, True, "Seasonal", "Marnie (Summer 2021)", "Grimmsnarl", ["sum Marnie", "sum marnie"]),
  Pair(5, True, "Seasonal", "Hilda (Summer 2022)", "Grapploct", ["sum Hilda", "sum hilda"]),
  Pair(5, True, "Seasonal", "N (Summer 2022)", "Zoroark", ["sum N", "sum n"]),
  Pair(5, True, "Seasonal", "Tate (Summer 2023)", "Jirachi", ["sum Tate", "sum tate"]),
  Pair(5, True, "Seasonal", "Liza (Summer 2023)", "Celesteela", ["sum Liza", "sum liza"]),
  Pair(5, True, "Seasonal", "Gardenia (Summer 2024)", "Dhelmise", ["sum Gardenia", "sum gardenia"]),
  Pair(5, True, "Seasonal", "Acerola (Summer 2024)", "Jellicent", ["sum Acerola", "sum acerola"]),
]

seasonalFall = [
  Pair(5, True, "Seasonal", "Hilbert (Fall 2020)", "Mightyena", ["fa Hilbert", "fa hilbert"]),
  Pair(5, True, "Seasonal", "Acerola (Fall 2020)", "Mimikyu", ["fa Acerola", "fa acerola"]),
  Pair(5, True, "Seasonal", "Morty (Fall 2021)", "Banette", ["fa Morty", "fa morty"]),
  Pair(5, True, "Seasonal", "Caitlin (Fall 2021)", "Sableye", ["fa Caitlin", "fa caitlin"]),
  Pair(5, True, "Seasonal", "Iris (Fall 2022)", "Naganadel", ["fa Iris", "fa iris"]),
  Pair(5, True, "Seasonal", "Allister (Fall 2022)", "Gourgeist", ["fa Allister", "fa allister"]),
  Pair(5, True, "Seasonal", "Roxanne (Fall 2023)", "Runerigus", ["fa Roxanne", "fa roxanne"]),
  Pair(5, True, "Seasonal", "Phoebe (Fall 2023)", "Cofagrigus", ["fa Phoebe", "fa phoebe"]),
  Pair(5, True, "Seasonal", "Shauntal (Fall 2024)", "Froslass", ["fa Shauntal", "fa shauntal"]),
  Pair(5, True, "Seasonal", "Iono (Fall 2024)", "Flutter Mane", ["fa Iono", "fa iono"])
]

seasonalFull = seasonalHoliday + seasonalNewYear + seasonalSpring + seasonalPalentines + seasonalSummer + seasonalFall

mixFull = mixExclusive + fiveStarPokeFair + seasonalFull # special costume in v2.0.0

# -----------

action = ""

def bannerSelect(banner: Banner):
  print("----------------------------------------")
  print(f"Scouting on {banner.name}...")
  print()
  print(f"Gems spent: {banner.singles*300} (Singles) + {banner.multis*3000} (Multis) = {banner.singles*300 + banner.multis*3000}")
  print()
  print("Featured Pair(s):")
  print(banner.__str__())
  print()
  print("(y) Single")
  print("(a) Multi")
  print("(b) Back")
  match input('> '):
    case "y":
      scouted = banner.single()
      print(rainbow(scouted.literal()) if scouted in banner.featuredPairs else scouted.__str__())
    case "a":
      banner.multi()
    case "b":
      pass
  awaitEnter()
  if input("Do you want to scout again on this banner? (y/n) \n> ") == "y":
    bannerSelect(banner)
  else:
    pass

def startSim():
  print("----------------------------------------")
  print("Choose the banner you want to simulate:")
  print("--- MAY 2025 ---")
  print("(a) Sygna Suit Bede Poke Fair Scout - Ongoing")
  print("(b) Arc Suit Alder Arc Suit Fair Scout - Ongoing")
  print("(c) Benga Poke Fair Scout - Ongoing")
  print("(d) Sygna Suit Iono Poke Fair Scout")
  print("(e) Sygna Suit (Alt.) Elesa Poke Fair Scout")
  print("(f) Rosa (Champion) Master Fair Scout - Ongoing")
  print("(g) [UNDER CONSTRUCTION]")
  print("(h) [UNDER CONSTRUCTION]")
  print("(i) [UNDER CONSTRUCTION]")
  print("--- APR 2025 ---")
  print("(j) [UNDER CONSTRUCTION]")
  print("(k) Lacey Poke Fair Scout")
  print("(l) Ilima Spotlight Scout")
  print("(m) Double Feature Poke Fair Scout")
  print("(n) [UNDER CONSTRUCTION]")
  print("(o) [UNDER CONSTRUCTION]")
  print("(p) [UNDER CONSTRUCTION]")
  print("(q) [UNDER CONSTRUCTION]")
  print("--- MAR 2025 (5.5th anni) ---")
  print("(r) [UNDER CONSTRUCTION]")
  print("(s) Triple Feature Master Fair Scout")
  print("(t) May (Champion) Master Fair Scout")
  print("(u) Brendan (Champion) Master Fair Scout")
  print("(v) Steven (Anniversary 2021) Master Fair Scout")
  print("(w) [UNDER CONSTRUCTION]")
  print("(x) Arc Suit N Arc Suit Fair Scout")
  print("(y) [UNDER CONSTRUCTION]")
  print("(z) Ortega Poke Fair Scout")
  print("(aa) Team Star Assemble! Super Spotlight Poke Fair Scout")
  print("(ab) Nate (Champion) Master Fair Scout")
  print()
  print("BANNERS OLDER THAN 5.5th ANNIVERSARY ARE YET TO BE AVAILABLE")
  print()
  print("(#) [UNDER CONSTRUCTION]")
  print("(!) [UNDER CONSTRUCTION]")
  print(f"(@) {cyan}Daily Scout (NO SPECIAL COSTUME YET){reset()}")
  print(f"($) {brown}5* Guaranteed Ticket Scout{reset()}")
  match input("Which banner do you want to scout on? \n> "):
    case "a":
      bannerSelect(Banner("Sygna Suit Bede Poke Fair Scout", [Pair(5, True, "Fair-Exclusive", "Sygna Suit Bede", "Iron Valiant", ["SS Bede", "ss bede"])], "pokeFair"))
    case "b":
      bannerSelect(Banner("Arc Suit Alder Arc Suit Fair Scout", [Pair(5, True, "Arc Suit Fair", "Arc Suit Alder", "Volcarona", ["AS Alder", "as alder", "ASA"])], "arcSuitFair"))
    case "c":
      bannerSelect(Banner("Benga Poke Fair Scout", [Pair(5, True, "Fair-Exclusive", "Benga", "Volcarona", [])], "pokeFair"))
    case "d":
      bannerSelect(Banner("Sygna Suit Iono Poke Fair Scout", [Pair(5, True, "Fair-Exclusive", "Sygna Suit Iono", "Raging Bolt", ["SS Iono", "ss iono"])], "pokeFair"))
    case "e":
      bannerSelect(Banner("Sygna Suit (Alt.) Elesa Poke Fair Scout", [Pair(5, True, "Fair-Exclusive", "Sygna Suit (Alt.) Elesa", "Thundurus-Therian", ["SSA Elesa", "ssa elesa"])], "pokeFair"))
    case "f":
      bannerSelect(Banner("Rosa (Champion) Master Fair Scout", [Pair(5, True, "Master Fair", "Rosa (Champion)", "Meloetta", ["NC Rosa", "nc rosa"])], "masterFair"))
    case "k":
      bannerSelect(Banner("Lacey Poke Fair Scout", [Pair(5, True, "Fair-Exclusive", "Lacey", "Granbull", [])], "pokeFair"))
    case "l":
      bannerSelect(Banner("Ilima Spotlight Scout", [Pair(5, True, "General", "Ilima", "Gumshoos", [])], "spotlight"))
    case "m":
      bannerSelect(Banner("Double Feature Poke Fair Scout", [Pair(5, True, "Fair-Exclusive", "Rei", "Decidueye-Hisui", []), Pair(5, True, "Fair-Exclusive", "Akari", "Samurott-Hisui", [])], "2xPF"))
    case "s":
      bannerSelect(Banner("Triple Feature Master Fair Scout", [Pair(5, True, "Master Fair", "Maxie", "Groudon", []), Pair(5, True, "Master Fair", "Archie", "Kyogre", []), Pair(5, True, "Master Fair", "Leon", "Charizard", [])], "3xMF"))
    case "t":
      bannerSelect(Banner("May (Champion) Master Fair Scout", [Pair(5, True, "Master Fair", "May (Champion)", "Kyogre", ["NC May", "nc may"])], "masterFair"))
    case "u":
      bannerSelect(Banner("Brendan (Champion) Master Fair Scout", [Pair(5, True, "Master Fair", "Brendan (Champion)", "Groudon", ["NC Brendan", "nc brendan"])], "masterFair"))
    case "v":
      bannerSelect(Banner("Steven (Anniversary 2021) Master Fair Scout", [Pair(5, True, "Master Fair", "Steven (Anniversary 2021)", "Rayquaza", ["Anni Steven", "anni steven", "anniSteven", "AnniSteven"])], "masterFair"))
    case "x":
      bannerSelect(Banner("Arc Suit N Arc Suit Fair Scout", [Pair(5, True, "Arc Suit Fair", "Arc Suit N", "Zoroark", ["AS N", "as n", "ASN"])], "arcSuitFair"))
    case "z":
      bannerSelect(Banner("Ortega Poke Fair Scout", [Pair(5, True, "Fair-Exclusive", "Ortega", "Dachsbun", [])], "pokeFair"))
    case "aa":
      bannerSelect(Banner("Team Star Assemble! Super Spotlight Poke Fair Scout", [Pair(5, True, "Fair-Exclusive", "Penny", "Sylveon", []), Pair(5, True, "Fair-Exclusive", "Atticus", "Revavroom", []), Pair(5, True, "Fair-Exclusive", "Ortega", "Dachsbun", []), Pair(5, True, "Fair-Exclusive", "Mela", "Armarouge", []), Pair(5, True, "Fair-Exclusive", "Eri", "Annihilape", []), Pair(5, True, "Fair-Exclusive", "Giacomo", "Kingambit", [])], "superScout"))
    case "ab":
      bannerSelect(Banner("Nate (Champion) Master Fair Scout", [Pair(5, True, "Master Fair", "Nate (Champion)", "Haxorus", ["NC Nate", "nc nate"])], "masterFair"))
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
      print("5* Variety: 0/34 (Priority: #3)")
      print("5* Damage Challenge: 0/??")
      print("5* Seasonal: 54/54 [COMPLETED]")
      print("5* Mix: 5/5 [COMPLETED]")
      print("5* Special Costume: 0/22 (Priority: #1)")
      print("5* Master Fair: 39/39 [COMPLETED]")
      print("5* Arc Suit Fair: 6/6 [COMPLETED]")
      print("Gym Scout: 0/6 (Priority: #2)")
    case "l":
      print("----------------------------------------")
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