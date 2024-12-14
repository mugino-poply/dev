class Fraction:
    """Class representing a fraction and operations on it

    Author : V. Van den Schrieck
    Date : October 2021
    This class allows fraction manipulations through several operations.
    """

    def __init__(self, num=0, den=1):
        """This builds a fraction based on some numerator and denominator.

        PRE : num is an integer, den is an integer except 0
        POST : fraction object is well initialised, with a numerator and a denominator, the fraction is in its reduced form
        """
        if not isinstance(num, int) or not isinstance(den, int):
            raise ValueError("Numerator and denominator must be integers")
        if den == 0:
            raise ValueError("Denominator cannot be zero")
        
        def pgcd(a, b):
            while b:
                a, b = b, a % b
            return a
        
        common_divisor = pgcd(num, den)
        self._numerator = num // common_divisor
        self._denominator = den // common_divisor

    @property
    def numerator(self):
        return self._numerator
    @property
    def denominator(self):
        return self._denominator

# ------------------ Textual representations ------------------

    def __str__(self) :
        """Return a textual representation of the reduced form of the fraction

        PRE : the fraction must be one
        POST : the return is a fraction in a textual form
        """
        if not isinstance(self, Fraction):
            raise TypeError("It must be a fraction")

        return f"{self.numerator}/{self.denominator}"

    def as_mixed_number(self) :
        """Return a textual representation of the reduced form of the fraction as a mixed number

        A mixed number is the sum of an integer and a proper fraction

        PRE : the fraction must be one
        POST : the return is a mixed number in a textual form
        """
        if not isinstance(self, Fraction):
            raise TypeError("It must be a fraction")

        int_part = self.numerator // self.denominator
        fract_part = self.numerator % self.denominator

        if fract_part == 0:
            return f"{int_part}"
        else:
            if int_part != 0:
                return f"{int_part} + {fract_part}/{self.denominator}" 
            else:
                return f"{fract_part}/{self.denominator}"

    
# ------------------ Operators overloading ------------------

    def __add__(self, other):
        """Overloading of the + operator for fractions

         PRE : it must be 2 fractions
         POST : the result is the result of an addition between 2 fractions
         """
        if not isinstance(self, Fraction) or not isinstance(other, Fraction):
            raise TypeError("It must be fractions")

        num_part1 = self.numerator
        num_part2 = other.numerator
        den_part1 = self.denominator
        den_part2 = other.denominator

        # If the denominators are the same, add the numerators
        if den_part1 == den_part2:
            new_num = num_part1 + num_part2
            new_den = den_part1
        else:
            # Find a common denominator and adjust numerators
            new_den = den_part1 * den_part2
            new_num = (num_part1 * den_part2) + (num_part2 * den_part1)

        # Create and return a new Fraction object, reduced to simplest form
        return Fraction(new_num, new_den)


    def __sub__(self, other):
        """Overloading of the - operator for fractions

        PRE : it must be 2 fractions
        POST : the result is the first fraction minus the second one
         """
        if not isinstance(self, Fraction) or not isinstance(other, Fraction):
            raise TypeError("It must be fractions")

        num_part1 = self.numerator
        num_part2 = other.numerator
        den_part1 = self.denominator
        den_part2 = other.denominator

        # If the denominators are the same, substract the numerators
        if den_part1 == den_part2:
            new_num = num_part1 - num_part2
            new_den = den_part1
        else:
            # Find a common denominator and adjust numerators
            new_den = den_part1 * den_part2
            new_num = (num_part1 * den_part2) - (num_part2 * den_part1)

        # Create and return a new Fraction object, reduced to simplest form
        return Fraction(new_num, new_den)


    def __mul__(self, other):
        """Overloading of the * operator for fractions

        PRE : it must be be 2 fractions
        POST : the result is the multiplication of the 2 fractions
        """
        if not isinstance(self, Fraction) or not isinstance(other, Fraction):
            raise TypeError("It must be fractions")

        num_part1 = self.numerator
        num_part2 = other.numerator
        den_part1 = self.denominator
        den_part2 = other.denominator

        return Fraction(num_part1*num_part2, den_part1*den_part2)


    def __truediv__(self, other):
        """Overloading of the / operator for fractions

        PRE : it must be be 2 fractions
        POST : the result is the division of the 2 fractions
        """
        if not isinstance(self, Fraction) or not isinstance(other, Fraction):
            raise TypeError("It must be fractions")

        reversed_other = Fraction(other.denominator, other.numerator)

        return self.__mul__(reversed_other)


    def __pow__(self, other):
        """Overloading of the ** operator for fractions

        PRE : it must be be 2 fractions
        POST : the result is the first fraction exponent the second one
        """
        if not isinstance(self, Fraction):
            raise TypeError("It must be fractions")

        num_part1 = self.numerator
        num_part2 = other.numerator
        den_part1 = self.denominator
        den_part2 = other.denominator

        base = Fraction(num_part1, den_part1)
        exponent = Fraction(num_part2, den_part2)

        inter_num = base.numerator ** exponent.numerator
        inter_den = base.denominator ** exponent.numerator

        num_root = round(inter_num ** (1 / exponent.denominator)) 
        den_root = round(inter_den ** (1 / exponent.denominator))

        return (num_root/den_root)
    
    
    def __eq__(self, other) : 
        """Overloading of the == operator for fractions
        
        PRE : it must be be 2 fractions
        POST : returns true if they are equal
        """
        if not isinstance(self, Fraction) or not isinstance(other, Fraction):
            raise TypeError("It must be fractions")

        return (self.numerator == other.numerator and self.denominator == other.denominator)
        
    def __float__(self) :
        """Returns the decimal value of the fraction

        PRE : it must be be 2 fractions
        POST : returns the decimal value of the fraction
        """
        if not isinstance(self, Fraction):
            raise TypeError("It must be a fraction")

        return (self.numerator/self.denominator)
    
# TODO : [BONUS] You can overload other operators if you wish (ex : <, >, ...)



# ------------------ Properties checking  ------------------

    def is_zero(self):
        """Check if a fraction's value is 0

        PRE : it must be a fraction
        POST : returns true if the fraction is equal to 0
        """
        if not isinstance(self, Fraction):
            raise TypeError("It must be a fraction")

        return (self.numerator == 0)


    def is_integer(self):
        """Check if a fraction is integer (ex : 8/4, 3, 2/2, ...)

        PRE : it must be a fraction
        POST : returns true if the fraction is an integer
        """
        if not isinstance(self, Fraction):
            raise TypeError("It must be a fraction")

        return (self.numerator % self.denominator == 0)

    def is_proper(self):
        """Check if the absolute value of the fraction is < 1

        PRE : it must be a fraction
        POST : returns true if the fraction is under 1
        """
        if not isinstance(self, Fraction):
            raise TypeError("It must be a fraction")

        return (self.numerator < self.denominator)

    def is_unit(self):
        """Check if a fraction's numerator is 1 in its reduced form

        PRE : it must be a fraction
        POST : returns True if the fraction is a unit fraction (numerator is 1 in its reduced form), otherwise False.
        """
        if not isinstance(self, Fraction):
            raise TypeError("It must be a fraction")

        reduced_fraction = Fraction(self.numerator, self.denominator)
        
        return (reduced_fraction.numerator == 1)


    def is_adjacent_to(self, other) :
        """Check if two fractions differ by a unit fraction

        Two fractions are adjacents if the absolute value of the difference them is a unit fraction

        PRE : it must be be 2 fractions
        POST : returns true if the substraction of the absolute value of both fractions is 1
        """
        if not isinstance(self, Fraction) or not isinstance(other, Fraction):
            raise TypeError("It must be fractions")
        
        reduced_fraction1 = Fraction(self.numerator, self.denominator)
        reduced_fraction2 = Fraction(other.numerator, other.denominator)

        diff1 = reduced_fraction1 - reduced_fraction2
        diff2 = reduced_fraction2 - reduced_fraction1

        return diff1.is_unit() or diff2.is_unit()
        


if __name__ == '__main__':
    fract1 = Fraction(2, 3)
    fract2 = Fraction(2, 7)
    fract3 = Fraction(1, 3)
    fract4 = Fraction(-1, 4)
    fract5 = Fraction(4, 3)
    fract6 = Fraction(-1, 3)
    print("Test __str__: ")
    print(fract6)
    print("Test as_mixed_number: ")
    print(fract5.as_mixed_number())
    print("Test +: ")
    print(fract1 + fract2)
    print("Test -: ")
    print(fract2 - fract3)
    print("Test *: ")
    print(fract3 * fract4)
    print("Test /: ")
    print(fract3 / fract4)
    print("Test ==: ")
    print(Fraction(4, 6) == fract1)
    print("Test **: ")
    print(fract5 ** 3)
    print("Test float conversion: ")
    print(float(fract6))
    print("Test is_zero(): ")
    print(Fraction(0, 6).is_zero())
    print("Test is_integer(): ")
    print(Fraction(8, 4).is_integer())
    print("Test is_proper(): ")
    print(Fraction(5, 6).is_proper())
    print("Test is_unit(): ")
    print(Fraction(2, 6).is_unit())
    print("Test is_adjacent_to ")
    print(fract1.is_adjacent_to(fract3))

