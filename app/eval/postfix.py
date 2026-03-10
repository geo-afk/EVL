
class Postfix:

    def infix_to_postfix(expression):
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '%': 2}
        post_fix_output = ""
        stack = []

        for char in expression:
            # If an operand
            if char.isalnum():
                post_fix_output += char
            elif char == ' ':
                continue
            elif char == '(':
                stack.append(char)
            elif char == ')':
                while stack and stack[-1] != '(':
                    post_fix_output += stack.pop()
                stack.pop()
            # If an operator is found
            else:
                while stack and stack[-1] != '(' and precedence[stack[-1]] >= precedence[char]:
                    post_fix_output += stack.pop()
                stack.append(char)

        # Pop remaining operators
        while stack:
            post_fix_output += stack.pop()

        return post_fix_output

    def evaluate_postfix(post_result):
        stack = []

        for char in post_result:
            if char == ' ':
                continue
            if char.isdigit():
                stack.append(int(char))
            else:
                b = stack.pop()  # right operand
                a = stack.pop()  # left operand

                if char == '+':
                    stack.append(a + b)
                elif char == '-':
                    stack.append(a - b)
                elif char == '*':
                    stack.append(a * b)
                elif char == '/':
                    stack.append(a / b)
                elif char == '%':
                    stack.append(a % b)
        return stack[0]

# expression = "( 8 + 2 ) * ( 3 - 1 ) / 4"
# post_result = infix_to_postfix(expression)
# result = evaluate_postfix(post_result)
# print("Postfix:", post_result)
# print("Result:", result)