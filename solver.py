import itertools
import warnings
import math
from random import shuffle

warnings.filterwarnings("ignore")


def main():
    diff = input('Enter difficulty (easy, medium, hard): ')
    if diff[0].lower() == 'e':
        guess_length = 5
        max_op_count = 1
    elif diff[0].lower() == 'm':
        guess_length = 6
        max_op_count = 2
    elif diff[0].lower() == 'h':
        guess_length = 8
        max_op_count = 3
    else:
        raise ValueError('Invalid difficulty')

    goal = int(input('Enter goal number: '))

    prev_guess = input('Enter previous guess (empty for none): ')

    alphabet = '1234567890*/+-'
    if guess_length == 8:  # hard mode
        alphabet += '()'
    ops = '+-*/'
    digits = '0123456789'

    # Index is symbol and value is list of indices in guess
    green = {}
    yellow = {}
    grey = set()

    for char in alphabet:
        green[char] = []
        yellow[char] = []

    if prev_guess:
        if len(prev_guess) != guess_length or eval(prev_guess) != goal:
            raise ValueError('Invalid previous guess')

        result = input('Enter result for previous guess (G=green, Y=yellow, X=grey): ')

        if len(result) != guess_length:
            raise ValueError('Invalid result')

        for i in range(len(result)):
            if result[i] == 'G':
                green[prev_guess[i]].append(i)
            elif result[i] == 'Y':
                yellow[prev_guess[i]].append(i)
            elif result[i] == 'X':
                grey.add(prev_guess[i])
            else:
                raise ValueError('Invalid result')

    # Lower and upper bounds for counts of characters in the answer
    alphabet_min_max = {}
    for char in alphabet:
        min = 0
        max = math.inf
        min += len(green[char])
        min += len(yellow[char])

        if char in grey:
            max = min

        alphabet_min_max[char] = (min, max)

    # Remove symbols we know aren't in the answer
    alphabet = list(alphabet)
    shuffle(alphabet)
    for char in alphabet:
        if alphabet_min_max[char][1] == 0:
            alphabet.remove(char)
    alphabet = "".join(alphabet)

    print(f'\nPossible symbols: {alphabet}')

    perms = itertools.product(*[alphabet] * guess_length)  # permutations with replacement

    print('\n========== POSSIBLE ANSWERS ==========')

    for permutation in perms:
        exp = "".join(permutation)

        invalid = False

        # Test for invalid mathler expressions
        for i in range(len(exp) - 1):
            # No two operators in a row (not sure if this is right)
            if exp[i] in ops and exp[i + 1] in ops:
                invalid = True
                break
            # No leading 0's
            if exp[i] == '0' and exp[i + 1] in digits:
                invalid = True
                break

        if not invalid and diff[0].lower() == 'h' and not matched(exp):
            invalid = True

        # Check number of operators
        op_count = 0
        for char in exp:
            if char in ops:
                op_count += 1
                if op_count > max_op_count:
                    invalid = True
                    break

        # Check green boxes
        if not invalid:
            for g in green.keys():
                for i in green[g]:
                    if exp[i] != g:
                        invalid = True
                        break

        # Check yellow boxes
        if not invalid:
            for y in yellow.keys():
                for i in yellow[y]:
                    if exp[i] == y:
                        # Cannot have that symbol on yellow space
                        invalid = True
                        break
                if yellow[y] and exp.count(y) - len(green[y]) != len(yellow[y]):
                    # Number of yellows doesn't match
                    invalid = True
                    break

        if not invalid:
            for g in grey:
                if exp.count(g) - len(green[g]) - len(yellow[g]) > 0:
                    invalid = True
                    break

        if not invalid:
            try:
                result = eval(exp)
                if result == goal:
                    print(exp)
            except Exception:
                pass


# https://stackoverflow.com/a/38834005/13176711
def matched(str):
    count = 0
    for i in str:
        if i == "(":
            count += 1
        elif i == ")":
            count -= 1
        if count < 0:
            return False
    return count == 0


if __name__ == '__main__':
    main()