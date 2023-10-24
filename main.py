# Homework 2: A* Pathfinding
# Author: Kenyon Leblanc

import csv  # Used in load_graph for reading csv
import os  # Check directory files
import heapq  # Heap usage

heuristic_data = []


def modify_graph(graph_data):
    """
    Turn edge weights from string to float
    :param graph_data: Loaded graph
    :return: modified graph
    """
    graph = {}
    for node, edges in graph_data.items():
        # Change all weights to floats
        graph[node] = [(to_node, float(weight)) for to_node, weight in edges]
    return graph


def load_graph(filename):
    """
    Load graph from file
    :param filename: Name of file
    :return: Graph object
    """
    graph = {}
    try:
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            # Skip first line
            next(reader)
            for row in reader:
                # Get data from line
                start_node, end_node, edge_cost = map(str, row)
                if start_node not in graph:
                    # Add starting node
                    graph[start_node] = []
                # Add end of edge and edge weight
                graph[start_node].append((end_node, edge_cost))
        return graph

    except Exception as e:
        print(f"{type(e).__name__} occurred: {e}")
        exit(1)


def load_heuristics(filename):
    """
    Load heuristic values from file to global variable
    :param filename: Name of file
    """
    try:
        with open(filename, 'r') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=",")
            # Check variable so that data starts being collected when 'FROM' is found
            check_var = None
            for row in csv_reader:
                if check_var is not None or row[0] == 'FROM':
                    check_var = 1
                    # Add each row as a list
                    heuristic_data.append(row)

    except Exception as e:
        print(f"{type(e).__name__} occurred: {e}")
        exit(1)


def get_heuristic(start_node, end_node):
    """
    Get heuristic value from global variable
    :param start_node: Starting node
    :param end_node: Ending node
    :return: Heuristic value as float or none if not found
    """
    col_num = None
    for index_y, row in enumerate(heuristic_data):
        # Get column number
        if row[0] == 'FROM':
            for index_x, value in enumerate(row):
                if value == end_node:
                    col_num = index_x
                    break
        # Get value where row and column intersect
        if row[0] == start_node:
            if row[col_num] == "":
                return float(heuristic_data[col_num][index_y])
            else:
                return float(row[col_num])
    return None


def astar(graph, start_node, end_node):
    """
    A* algorithm
    :param graph: graph object
    :param start_node: starting node
    :param end_node: ending node
    :return: Path and path cost
    """
    # Initialize queue with start_node and f value of 0
    queue = [(0, start_node)]
    # Store parent node of each node
    parent_nodes = {}

    # Initialize travel values
    g_value = {}
    for node in graph:
        g_value[node] = float('inf')
    # Set starting travel value to 0
    g_value[start_node] = 0

    # Nodes already seen
    visited_nodes = []

    while queue:
        # Get lowest f value
        current_cost, current = heapq.heappop(queue)

        # Check if the node has been visited
        if current in visited_nodes:
            continue
        # Add node to visited
        visited_nodes.append(current)

        if current == end_node:
            path = []
            while current in parent_nodes:
                # build path starting with end
                path.insert(0, current)
                current = parent_nodes[current]
            # insert first node
            path.insert(0, start_node)
            # Return both path and path cost
            return path, g_value[end_node]

        for adjacent_nodes, edge_weight in graph[current]:
            # add edge weight to total travel weight
            total_g = g_value[current] + edge_weight

            if total_g < g_value[adjacent_nodes]:
                # update parent nodes
                parent_nodes[adjacent_nodes] = current
                # Change g value
                g_value[adjacent_nodes] = total_g
                # A* equation: f = g + h
                f_value = total_g + get_heuristic(adjacent_nodes, end_node)
                # Add to queue
                heapq.heappush(queue, (f_value, adjacent_nodes))

    # Nothing found
    return None, float('inf')


def check_starting_node(graph, start_node: str):
    """
    Check to make sure node are valid.
    :param graph: Loaded graph
    :param start_node: User input for starting node
    :return: valid start node
    """
    while start_node not in graph:
        print("Not a valid starting node, please try again.")
        start_node = input("Enter starting node: ")

    return start_node


def check_ending_node(graph, end_node: str):
    """
    Check to make sure node are valid.
    :param graph: Loaded graph
    :param end_node: User input for starting node
    :return: valid end node
    """
    while end_node not in graph:
        print("Not a valid ending node, please try again.")
        end_node = input("Enter ending node: ")

    return end_node


def check_valid_file(file_name):
    """
    Check if file provided by user input is valid
    :param file_name: file name w/ extension
    :return: valid file name
    """
    # Current directory
    directory = os.getcwd()
    # List of files from cwd
    listed_directory = os.listdir(directory)
    # Continue loop until valid file name is given
    while file_name not in listed_directory:
        print("File not found, please try again.")
        file_name = input("Please enter file name with extension: ")

    return file_name


if __name__ == '__main__':
    arrow = " -> "

    # Gather file names and load graph
    file_name = input("Please enter edge weight file name with extension: ")
    file_name = check_valid_file(file_name)
    file_name2 = input("Please enter heuristic file name with extension: ")
    file_name2 = check_valid_file(file_name2)
    print("Loading...")
    graph = load_graph(file_name)
    graph = modify_graph(graph)
    load_heuristics(file_name2)

    # Collect start/end node
    graph_keys = list(graph.keys())
    start = input(f"Enter starting node({graph_keys[0]}-{graph_keys[-1]}): ")
    start = check_starting_node(graph, start)
    end = input(f"Enter ending node({graph_keys[0]}-{graph_keys[-1]}): ")
    end = check_ending_node(graph, end)

    # Perform A* search
    path, cost = astar(graph, start, end)

    # Print findings
    if path is not None:
        result = arrow.join(path)
        print("\nA* Search")
        print(f"({round(cost, 10)}) {result}")
    else:
        print("No Path was found")

    exit(0)
