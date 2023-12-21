import random

def random_gender():
    genders = ["male", "female"]
    return random.choice(genders)

# Test the function
if __name__ == "__main__":
    for _ in range(10):  # Generate 10 random genders as an example
        print(random_gender())
