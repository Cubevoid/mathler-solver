import itertools
from tqdm import tqdm

GUESS_LENGTH = 6

print('Enter goal number: ')
goal = int(input())

print('Enter previous guess (empty for none): ')
prev_guess = input()

yellow = []  # tuples are (value, index) where index is the known WRONG index
grey = []
green = []

if prev_guess:
    if len(prev_guess) != GUESS_LENGTH:
        raise ValueError('Invalid previous guess')

    print('Enter result for previous guess (G=green, Y=yellow, X=grey): ')
    result = input()
    if len(result) != GUESS_LENGTH:
        raise ValueError('Invalid result')

    for i in range(len(result)):
        if result[i] == 'G':
            green.append((prev_guess[i], i))
        elif result[i] == 'Y':
            yellow.append((prev_guess[i], i))
        elif result[i] == 'X':
            grey.append(prev_guess[i])
        else:
            raise ValueError('Invalid result')

alphabet = '1234567890*/+-'
ops = '+-*/'
digits = '0123456789'
perms = itertools.product(*([alphabet] * 6))  # permutations with replacement

answers = []

print('\nComputing possible answers...')

for permutation in tqdm(perms):
    exp = "".join(permutation)

    invalid = False

    # Test for invalid mathler expressions
    for i in range(len(exp) - 1):
        # No two operators in a row (not sure if this is right)
        if exp[i] in ops and exp[i+1] in ops:
            invalid = True
            break

        # No leading 0's
        elif exp[i] == '0' and exp[i+1] in digits:
            invalid = True
            break
    
    for g in green:
        if exp[g[1]] != g[0]:
            invalid = True

    for y in yellow:
        if y[0] not in exp:
            invalid = True
        if exp[y[1]] == y[0]:
            invalid = True

    for g in grey:
        if g in exp:
            invalid = True
    
    if not invalid:
        try:
            result = eval(exp)
            if result == goal:
                answers.append(exp)
        except Exception:
            pass

print('\n========== POSSIBLE ANSWERS ==========')
for a in answers:
    print(a)