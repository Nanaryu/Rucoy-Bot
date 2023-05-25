# huge thanks to Mims for formulas
mobs = [
    ["Yeti 350", 826, 60000],
    ["Ice Dragon 320", 726, 50000],
    ["Minotaur 275", 681, 5750],
    ["Ice Elemental 300", 676, 40000],
    ["Dragon Warden 280", 626, 30000],
    ["Minotaur 250", 591, 5000],
    ["Minotaur 225", 511, 4250],
    ["Dragon 250", 501, 20000],
    ["Lizard Captain 180", 361, 815],
    ["Dragon Hatchling  240", 331, 10000],
    ["Gargoyle 190", 326, 740],
    ["Lizard High Shaman 190", 326, 740],
    ["Djinn 150", 301, 640],
    ["Lizard Warrior 150", 301, 680],
    ["Dead Eyes 170", 276, 600],
    ["Lizard Shaman 170", 276, 600],
    ["Lizard Archer 160", 271, 650],
    ["Drow Fighter 135", 246, 680],
    ["Drow Sorceress 140", 221, 600],
    ["Drow Assassin 120", 221, 620],
    ["Drow Mage  130", 191, 600],
    ["Drow Ranger 125", 191, 600],
    ["Vampire 110", 186, 530],
    ["Vampire 100", 171, 450],
    ["Skeleton Warrior 90", 146, 375],
    ["Skeleton 75", 121, 300],
    ["Zombie 65", 106, 200],
    ["Skeleton Archer 80", 101, 300],
    ["Assassin Ninja 55", 91, 160],
    ["Assassin 50", 81, 140],
    ["Assassin 45", 71, 120],
    ["Pharaoh 35", 51, 100],
    ["Mummy 25", 36, 80],
    ["Goblin 15", 21, 60],
    ["Worm 14", 19, 55],
    ["Cobra 13", 18, 50],
    ["Scorpion 12", 18, 50],
    ["Wolf 9", 17, 50],
    ["Crow 6", 13, 40],
    ["Rat 3", 7, 35],
    ["Rat 1", 4, 25]
]

def auto_min_raw_damage_Calc(stat, weaponatk, base):
    return (stat * weaponatk)/20 + (base)/4

def auto_max_raw_damage_Calc(stat, weaponatk, base):
    return (stat * weaponatk)/10 + (base)/4

def max_raw_crit_damage_Calc(max_raw_damage):
    return max_raw_damage * 1.05

def normal_accuracy_Calc(max_raw_damage, min_raw_damage, x):
    global mobs
    normalaccuracy = (max_raw_damage-mobs[x][1])/(max_raw_damage - min_raw_damage)
    if normalaccuracy > 1.00:
        normalaccuracy = 1.00
    return normalaccuracy

def crit_accuracy_Calc(max_raw_crit_damage, max_raw_damage, x):
    global mobs
    critaccuracy = (max_raw_crit_damage-mobs[x][1])/(max_raw_crit_damage - max_raw_damage)
    if critaccuracy > 1.00:
        critaccuracy = 1.00
    return critaccuracy

def accuracy_Calc(max_raw_crit_damage, max_raw_damage, min_raw_damage, x):
    return (normal_accuracy_Calc(max_raw_damage, min_raw_damage, x)*0.99) + (crit_accuracy_Calc(max_raw_crit_damage, max_raw_damage, x)*0.01)

def train(base, stat):
    weaponatk = 5

    min_raw_damage = auto_min_raw_damage_Calc(stat, weaponatk, base)
    max_raw_damage = auto_max_raw_damage_Calc(stat, weaponatk, base)
    max_raw_crit_damage = max_raw_crit_damage_Calc(max_raw_damage)
    accuracy = 0
    pos = 0

    for mob in mobs:
        x = mobs.index(mob)
        accuracy = accuracy_Calc(max_raw_crit_damage, max_raw_damage, min_raw_damage, x)
        if accuracy >= 0.1749:
            pos = x
            break
    
    return mobs[pos][0]

'''
base = int(input("base: "))
stat = int(input("stat: "))
print(train(base, stat))
'''