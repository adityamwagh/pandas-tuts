def get_operations(t, x, y):
    # Function to count how many times a specific operation is used in a sequence
    def count_ops(seq, op):
        return sum([int(s.split()[-1]) for s in seq if s.startswith(op)])

    # Initialize DP array. Each entry contains a tuple (number of operations, operation list)
    # We use float('inf') as a placeholder for unreachable values.
    dp = [(float('inf'), []) for _ in range(t+1)]
    dp[1] = (0, [])

    for i in range(2, t+1):
        # If we can add x to get to i
        if i - x > 0 and dp[i-x][0] != float('inf'):
            add_ops = dp[i-x][1].copy()
            if add_ops and add_ops[-1].startswith("operator_add"):
                count = int(add_ops[-1].split()[-1])
                add_ops[-1] = f"operator_add {count + 1}"
            else:
                add_ops.append("operator_add 1")
            dp[i] = (dp[i-x][0] + 1, add_ops)

        # If we can multiply by y to get to i
        if i % y == 0 and dp[i//y][0] != float('inf'):
            mul_ops = dp[i//y][1].copy()
            if mul_ops and mul_ops[-1].startswith("operator_multiply"):
                count = int(mul_ops[-1].split()[-1])
                mul_ops[-1] = f"operator_multiply {count + 1}"
            else:
                mul_ops.append("operator_multiply 1")

            # Prioritize more multiplies and then fewer additions
            if (count_ops(mul_ops, "operator_multiply") > count_ops(dp[i][1], "operator_multiply")) or \
               (count_ops(mul_ops, "operator_multiply") == count_ops(dp[i][1], "operator_multiply") and
                count_ops(mul_ops, "operator_add") < count_ops(dp[i][1], "operator_add")):
                dp[i] = (dp[i//y][0] + 1, mul_ops)

    if dp[t][0] == float('inf'):
        return ["no_solution"]
    return dp[t][1]

# Test Cases
print(get_operations(54, 1, 3))  # ["operator_add 1", "operator_multiply 3"]
print(get_operations(3, 4, 4))   # ["no_solution"]
