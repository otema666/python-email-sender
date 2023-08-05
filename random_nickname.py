import random

def generate_random_nickname():
    adjectives = ['cool', 'slick', 'swift', 'neat', 'smooth', 'sleek', 'awesome', 'stellar', 'excellent', 'epic']
    nouns = ['tiger', 'wolf', 'hawk', 'rider', 'joker', 'wizard', 'phoenix', 'hunter', 'ninja', 'sprinter']
    numbers = [str(random.randint(10, 99)) for _ in range(2)]

    adjective = random.choice(adjectives)
    noun = random.choice(nouns)
    number = ''.join(numbers)

    nickname = f'{adjective.capitalize()}{noun.capitalize()}{number}'
    return nickname

# Example usage
nickname = generate_random_nickname()
print(nickname)
