
class Node:
    def __init__(self, data,weight):
        self.data = data
        self.weight = weight
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def add_new_head(self, data, weight):
        new_node = Node(data, weight)
        new_node.next = self.head
        self.head = new_node

    def linked_list_to_list(self):
        temp = self.head
        list = []
        while temp is not None:
            list.append(temp.data)
            temp = temp.next
        return list

    def linked_list_to_list_with_weight(self):
        temp = self.head
        list = []
        while temp is not None:
            data = [temp.data,temp.weight]
            list.append(data)
            temp = temp.next
        return list

    def delete_node(self, node_data):
        temp = self.head
        if self.head:
            while temp.data == node_data:
                self.head = temp.next
                temp = temp.next
                if not temp:
                    break
            while temp is not None:
                if temp.next is None:
                    break
                elif temp.next.data == node_data:
                    deleted_node = temp.next
                    temp.next = temp.next.next
                    deleted_node.next = None
                else:
                    temp = temp.next
        else:
            return



