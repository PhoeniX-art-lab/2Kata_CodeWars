number_stack = []
operations_stack = []

numbers = tuple(chr(i) for i in range(48, 58))
parentheses = ('-(', '(')


def priority(value):
    match value:
        case "+" | "-":
            return 1
        case "*" | "/":
            return 2


def grammar_check(expression):
    working_list = []
    i = 0
    while i < len(expression):
        temp_number = ''
        if expression[i] == '-' and expression[i + 1] == '(':
            temp_number += expression[i]
            temp_number += expression[i + 1]
            working_list.append(temp_number)
            i += 2
            continue
        if expression[i] in numbers or expression[i] == '-' or expression[i] == '.':
            temp_number += expression[i]
            i += 1
            try:
                while expression[i] in numbers or expression[i] == '.':
                    temp_number += expression[i]
                    i += 1
            except IndexError:
                break
            finally:
                working_list.append(temp_number)
        if expression[i] not in numbers and expression[i] != ' ':
            working_list.append(expression[i])
        i += 1

    for i in range(len(working_list)):
        try:
            working_list[i] = float(working_list[i])
        except ValueError:
            pass

    return working_list


def calculate():
    match operations_stack.pop(-1):
        case '*':
            return number_stack.pop(-2) * number_stack.pop(-1)
        case '/':
            return number_stack.pop(-2) / number_stack.pop(-1)
        case '+':
            return number_stack.pop(-2) + number_stack.pop(-1)
        case '-':
            return number_stack.pop(-2) - number_stack.pop(-1)
        case _:
            return 0


def calc(expression):
    number_stack.clear()
    operations_stack.clear()
    working_list = grammar_check(expression)
    i = 0
    while i < len(working_list):
        if type(working_list[i]) is float:
            number_stack.append(working_list[i])
        else:
            if len(operations_stack) == 0:
                operations_stack.append(working_list[i])
            else:
                if working_list[i] == ')':
                    while operations_stack[-1] not in parentheses:
                        number_stack.append(calculate())
                    if operations_stack[-1] == '-(':
                        number_stack.append(-number_stack.pop(-1))
                    operations_stack.pop(-1)
                elif working_list[i] in parentheses or operations_stack[-1] in parentheses or priority(
                        working_list[i]) > priority(operations_stack[-1]):
                    operations_stack.append(working_list[i])
                elif priority(working_list[i]) <= priority(operations_stack[-1]):
                    while operations_stack[-1] not in parentheses and priority(working_list[i]) <= priority(
                            operations_stack[-1]):
                        number_stack.append(calculate())
                        if len(operations_stack) == 0:
                            break
                    continue

        i += 1
    while operations_stack:
        number_stack.append(calculate())

    return sum(number_stack)
  
