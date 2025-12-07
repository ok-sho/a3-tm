"""
Pi Calculator Demo
"""

from decimal import Decimal, getcontext


def compute_pi_chudnovsky(n_digits=33, verbose=True):
    """
    Using Chudnovsky algorithm - it converges really fast apparently
    """
    if verbose:
        print(f"trying to get {n_digits} digits of pi with chudnovsky...")
    
    # Set precision higher than needed
    getcontext().prec = n_digits + 10
    
    C = 426880 * Decimal(10005).sqrt()
    K = Decimal(6)
    M = Decimal(1)
    X = Decimal(1)
    L = Decimal(13591409)
    S = Decimal(13591409)
    
    for i in range(1, n_digits):
        M = M * (K ** 3 - 16 * K) / ((i) ** 3)
        K += 12
        L += 545140134
        X *= -262537412640768000
        S += Decimal(M * L) / X
        
        if verbose and i % 5 == 0:
            print(f"  iteration {i}/{n_digits}...")
    
    pi_value = C / S
    
    pi_string = str(pi_value)[:n_digits + 2]
    
    if verbose:
        print()
        print("done!")
        print(f"pi = {pi_string}")
    
    return pi_string


def compute_pi_machin(n_digits=33, verbose=True):
    """
    Machin's formula: π/4 = 4*arctan(1/5) - arctan(1/239)
    this one is pretty old but works well
    """
    if verbose:
        print(f"computing pi to {n_digits} digits with machin's formula...")
    
    # Set precision
    getcontext().prec = n_digits + 10
    
    def arctan(x, num_terms=500):
        """arctan using taylor series"""
        power = x
        result = power
        for n in range(1, num_terms):
            power *= -x * x
            result += power / (2 * n + 1)
        return result
    
    if verbose:
        print("  calculating arctan(1/5)...")
    
    term1 = 4 * arctan(Decimal(1) / Decimal(5))
    
    if verbose:
        print("  calculating arctan(1/239)...")
    
    term2 = arctan(Decimal(1) / Decimal(239))
    
    pi_over_4 = term1 - term2
    pi_value = 4 * pi_over_4
    
    pi_string = str(pi_value)[:n_digits + 2]
    
    if verbose:
        print()
        print("done!")
        print(f"pi = {pi_string}")
    
    return pi_string


def compute_pi_simple_spigot(n_digits=33, verbose=True):
    """
    simpler spigot algorithm 
    """
    if verbose:
        print(f"computing pi to {n_digits} digits with spigot algorithm...")
    
    def generate_pi_digits(n):
        """generates n digits"""
        q, r, t, k, m, x = 1, 0, 1, 1, 3, 3
        digits = []
        
        iteration = 0
        # keep going until we have n+1 digits (including the "3")
        while len(digits) < n + 1:
            if verbose and iteration % 20 == 0:
                print(f"  iteration {iteration}, generated {len(digits)} digits so far...")
            
            if 4 * q + r - t < m * t:
                digits.append(m)
                q, r, t, k, m, x = (
                    10*q, 10*(r-m*t), t, k, (10*(3*q+r))//t - 10*m, x
                )
            else:
                q, r, t, k, m, x = (
                    q*k, (2*q+r)*x, t*x, k+1, (q*(7*k+2)+r*x)//(t*x), x+2
                )
            
            iteration += 1
            
            # safety check to prevent infinite loop
            if iteration > 10000:
                print("  warning: too many iterations, stopping")
                break
        
        return digits
    
    digits = generate_pi_digits(n_digits)
    
    if len(digits) > 0:
        pi_string = str(digits[0]) + '.' + ''.join(map(str, digits[1:]))
    else:
        pi_string = ""
    
    if verbose:
        print()
        print("done!")
        print(f"pi = {pi_string}")
    
    return pi_string


def verify_result(computed_pi, n_digits=33):
    """
    check if we got the right answer
    """
    # known digits for checking
    known_pi = "3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679"
    
    expected = known_pi[:min(len(computed_pi), len(known_pi))]
    
    print()
    print("checking answer...")
    print(f"what we got:  {computed_pi}")
    print(f"should be:    {expected[:len(computed_pi)]}")
    
    match_count = 0
    for c, e in zip(computed_pi, expected):
        if c == e:
            match_count += 1
        else:
            break
    
    if computed_pi[:len(expected)] == expected[:len(computed_pi)]:
        print("digits match")
    else:
        print(f"uh oh, only matched {match_count} characters")
        for i, (c, e) in enumerate(zip(computed_pi, expected)):
            if c != e:
                print(f"  difference at position {i}: got '{c}' but expected '{e}'")
                break
    print()


if __name__ == "__main__":
    print("\npi calculator - testing different methods\n")
    
    # spigot method
    print("method 1: spigot algorithm")
    result1 = compute_pi_simple_spigot(n_digits=33, verbose=True)
    verify_result(result1, n_digits=33)
    
    print()
    
    # machin's formula
    print("method 2: machin's formula")
    result2 = compute_pi_machin(n_digits=33, verbose=True)
    verify_result(result2, n_digits=33)
    
    print("all done!\n")