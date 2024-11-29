import unittest

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
        if not isinstance(self, Fraction) or not isinstance(other, Fraction):
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
        if not isinstance(other, Fraction):
            return False

        return (self.numerator == other.numerator and self.denominator == other.denominator)
        
    def __abs__(self):
        """Return the absolute value of the fraction

        PRE : it must be a fraction
        POST : returns a new fraction which is the absolute value of the original fraction
        """
        num_part = self.numerator
        den_part = self.denominator

        if num_part < 0 and den_part > 0:
            num_part *= -1
        elif den_part < 0 and num_part > 0:
            den_part *= -1
        return Fraction(num_part, den_part)

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

    difference = abs(self - other)
    print(f"Difference: {difference}")  # Debug print

    result = difference.is_unit()
    print(f"Is unit: {result}")  # Debug print

    return result
            

class FractionTestCase(unittest.TestCase):

    def test_initialization(self):
        """Test initialization of Fraction"""
        f = Fraction(3, 4)
        self.assertEqual(f.numerator, 3)
        self.assertEqual(f.denominator, 4)

        f = Fraction(-3, 4)
        self.assertEqual(f.numerator, -3)
        self.assertEqual(f.denominator, 4)

        with self.assertRaises(ValueError):
            Fraction(1, 0)

        with self.assertRaises(ValueError):
            Fraction(1.5, 2)

    def test_str(self):
        """Test the __str__ method"""
        f = Fraction(3, 4)
        self.assertEqual(str(f), "3/4")

        f = Fraction(-3, 4)
        self.assertEqual(str(f), "-3/4")

    def test_as_mixed_number(self):
        """Test the as_mixed_number method"""
        f = Fraction(7, 4)
        self.assertEqual(f.as_mixed_number(), "1 + 3/4")

        f = Fraction(4, 4)
        self.assertEqual(f.as_mixed_number(), "1")

        f = Fraction(3, 4)
        self.assertEqual(f.as_mixed_number(), "3/4")

    def test_addition(self):
        """Test the __add__ method"""
        f1 = Fraction(1, 4)
        f2 = Fraction(1, 4)
        result = f1 + f2
        self.assertEqual(result, Fraction(1, 2))

        f1 = Fraction(1, 2)
        f2 = Fraction(1, 3)
        result = f1 + f2
        self.assertEqual(result, Fraction(5, 6))

    def test_subtraction(self):
        """Test the __sub__ method"""
        f1 = Fraction(3, 4)
        f2 = Fraction(1, 4)
        result = f1 - f2
        self.assertEqual(result, Fraction(1, 2))

    def test_multiplication(self):
        """Test the __mul__ method"""
        f1 = Fraction(2, 3)
        f2 = Fraction(3, 4)
        result = f1 * f2
        self.assertEqual(result, Fraction(1, 2))

    def test_division(self):
        """Test the __truediv__ method"""
        f1 = Fraction(3, 4)
        f2 = Fraction(2, 3)
        result = f1 / f2
        self.assertEqual(result, Fraction(9, 8))

    def test_power(self):
        """Test the __pow__ method"""
        f1 = Fraction(2, 3)
        f2 = Fraction(2, 1)
        result = f1 ** f2
        self.assertEqual(result, 4/9)

    def test_equality(self):
        """Test the __eq__ method"""
        f1 = Fraction(1, 2)
        f2 = Fraction(1, 2)
        self.assertEqual(f1, f2)

        f1 = Fraction(1, 2)
        f2 = Fraction(2, 4)
        self.assertEqual(f1, f2)

    def test_float_conversion(self):
        """Test the __float__ method"""
        f = Fraction(1, 2)
        self.assertEqual(float(f), 0.5)

    def test_is_zero(self):
        """Test the is_zero method"""
        f = Fraction(0, 1)
        self.assertTrue(f.is_zero())

        f = Fraction(1, 2)
        self.assertFalse(f.is_zero())

    def test_is_integer(self):
        """Test the is_integer method"""
        f = Fraction(2, 2)
        self.assertTrue(f.is_integer())

        f = Fraction(3, 2)
        self.assertFalse(f.is_integer())

    def test_is_proper(self):
        """Test the is_proper method"""
        f = Fraction(1, 2)
        self.assertTrue(f.is_proper())

        f = Fraction(3, 2)
        self.assertFalse(f.is_proper())

    def test_is_unit(self):
        """Test the is_unit method"""
        f = Fraction(1, 2)
        self.assertTrue(f.is_unit())

        f = Fraction(2, 3)
        self.assertFalse(f.is_unit())

    def test_is_adjacent_to(self):
        """Test the is_adjacent_to method"""
        f1 = Fraction(1, 2)
        f2 = Fraction(2, 3)
        f3 = Fraction(1, 6)
        f4 = Fraction(1, 3)
        self.assertTrue(f1.is_adjacent_to(Fraction(2, 3)))  
        self.assertFalse(f1.is_adjacent_to(f2)) 
        self.assertTrue(f1.is_adjacent_to(Fraction(1, 3)))  
        self.assertFalse(f2.is_adjacent_to(f3)) 
        self.assertFalse(f3.is_adjacent_to(f4))


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
