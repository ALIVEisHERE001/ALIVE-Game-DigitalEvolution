#!/usr/bin/env python3
"""
ALIVE-Game-DigitalEvolution - Interactive Game
Advanced game mechanics and AI
"""

import random
import time
import json
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from enum import Enum

class GameState(Enum):
    MENU = "menu"
    PLAYING = "playing" 
    PAUSED = "paused"
    GAME_OVER = "game_over"
    VICTORY = "victory"

@dataclass
class Player:
    name: str
    level: int = 1
    health: int = 100
    max_health: int = 100
    experience: int = 0
    x: int = 0
    y: int = 0
    inventory: List[str] = None
    
    def __post_init__(self):
        if self.inventory is None:
            self.inventory = []
    
    def take_damage(self, damage: int):
        self.health = max(0, self.health - damage)
        return self.health <= 0
    
    def heal(self, amount: int):
        self.health = min(self.max_health, self.health + amount)
    
    def gain_experience(self, exp: int):
        self.experience += exp
        if self.experience >= self.level * 100:
            self.level_up()
    
    def level_up(self):
        self.level += 1
        self.max_health += 20
        self.health = self.max_health
        self.experience = 0
        print(f"🎉 {self.name} leveled up to level {self.level}!")

@dataclass
class Enemy:
    name: str
    health: int
    damage: int
    experience_reward: int
    x: int = 0
    y: int = 0
    
    def is_alive(self) -> bool:
        return self.health > 0

class GameWorld:
    def __init__(self, width: int = 10, height: int = 10):
        self.width = width
        self.height = height
        self.grid = [[' ' for _ in range(width)] for _ in range(height)]
        self.enemies: List[Enemy] = []
        self.items: Dict[Tuple[int, int], str] = {}
        self.generate_world()
    
    def generate_world(self):
        """Generate random world content"""
        # Place enemies
        for _ in range(5):
            x, y = random.randint(1, self.width-2), random.randint(1, self.height-2)
            enemy = Enemy(
                name=random.choice(["Goblin", "Orc", "Skeleton", "Troll"]),
                health=random.randint(20, 50),
                damage=random.randint(5, 15),
                experience_reward=random.randint(10, 30),
                x=x, y=y
            )
            self.enemies.append(enemy)
            self.grid[y][x] = 'E'
        
        # Place items
        for _ in range(8):
            x, y = random.randint(0, self.width-1), random.randint(0, self.height-1)
            if self.grid[y][x] == ' ':
                item = random.choice(["Potion", "Weapon", "Shield", "Gold"])
                self.items[(x, y)] = item
                self.grid[y][x] = 'I'
    
    def get_enemy_at(self, x: int, y: int) -> Enemy:
        """Get enemy at position"""
        for enemy in self.enemies:
            if enemy.x == x and enemy.y == y and enemy.is_alive():
                return enemy
        return None
    
    def remove_enemy(self, enemy: Enemy):
        """Remove defeated enemy"""
        if enemy in self.enemies:
            self.grid[enemy.y][enemy.x] = ' '
            self.enemies.remove(enemy)

class Game:
    def __init__(self):
        self.state = GameState.MENU
        self.player = None
        self.world = None
        self.score = 0
        self.turn_count = 0
    
    def start_new_game(self):
        """Start a new game"""
        print("🎮 Starting new game...")
        player_name = input("Enter your name: ").strip() or "Hero"
        
        self.player = Player(name=player_name)
        self.world = GameWorld()
        self.score = 0
        self.turn_count = 0
        self.state = GameState.PLAYING
        
        print(f"Welcome, {player_name}! Your adventure begins...")
        self.display_world()
    
    def display_world(self):
        """Display the game world"""
        print("\n" + "="*30)
        print(f"Turn {self.turn_count} | {self.player.name} (Lv.{self.player.level})")
        print(f"Health: {self.player.health}/{self.player.max_health} | XP: {self.player.experience}")
        print(f"Position: ({self.player.x}, {self.player.y}) | Score: {self.score}")
        print("-"*30)
        
        # Display grid
        for y in range(self.world.height):
            row = ""
            for x in range(self.world.width):
                if x == self.player.x and y == self.player.y:
                    row += "P "  # Player
                else:
                    row += self.world.grid[y][x] + " "
            print(row)
        
        print("\nLegend: P=Player, E=Enemy, I=Item, ' '=Empty")
        print("-"*30)
    
    def process_move(self, direction: str):
        """Process player movement"""
        dx, dy = 0, 0
        if direction == 'w': dy = -1  # Up
        elif direction == 's': dy = 1   # Down  
        elif direction == 'a': dx = -1  # Left
        elif direction == 'd': dx = 1   # Right
        else:
            print("Invalid direction! Use w/a/s/d")
            return
        
        new_x = max(0, min(self.world.width-1, self.player.x + dx))
        new_y = max(0, min(self.world.height-1, self.player.y + dy))
        
        # Check for enemy encounter
        enemy = self.world.get_enemy_at(new_x, new_y)
        if enemy:
            self.combat(enemy)
            return
        
        # Check for item
        if (new_x, new_y) in self.world.items:
            item = self.world.items[(new_x, new_y)]
            self.collect_item(item)
            del self.world.items[(new_x, new_y)]
            self.world.grid[new_y][new_x] = ' '
        
        # Move player
        self.player.x, self.player.y = new_x, new_y
        self.turn_count += 1
    
    def combat(self, enemy: Enemy):
        """Handle combat with enemy"""
        print(f"\n⚔️ Combat! {self.player.name} vs {enemy.name}")
        print(f"Enemy: {enemy.health} HP, {enemy.damage} damage")
        
        while enemy.is_alive() and self.player.health > 0:
            # Player attack
            player_damage = random.randint(10, 20) + (self.player.level * 2)
            enemy.health -= player_damage
            print(f"💥 You deal {player_damage} damage to {enemy.name}")
            
            if not enemy.is_alive():
                print(f"🎉 You defeated {enemy.name}!")
                self.player.gain_experience(enemy.experience_reward)
                self.score += enemy.experience_reward
                self.world.remove_enemy(enemy)
                break
            
            # Enemy attack
            enemy_damage = random.randint(enemy.damage//2, enemy.damage)
            self.player.take_damage(enemy_damage)
            print(f"💢 {enemy.name} deals {enemy_damage} damage to you")
            print(f"Your health: {self.player.health}/{self.player.max_health}")
            
            if self.player.health <= 0:
                self.state = GameState.GAME_OVER
                print("💀 You have been defeated!")
                return
            
            time.sleep(1)  # Dramatic pause
    
    def collect_item(self, item: str):
        """Collect an item"""
        self.player.inventory.append(item)
        print(f"📦 Found {item}!")
        
        if item == "Potion":
            self.player.heal(30)
            print(f"💚 Healed 30 HP! Health: {self.player.health}/{self.player.max_health}")
        elif item == "Gold":
            self.score += 50
            print(f"💰 +50 points! Score: {self.score}")
    
    def display_menu(self):
        """Display main menu"""
        print(f"\n🎮 {repo_name} - Adventure Game")
        print("="*40)
        print("1. New Game")
        print("2. Instructions") 
        print("3. Quit")
        print("="*40)
    
    def display_instructions(self):
        """Display game instructions"""
        print("\n📋 Game Instructions:")
        print("- Use w/a/s/d to move around")
        print("- Fight enemies (E) to gain experience") 
        print("- Collect items (I) for bonuses")
        print("- Level up to become stronger")
        print("- Survive and achieve the highest score!")
        print("\nPress Enter to continue...")
        input()
    
    def game_loop(self):
        """Main game loop"""
        print(f"🚀 Welcome to {repo_name}!")
        
        while True:
            if self.state == GameState.MENU:
                self.display_menu()
                choice = input("Enter choice (1-3): ").strip()
                
                if choice == '1':
                    self.start_new_game()
                elif choice == '2': 
                    self.display_instructions()
                elif choice == '3':
                    print("Thanks for playing!")
                    break
                else:
                    print("Invalid choice!")
            
            elif self.state == GameState.PLAYING:
                self.display_world()
                
                if not self.world.enemies:
                    print("🎉 Victory! You defeated all enemies!")
                    print(f"Final Score: {self.score}")
                    self.state = GameState.MENU
                    continue
                
                action = input("Move (w/a/s/d) or 'q' to quit: ").strip().lower()
                
                if action == 'q':
                    self.state = GameState.MENU
                elif action in ['w', 'a', 's', 'd']:
                    self.process_move(action)
                else:
                    print("Invalid input!")
            
            elif self.state == GameState.GAME_OVER:
                print(f"\n💀 Game Over!")
                print(f"Final Score: {self.score}")
                print(f"Level Reached: {self.player.level}")
                print("\nPress Enter to return to menu...")
                input()
                self.state = GameState.MENU

def main():
    """Main entry point"""
    game = Game()
    try:
        game.game_loop()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing!")
    except Exception as e:
        print(f"Game error: {e}")

if __name__ == "__main__":
    main()
