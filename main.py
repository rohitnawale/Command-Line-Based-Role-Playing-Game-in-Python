import game
import magic
from inventory import Item
import random

print("\n\n")
'''print(game.Bcolors.OKBLUE + game.Bcolors.BOLD + "NAME                    HP                                         MP" + game.Bcolors.ENDC)

print("                        -------------------------                 ---------- ")

print(game.Bcolors.OKORANGE +"JARVIS:        460/460 |                         |         65/65 |██████████|"+game.Bcolors.ENDC)

print("                        -------------------------                 ---------- ")
print(game.Bcolors.OKORANGE +"Vision:        460/460 |                         |         65/65 |██████████|"+game.Bcolors.ENDC)

print("                        -------------------------                 ---------- ")
print(game.Bcolors.OKORANGE +"JARVIS:        460/460 |                         |         65/65 |██████████|"+game.Bcolors.ENDC)

'''
#Create black magic
fire = magic.Spell("Fire" ,25, 600, "black")
thunder = magic.Spell("Thunder" ,25, 600, "black")
blizzard = magic.Spell("Blizzard" ,25, 600, "black")
meteor = magic.Spell("Meteor" ,40, 1200, "black")
quake = magic.Spell("Quake" ,14, 140, "black")

#Create white magic
cure = magic.Spell("Cure", 25, 600, "white")
cura = magic.Spell("Cura", 32, 1200, "white")

#Create Items
potion = Item("Potion", "potion", "Heals 50 HP ", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals 1000 HP",1000)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one party member", 9999)
hielixer = Item("MegaElixer", "elixer" , "Fully restores HP/MP of all party members", 9999)
grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

player_spells = [fire, thunder, blizzard, meteor, cure, cura]
enemy_spells = [fire, meteor ,cure]
player_items = [{"item":potion , "quantity":15}, {"item":hipotion , "quantity":5},
                {"item":superpotion ,"quantity": 5}, {"item" :elixer , "quantity":5},
                {"item":hielixer, "quantity":2},{"item":grenade , "quantity":5}]
#
player1 = game.Person("JARVIS:", 3860,132,300,34,player_spells, player_items)
player2 = game.Person("Vision:", 3690,188,320,34,player_spells, player_items)
player3 = game.Person("Tony  :", 4060,174,280,34,player_spells, player_items)

players = [player1, player2, player3]

enemy1 = game.Person("Loki  " , 1250, 130, 560, 325,enemy_spells,[])
enemy2 = game.Person("Thanos", 9000, 701, 545, 25, enemy_spells,[])
enemy3 = game.Person("Ultron", 1250, 130, 560, 325, enemy_spells, [])

enemies = [enemy1, enemy2, enemy3]

running = True
i = 0
print(game.Bcolors.FAIL + game.Bcolors.BOLD + "AN ENEMY ATTACKS!" + game.Bcolors.ENDC)

while running:
    print("====================================")

    print(game.Bcolors.OKBLUE + game.Bcolors.BOLD + "NAME                  HP                                            MP" + game.Bcolors.ENDC)
    for player in players:
        #print("\n\n")
        player.get_stats()
        print("\n")

    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:

        player.choose_action()
        choice = input("   Choose Action: ")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)
            enemies[enemy].take_damage(dmg)
            print("You attacked "+ enemies[enemy].name.replace(" ","") + "for ", dmg , "points of damage . Enemy HP: " + str(enemies[enemy].get_hp()))

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name + " has died.")
                del enemies[enemy]

        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("   Choose magic : ")) - 1

            if magic_choice == -1:
                continue
            #magic_dmg = player.generate_spell_damage(magic_choice)
            #spell = player.get_spell_name(magic_choice)
            #cost = player.get_spell_mp_cost(magic_choice)
            current_mp = player.get_mp()

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            if spell.cost > current_mp:
                print(game.Bcolors.FAIL + "\nNot enough mp\n " + game.Bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(game.Bcolors.OKBLUE + "\n" + spell.name + "heals for ", str(magic_dmg) ,"HP" + game.Bcolors.ENDC)

            elif spell.type == "black":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)

                print(game.Bcolors.OKBLUE + "\n" + spell.name + " deals " , str(magic_dmg) , "points of damage to"+ enemies[enemy].name.replace(" ","") + game.Bcolors.ENDC)

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name + " has died.")
                del enemies[enemy]

        elif index == 2:
            player.choose_items()
            item_choice = int(input("   Choose Item")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]

            if player.items[item_choice]["item"] == 0:
                print(game.Bcolors.FAIL + "None left..." + game.Bcolors.ENDC)
                continue

            #player.items[item_choice]["item"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(game.Bcolors.OKGREEN + "\n" + item.name + "heals for ", str(item.prop), "HP" + game.Bcolors.ENDC)

            elif item.type == "elixer":

                if item.name == "MegaElixier":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(game.Bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP " + game.Bcolors.ENDC)

            elif item.type == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)

                print(game.Bcolors.FAIL + "\n" + item.name + " deals" , str(item.prop) , "points of damage to "+ enemies[enemy].name + game.Bcolors.ENDC)

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name.replace(" ", "") + " has died.")
                del enemies[enemy]

    #check if game is over
    defeated_enemies = 0
    defeated_players = 0
    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    #check if player won
    if defeated_enemies == 2:
        print(game.Bcolors.OKGREEN + "You win " + game.Bcolors.ENDC)
        running = False
    #check if enemy won
    elif defeated_players == 2:
        print(game.Bcolors.FAIL + "Enemies have defeated you!" + game.Bcolors.ENDC)
        running = False

    #Enemy attack phase
    for enemy in enemies:

        enemy_choice = random.randrange(0,2)

        if enemy_choice == 0:
            #chose attack
            target = random.randrange(0,3)
            enemy_dmg = enemy.generate_damage()
            players[target].take_damage(enemy_dmg)
            print(enemy.name.replace(" ","") + " attacked " + players[target].name.replace(" ","") +"for ", enemy_dmg, "points of damage")

            print("------------------------------")
    #print("Enemy HP : " + game.Bcolors.FAIL  + str(enemy.get_hp()) + "/" + str(enemy.get_max_hp()) + game.Bcolors.ENDC + "\n")
    #print("Your HP : " + game.Bcolors.OKGREEN + str(player.get_hp()) + "/" + str(player.get_max_hp()) + game.Bcolors.ENDC + "\n")
    #print("Your MP : " + game.Bcolors.OKGREEN + str(player.get_mp()) + "/" + str(player.get_max_mp()) + game.Bcolors.ENDC + "\n")




        elif enemy_choice == 1:
            spell , magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)




            if spell.type == "white":
                enemy.heal(magic_dmg)
                print(game.Bcolors.OKBLUE + "\n" + spell.name + "heals "+ enemy.name+"for ", str(magic_dmg) ,"HP" + game.Bcolors.ENDC)

            elif spell.type == "black":
                target = random.randrange(0, 3)
                players[target].take_damage(magic_dmg)

                print(game.Bcolors.OKBLUE + "\n"+enemy.name.replace(" ","")+"'s " + spell.name + " deals " , str(magic_dmg) , "points of damage to"+ players[target].name.replace(" ","") + game.Bcolors.ENDC)

                if players[target].get_hp() == 0:
                    print(players[target].name + " has died.")
                    del players[target]
                #print("Enemy Chose " , spell , "damage is " ,magic_dmg)
