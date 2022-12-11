#!/usr/bin/env python

class Monkey:
    def __init__(self,
            items: list[int],
            operation: str,
            test: int,
            throw_list: list[int]):
        self.items = items
        self.operation = operation
        self.test = test
        self.throw_list = throw_list
        self.inspected = 0

    def inspect(self):
        self.inspected += 1
        old = self.items[0]
        self.items[0] = eval(self.operation)
        self.items[0] //= 3
        if self.items[0] % self.test:
            return self.throw_list[1]
        else:
            return self.throw_list[0]

def main():
    with open('puzzle_input.txt', 'r') as f:
        input_lines = f.read().splitlines()

    monkeys: list[Monkey] = []
    throw_list = []
    for line in input_lines:
        match line.split():
            case ['Starting', 'items:', *i]:
                items = [int(item.strip(',')) for item in i]
            case ['Operation:', 'new', '=', *o]:
                operation = ' '.join(o)
            case ['Test:', 'divisible', 'by', t]:
                test = int(t)
            case ['If', 'true:', 'throw', 'to', 'monkey', tt]:
                throw_list.append(int(tt))
            case ['If', 'false:', 'throw', 'to', 'monkey', tt]:
                throw_list.append(int(tt))
                monkeys.append(Monkey(items, operation, test, throw_list))
                throw_list = []

    for _ in range(20):
        for m in monkeys:
            while m.items:
                throw_to = m.inspect()
                monkeys[throw_to].items.append(m.items.pop(0))

    inspected_list = [m.inspected for m in monkeys]
    inspected_list.sort(reverse=True)
    monkey_business = inspected_list[0] * inspected_list[1]

    print('Amount of monkey business:', monkey_business)

if __name__ == "__main__":
    main()
