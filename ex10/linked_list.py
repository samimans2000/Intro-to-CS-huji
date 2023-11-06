


class SimpleDoublyLinkedList:
    """
    class representing a VERY minimalistic version of the doubly linked list
    data structure.
    """

    def __init__(self, head=None):
        """
        Constructor. Creates a LinkedList with an optional head (Node).
        :param head: a [doubly linked] Node to be head of the list (optional)
        """
        self.__head = head

    def get_head(self):
        """
        :return: The list's head ([doubly linked] Node)
        """
        return self.__head

    def is_empty(self):
        """
        :return: True if the list is empty, False otherwise
        """
        return self.__head is None

    def add(self, node):
        """
        Adds a single doubly linked node to the start of the list.
        :param node: a doubly linked node to add
        """
        if self.__head is None:
            self.__head = node
        else:
            node.set_next(self.__head)
            self.__head.set_prev(node)
            self.__head = node

    def remove(self, node):
        """
        removes a [doubly linked] node from the list by reference only.
        :param node: node to remove (assumed to be in the list!)
        """
        if node.get_prev() is None:
            # function assumes input node is in list, so it must be the head!
            if node.get_next() is None:
                self.__head = None
            else:
                self.__head = node.get_next()
                self.__head.set_prev(None)
        else:
            if node.get_next() is None:
                node.get_prev().set_next(None)
            else:
                node.get_prev().set_next(node.get_next())
                node.get_next().set_prev(node.get_prev())
