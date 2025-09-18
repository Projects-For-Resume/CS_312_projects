def find_shortest_path_with_heap(
        graph: dict[int, dict[int, float]],
        source: int,
        target: int
) -> tuple[list[int], float]:
    """
    Find the shortest (least-cost) path from `source` to `target` in `graph`
    using the heap-based algorithm.

    Return:
        - the list of nodes (including `source` and `target`)
        - the cost of the path
    """
    heap_priority_queue:list = [None]
    node_index_dict:dict[int, int] = {}
    dist:dict[int, float] = {}
    prev: dict[int, int|None] = {}

    for nd in graph.keys():
        if nd == source:
            dist[nd] = 0
            heap_priority_queue = heap_insert(heap_priority_queue, (nd, 0), node_index_dict)
            prev[nd] = None
        else:
            dist[nd] = float('inf')
            prev[nd] = None 
    
    while len(heap_priority_queue) > 0:  
        smallest_node_info = delete_min_heap(heap_priority_queue, dist, node_index_dict)
        name_smallest_node = smallest_node_info[0]

        if name_smallest_node == target:
            break

        for neighbor, weight in graph[name_smallest_node].items():
            dist_to_current_node = dist[name_smallest_node]
            new_distance = dist_to_current_node + weight

            old_distance = dist[neighbor]

            if new_distance < old_distance:
                prev[neighbor] = name_smallest_node
                dist[neighbor] = new_distance
                decrease_key_heap(heap_priority_queue, (neighbor, new_distance), node_index_dict)


    path:list = []
    path_node:int|None = target

    while path_node is not None:
        path.append(path_node)
        path_node = prev[path_node]
    
    path.reverse()

    if dist[target] == float('inf'):

        return [], float('inf')

    return path, dist[target]

def heap_insert(heap_priority_queue: list[tuple[int, float]], value: tuple[int, float], node_index_dict: dict[int, int]) -> list:
    heap_priority_queue.append(value)
    current_index = len(heap_priority_queue) - 1
    node_index_dict[value[0]] = current_index
    
    while current_index > 1:
        parent_index = current_index // 2
        if heap_priority_queue[parent_index][1] > heap_priority_queue[current_index][1]:
            
            heap_priority_queue[current_index], heap_priority_queue[parent_index] = (
                heap_priority_queue[parent_index],
                heap_priority_queue[current_index],
            )
            
            node_index_dict[heap_priority_queue[current_index][0]] = current_index
            node_index_dict[heap_priority_queue[parent_index][0]] = parent_index

            current_index = parent_index
        else:
            break

    return heap_priority_queue

def delete_min_heap(heap_prioity_queue:list[tuple[int, float]], dist:dict[int, float], node_index_dict:dict[int, int]):
    if len(heap_prioity_queue) == 1:
        return None

    value = heap_prioity_queue[1]

    last_elem = heap_prioity_queue.pop()

    node_index_dict[last_elem[0]] = 1

    if value[0] in node_index_dict:
        node_index_dict.pop(value[0])


    if (len(heap_prioity_queue) < 2):
        return value
    
    heap_prioity_queue[1] = last_elem

    current_index = 1

    while current_index * 2 < len(heap_prioity_queue):
        right_child_index = current_index * 2 + 1
        left_child_index = current_index*2

        if right_child_index < len(heap_prioity_queue) and heap_prioity_queue[right_child_index][1] < heap_prioity_queue[left_child_index][1]:
            smaller_child_index = right_child_index
            
        else:
            smaller_child_index = left_child_index

        if heap_prioity_queue[current_index][1] > heap_prioity_queue[smaller_child_index][1]:
            node_index_dict[heap_prioity_queue[current_index][0]] = smaller_child_index
            node_index_dict[heap_prioity_queue[smaller_child_index][0]] = current_index
            heap_prioity_queue[current_index], heap_prioity_queue[smaller_child_index] = (heap_prioity_queue[smaller_child_index], heap_prioity_queue[current_index])
            current_index = smaller_child_index
           
        else:
            break
        
    return value


def decrease_key_heap(heap_priority_queue: list[tuple[int, float]], value: tuple[int, float], node_index_dict: dict[int, int]) -> None:
    if value[0] in node_index_dict:
        current_index = node_index_dict[value[0]]
        heap_priority_queue[current_index] = value

        while current_index > 1:
            parent_index = current_index // 2
            if heap_priority_queue[parent_index][1] > heap_priority_queue[current_index][1]:
                
                heap_priority_queue[current_index], heap_priority_queue[parent_index] = (
                    heap_priority_queue[parent_index],
                    heap_priority_queue[current_index],
                )
                
                node_index_dict[heap_priority_queue[current_index][0]] = current_index
                node_index_dict[heap_priority_queue[parent_index][0]] = parent_index

                current_index = parent_index
            else:
                break
    else:
        heap_insert(heap_priority_queue, value, node_index_dict)

def find_shortest_path_with_array(
        graph: dict[int, dict[int, float]],
        source: int,
        target: int
) -> tuple[list[int], float]:
    """
    Find the shortest (least-cost) path from `source` to `target` in `graph`
    using the array-based (linear lookup) algorithm.

    Return:
        - the list of nodes (including `source` and `target`)
        - the cost of the path
    """
    dist: dict[int, float] = {}
    prev: dict[int, int | None] = {}
    priority_queue:dict[int,tuple] = {}
    for node in graph.keys():
        if node == source:
            dist[node] = 0
            prev[node] = None
            priority_queue[node] = (0, None)  #(Node ID, distance, previous)
        else:
            dist[node] = float('inf')
            prev[node] = None
            priority_queue[node] = (float('inf'), None)

        
    while priority_queue:
        smallest_key, smallest_distance_info = delete_min_array(priority_queue)

        if smallest_key == target:
            break

        for neighbor, weight in graph[smallest_key].items():
            if neighbor in priority_queue: #has the node that I'm looking at already been processed?
                new_distance = smallest_distance_info[0] + weight
                if new_distance < priority_queue[neighbor][0]:  # Found a shorter path
                    dist[neighbor] = new_distance # Update dist and prev
                    prev[neighbor] = smallest_key
                    priority_queue[neighbor] = (new_distance, smallest_key)

    path:list = []
    path_node:int|None = target
    while path_node is not None:
        path.append(path_node)
        path_node = prev[path_node]
    
    path.reverse()

    if dist[target] == float('inf'):
        return [], float('inf')

    return path, dist[target]

def delete_min_array(priority_queue: dict[int, tuple]) -> tuple[int, tuple]:
    smallest_key = None
    smallest_distance = (float('inf'), None)

    for node, distance in priority_queue.items():
        if distance[0] < smallest_distance[0]:
            smallest_key = node
            smallest_distance = distance

    if smallest_key is not None:
        del priority_queue[smallest_key]
        return (smallest_key, smallest_distance)
    
    raise ValueError("Something went wrong in 'delete_min' for the array")


    