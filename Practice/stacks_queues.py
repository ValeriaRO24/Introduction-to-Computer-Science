"""ADTs: Stacks and Queues

**************************
Copyright information
**************************
CSC148 Winter 2021
Department of Mathematical and Computational Sciences,
University of Toronto Mississauga

**************************
Module description
**************************
This module contains all of the code covered in Week 4 of the course:
stacks, queues, and timing experiments.
"""
from typing import Generic, List, Optional, TypeVar, Any


class EmptyStackError(Exception):
    """Exception raised when an error occurs."""
    pass


###############################################################################
# Stacks
###############################################################################
class Stack:
    """A last-in-first-out (LIFO) stack of items.

    Stores data in a last-in, first-out order. When removing an item from the
    stack, the most recently-added item is the one that is removed.
    """
    # === Private Attributes ===
    # _items:
    #     The items stored in this stack. The end of the list represents
    #     the top of the stack.
    _items: List

    def __init__(self) -> None:
        """Initialize a new empty stack."""
        self._items = []

    def is_empty(self) -> bool:
        """Return whether this stack contains no items.

        >>> s = Stack()
        >>> s.is_empty()
        True
        >>> s.push('hello')
        >>> s.is_empty()
        False
        """
        return self._items == []

    def push(self, item: Any) -> None:
        """Add a new element to the top of this stack."""
        self._items.append(item)

    def pop(self) -> Any:
        """Remove and return the element at the top of this stack.

        Raise an EmptyStackError if this stack is empty.

        >>> s = Stack()
        >>> s.push('hello')
        >>> s.push('goodbye')
        >>> s.pop()
        'goodbye'
        """
        if self.is_empty():
            raise EmptyStackError
        else:
            return self._items.pop()


class Stack2:
    """Alternate stack implementation.

    This implementation uses the *front* of the Python list to represent
    the top of the stack.
    """
    # === Private Attributes ===
    # _items:
    #     The items stored in the stack. The front of the list represents
    #     the top of the stack.
    _items: List

    def __init__(self) -> None:
        """Initialize a new empty stack."""
        self._items = []

    def is_empty(self) -> bool:
        """Return whether this stack contains no items.

        >>> s = Stack()
        >>> s.is_empty()
        True
        >>> s.push('hello')
        >>> s.is_empty()
        False
        """
        return self._items == []

    def push(self, item: Any) -> None:
        """Add a new element to the top of this stack."""
        self._items.insert(0, item)

    def pop(self) -> Any:
        """Remove and return the element at the top of this stack.

        Raise an EmptyStackError if this stack is empty.

        >>> s = Stack()
        >>> s.push('hello')
        >>> s.push('goodbye')
        >>> s.pop()
        'goodbye'
        """
        if self.is_empty():
            raise EmptyStackError
        else:
            return self._items.pop(0)


###############################################################################
# Queues
###############################################################################
class Queue:
    """A first-in-first-out (FIFO) queue of items.

    Stores data in a first-in, first-out order. When removing an item from the
    queue, the most recently-added item is the one that is removed.
    """
    # === Private attributes ===
    # _items: a list of the items in this queue
    _items: List

    def __init__(self) -> None:
        """Initialize a new empty queue."""
        self._items = []

    def is_empty(self) -> bool:
        """Return whether this queue contains no items.

        >>> q = Queue()
        >>> q.is_empty()
        True
        >>> q.enqueue('hello')
        >>> q.is_empty()
        False
        """
        return self._items == []

    def enqueue(self, item: Any) -> None:
        """Add <item> to the back of this queue.
        """
        self._items.append(item)

    def dequeue(self) -> Optional[Any]:
        """Remove and return the item at the front of this queue.

        Return None if this Queue is empty.
        (We illustrate a different mechanism for handling an erroneous case.)

        >>> q = Queue()
        >>> q.enqueue('hello')
        >>> q.enqueue('goodbye')
        >>> q.dequeue()
        'hello'
        """
        if self.is_empty():
            return None
        else:
            return self._items.pop(0)


###############################################################################
# Stack and Queue functions (practice)
###############################################################################
def size(s: Stack) -> int:
    """Return the number of items in s.

    Do not mutate s.

    >>> s = Stack()
    >>> size(s)
    0
    >>> s.push('hi')
    >>> s.push('more')
    >>> s.push('stuff')
    >>> size(s)
    3
    """
    side_stack = Stack()
    count = 0
    # Pop everything off <s> and onto <side_stack>, counting as we go.
    while not s.is_empty():
        side_stack.push(s.pop())
        count += 1
    # Now pop everything off <side_stack> and back onto <s>.
    while not side_stack.is_empty():
        s.push(side_stack.pop())
    # <s> is restored to its state at the start of the function call.
    # We consider that it was not mutated.
    return count


def size_broken1(s: Stack) -> int:
    """This version of size won't work. We cannot iterate over a Stack.
    """
    count = 0
    for _ in s:
        count += 1
    return count


def size_broken2(s: Stack) -> int:
    """This version of size does work for both of our
    implementations of Stack. But it looks at the
    private attribute _items. This is not just 'bad style';
    it has implications: If we change the implementation
    of the stack, _items might no longer be a list, or
    may not even exist!  Our function would crash.
    If instead we respect the privacy of attributes
    and use only the public interface of our stack class,
    as our first version of method size does, we get
    'plug-out / plug-in compatability'.
    """
    return len(s._items)


def size_broken3(s: Stack) -> int:
    """This version actually passes the doctests. But it has a serious problem.
    Can you see it?

    >>> s = Stack()
    >>> size(s)
    0
    >>> s.push('hi')
    >>> s.push('more')
    >>> s.push('stuff')
    >>> size_broken3(s)
    3
    """
    count = 0
    while not s.is_empty():
        s.pop()
        count += 1
    return count


def size_broken4(s: Stack) -> int:
    """Here we try to fix the problem with the previous version. Do we?

    >>> s = Stack()
    >>> size(s)
    0
    >>> s.push('hi')
    >>> s.push('more')
    >>> s.push('stuff')
    >>> size_broken4(s)
    3
    """
    copy = s
    count = 0
    while not copy.is_empty():
        copy.pop()
        count += 1
    return count


def remove_big(s: Stack) -> None:
    """Remove the items in <stack> that are greater than 5.

    Do not change the relative order of the other items.

    >>> s = Stack()
    >>> s.push(1)
    >>> s.push(29)
    >>> s.push(8)
    >>> s.push(4)
    >>> remove_big(s)
    >>> s.pop()
    4
    >>> s.pop()
    1
    >>> s.is_empty()
    True
    """
    new_stack = Stack()
    while not s.is_empty():
        item = s.pop()
        if item <= 5:
            new_stack.push(item)

    while not new_stack.is_empty():
        s.push(new_stack.pop())


def double_stack(s: Stack) -> Stack:
    """Return a new stack that contains two copies of every item in <stack>.

    We'll leave it up to you to decide what order to put the copies into in
    the new stack.

    >>> s = Stack()
    >>> s.push(1)
    >>> s.push(29)
    >>> new_stack = double_stack(s)
    >>> s.pop()  # s should be unchanged.
    29
    >>> s.pop()
    1
    >>> s.is_empty()
    True
    >>> new_items = []
    >>> new_items.append(new_stack.pop())
    >>> new_items.append(new_stack.pop())
    >>> new_items.append(new_stack.pop())
    >>> new_items.append(new_stack.pop())
    >>> sorted(new_items)
    [1, 1, 29, 29]
    """
    temp_stack = Stack()
    new_stack = Stack()
    while not s.is_empty():
        item = s.pop()
        temp_stack.push(item)

    while not temp_stack.is_empty():
        item = temp_stack.pop()
        s.push(item)
        new_stack.push(item)
        new_stack.push(item)

    return new_stack


def product(integer_queue: Queue) -> int:
    """Return the product of integers in the queue.

    Postcondition: integer_queue.is_empty() is True.

    >>> q = Queue()
    >>> q.enqueue(2)
    >>> q.enqueue(4)
    >>> q.enqueue(6)
    >>> product(q)
    48
    >>> q.is_empty()
    True
    """
    if integer_queue.is_empty():
        return 0

    result = 1
    while not integer_queue.is_empty():
        result *= integer_queue.dequeue()
    return result


def product_star(integer_queue: Queue) -> int:
    """Return the product of integers in the queue. Do not destroy
    integer_queue.

    Postcondition: the final state of integer_queue is equal to its
        initial state.

    >>> q = Queue()
    >>> q.enqueue(2)
    >>> q.enqueue(4)
    >>> product_star(q)
    8
    >>> q.dequeue()
    2
    >>> q.dequeue()
    4
    >>> q.is_empty()
    True
    """
    if integer_queue.is_empty():
        return 0

    result = 1
    line = []
    while not integer_queue.is_empty():
        item = integer_queue.dequeue()
        line.append(item)
        result *= item

    for item in line:
        integer_queue.enqueue(item)

    return result


###############################################################################
# Generic versions
###############################################################################
# Create a "type variable" to represent the generic type of a stack or queue.
T = TypeVar('T')

###############################################################################
# Timing experiments
###############################################################################
def push_and_pop(s: Stack) -> None:
    """Push and pop a new item onto the given stack."""
    s.push(1)
    s.pop()


def setup_queues(qsize: int, n: int) -> List[Queue]:
    """Return a list of <n> queues, each of the given size."""
    # Experiment preparation: make a list containing <n> queues,
    # each of size <qsize>.
    # You can "cheat" here and set your queue's _items attribute
    # directly to a list of the appropriate size by writing something like
    #
    # queue._items = list(range(qsize))
    #
    # to save a bit of time in setting up the experiment.
    queue_list = []
    for _ in range(n):
        q = Queue()
        # This line is cheating, but makes your experiment a bit faster.
        q._items = list(range(qsize))
        queue_list.append(q)
    return queue_list


if __name__ == '__main__':
    # import python_ta
    # python_ta.check_all(config={'pyta-type-check': True})
    import doctest
    doctest.testmod()

    # Import the main timing function.
    from timeit import timeit

    # The stack sizes we want to try.
    STACK_SIZES = [1000, 10000, 100000, 1000000, 10000000]
    for stack_size in STACK_SIZES:
        # Uncomment the stack implementation that we want to time.
        stack = Stack()
        # stack = Stack2()

        # Bypass the Stack interface to create a stack of size <stack_size>.
        # This speeds up the experiment, but we know this violates
        # encapsulation!
        stack._items = list(range(stack_size))

        # Call push_and_pop(stack) 1000 times, and store the time taken in
        # <time>. The globals=globals() is used for a technical reason that
        # you can ignore.
        time = timeit('push_and_pop(stack)', number=1000, globals=globals())

        # Finally, report the result. The :>8 is used to right-align the
        # stack size when it's printed, leading to a more visually-pleasing
        # report.
        print(f'Stack size {stack_size:>8}, time {time}')

    # Queue timing experiment.
    QUEUE_SIZES = [10000, 20000, 40000, 80000, 160000]
    TRIALS = 300

    for queue_size in QUEUE_SIZES:
        queues = setup_queues(queue_size, TRIALS)
        time = 0
        for queue in queues:
            time += timeit('queue.enqueue(1)', number=1000, globals=globals())
        print(f'enqueue: Queue size {queue_size:>7}, time {time}')

    for queue_size in QUEUE_SIZES:
        queues = setup_queues(queue_size, TRIALS)
        time = 0
        for queue in queues:
            time += timeit('queue.dequeue()', number=1000, globals=globals())
        print(f'dequeue: Queue size {queue_size:>7}, time {time}')
