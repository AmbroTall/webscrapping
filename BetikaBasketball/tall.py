data = [
	{'over_under': 'Over 39.5', 'odd_value': '1.54'},
	{'over_under': 'Over 40.5', 'odd_value': '1.78'},
	{'over_under': 'Over 41.5', 'odd_value': '2.09'},
	{'over_under': 'Over 42.5', 'odd_value': '2.51'},
	{'over_under': 'Under 39.5', 'odd_value': '2.21'},
	{'over_under': 'Under 40.5', 'odd_value': '1.86'},
	{'over_under': 'Under 41.5', 'odd_value': '1.61'},
	{'over_under': 'Under 42.5', 'odd_value': '1.43'}
]

over_values = [d for d in data if d['over_under'].startswith('Over')]

if over_values:
	lowest_over = min(over_values, key=lambda x: float(x['over_under'].split()[1]))
	print(lowest_over)
	print(lowest_over)
else:
	print("No 'Over' values found.")
