import networkx as nx
import pandas as pd
import heapq


KyivMetro_Weighted = nx.Graph()

line_M1 = ['Політехнічний інститут', 'Вокзальна', 'Університет',
           'Театральна', 'Хрещатик', 'Арсенальна', 'Дніпро', 'Дарниця']

line_M2 = ['Почайна', 'Контрактова площа', 'Поштова площа',
           'Майдан Незалежності', 'Площа Українських героїв',
           'Олімпійська', 'Палац "Україна"', 'Либідська']

line_M3 = ['Сирець', 'Дорогожичі', 'Лукянівська',
           'Золоті Ворота', 'Палац Спорту', 'Кловська']

KyivMetro_Weighted.add_nodes_from(line_M1 + line_M2 + line_M3)


def add_weighted_path(graph, line, weight=2.5):
    for i in range(len(line) - 1):
        graph.add_edge(line[i], line[i+1], weight=weight)


# додавання ваг до ліній
add_weighted_path(KyivMetro_Weighted, line_M1)
add_weighted_path(KyivMetro_Weighted, line_M2)
add_weighted_path(KyivMetro_Weighted, line_M3)

# індивідуальні ваги
KyivMetro_Weighted.add_edge('Арсенальна', 'Дніпро', weight=3.5)
KyivMetro_Weighted.add_edge('Дніпро', 'Дарниця', weight=3.5)

# пересадки
transfer = 5.0
KyivMetro_Weighted.add_edge('Театральна', 'Золоті Ворота', weight=transfer)
KyivMetro_Weighted.add_edge('Хрещатик', 'Майдан Незалежності', weight=transfer)
KyivMetro_Weighted.add_edge('Площа Українських героїв', 'Палац Спорту', weight=transfer)

print("Граф зі зваженими ребрами створено.")


def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph.nodes()}
    distances[start] = 0

    pq = [(0, start)]
    visited = set()

    while pq:
        current_dist, node = heapq.heappop(pq)

        if node in visited:
            continue
        visited.add(node)

        for neighbor in graph[node]:
            w = graph[node][neighbor]['weight']
            new_dist = current_dist + w

            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heapq.heappush(pq, (new_dist, neighbor))

    return distances

start = "Політехнічний інститут"
target = "Либідська"

distances = dijkstra(KyivMetro_Weighted, start)

print(f"\nНайкоротша відстань ({start} → {target}): {distances[target]:.1f} хв")



all_distances = {}

for node in KyivMetro_Weighted.nodes():
    all_distances[node] = dijkstra(KyivMetro_Weighted, node)

df = pd.DataFrame(all_distances)

print("\nМатриця найкоротших відстаней (у хвилинах):")
print(df.round(1))