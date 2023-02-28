home_team = "Manchester United"
options = ["Man United", "Man City"]

if len(home_team.split(" ")) > 1:
    home_team = home_team.split(" ")

perfect_match = None  # Initialize a variable to store the perfect match

for home_word in home_team:
    for option in options:
        if home_word in option.split(" "):
            perfect_match = option  # Store the perfect match
            break  # Exit the inner loop if a match is found
    if perfect_match:  # Exit the outer loop if a perfect match is found
        break

if perfect_match:
    home_team = perfect_match  # Update the home_team variable with the perfect match

print(home_team)  # Print the updated value of home_team
