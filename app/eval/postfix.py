class Postfix:

    @staticmethod
    def _is_number(token):
        """Check if a token is a number (integer or float)."""
        if not token:
            return False

        # Check each character
        has_digit = False
        has_decimal = False

        for i, char in enumerate(token):
            if char.isdigit():
                has_digit = True
            elif char == '.':
                # Decimal point can't be at start or end, and only one allowed
                if has_decimal or i == 0 or i == len(token) - 1:
                    return False
                has_decimal = True
            elif char == '-' and i == 0:
                # Negative sign only allowed at start
                continue
            else:
                return False

        return has_digit

    @staticmethod
    def _tokenize(expression):
        """Split expression into tokens (numbers, operators, parentheses)."""
        tokens = []
        current_token = ""

        i = 0
        while i < len(expression):
            char = expression[i]

            if char.isspace():
                # Space - end current token if any
                if current_token:
                    tokens.append(current_token)
                    current_token = ""
                i += 1

            elif char in '+-*/%()':
                # Operator or parenthesis - end current token and add operator
                if current_token:
                    tokens.append(current_token)
                    current_token = ""
                tokens.append(char)
                i += 1

            elif char.isdigit() or char == '.':
                # Start or continue a number
                current_token += char
                i += 1

            else:
                # Skip any other characters
                i += 1

        # Add the last token if any
        if current_token:
            tokens.append(current_token)

        return tokens

    @staticmethod
    def infix_to_postfix(expression):
        """Convert infix expression to postfix notation."""
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '%': 2}
        output = []
        stack = []

        tokens = Postfix._tokenize(expression)

        for token in tokens:
            if Postfix._is_number(token):
                # Number goes directly to output
                output.append(token)

            elif token == '(':
                stack.append(token)

            elif token == ')':
                # Pop until matching '('
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if stack:  # Remove the '('
                    stack.pop()

            else:  # Operator
                # Pop higher or equal precedence operators from stack
                while (stack and stack[-1] != '(' and
                       stack[-1] in precedence and
                       precedence[stack[-1]] >= precedence[token]):
                    output.append(stack.pop())
                stack.append(token)

        # Pop remaining operators
        while stack:
            output.append(stack.pop())

        return ' '.join(output)

    @staticmethod
    def evaluate_postfix(postfix_expr):
        """Evaluate a postfix expression."""
        stack = []
        tokens = postfix_expr.split()

        for token in tokens:
            if Postfix._is_number(token):
                # Convert to appropriate number type
                if '.' in token:
                    stack.append(float(token))
                else:
                    stack.append(int(token))

            else:  # Operator
                if len(stack) < 2:
                    raise ValueError("Not enough operands")

                b = stack.pop()
                a = stack.pop()

                if token == '+':
                    stack.append(a + b)
                elif token == '-':
                    stack.append(a - b)
                elif token == '*':
                    stack.append(a * b)
                elif token == '/':
                    if b == 0:
                        raise ZeroDivisionError("Division by zero")
                    stack.append(a / b)
                elif token == '%':
                    if b == 0:
                        raise ZeroDivisionError("Modulo by zero")
                    stack.append(a % b)
                else:
                    raise ValueError(f"Unknown operator: {token}")

        if len(stack) != 1:
            raise ValueError("Invalid expression")

        return stack[0]

    @staticmethod
    def get_result(expression):
        """Convert infix to postfix and evaluate."""
        postfix = Postfix.infix_to_postfix(expression)
        result = Postfix.evaluate_postfix(postfix)

        # Convert float to int if it's a whole number
        if isinstance(result, float) and result.is_integer():
            result = int(result)

        return result