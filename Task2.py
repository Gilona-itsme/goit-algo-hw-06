import networkx as nx
from collections import deque 


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

def dfs_search(graph, start, target):
    """Пошук у глибину, що повертає шлях до цілі."""
    stack = [(start, [start])] 
    visited = set()

    while stack:
        (vertex, path) = stack.pop()
        if vertex not in visited:
            if vertex == target:
                return path
            
            visited.add(vertex)
            for neighbor in sorted(graph.neighbors(vertex), reverse=True):
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))
    return None

def bfs_search(graph, start, target):
    """Пошук у ширину, що повертає найкоротший шлях до цілі."""
    queue = deque([(start, [start])]) 
    visited = {start}

    while queue:
        (vertex, path) = queue.popleft() 
        if vertex == target:
            return path

        for neighbor in sorted(graph.neighbors(vertex)):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    return None

start_node = "Політехнічний інститут"
target_node = "Дарниця"

dfs_path = dfs_search(KyivMetro, start_node, target_node)
bfs_path = bfs_search(KyivMetro, start_node, target_node)

print(f"--- Результати пошуку ({start_node} -> {target_node}) ---")
print(f"1. Шлях DFS (Пошук у глибину): {dfs_path}")
print(f"2. Шлях BFS (Пошук у ширину): {bfs_path}")
print(f"Довжина DFS: {len(dfs_path)-1}")
print(f"Довжина BFS: {len(bfs_path)-1}")
