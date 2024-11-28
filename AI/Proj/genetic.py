import random

# Default genes set
GENES = '''abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOP
QRSTUVWXYZ 1234567890, .-;:_!"#%&/()=?@${[]}'''

class Individual:
    def __init__(self, chromosome, target):
        self.chromosome = chromosome
        self.target = target
        self.fitness = self.cal_fitness()
        print(f"Created Individual: {''.join(self.chromosome)} | Fitness: {self.fitness}")

    @classmethod
    def mutated_genes(cls, genes):
        gene = random.choice(genes)
        print(f"Mutated gene selected: {gene}")
        return gene

    @classmethod
    def create_gnome(cls, target, genes):
        print(f"Creating a gnome for target '{target}'")
        gnome = [cls.mutated_genes(genes) for _ in range(len(target))]
        print(f"Generated gnome (chromosome): {''.join(gnome)}")
        return gnome

    def mate(self, par2, genes):
        print(f"Mating:\n  Parent 1: {''.join(self.chromosome)}\n  Parent 2: {''.join(par2.chromosome)}")
        child_chromosome = []
        for gp1, gp2 in zip(self.chromosome, par2.chromosome):
            prob = random.random()
            if prob < 0.45:
                child_chromosome.append(gp1)
            elif prob < 0.90:
                child_chromosome.append(gp2)
            else:
                child_chromosome.append(self.mutated_genes(genes))
        print(f"Child Chromosome: {''.join(child_chromosome)}")
        return Individual(child_chromosome, self.target)

    def cal_fitness(self):
        fitness = sum(gs != gt for gs, gt in zip(self.chromosome, self.target))
        print(f"Calculating fitness for {''.join(self.chromosome)} | Fitness: {fitness}")
        return fitness

# Driver code
def main():
    print("Welcome to the Genetic Algorithm!")
    target = input("Enter the target string: ").strip()

    while True:
        try:
            population_size = int(input("Enter the population size (e.g., 100): ").strip())
            if population_size <= 0:
                raise ValueError("Population size must be a positive integer.")
            break
        except ValueError as e:
            print(f"Invalid input: {e}. Please enter a valid number.")

    generation = 1
    found = False
    population = []

    # Create initial population
    print("\nCreating initial population...")
    for i in range(population_size):
        print(f"Creating individual {i + 1}/{population_size}")
        gnome = Individual.create_gnome(target, GENES)
        population.append(Individual(gnome, target))
    print("Initial population created.\n")

    while not found:
        print(f"--- Generation {generation} ---")
        # Sort population by fitness
        population = sorted(population, key=lambda x: x.fitness)
        print(f"Best Chromosome in Generation {generation}: {''.join(population[0].chromosome)} | Fitness: {population[0].fitness}")

        if population[0].fitness <= 0:
            found = True
            break

        new_generation = []

        # Elitism: 10% of the fittest individuals
        elite_size = int(0.1 * population_size)
        print(f"Elitism: Carrying forward {elite_size} best individuals.")
        new_generation.extend(population[:elite_size])

        # Generate new individuals
        for _ in range(population_size - elite_size):
            parent1 = random.choice(population[:50])
            parent2 = random.choice(population[:50])
            print(f"Selected Parents for Reproduction:\n  Parent 1: {''.join(parent1.chromosome)}\n  Parent 2: {''.join(parent2.chromosome)}")
            child = parent1.mate(parent2, GENES)
            new_generation.append(child)

        population = new_generation
        generation += 1

    print(f"\nTarget achieved in Generation {generation}: {''.join(population[0].chromosome)} | Fitness: {population[0].fitness}")

if __name__ == "__main__":
    main()
