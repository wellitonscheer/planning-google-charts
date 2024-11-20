# Example list of lists
data_list = [
    ['p1_f1', '21420 unidades do produto p1 em quarentena na fábrica f1 por 20 dias', 'new Date(2024, 0, 3)', 'new Date(2024, 0, 23)'],
    ['p2_f2', '5000 unidades do produto p2 em quarentena na fábrica f2 por 15 dias', 'new Date(2024, 1, 10)', 'new Date(2024, 1, 25)'],
]

# Format the list for JavaScript
formatted_data_list = [
    f"[{repr(item[0])}, {repr(item[1])}, {item[2]}, {item[3]}]"
    for item in data_list
]

# Join the formatted data as a single string
result = f"[{', '.join(formatted_data_list)}]"

print(result)