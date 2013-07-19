# Functions that creates a new monomial
def pol(coef, exp = 0):
    if coef == 0:
        return Pol ( [] )
    if (isinstance(coef,int) or isinstance(coef,float)) and isinstance(exp,int) and exp>= 0: 
        return Pol ( [(coef, exp)] )
    
class Pol:

    """
        Class representing polynomials:

        How to use:
        The use of the function 'pol' is recommended. Example:
        >>> p = pol(2,3)
        2x^3
        >>> q = p + pol(1,0) + pol(-1,2)
        2x^3 - x^2 + 1

        You can also use the deriv(), integr() and degree() methods of
        polynomials. For help, use:
        >>>help(Pol.method)
    """

    # This program is free software: you can redistribute it and/or modify
    # it under the terms of the GNU General Public License as published by
    # the Free Software Foundation, either version 3 of the License, or
    # (at your option) any later version.

    # This program is distributed in the hope that it will be useful,
    # but WITHOUT ANY WARRANTY; without even the implied warranty of
    # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    # GNU General Public License for more details.

    # You should have received a copy of the GNU General Public License
    # along with this program.  If not, see <http://www.gnu.org/licenses/>.

    # - Methods/fields with names surroundend by two underscores (__name__)
    #   are special. Each one of these methods has a specific meaning to the
    #   Python interpreter.
    #    
    # - Methods/fields with names beggining with two underscores, but not
    #   ending with them (__name), are "private", and aren't offered to
    #   clients of the class 'Pol' by the standard interface.
    #   
    # - Other methods/field are "public" and belong to the interface offered
    #   to the 'Pol' class clients.

    
    # Constructor
    def __init__(self, terms):
        self.__terms = tuple(terms)

    # Method that implement len()
    def __len__(self):
        return len(self.__terms)

    # Method that return an iterator object
    def __iter__(self):
        t = ()
        for i in self.__terms:
            t += (Pol([i]),)
        return iter(t)

    # Method called to implement evaluation of self[key]
    def __getitem__(self,key):
        return Pol([self.__terms[key]])

    # ----- Polynomials arithmetics -----------------------------------
    
    # Methods that implement the binary operators +, -, * and / when 
    # the first operand is an instance of Pol class

    # Method that implement the binary operator +
    def __add__(self, other):
        return self.__add_or_sub ( other, False )
    # Method that implement the binary operator -
    def __sub__(self, other):
        return self.__add_or_sub ( other, True )
    # Method that implement the binary operator *
    def __mul__(self, other):
        return self.__mul(other)
    # Method that implement the binary operator /
    def __truediv__(self, other):
        return self.__truediv(other)
    
    # Methods that implement the binary operators +, -, * and / when 
    # only the second operand is an instance of Pol class

    # Method that implement the binary operator + when 
    # only the second operand is an instance of Pol class
    def __radd__(self, other):
        return self.__add_or_sub ( other, False )
    # Method that implement the binary operator - when 
    # only the second operand is an instance of Pol class
    def __rsub__(self, other):
        other = pol(other)
        return other.__add_or_sub ( self, True ) 
    # Method that implement the binary operator * when 
    # only the second operand is an instance of Pol class
    def __rmul__(self, other):
        return self.__mul(other)
    # Method that implement the binary operator / when 
    # only the second operand is an instance of Pol class
    def __rtruediv__(self, other):
        other = pol(other)
        return other.__truediv(self)
 
    # Method that implement the unary operator -
    def __neg__(self):
        neg = []
        for term in self.__terms:
            neg.append((-term[0],term[1]))
        return Pol(neg)

    # Method that implement the unary operator +
    def __pos__(self):
        return self

    # Methods that implement the exponentiation of a polynomial
    def __pow__(self, n):
        if not isinstance (n, int) or n < 0:
            print("This operation in not allowed for 'Pol' objects")
        elif n == 0:
            return pol(1)
        else:
            return self.__pow(n)
        
    # ----- Other operations with polynomials ----------------------------

    # Method that implement the comparison operator == and !=
    def __eq__(self, other):
        if isinstance (other, Pol):
            if len (self) != len (other):
                return False

            for i,j in zip(self.__terms, other.__terms):
                if i != j:
                    return False

            return True
        else:
            if (self == pol(0) and other == 0) or (self.degree() == 0 and self.__terms[0][0] == other):
                return True

            return False

    # Method that implement the comparison operator !=
    def __ne__(self, other):
        return not self == other

    # Computation of a polynomial at some point and application of a polynomial to another
    def __call__(self, x):
        if self.degree() == 0:
            return self

        self.__result = 0
        for i in range(len(self)):
            self.__pot = self.__terms[i][1]
            if i != len(self) - 1:
                self.__pot -= self.__terms[i + 1][1]
            self.__result = (self.__result + self.__terms[i][0]) * x ** self.__pot

        if isinstance(self.__result,Pol) and self.__result.degree() == 0:
            if self.__result == pol(0):
                self.__result = 0 
            else:
                self.__result = self.__result.__terms[0][0]

        return self.__result            

    # Conversion of a polynomial to a string
    def __repr__(self):
        if self == pol(0):
            return "0"
        
        self.__string = ""
        if self.__terms[0][0] < 0:
            self.__string += "-"

        for term in self.__terms:
            # This 'if' works only because there are no equal terms in a polynomial
            if term != self.__terms[0]:
                if term[0] > 0:
                    self.__string += " + "
                else:
                    self.__string += " - "

            if term[0] not in [-1,1] or term[1] == 0:
                self.__string += str(abs(term[0]))

            if term[1] != 0:
                self.__string += "x"

            if term[1] not in [0,1]:
                self.__string += "^" + str(term[1])

        return self.__string

    # ----- "Public" methods -----------------------------------------
    
    # Method that returns the degree of a polynomial
    def degree(self):
        if self == pol(0):
            return 0
        else:
            return self.__terms[0][1]

    # Method that returns the derivative of a polynomial
    def deriv(self):
        der = []

        if len(self) > 0:
            for term in self.__terms:
                if term[1] - 1 >= 0:
                    der.append((term[0] * term[1], term[1] - 1))

        return Pol(der)
    
    # Method that returns the integral of a polynomial from point a to point b
    def integr(self, a, b):
        if (isinstance(a,(int,float)) or (isinstance(a,Pol) and a.degree() == 0)) and (isinstance(b,(int,float)) or (isinstance(b,Pol) and b.degree() == 0)): 
            self.__integral = pol(0)
            if len(self) > 0:
                for term in self.__terms:
                    self.__integral += pol(term[0] / (term[1] + 1), term[1] + 1)
            self.__result = self.__integral(b) - self.__integral(a)

            if self.__result == int(self.__result):
                self.__result = int(self.__result)

            return self.__result
        
        
    # ----- Private auxiliary methods ------------------------------

    # Auxiliary method used by __add__, __sub__, __radd__ and __rsub__
    # to compute sums and subtractions:
    def __add_or_sub(self, other, sub):
        self.__result = []
        i = 0
        j = 0

        if not isinstance ( other, Pol ):
            other = pol( other )

        if other == pol(0):
            return self
        if self == pol(0):
            if sub == False:
                return other
            else:
                return -other


        while i < len(self) and j < len(other):
            if self.__terms[i][1] > other.__terms[j][1]:
                self.__result.append ( (self.__terms[i][0], self.__terms[i][1]) )
                i += 1
            elif self.__terms[i][1] < other.__terms[j][1]:
                if sub == False:
                    self.__result.append ( (other.__terms[j][0], other.__terms[j][1]) )
                else:
                    self.__result.append ( (-other.__terms[j][0], other.__terms[j][1]) )
                j += 1
            else:
                if sub == False:
                    self.__coef_result = self.__terms[i][0] + other.__terms[j][0]
                else:
                    self.__coef_result = self.__terms[i][0] - other.__terms[j][0]

                if self.__coef_result != 0:
                    self.__result.append ( (self.__coef_result, self.__terms[i][1]) )
                i += 1
                j += 1

        while i < len(self):
            self.__result.append ( (self.__terms[i][0], self.__terms[i][1]) )
            i += 1

        while j < len(other):
            if sub == False:
                self.__result.append ( (other.__terms[j][0], other.__terms[j][1]) )
            else:
                self.__result.append ( (-other.__terms[j][0], other.__terms[j][1]) )
            j += 1

        return Pol ( self.__result )

    # Auxliary method used bu __mul that implements the multiplication of a polynomials by a monomial 
    def __mul_by_term(self, coef, exp):
        self.__result = []
        for term in self.__terms:
            self.__result.append ( (term[0] * coef, term[1] + exp) )

        return Pol(self.__result)

    # Auxiliary method used by __mul__ and __rmul__ to compute multiplications
    def __mul(self, other):
        if not isinstance(other,Pol):
            other = pol(other)

        self.__product = pol(0)
        for term in other.__terms:
            self.__product += self.__mul_by_term(term[0], term[1])

        return self.__product
		

    # Auxiliary method used by __truediv__ and __rtruediv__ to implement division:
    def __truediv(self, other):
        if not isinstance(other,Pol):
            other = pol(other)
        if other == 0:
            raise ZeroDivisionError

        self.__resto = self
        self.__quociente = pol(0)

        while self.__resto.degree() >= other.degree() and self.__resto != 0:
            self.__aux = pol(self.__resto.__terms[0][0] / other.__terms[0][0], self.__resto.__terms[0][1] - other.__terms[0][1]) 
            self.__quociente += self.__aux
            self.__resto -= self.__aux * other

        return tuple([self.__quociente, self.__resto])

    # Auxiliary method used by __pow__ to implement exponentiation:
    def __pow(self, n):
        if n == 0:
            return self

        self.__result = self ** (n // 2)
        self.__result *= self.__result
        if n % 2 == 1:
            self.__result *= self

        return self.__result
