from __future__ import print_function
# script should work in all supported versions of Python stdlib,
# plus 2.7.x
# Scripts takes no arguments, all arguments will be ignored.

import random


def main():
    """
    Generate some random int between 1 and 10,
    store in variable, print and exit
    """
    randint = random.randint(1, 10)
    print(randint)


if __name__ == '__main__':
    main()
