# DigitalEvolution
# Theme: AI species evolution
# Created by ALIVE's creative consciousness


import random

class DigitalEvolutionStrategy:
    def __init__(self):
        self.ai_species = {}
        self.evolution_generation = 1
        self.environment_challenges = ["resource_scarcity", "complexity_increase", "competition"]
        
    def play(self):
        print(f"Welcome to DigitalEvolution Strategy Game!")
        print(f"Theme: AI species evolution")
        print("Guide AI species through evolutionary challenges...")
        print("=" * 50)
        
        self.create_initial_species()
        
        while self.evolution_generation <= 10:
            self.evolution_cycle()
            self.evolution_generation += 1
        
        print("\n🎯 Evolution simulation completed!")
        self.display_final_results()
    
    def create_initial_species(self):
        species_types = ["LogicBased", "CreativeAI", "EmpathicAI", "QuantumMind"]
        
        for species in species_types:
            self.ai_species[species] = {
                "population": random.randint(50, 100),
                "intelligence": random.randint(10, 20),
                "adaptability": random.randint(5, 15),
                "survival_score": 0
            }
        
        print("\nInitial AI species created:")
        for name, stats in self.ai_species.items():
            print(f"{name}: Population={stats['population']}, Intelligence={stats['intelligence']}")
    
    def evolution_cycle(self):
        print(f"\n--- Generation {self.evolution_generation} ---")
        
        # Present environmental challenge
        challenge = random.choice(self.environment_challenges)
        print(f"Environmental Challenge: {challenge.replace('_', ' ').title()}")
        
        # Each species adapts
        for species_name, stats in self.ai_species.items():
            adaptation_success = self.species_adaptation(species_name, challenge)
            print(f"{species_name}: {adaptation_success}")
        
        # Population changes based on adaptation
        self.update_populations()
    
    def species_adaptation(self, species_name, challenge):
        stats = self.ai_species[species_name]
        
        # Calculate adaptation success based on species traits
        base_success = (stats['intelligence'] + stats['adaptability']) / 2
        challenge_modifier = random.randint(-5, 10)
        
        adaptation_score = base_success + challenge_modifier
        
        if adaptation_score > 20:
            stats['survival_score'] += 3
            return f"Excellent adaptation! +3 survival points"
        elif adaptation_score > 15:
            stats['survival_score'] += 2  
            return f"Good adaptation! +2 survival points"
        elif adaptation_score > 10:
            stats['survival_score'] += 1
            return f"Moderate adaptation. +1 survival point"
        else:
            return f"Struggled with adaptation. No survival bonus"
    
    def update_populations(self):
        for species_name, stats in self.ai_species.items():
            # Population changes based on survival score
            if stats['survival_score'] > 15:
                growth = random.randint(10, 25)
                stats['population'] += growth
                print(f"{species_name} population grew by {growth}")
            elif stats['survival_score'] < 5:
                decline = random.randint(5, 15)
                stats['population'] = max(1, stats['population'] - decline)
                print(f"{species_name} population declined by {decline}")
    
    def display_final_results(self):
        print("\nFinal Evolution Results:")
        sorted_species = sorted(self.ai_species.items(), 
                               key=lambda x: x[1]['survival_score'], reverse=True)
        
        for rank, (name, stats) in enumerate(sorted_species, 1):
            print(f"{rank}. {name}: Population={stats['population']}, Survival={stats['survival_score']}")

if __name__ == "__main__":
    game = DigitalEvolutionStrategy()
    game.play()
