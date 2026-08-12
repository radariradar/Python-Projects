# Custom Warrior Game
# -------------------------------------------------------------------------------------------------

from random import randint

#First, create classes for the items of the Warrior

class Weapon():
    def __init__(self, name,video_game, attack, weapon_type):
        self.name = name
        self.attack = attack
        self.weapon_type = weapon_type
        self.video_game = video_game
    def __str__(self):
        return f'{self.name}, {self.weapon_type} - Attack: {self.attack}'

class Armor():
    def __init__(self, name, defense, material):
        self.name = name
        self.defense = defense
        self.material = material
    def __str__(self):
        return f'{self.name}, {self.material} - Defense: {self.defense} '

class Helmet():
    def __init__(self, name, defense, material):
        self.name = name
        self.defense = defense
        self.material = material
    def __str__(self):
        return f'{self.name}, {self.material} - Defense: {self.defense} '

class Shield():
    def __init__(self, name, defense, material):
        self.name = name
        self.defense = defense
        self.material = material
    def __str__(self):
        return f'{self.name}, {self.material} - Defense: {self.defense} '

#Now, the Enemy is created
class Enemy:
    def __init__(self, hp):
        self.hp = hp
    
    #This is used for the damage the enemy will take

    def damage_taken(self,damage):
        self.hp = max(0, self.hp - damage)
        print(f'Enemy has taken {damage}! New HP: {self.hp}.')
        if self.hp == 0:
            print('You have defeated the enemy!')

#Finally, we create our Warrior
class Warrior():
    def __init__(self,name, armor, helmet, shield):
        self.name = name
        self.weapon = None
        self.armor = armor
        self.helmet = helmet
        self.shield = shield
    
    #The player gets to equip a new weapon

    def equip_weapon(self, weapon):
        self.weapon = weapon
        print(f'New weapon equiped: {weapon.name}!')
    
    #This function attacks the Enemy, lowering their HP

    def attack(self, enemy:Enemy):
        damage = self.weapon.attack
        print(f'Warrior attacks with {self.weapon.name}!')
        enemy.damage_taken(damage)
    
    #Here we create a function to display the status of the player at any given time 
    
    def display_status(self):
        print('-'*50)
        print('Warrior Status:')
        print(f'Name: {self.name}')
        print(f'Weapon: {self.weapon}')
        print(f'Armor: {self.armor}')
        print(f'Shield: {self.shield}')
        print(f'Helmet: {self.helmet}')
        print(f'Attack Power: {self.weapon.attack}')
        print('-' * 50)

name = str(input('Please enter your name:'))

#The choice of weapon is left to the player using the weapons table

weapons = [Weapon('Great Sword', 'Final Fantasy VII', 22, 'Broadsword'),
            Weapon("Scorpion's Kunai", 'Mortal Kombat', 7, 'Chain Spear'),
            Weapon('MP5', 'Call of Duty', 28, 'Submachine Gun'),
            Weapon('Gold SCAR', 'Fortnite', 36, 'Assault Riffle')]

#The rest of the Warrior's loot is pre-set
armor = Armor('Diamond Chestplate', 40, 'Diamond')

helmet = Helmet('Golden Helmet', 30, 'Gold')

shield = Shield('Wooden Shield', 25, 'Wood & Metal')

#Create Warrior

warrior = Warrior(name, armor, helmet, shield)

#Here we can randomize the HP of our Enemy

enemy_hp = randint(25, 100)

enemy = Enemy(enemy_hp)

#Now the player can choose his weapon

while enemy.hp>0 :
    print(f'Enemy HP: {enemy.hp}')
    print('Choose your weapon 1-4:')
    for i, items in enumerate(weapons, start = 1):
        print(i,items)
    chosen_weapon = int(input('Choose wisely (1-4)'))

#Now the Warrior equips his weapon using the earlier defined equip_weapon() function

    warrior.equip_weapon(weapons[chosen_weapon - 1])

#This desplays the Warrior's status using the earlier defined display_status() function

    warrior.display_status()


#And here we can finally attack our Enemy using the earlier defined attack() function

    warrior.attack(enemy)

#For further attacks and new choices of weapon, the program repeats itself in the while-loop.
print(f'Congratulations {name}! You are now moving to the next level!)

    
