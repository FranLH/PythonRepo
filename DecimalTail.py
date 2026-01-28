from fractions import Fraction
import matplotlib.pyplot as plt

def tail_class(frac):
    """
    Returns the equivalence class of the decimal tail of frac
    according to the user's rules.
    """
    numerator = frac.numerator
    denominator = frac.denominator

    seen = {}
    remainder = numerator % denominator
    digits = []
    pos = 0

    # Long division to detect termination or repetition
    while remainder != 0 and remainder not in seen:
        seen[remainder] = pos
        remainder *= 10
        digit = remainder // denominator
        digits.append(str(digit))
        remainder %= denominator
        pos += 1

    if remainder == 0:
        # Finite decimal: class determined by last digit
        if not digits:
            return ("finite", "0")
        return ("finite", digits[-1])
    else:
        # Periodic decimal: class determined by repeating block
        start = seen[remainder]
        repeating_block = "".join(digits[start:])
        return ("periodic", repeating_block)

def T(n):
    """
    Computes T(n): number of distinct decimal-tail classes
    of k/n for k = 0, 1, ..., n-1
    """
    classes = set()
    for k in range(n):
        frac = Fraction(k, n)
        classes.add(tail_class(frac))
    return len(classes)

# -------- plotting --------

N = 1000   # increase this (e.g. 1000, 2000) if your machine can handle it

x = list(range(1, N + 1))
y = [T(n) for n in x]

plt.figure()
plt.plot(x, y)
plt.grid()
plt.xlabel("n")
plt.ylabel("T(n)")
plt.title("Decimal-tail complexity function T(n)")
plt.show()