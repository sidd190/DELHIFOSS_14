#!/usr/bin/env python3
"""Compare two defenses and attacks using strict dominance and worst-case loss."""
import argparse
import json
from fractions import Fraction as F


def solve(matrix):
    """Rows minimize defender loss; columns maximize it. Return pure-action facts."""
    if len(matrix) != 2 or any(len(row) != 2 for row in matrix):
        raise ValueError('Expected exactly two rows and two columns')
    m = [[F(str(x)) for x in row] for row in matrix]
    dominated_attacks = [dict(dominated=j, by=k) for j, k in ((0, 1), (1, 0))
                         if all(m[i][k] > m[i][j] for i in range(2))]
    dominated_defenses = [dict(dominated=i, by=k) for i, k in ((0, 1), (1, 0))
                          if all(m[k][j] < m[i][j] for j in range(2))]
    worst = [max(row) for row in m]
    best_rows = [i for i in range(2) if worst[i] == min(worst)]
    best_responses = [[j for j in range(2) if m[i][j] == worst[i]] for i in range(2)]
    saddle_points = [dict(defense=i, attack=j, loss=m[i][j])
                     for i in range(2) for j in range(2)
                     if m[i][j] == max(m[i]) and m[i][j] == min(m[k][j] for k in range(2))]
    return dict(dominated_attacks=dominated_attacks, dominated_defenses=dominated_defenses,
                row_worst_cases=worst, best_defenses=best_rows,
                worst_case_loss=min(worst), attacker_best_responses=best_responses,
                pure_saddle_points=saddle_points)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('values', nargs='*', help='four loss values in row order')
    parser.add_argument('--file', help='JSON file with a matrix key')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    try:
        if args.file and args.values:
            raise ValueError('Use values OR --file')
        if args.file:
            with open(args.file, encoding='utf-8') as f:
                matrix = json.load(f)['matrix']
        else:
            values = args.values or ['2', '8', '4', '5']
            if len(values) != 4:
                raise ValueError('Supply exactly four values: a b c d')
            matrix = [values[:2], values[2:]]
        result = solve(matrix)
    except (ValueError, TypeError, KeyError, ZeroDivisionError, OSError) as error:
        parser.error(str(error))
    if args.json:
        print(json.dumps(result, default=str, indent=2))
        return
    defenses, attacks = ['Fix API', 'Harden admin'], ['Attack API', 'Attack admin']
    print('LOSS TO THE SHOP\n')
    print('                       Attack API     Attack admin')
    for label, row in zip(defenses, matrix):
        print(f'{label:22} {str(row[0]):>10} {str(row[1]):>16}')
    print()
    for pair in result['dominated_attacks']:
        print(f"{attacks[pair['dominated']]} is strictly dominated by {attacks[pair['by']]}.")
    if not result['dominated_attacks']:
        print('Neither attack is strictly dominated.')
    for pair in result['dominated_defenses']:
        print(f"{defenses[pair['dominated']]} is strictly dominated by {defenses[pair['by']]}.")
    print('Row worst cases: ' + ', '.join(map(str, result['row_worst_cases'])))
    print('Choose: ' + ' or '.join(defenses[i] for i in result['best_defenses']))
    print(f"Worst-case loss: {result['worst_case_loss']}")
    if not result['pure_saddle_points']:
        print('No pure-strategy saddle point; this is a worst-case pure-action recommendation.')


if __name__ == '__main__':
    main()
