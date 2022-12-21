#!/usr/bin/env python
import sympy as sy
from time import perf_counter

def main():
    with open('puzzle_input.txt', 'r') as f:
        input_lines = f.read().splitlines()

    monkeys = dict(line.split(':') for line in input_lines)
    waiting = {m: e.strip() for m, e in monkeys.items() if len(e) > 8}
    yelling = {m: int(n) for m, n in monkeys.items() if len(n) <= 8}

    root_eq = waiting['root'].split()
    root_eq[1] = '='
    waiting['root'] = ' '.join(root_eq)

    next_name = 'humn'
    name_chain = ['humn']
    while next_name != 'root':
        for name, eq in waiting.items():
            if not next_name in eq:
                continue
            next_name = name
            name_chain.append(name)
            break

    eq_chain: list[str] = []
    while waiting:
        to_remove = []
        for name, eq in waiting.items():
            m_1 = eq[:4]
            m_2 = eq[7:]
            if not all(m in yelling for m in [m_1, m_2]):
                continue
            if m_1 == name_chain[0]:
                eq_chain.append(f'(x{eq[5]}{yelling[m_2]})')
                name_chain.pop(0)
            elif m_2 == name_chain[0]:
                eq_chain.append(f'({yelling[m_1]}{eq[5]}x)')
                name_chain.pop(0)
            if name == 'root':
                result = eq
            else:
                result = int(eval(f'{yelling[m_1]}{eq[5]}{yelling[m_2]}'))
            yelling[name] = result
            to_remove.append(name)

        for monkey in to_remove:
            del waiting[monkey]

    humn_eq = eq_chain.pop(0)
    for eq in eq_chain:
        humn_eq = eq.replace('x', humn_eq)
    humn_eq = 'Eq'+humn_eq.replace('=', ',')

    print('I yell:', sy.solve(sy.sympify(humn_eq))[0])

if __name__ == "__main__":
    start = perf_counter()
    main()
    end = perf_counter()
    print('Completed in:', round((end - start) * 1000, 2), 'ms')
