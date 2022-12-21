#!/usr/bin/env python
from time import perf_counter

def main():
    with open('puzzle_input.txt', 'r') as f:
        input_lines = f.read().splitlines()

    monkeys = dict(line.split(':') for line in input_lines)
    waiting = {m: e.strip() for m, e in monkeys.items() if len(e) > 8}
    yelling = {m: int(n) for m, n in monkeys.items() if len(n) <= 8}

    while waiting:
        to_remove = []
        for name, eq in waiting.items():
            m_1 = eq[:4]
            m_2 = eq[7:]
            if not all(m in yelling for m in [m_1, m_2]):
                continue
            result = eval(f'{yelling[m_1]}{eq[5]}{yelling[m_2]}')
            if name == 'root':
                print('Root yells:', int(result))
                return
            yelling[name] = result
            to_remove.append(name)

        for monkey in to_remove:
            del waiting[monkey]

if __name__ == "__main__":
    start = perf_counter()
    main()
    end = perf_counter()
    print('Completed in:', round((end - start) * 1000, 2), 'ms')
