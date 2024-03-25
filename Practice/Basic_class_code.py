"""Top program docstring

"""
from datetime import date
from typing import Dict, List, Tuple
from __future__ import annotations

class Name():
    """
    Description:

    === Attributes ===

    attribute: description

    === Representation Invariants ===

    - name
        description

    """

    #Attributes types
    #List all the attributes ex, a: int

    def __init__(self, ) -> None:
        """
        Initialize a new class name
        """
        self.a = []


    def method_name(self, ) -> type:
        """
        Method description
        And doctests
        >>>

        >>>
        """
        self.a = 1 + 2




#################################################
#Custom Errors

class ErrorName(Exception):
    def __str__(self) -> str:
        return "Message"

#EXPECTATIONS
     try:
         #Code to run
         #If an error automatically happens it'll go into the except blocks
         #If statement which raises custom error if it passes through
       
    except Exception:

    except ValueError:
                
    finally:
        




if __name__ == '__main__':
    import doctest
    doctest.testmod()

##    option = 'y'
##    while option == 'y':
##        value = input('Give me an integer to check if it is a divisor of 42: ')
##        try:
##            is_divisor = (42 % int(value) == 0)
##            print(is_divisor)
##        except ZeroDivisionError:
##            print("Uh-oh, invalid input: 0 cannot be a divisor of any number!")
##        except ValueError:
##            print("Type mismatch, expecting an integer!")
##        finally:
##            print("Now let's try another number...")
##        option = input('Would you like to continue (y/n): ')
