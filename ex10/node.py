


class Node:
    """
    class representing doubly linked nodes
    """

    def __init__(self, data=None, next_node=None, prev=None):
        """
        Constructor, initializes the node.
        :data: data for the node (optional)
        :next_node: Next node to be attached to (type Node, optional)
        :prev: Node to be attached to from behind (type Node, optional)
        """
        self.__data = data
        self.__next = next_node
        self.__prev = prev

    def get_data(self):
        """
        :return: node's data
        """
        return self.__data

    def get_next(self):
        """
        :return: next Node
        """
        return self.__next

    def get_prev(self):
        """
        :return: previous Node
        """
        return self.__prev

    def set_data(self, new_data):
        """
        updates the node's data
        :param new_data: new data for the update.
        """
        self.__data = new_data

    def set_next(self, new_next):
        """
        sets the next Node
        :param new_next: new Node to be next to this one
        """
        self.__next = new_next

    def set_prev(self, new_prev):
        """
        sets the previous Node
        :param new_prev: new Node to be previous to this one
        """
        self.__prev = new_prev
