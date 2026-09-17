#!/usr/bin/env python3
"""
Tribonacci Constant Calculator (HPC OEIS Edition)
======================================================
Calculates Tribonacci Constant to exactly [N] significant digits 
using an extremely efficient Newton-Raphson iteration with gmpy2.
"""

import sys
import time
import argparse
import os

os.environ['MPMATH_GMPY2'] = '1'
import gmpy2
import mpmath

sys.set_int_max_str_digits(0)

def save_oeis_files(constant_name: str, digits_str: str, target_digits: int) -> None:
    """Saves the computed digits to a raw text file and an OEIS b-file."""
    clean_digits = digits_str.replace(".", "")[:target_digits]
    
    raw_filename = f"{constant_name}_{target_digits}_digits.txt"
    with open(raw_filename, "w", encoding="utf-8") as f:
        f.write(clean_digits)
    print(f"Saved raw digit output to {raw_filename}")

    b_filename = f"b_file_{constant_name}_{target_digits}.txt"
    with open(b_filename, "w", encoding="utf-8") as f:
        for idx, digit in enumerate(clean_digits, start=1):
            f.write(f"{idx} {digit}\n")
    print(f"Saved OEIS b-file output to {b_filename}")

def compute_tribonacci_constant_hpc(target_digits: int) -> str:
    """
    Calculates the Tribonacci Constant to exactly [target_digits] significant digits
    using an extremely efficient Newton-Raphson iteration with gmpy2.
    """
    if target_digits < 1:
        raise ValueError("Number of digits must be at least 1")

    try: 
        # Newton-Raphson using gmpy2 (extremely fast)
        # Precision in bits: (target_digits + 50) * log2(10)
        prec_bits = int((target_digits + 50) * 3.3219280948873626) + 100
        
        curr_prec = 53
        gmpy2.get_context().precision = curr_prec
        x = gmpy2.mpfr("1.8392867552141612")
        
        while curr_prec < prec_bits:
            curr_prec = min(curr_prec * 2, prec_bits)
            gmpy2.get_context().precision = curr_prec
            # Newton step for x^3 - x^2 - x - 1 = 0
            x2 = x * x
            f = x2 * x - x2 - x - 1
            df = 3 * x2 - 2 * x - 1
            x = x - f / df
            
        # Format to target_digits + 10 decimal places to be safe
        s = format(x, f".{target_digits + 10}f")
        clean_digits = s.replace(".", "")[:target_digits]
    except (ImportError, AttributeError, NameError):
        # Fallback to mpmath if gmpy2 is not fully functional
        dps_working = target_digits + 50
        mpmath.mp.dps = dps_working
        ctx = mpmath.mp
        # Analytical formula
        val = (ctx.mpf('1') + (ctx.mpf('19') - ctx.mpf('3')*ctx.sqrt(33))**(ctx.mpf('1')/3) + (ctx.mpf('19') + ctx.mpf('3')*ctx.sqrt(33))**(ctx.mpf('1')/3)) / 3
        val_str = ctx.nstr(val, dps_working)
        clean_digits = val_str.replace(".", "")[:target_digits]

    save_oeis_files("Tribonacci_Constant", clean_digits, target_digits)
    return clean_digits

def main() -> None:
    parser = argparse.ArgumentParser(description="HPC Tribonacci Constant OEIS Calculator")
    parser.add_argument("-n", "--digits", type=int, default=1000, help="Target digits (default: 1000)")
    args = parser.parse_args()

    t0 = time.time()
    _ = compute_tribonacci_constant_hpc(args.digits)
    t1 = time.time()

    print(f"Execution finished in {t1 - t0:.4f} seconds.")

if __name__ == "__main__":
    main()