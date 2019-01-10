import random
#from magic import Spell
import pprint


class Bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    OKORANGE = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Person:
    def __init__(self,name, hp, mp, atk, df, magic, items):
        self.name = name
        self.maxhp = hp
        self.hp = hp
        self.maxmp = mp
        self.mp = mp
        self.atkl = atk-10
        self.atkh = atk+10
        self.df = df
        self.magic = magic
        self.items = items
        self.actions = ["Attack", "Magic","Items"]


    def generate_damage(self):
        return random.randrange(self.atkl, self.atkh)

    def heal(self,hp):
        self.hp += hp
        if self.hp > self.maxhp:
            self.hp = self.maxhp


    def generate_spell_damage(self,i):
        mgl = self.magic[i]["dmg"]-5
        mgh = self.magic[i]["dmg"]+5
        return random.randrange(mgl, mgh)

    def take_damage(self,dmg):
        self.hp -= dmg
        if self.hp <0:
            self.hp = 0
        return self.hp

    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.maxhp

    def get_mp(self):
        return self.mp

    def get_max_mp(self):
        return self.maxmp

    def reduce_mp(self,cost):
        self.mp -= cost

    def get_spell_name(self, i):
        return self.magic[i]["name"]

    def get_spell_mp_cost(self, i):
        return self.magic[i]["cost"]

    def choose_action(self):
        i = 1
        print("\n" + "    "+Bcolors.BOLD + self.name + Bcolors.ENDC)
        print(Bcolors.FAIL + Bcolors.BOLD + "    ACTIONS" + Bcolors.ENDC)
        for item in self.actions:
            print("     "+str(i) + " : " , item )
            i += 1

    def choose_magic(self):
        i = 1
        print("\n"+ Bcolors.OKGREEN + Bcolors.BOLD + "    MAGIC" + Bcolors.ENDC)
        for spell in self.magic:
            print("     "+str(i) + ":" , spell.name, "(cost:" , str(spell.cost) + ")")
            i += 1

    def choose_items(self):
        i = 1
        print("\n"+ Bcolors.OKBLUE + Bcolors.BOLD + "    ITEMS" + Bcolors.ENDC)
        for item in self.items:
            print("     "+str(i) + ".", item["item"].name, ":", item["item"].description, "(x" + str(item["quantity"]))
            i += 1


    def choose_target(self,enemies):
        i = 1
        print(Bcolors.FAIL + Bcolors.BOLD + "    TARGET:" + Bcolors.ENDC)
        for enemy in enemies:
            if enemy.get_hp() != 0:
                print("       " + str(i) + ".", enemy.name)
                i += 1

        choice = int(input("    Choose Target:")) - 1
        return choice

    def get_enemy_stats(self):
        hp_bar  = ""
        bar_ticks = ((self.hp / self.maxhp) * 100) / 2

        while bar_ticks > 0:
            hp_bar += "█"
            bar_ticks -= 1

        while len(hp_bar) < 50:
            hp_bar += " "

        print("                                  -------------------------------------------------- ")

        print(Bcolors.FAIL + self.name + "      :        " + str(self.hp) + "/" + str(
            self.maxhp) + " |" + hp_bar + "|         " + Bcolors.ENDC)

    def get_stats(self):
        hp_bar = ""
        bar_ticks = ((self.hp / self.maxhp) * 100 ) / 4

        mp_bar = ""
        mp_ticks = ((self.mp / self.maxmp) * 100 ) / 10
        while bar_ticks > 0:
            hp_bar += "█"
            bar_ticks -= 1

        while mp_ticks > 0:
            mp_bar += "█"
            mp_ticks -= 1

        while len(hp_bar) < 25:
            hp_bar += " "

        while len(mp_bar) < 10:
            mp_bar += " "


        print("                                 -------------------------                ---------- ")

        print(Bcolors.OKORANGE + self.name + "      :        " +str(self.hp) + "/"+str(self.maxhp) +" |" + hp_bar + "|         "+ str(self.mp) + "/" + str(self.maxmp) +Bcolors.ENDC + Bcolors.OKBLUE+ "|"+mp_bar + "|"+Bcolors.ENDC)


    def choose_enemy_spell(self):
        magic_choice = random.randrange(0, len(self.magic))
        spell = self.magic[magic_choice]
        magic_dmg = spell.generate_damage()

        pct = (self.hp / self.maxhp ) * 100
        if self.mp < spell.cost or spell.type == "white ":
            self.choose_enemy_spell()

        else:
            return spell,magic_dmg