"""
Assignment 2: Quadtree Compression

=== CSC148 Winter 2021 ===
Department of Mathematical and Computational Sciences,
University of Toronto Mississauga

=== Module Description ===
This module contains the test suite
"""

import pytest
from a2tree import QuadTreeNode, QuadTreeNodeEmpty, QuadTreeNodeLeaf, QuadTree,\
    QuadTreeNodeInternal

"""
Test cases
"""


def test_split_quadrants_1():
    """
    This test case tests the output of split_quadrants a balanced input,
    where the divide is at the center both vertical and horizontal
    """
    example = QuadTree()
    lst = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
    got = example._split_quadrants(lst)
    expected = [[[1, 2], [5, 6]], [[3, 4], [7, 8]], [[9, 10], [13, 14]], [[11, 12], [15, 16]]]
    assert got == expected


def test_split_quadrants_2():
    """
    This test case tests the output of split_quadrants an unbalanced input,
    where the divide is not at the center both vertical and horizontal
    """
    example = QuadTree()
    lst = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
    got = example._split_quadrants(lst)
    expected = [[[1, 2]], [[3, 4]], [[5, 6], [9, 10]], [[7, 8], [11, 12]]]
    assert got == expected


def test_split_quadrants_3():
    """
    This test case tests the output of split_quadrants an unbalanced input,
    where the divide is at the center both vertical and horizontal
    This deals with empty leftover splits
    """
    example = QuadTree()
    lst = [[1, 2, 3]]
    got = example._split_quadrants(lst)
    expected = [[[]], [[]], [[1]], [[2, 3]]]
    assert got == expected


def test_restore_from_preorder_1():
    """
    This tests the restore from preorder method using a given preorder list.
    It tests to make sure the generated quadtreeInternal is made correctly.
    Start index at 0
    """
    example = QuadTreeNodeInternal()
    lst = ['', 'E', '4', '', '5', '6', '7', 'E', 'E']
    got = example.restore_from_preorder(lst, 0)
    print(example.preorder())
    expected = 9

    assert got == expected
    assert example.children[1].value == 4
    assert example.children[2].children[0].value == 5


def test_restore_from_preorder_2():
    """
    This tests the restore from preorder method using a given preorder list.
    It tests to make sure the generated quadtreeInternal is made correctly.
    This tests with a new start index
    """
    example = QuadTreeNodeInternal()
    lst = ['', 'E', '4', '', '5', '5', '5', 'E', 'E']
    got = example.restore_from_preorder(lst, 3)
    print(example.preorder())
    expected = 5
    assert got == expected


def test_restore_from_preorder_3():
    """
    This tests the restore from preorder method using a given preorder list.
    It tests to make sure the generated quadtreeInternal is made correctly.
    This tests with a greater length preorder
    """
    example = QuadTreeNodeInternal()
    lst = ['', 'E', '3', '', '1', '2', '3', '4', '', 'E', '8', '9', 'E']
    got = example.restore_from_preorder(lst, 0)
    print(example.preorder())
    expected = 13
    assert got == expected
    assert example.children[1].value == 3
    assert example.children[2].children[1].value == 2
    assert example.children[2].children[3].value == 4
    assert example.children[3].children[1].value == 8
    assert example.children[3].children[2].value == 9


if __name__ == '__main__':

    pytest.main(['a2test_student.py'])
