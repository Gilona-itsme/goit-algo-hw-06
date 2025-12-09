import networkx as nx
import matplotlib.pyplot as plt


KyivMetro = nx.Graph()

line_M1 = [ 'Політехнічний інститут', 'Вокзальна', 'Університет', 'Театральна', 'Хрещатик', 'Арсенальна', 'Дніпро', 'Дарниця']
line_M2 = [ 'Почайна', 'Контрактова площа', 'Поштова площа', 
    'Майдан Незалежності', 'Площа Українських героїв', 'Олімпійська', 'Палац "Україна"', 'Либідська']
line_M3 = ['Сирець', 'Дорогожичі', 'Лукянівська', 'Золоті Ворота', 'Палац Спорту', 'Кловська']

KyivMetro.add_nodes_from(line_M1 + line_M2 + line_M3)

def add_line_edges(graph, line_stations):
    nx.add_path(graph, line_stations)

add_line_edges(KyivMetro, line_M1)
add_line_edges(KyivMetro, line_M2)
add_line_edges(KyivMetro, line_M3)


KyivMetro.add_edge('Театральна', 'Золоті Ворота')
KyivMetro.add_edge('Хрещатик', 'Майдан Незалежності')
KyivMetro.add_edge('Площа Українських героїв', 'Палац Спорту')

pos = {}

center_x_coord = 4.2
center_y_coord = -3.0
M1_step = 1.5

# 🔴 М1 — Червона (горизонтальна)
x_offset = center_x_coord - (4 * M1_step)

for i, st in enumerate(line_M1):
    pos[st] = (i * M1_step + x_offset, center_y_coord * 1.3)


# 🔵 М2 — Синя (вертикальна)

for i, st in enumerate(line_M2):
    pos[st] = (center_x_coord + 0.9, center_y_coord - (i - 3) * 2.9)


# 🟢 М3 — Зелена (навхрест через центр)

offset = 0.9
pos['Золоті Ворота'] = (center_x_coord - offset , center_y_coord + offset)
pos['Палац Спорту']  = (center_x_coord - 0.4, center_y_coord - offset * 3.1 )

start_point = (center_x_coord - 5, center_y_coord + 3)   
end_point = (center_x_coord + 2, center_y_coord - 7)     

pos['Сирець'] = start_point
pos['Кловська'] = end_point


intermediate_stations = ['Дорогожичі', 'Лукянівська']
start_coord = pos['Сирець']
end_coord = pos['Золоті Ворота']

for i, st in enumerate(intermediate_stations, start=1):
    x = start_coord[0] + (end_coord[0] - start_coord[0]) * (i / 3)
    y = start_coord[1] + (end_coord[1] - start_coord[1]) * (i / 3)
    pos[st] = (x, y)


edge_colors = []

for u, v in KyivMetro.edges():
    if u in line_M1 and v in line_M1:
        edge_colors.append("red")
    elif u in line_M2 and v in line_M2:
        edge_colors.append("blue")
    elif u in line_M3 and v in line_M3:
        edge_colors.append("green")
    else:
        edge_colors.append("gold")

transfer_nodes = ['Театральна', 'Золоті Ворота',
                  'Хрещатик', 'Майдан Незалежності',
                  'Площа Українських героїв', 'Палац Спорту']

node_colors = [
    "gold" if node in transfer_nodes else "lightgray"
    for node in KyivMetro.nodes()
]

plt.figure(figsize=(16, 8))
nx.draw(
    KyivMetro,
    pos,
    with_labels=True,
    node_color=node_colors,
    edge_color=edge_colors,
    node_size=2000,
    font_size=5,
    font_weight="bold"
)

plt.title("Київський метрополітен — трилінійна схема (Центрована)")
plt.axis("off")
plt.show()

num_nodes = KyivMetro.number_of_nodes()
num_edges = KyivMetro.number_of_edges()
degree_centrality = nx.degree_centrality(KyivMetro)

print(f"\nКількість вершин: {num_nodes}")
print(f"Кількість ребер: {num_edges}")

print("\nСтупінь вершин (Топ-6):")
for node in transfer_nodes:
    print(f"{node}: {degree_centrality[node]:.2f}")

source = 'Дніпро'
target = 'Сирець'
shortest_path = nx.shortest_path(KyivMetro, source=source, target=target)
path_length = len(shortest_path) - 1

print(f"\nНайкоротший шлях від {source} до {target}:")
print(" -> ".join(shortest_path))
print(f"Кількість перегонів (ребер): {path_length}")
