#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
This module contains:
    Logger: 
        A modified logger class inherited from logging.Logger.
    memory_usage(): 
        A function that returns the memory used.
    nlargest_dict: 
        A function to find n largest attributes in dictionary according to
        a specified attribute and return the list of those keys and values.
    nsmallest_dict: 
        A function to find n largest attributes in dictionary according to
        a specified attribute and return the list of those keys and values.
    LinkedList: 
        A class for linked lists sorted in ascending order.
    Node: 
        A class for node in linked lists.
Author: Yuan Huang
"""

import logging
import os
import sys
import heapq
import unittest

class Logger(logging.Logger):
    """
    A modified logger class inherited from logging.Logger.
    """
    def __init__(self, workspace):
        """
        Initialize the logger.
        Assign a stream_handler and a file_handler to the logger.
        The log file is writen in the specified workspace.
        Args:
            workspace: the directory to put the log file.
        """
        super(Logger, self).__init__(__name__)
        self.setLevel(logging.INFO)

        self.stream_handler = logging.StreamHandler(sys.stdout)
        self.file_handler = logging.FileHandler(os.path.join(workspace, 'process.log'))

        self.stream_handler.setLevel(logging.INFO)
        self.file_handler.setLevel(logging.INFO)

        formatter = logging.Formatter(fmt="[%(asctime)s][%(levelname)s]:\n%(message)s",
                                      datefmt='%y/%m/%d %H:%M:%S')

        self.stream_handler.setFormatter(formatter)
        self.file_handler.setFormatter(formatter)

        self.addHandler(self.stream_handler)
        self.addHandler(self.file_handler)

    def Abort(self, msg):
        """
        Print out the error msg to the stream and log file and raise an AssertionError.
        Args:
            msg(str): the error message to print out.
        Raises:
            AssertionError
        """
        self.error(msg)
        raise AssertionError


def memory_usage():
    """
    Return the memory used in the job.
    Returns:
        mem(float): the memory used in units of MB.
    """
    import subprocess
    out = subprocess.Popen(['ps', 'v', '-p', str(os.getpid())],
                           stdout=subprocess.PIPE).communicate()[0].split(b'\n')
    vsz_index = out[0].split().index(b'RSS')
    mem = float(out[1].split()[vsz_index]) / 1024
    return mem

def nlargest_dict(n_top, dictionary, axis):
    """
    Find n largest entries in a dictionary, the sort axis is specified as axis.
    Args:
        n_top(int): the number of top entries
        dict(dict): the data in dictionary
        axis(int): the index to sort.
    Returns:
        top_keys(list): The top n keys in a list.
        top_values(list): The top n values in a list.
    """
    top_keys = heapq.nlargest(n_top, dictionary, key = lambda x: dictionary[x][axis])
    return  top_keys, [dictionary[key][axis] for key in top_keys]

def nsmallest_dict(n_bottom, dictionary, axis):
    """
    Find n smallest entries in a dictionary, the sort axis is specified as axis.
    Args:
        n_bottom(int): the number of least entries
        dict(dict): the data in dictionary
        axis(int): the index to sort.
    Returns:
        bottom_keys(list): The n keys at the bottom in a list.
        bottom_values(list): The n values at the bottom in a list.
    """
    bottom_keys = heapq.nsmallest(n_bottom, dictionary, key=lambda x: (dictionary[x][axis], x))
    return  bottom_keys, [dictionary[key][axis] for key in bottom_keys]

class Node:
    """
    The Node class with pointer "next" and "data".
    """

    def __init__(self, data):
        """Initialize a node with data.
        Args:
            data(any object): the data of the new node.
        """
        self.data = data
        self.next = None

    def replace_data(self, new_data):
        """Replace the data on a node.
        Args:
            new_data(data object): new data to put in node.
        """
        self.data = new_data

class LinkedList:
    """
    LinkedList: a ascending ordered linked list with a maximum length.
    """

    def __init__(self, max_length):
        """
        Initialize a linked list with fixed length.
        Args:
            length(int): the fixed maximum length of the linked list.
        """
        self.head = None
        self.length = 0
        self.max_length = max_length

    def sorted_insert_data(self, new_data):
        """
        Insert a new data into the sorted linked list.
        The linked list is already in increasing order.
        Args:
            new_data(data object): the data of the new node that needs to be inserted.
        Returns:
            new_node(Node): the new node in the list, the linked list remains sorted
            after the insertion.
        """
        new_node = Node(new_data)
        self.sorted_insert_node(new_node)
        return new_node

    def sorted_insert_node(self, new_node):
        """
        Insert a new node into the sorted linked list.
        The linked list is already in increasing order.
        Args:
            new_node(Node): the new node needs to be inserted.
        Returns:
            new_node(Node): the node in the list, the linked list remains sorted
            after the insertion.
        """
        # Special case for the empty linked list
        if self.head is None:
            new_node.next = self.head
            self.head = new_node

        # Special case for head at end
        elif self.head.data >= new_node.data:
            new_node.next = self.head
            self.head = new_node

        else:
            # Locate the node before the point of insertion
            current = self.head
            while current.next is not None and current.next.data < new_node.data:
                current = current.next

            new_node.next = current.next
            current.next = new_node

        # Increase the length of the linked list by 1.
        self.length += 1
        # When the length exceeds the maximum length, remove the node with smallest value (head).
        if self.length > self.max_length:
            self.remove(self.head)
        return new_node

    def remove(self, node):
        """Remove a node in the linked list.
        Args:
            node(Node): The node to be removed.
        """
        # Locate the node before the node that needs to be removed.
        current = self.head
        prev = None
        while current is not node and current is not None:
            prev = current
            current = current.next

        # Remove the node and assign its next to prev.next
        if prev is not None:
            prev.next = node.next
        else:
            # Special case when the node to be removed is the head
            self.head = node.next

        # Decrease the length of the linked list by 1.
        self.length -= 1

    def sort_node(self, node_to_sort):
        """Put one node in the right place of the sorted linked list (except for this one node).
        The current linked list is in sorted order except for one node: node_to_sort. This function
        put this node in the right place without changing the relative positions of other nodes.
        Args:
            node_to_sort(Node): the node that needs to be sorted.
        Returns:
            node_to_sort(Node): the node in the right position.
        """

        # Remove the node to be sorted, the linked list becomes a sorted list with n-1 nodes.
        self.remove(node_to_sort)
        # Insert the node into the sorted linked list in its right position.
        node_to_sort = self.sorted_insert_node(node_to_sort)
        return node_to_sort

    def min(self):
        """
        Get the minimum value of the linked list.
        Returns:
            minimum_data(data object): the data of the head node (the linked list is in
            ascending order).
        """
        return self.head.data

    def get_list(self, order="ascend"):
        """
        Get a list of data in the linked list in ascending order.
        Returns:
            return_list(list): a list of all data in each nodes of the linked list, the list is
            ordered according to its data values.
        """
        data_list = []
        current = self.head
        while current is not None:
            data_list.append(current.data)
            current = current.next
        return_list = data_list
        if order == "descend":
            return_list = []
            for i in range(len(data_list))[::-1]:
                return_list.append(data_list[i])
        return return_list

class Heap:
    """
    Heap: a min-heaps is implemented
    """

    def __init__(self, max_length):
        """
        Initialize a min-heaps with fixed length.
        Args:
            length(int): the fixed maximum length of the sorted list.
        """
        self.__max_length = max_length
        self.__minheap = []
        self.__length = 0

    def push(self, new_data):
        """
        Insert a new data into the min-heap.
        Args:
            new_data(data object): the data of the new node that needs to be inserted.
        """
        if self.__length < self.__max_length:
            heapq.heappush(self.__minheap, new_data)
            self.__length += 1
        else:
            heapq.heappushpop(self.__minheap, new_data)

    def length(self):
        """
        Get the length of the list.
        Returns:
            length(int): the length of the list
        """
        return self.__length

    def min(self):
        """
        Get the minimum value of the list.
        Returns:
            minimum_data(data object): the smallest data in the list
        """
        return self.__minheap[0]

    def get(self, order="descend"):
        """
        Get a list of data in the list in descending order.
        Returns:
            return_list(list): the sorted list in descending order
        """
        if order == "descend":
            return sorted(self.__minheap, reverse=True)
        elif order == "ascend":
            return sorted(self.__minheap)
        else:
            raise NotImplementedError("sorting order {0} is not implemented.".format(order))

class TestAlgorithms(unittest.TestCase):
    """The unittest class for nlargest_dict and linked list."""
    def setUp(self):
        """Set up for the test cases."""
        self.dict = {"A": [15, 300], "B":[15, 200], "C": [1, 3000]}

        
        #unit test for the heap
        container=Heap(10)
        container.push(5)
        container.push(1)
        container.push(3)
        container.push(2)
        container.push(15)
        container.push(12)
        container.push(32)
        container.push(24)
        container.push(41)
        container.push(4)
        container.push(2)
        self.container=container


    def test_heap(self):
        """Test for replace data to a node and reinsert it in linked list."""
        self.assertEqual(self.container.get("descend"),[41,32,24,15,12,5,4,3,2,2])

        self.container.push(44)
        self.assertEqual(self.container.get("ascend"),[2,3,4,5,12,15,24,32,41,44])

    def test_nlargest_dict(self):
        """Test for the nlargest functionality for a dictionary."""
        keys, values = nlargest_dict(2, self.dict, 0)
        self.assertEqual(keys[0], "A")
        self.assertEqual(values[0], 15)
        self.assertEqual(keys[1], "B")
        self.assertEqual(values[1], 15)

        keys, values = nlargest_dict(2, self.dict, 1)
        self.assertEqual(keys[0], "C")
        self.assertEqual(values[0], 3000)
        self.assertEqual(keys[1], "A")
        self.assertEqual(values[1], 300)

if __name__ == '__main__':
    unittest.main()
