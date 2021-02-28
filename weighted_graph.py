from collections import deque
import json
from linked_list_for_project import Node, LinkedList

def list_of_edges(list_connection):
    edges_list = []
    for i in list_connection:
        for k, v in i.items():
            edges_list.append(k)
    return edges_list

def list_of_dict_to_list_of_list(list_dicts):
    temp = []
    dictlist = []
    for i in list_dicts:
        for k, v in i.items():
            ak = k
            av = v
            temp.append(ak)
            temp.append(av)
            dictlist.append(temp)
            temp = []
    return dictlist


def find_wegiht(edge,list_of_dicts):
    for i in list_of_dict_to_list_of_list(list_of_dicts):
        if i[0] == edge:
            return i[1]


class Graph:

    @staticmethod
    def deserialize(dictionary):
        graph = Graph(dictionary)
        return graph

    def __init__(self, dictionary):
        self.LLW_dict = dictionary
        for vertex in self.LLW_dict.keys():
            linked_list = LinkedList()
            for edge, weight in dictionary[vertex]:
                linked_list.add_new_head(edge, weight)
            self.LLW_dict[vertex] = linked_list

    def get_vertices(self):
        return list(self.LLW_dict.keys())

    def get_edges(self):
        edges = []
        for vertex in self.LLW_dict:
            temp = self.LLW_dict[vertex].head
            while temp is not None:
                if [vertex, temp.data, temp.weight] not in edges and [temp.data, vertex, temp.weight] not in edges :
                    edges.append([vertex, temp.data, temp.weight])
                temp = temp.next
        return edges

#connection looks like: [{"tel-aviv":5.344},{"haifa",6.44}] . to right on report what we did with list of dicts

    def add_vertex(self, vertex, conection):
        for i in list_of_edges(conection):
            if i not in self.LLW_dict.keys():
                print("Error - wrong edge input, graph vertex " + i + " doesn't exist.")
                return
        if vertex in self.LLW_dict.keys():
            edges = list_of_edges(conection)
            added_edges = set(edges) - set(self.LLW_dict[vertex].linked_list_to_list()) - set(vertex)
            for edge in added_edges:
                     self.LLW_dict[vertex].add_new_head(edge,find_wegiht(edge, conection))
                     self.LLW_dict[edge].add_new_head(vertex,find_wegiht(edge, conection))
        else:
            linked_list = LinkedList()
            for edge, weight in list_of_dict_to_list_of_list(conection):
                linked_list.add_new_head(edge,weight)
                self.LLW_dict[edge].add_new_head(vertex,weight)
            self.LLW_dict[vertex] = linked_list


    def delete_vertex(self, del_vertex):
        if del_vertex not in self.LLW_dict.keys():
            print("Cannot delete the Vertex " + del_vertex + " - It doesn't exist in the Graph.")
        else:
            for vertex in self.LLW_dict.keys():
                self.LLW_dict[vertex].delete_node(del_vertex)
            del self.LLW_dict[del_vertex]


    def BFS(self, start, goal):
        results = []
        if start not in self.get_vertices():
            print("vertex "+ start + " doesn't exist in the graph. There are no available paths.")
            return results
        elif goal not in self.get_vertices():
            print("vertex "+ goal + " doesn't exist in the graph. There are no available paths.")
            return results
        else:
            x = (start, [start])
            queue = deque()
            queue.append(x)
            while queue:
                (vertex, path) = queue.popleft()
                vertex_edges = self.LLW_dict[vertex].linked_list_to_list()
                for next in set(vertex_edges) - set(path):
                    if next == goal:
                        results.append(path + [next])
                    else:
                        queue.append((next, path + [next]))
            if results:
                return results
            else:
                print("There are no available paths between the start and goal vertices.")
                return results



    def get_shortest_path(self, source, target):
        paths = self.BFS(source, target)
        sum_weight_final = 0
        for path in paths:
            sum_weight =  0
            for i in path:
                if i == path[0]:
                    last_path = i
                else:
                    temp = self.LLW_dict[i].head
                    while temp :
                        if temp.data == last_path:
                            sum_weight += temp.weight
                            temp = temp.next
                            last_path = i
                        else : temp = temp.next
            if sum_weight < sum_weight_final or sum_weight_final == 0:
                best_path = []
                best_path.append(path)
                sum_weight_final = sum_weight

        return best_path


    def serialize(self):
        graph_hash = self.LLW_dict
        for vertex in graph_hash:
            graph_edges = graph_hash[vertex].linked_list_to_list_with_weight()
            graph_hash[vertex] = graph_edges
        return graph_hash

def load_data(file_name):
    with open(file_name+'.JSON', 'r') as graph_data:
        graph_hash_table = json.load(graph_data)
    graph = Graph.deserialize(graph_hash_table)
    return graph


# Complexity time - O(|V|+|E|)
def save_data(graph, file_name):
    graph_hash = graph.serialize()
    with open(file_name+'.JSON', 'w') as graph_data:
        json.dump(graph_hash, graph_data)



graph = load_data('weighted_graph')
print(graph.get_vertices())
print(graph.get_edges())
graph.add_vertex('LAPID', [{"Jerusalem":6.78}, {"Rehovot":3.298}])
graph.delete_vertex("Tel-Aviv")
print(graph.BFS("Netanya","Zefat"))
print(graph.get_shortest_path("Netanya","Zefat"))
save_data(graph,'new.json')




