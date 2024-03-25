"""
Assignment 2: Quadtree Compression

=== CSC148 Winter 2021 ===
Department of Mathematical and Computational Sciences,
University of Toronto Mississauga

=== Module Description ===
This module contains classes implementing the quadtree.
"""

from __future__ import annotations
import math
from typing import List, Tuple, Optional
from copy import deepcopy
# No other imports allowed


def mean_and_count(matrix: List[List[int]]) -> Tuple[float, int]:
    """
    Returns the average of the values in a 2D list
    Also returns the number of values in the list
    """
    total = 0
    count = 0
    for row in matrix:
        for v in row:
            total += v
            count += 1
    return total / count, count


def standard_deviation_and_mean(matrix: List[List[int]]) -> Tuple[float, float]:
    """
    Return the standard deviation and mean of the values in <matrix>

    https://en.wikipedia.org/wiki/Root-mean-square_deviation

    Note that the returned average is a float.
    It may need to be rounded to int when used.
    """
    avg, count = mean_and_count(matrix)
    total_square_error = 0
    for row in matrix:
        for v in row:
            total_square_error += ((v - avg) ** 2)
    return math.sqrt(total_square_error / count), avg


class QuadTreeNode:
    """
    Base class for a node in a quad tree
    """

    def __init__(self) -> None:
        pass

    def tree_size(self) -> int:
        raise NotImplementedError

    def convert_to_pixels(self, width: int, height: int) -> List[List[int]]:
        raise NotImplementedError

    def preorder(self) -> str:
        raise NotImplementedError

    def _mirror_helper(self) -> None:
        raise NotImplementedError


class QuadTreeNodeEmpty(QuadTreeNode):
    """
    An empty node represents an area with no pixels included
    """

    def __init__(self) -> None:
        super().__init__()

    def tree_size(self) -> int:
        """
        Note: An empty node still counts as 1 node in the quad tree
        """
        return 1

    def convert_to_pixels(self, width: int, height: int) -> List[List[int]]:
        """
        Convert to a properly formatted empty list
        """
        # Note: Normally, this method should return an empty list or a list of
        # empty lists. However, when the tree is mirrored, this returned list
        # might not be empty and may contain the value 255 in it. This will
        # cause the decompressed image to have unexpected white pixels.
        # You may ignore this caveat for the purpose of this assignment.
        return [[255] * width for _ in range(height)]

    def preorder(self) -> str:
        """
        The letter E represents an empty node
        """
        return 'E'

    def _mirror_helper(self) -> None:
        return


class QuadTreeNodeLeaf(QuadTreeNode):
    """
    A leaf node in the quad tree could be a single pixel or an area in which
    all pixels have the same colour (indicated by self.value).
    """

    value: int  # the colour value of the node

    def __init__(self, value: int) -> None:
        super().__init__()
        assert isinstance(value, int)
        self.value = value

    def tree_size(self) -> int:
        """
        Return the size of the subtree rooted at this node
        """
        return 1

    def convert_to_pixels(self, width: int, height: int) -> List[List[int]]:
        """
        Return the pixels represented by this node as a 2D list

        >>> sample_leaf = QuadTreeNodeLeaf(5)
        >>> sample_leaf.convert_to_pixels(2, 2)
        [[5, 5], [5, 5]]
        >>> sample_leaf.convert_to_pixels(2, 3)
        [[5, 5], [5, 5], [5, 5]]
        >>> sample_leaf.convert_to_pixels(3, 3)
        [[5, 5, 5], [5, 5, 5], [5, 5, 5]]
        """
        lst = []
        for x in range(height):
            inner_lst = []
            for y in range(width):
                inner_lst.append(self.value)
            lst.append(inner_lst)

        return lst

    def preorder(self) -> str:
        """
        A leaf node is represented by an integer value in the preorder string
        """
        return str(self.value)

    def _mirror_helper(self) -> None:
        return


class QuadTreeNodeInternal(QuadTreeNode):
    """
    An internal node is a non-leaf node, which represents an area that will be
    further divided into quadrants (self.children).

    The four quadrants must be ordered in the following way in self.children:
    top-left, top-right, bottom-left, bottom-right

    (List indices increase from left to right, top to bottom)

    Representation Invariant:
    - len(self.children) == 4
    """
    children: List[Optional[QuadTreeNode]]

    def __init__(self) -> None:
        """
        Order of children: top left, top right, bottom left, bottom right
        """
        super().__init__()

        # Length of self.children must be always 4.
        self.children = [None, None, None, None]

    def tree_size(self) -> int:
        """
        The size of the subtree rooted at this node.

        This method returns the number of nodes that are in this subtree,
        including the root node.
        """
        count = 1
        count += self.children[0].tree_size()
        count += self.children[1].tree_size()
        count += self.children[2].tree_size()
        count += self.children[3].tree_size()
        return count

    def convert_to_pixels(self, width: int, height: int) -> List[List[int]]:
        """
        Return the pixels represented by this node as a 2D list.

        You'll need to recursively get the pixels for the quadrants and
        combine them together.

        Make sure you get the sizes (width/height) of the quadrants correct!
        Read the docstring for split_quadrants() for more info.

        [ [ 1, 2, 2, 2,2 ,2...], [ ], [ ], [ ] ]
        """

        tl = self.children[0].convert_to_pixels(width//2, height//2)
        tr = self.children[1].convert_to_pixels(width - width//2, (height//2))
        bl = self.children[2].convert_to_pixels(width//2, (height - height//2))
        br = self.children[3].convert_to_pixels(width - width//2, (height - height//2))

        total = []
        top = []
        for i in range(len(tl)):
            top = []
            top.extend(tl[i])
            top.extend(tr[i])
            total.append(top)

        bottom = []
        for j in range(len(br)):
            bottom = []
            bottom.extend(bl[j])
            bottom.extend(br[j])
            total.append(bottom)
        return total

    def preorder(self) -> str:
        """
        Return a string representing the preorder traversal or the tree rooted
        at this node. See the docstring of the preorder() method in the
        QuadTree class for more details.

        An internal node is represented by an empty string in the preorder
        string.
        """

        order = ','
        order += self.children[0].preorder() + ','
        order += self.children[1].preorder() + ','
        order += self.children[2].preorder() + ','
        order += self.children[3].preorder()
        return order

    def restore_from_preorder(self, lst: List[str], start: int) -> int:
        """
        Restore subtree from preorder list <lst>, starting at index <start>
        Return the number of entries used in the list to restore this subtree
        ['', 'E', '4', '', '4', '4', '4', 'E', 'E']

        >>> example = QuadTreeNodeInternal()
        >>> example.restore_from_preorder(['', 'E', '4', '', '4', '4', '4', 'E', 'E'], 0)
        >>> print(example.children[2].children[0].value)
        """

        # This assert will help you find errors.
        # Since this is an internal node, the first entry to restore should
        # be an empty string
        assert lst[start] == ''

        counter = 1
        child = 0
        for i in range(1, 5):
            if lst[start + counter] == 'E':
                self.children[child] = QuadTreeNodeEmpty()
                counter += 1
            elif lst[start + counter] != '':
                self.children[child] = QuadTreeNodeLeaf(int(lst[start + counter]))
                counter += 1
            else:
                x = QuadTreeNodeInternal()
                num = x.restore_from_preorder(lst, (start + counter))
                self.children[child] = x
                counter += num
            child += 1
        return counter

    def mirror(self) -> None:
        """
        Mirror the bottom half of the image represented by this tree over
        the top half

        Example:
            Original Image
            1 2
            3 4

            Mirrored Image
            3 4 (this row is flipped upside down)
            3 4

        See the assignment handout for a visual example.
        """
        left = deepcopy(self.children[0])
        right = deepcopy(self.children[1])

        if isinstance(left, QuadTreeNodeInternal):
            left._mirror_helper()

        if isinstance(right, QuadTreeNodeInternal):
            right._mirror_helper()

        self.children[2] = left
        self.children[3] = right

    def _mirror_helper(self) -> None:
        """
        Flip the tree around
        """
        self.children[0]._mirror_helper()
        self.children[1]._mirror_helper()
        self.children[2]._mirror_helper()
        self.children[3]._mirror_helper()

        self.children[0], self.children[2] = self.children[2], self.children[0]
        self.children[1], self.children[3] = self.children[3], self.children[1]


class QuadTree:
    """
    The class for the overall quadtree
    """

    loss_level: float
    height: int
    width: int
    root: Optional[QuadTreeNode]  # safe to assume root is an internal node

    def __init__(self, loss_level: int = 0) -> None:
        """
        Precondition: the size of <pixels> is at least 1x1
        """
        self.loss_level = float(loss_level)
        self.height = -1
        self.width = -1
        self.root = None

    def build_quad_tree(self, pixels: List[List[int]],
                        mirror: bool = False) -> None:
        """
        Build a quad tree representing all pixels in <pixels>
        and assign its root to self.root

        <mirror> indicates whether the compressed image should be mirrored.
        See the assignment handout for examples of how mirroring works.
        """
        # print('building_quad_tree...')
        self.height = len(pixels)
        self.width = len(pixels[0])
        self.root = self._build_tree_helper(pixels)
        if mirror:
            self.root.mirror()
        return

    def _build_tree_helper(self, pixels: List[List[int]]) -> QuadTreeNode:
        """
        Build a quad tree representing all pixels in <pixels>
        and return the root

        Note that self.loss_level should affect the building of the tree.
        This method is where the compression happens.

        IMPORTANT: the condition for compressing a quadrant is the standard
        deviation being __LESS THAN OR EQUAL TO__ the loss level. You must
        implement this condition exactly; otherwise, you could fail some
        test cases unexpectedly.
        >>> example = QuadTree(2)
        >>> example.build_quad_tree([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
        >>> print(example.preorder())
        """
        quadrents = self._split_quadrants(pixels)

        root = QuadTreeNodeInternal()

        for index, sublist in enumerate(quadrents):

            if [] in sublist:
                root.children[index] = QuadTreeNodeEmpty()
            else:

                value = standard_deviation_and_mean(sublist)[0]

                if value <= self.loss_level:
                    root.children[index] = QuadTreeNodeLeaf(round(mean_and_count(sublist)[0]))
                else:
                    sub = QuadTree(round(self.loss_level))
                    new_root = sub._build_tree_helper(sublist)
                    root.children[index] = new_root

        return root

    @staticmethod
    def _split_quadrants(pixels: List[List[int]]) -> List[List[List[int]]]:
        """
        Precondition: size of <pixels> is at least 1x1
        Returns a list of four lists of lists, correspoding to the quadrants in
        the following order: top-left, top-right, bottom-left, bottom-right

        IMPORTANT: when dividing an odd number of entries, the smaller half
        must be the left half or the top half. See the assignment handout
        for more detail.

        Postcondition: the size of the returned list must be 4

        >>> example = QuadTree(0)
        >>> example._split_quadrants([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        [[[1]], [[2, 3]], [[4], [7]], [[5, 6], [8, 9]]]
        """
        x = len(pixels)//2
        y = len(pixels[0])//2

        top = []
        bottom = []
        tl = []
        tr = []
        bl = []
        br = []

        if x >= len(pixels):
            top = []
            bottom = pixels[:]
        else:
            top = pixels[:x]
            bottom = pixels[x:]

        if len(top) == 0:
            tl = [[]]
            tr = [[]]

        for value in top:
            if y >= len(value):
                tr.append(value[:])
            else:
                tl.append(value[:y])
                tr.append(value[y:])

        for value in bottom:
            if y >= len(value):
                br.append(value[:])
            else:
                bl.append(value[:y])
                br.append(value[y:])

        return [tl, tr, bl, br]

    def tree_size(self) -> int:
        """
        Return the number of nodes in the tree, including all Empty, Leaf, and
        Internal nodes.
        """
        return self.root.tree_size()

    def convert_to_pixels(self) -> List[List[int]]:
        """
        Return the pixels represented by this tree as a 2D matrix
        """
        return self.root.convert_to_pixels(self.width, self.height)

    def preorder(self) -> str:
        """
        return a string representing the preorder traversal of the quadtree.
        The string is a series of entries separated by comma (,).
        Each entry could be one of the following:
        - empty string '': represents a QuadTreeNodeInternal
        - string of an integer value such as '5': represents a QuadTreeNodeLeaf
        - string 'E': represents a QuadTreeNodeEmpty

        For example, consider the following tree with a root and its 4 children
                __      Root       __
              /      |       |        \
            Empty  Leaf(5), Leaf(8), Empty

        preorder() of this tree should return exactly this string: ",E,5,8,E"

        (Note the empty-string entry before the first comma)
        """
        return self.root.preorder()

    @staticmethod
    def restore_from_preorder(lst: List[str],
                              width: int, height: int) -> QuadTree:
        """
        Restore the quad tree from the preorder list <lst>
        The preorder list <lst> is the preorder string split by comma

        Precondition: the root of the tree must be an internal node (non-leaf)
        """
        tree = QuadTree()
        tree.width = width
        tree.height = height
        tree.root = QuadTreeNodeInternal()
        tree.root.restore_from_preorder(lst, 0)
        return tree


def maximum_loss(original: QuadTreeNode, compressed: QuadTreeNode) -> float:
    """
    Given an uncompressed image as a quad tree and the compressed version,
    return the maximum loss across all compressed quadrants.

    Precondition: original.tree_size() >= compressed.tree_size()

    Note: original, compressed are the root nodes (QuadTreeNode) of the
    trees, *not* QuadTree objects

    >>> pixels = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    >>> orig, comp = QuadTree(0), QuadTree(2)
    >>> orig.build_quad_tree(pixels)
    >>> comp.build_quad_tree(pixels)
    >>> maximum_loss(orig.root, comp.root)
    1.5811388300841898
    """
    if isinstance(compressed, QuadTreeNodeLeaf) and isinstance(original, QuadTreeNodeLeaf):
        return 0
    if (isinstance(compressed, QuadTreeNodeLeaf) or isinstance(compressed, QuadTreeNodeEmpty)) \
        and isinstance(original, QuadTreeNodeInternal):
        lst = []

        for i in range(4):

            if isinstance(original.children[i], QuadTreeNodeEmpty):
                lst.append([])

            else:
                lst.append([original.children[i].value])
        return standard_deviation_and_mean(lst)[0]

    else:
        v1 = maximum_loss(original.children[0], compressed.children[0])
        v2 = maximum_loss(original.children[1], compressed.children[1])
        v3 = maximum_loss(original.children[2], compressed.children[2])
        v4 = maximum_loss(original.children[3], compressed.children[3])

        return max([v1, v2, v3, v4])
