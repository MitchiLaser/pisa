#!/usr/bin/env python3


import argparse


def fib(n):
    return 0 if n == 0 else 1 if n <= 2 else fib(n - 1) + fib(n - 2)


def main():
    parser = argparse.ArgumentParser(description='Calculate the Fibonacci number of a given number')
    parser.add_argument('-n', '--number', type=int, required=True, help='The number to calculate the Fibonacci number for')
    args = parser.parse_args()

    fib_number = fib(args.number)
    print(f"The Fibonacci number of {args.number} is {fib_number}")


if __name__ == "__main__":
    main()
