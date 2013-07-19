Python Polynomial Module
========================

This is a simple module for Python that allows the use of polynomial (or simply Pol) objects. They behave as expected (simple operations with other polynomials and with other data types, as well as simple calculations) and is best suited for use in Python's interactive mode.

Usage
-----

With a Python 3.3.2 interpreter opened in the module's directory:
    
    >>> from pol-module import *
    # Import everything that is in the module
    >>> x = pol(1,2) + pol(3,1) + pol(5,0)
    # Create a new x polynomial from the addition of monomials
    >>> print(x)
    x^2 - 3x + 5
