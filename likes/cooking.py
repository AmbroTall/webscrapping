import random
import string


def generate_random_name():
    # Generate a random prefix using a combination of letters
    prefix = ''.join(random.choice(string.ascii_lowercase) for _ in range(3))

    # Generate a random suffix using a combination of letters and digits
    suffix = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(3))

    # Combine the prefix and suffix to create the random name
    random_name = prefix + suffix

    return random_name


# Test the function
if __name__ == "__main__":
    for _ in range(10):  # Generate 10 random names as an example
        print(generate_random_name())
