from clause import Clause

"""
For the queen problem, the only code you have to do is in this file.

You should replace

# your code here

by a code generating a list of clauses modeling the queen problem
for the input file.

You should build clauses using the Clause class defined in clause.py

Read the comment on top of clause.py to see how this works.
"""


def get_expression(size, queens=None):
    expression = []

    if queens != None:
        for queen in queens:
            c_required_queen_position = Clause(size)
            c_required_queen_position.add_positive(queen[0], queen[1])
            expression.append(c_required_queen_position)

    for i in range(size):
        c_at_least_one_per_column = Clause(size)
        for j in range(size):
            for k in range(j+1, size):
                c_at_most_one_per_column = Clause(size)
                c_at_most_one_per_column.add_negative(i, j)
                c_at_most_one_per_column.add_negative(i, k)
                expression.append(c_at_most_one_per_column)

                c_at_most_one_per_row = Clause(size)
                c_at_most_one_per_row.add_negative(j, i)
                c_at_most_one_per_row.add_negative(k, i)
                expression.append(c_at_most_one_per_row)

                if i < size-1 and i+k < size:
                    c_main_diag_left_top = Clause(size)
                    c_main_diag_left_top.add_negative(j, j+i)
                    c_main_diag_left_top.add_negative(k, k+i)
                    expression.append(c_main_diag_left_top)

                    c_main_diag_right_top = Clause(size)
                    c_main_diag_right_top.add_negative(j, size-1-j-i)
                    c_main_diag_right_top.add_negative(k, size-1-k-i)
                    expression.append(c_main_diag_right_top)

                    if i != 0:
                        c_main_diag_left_bottom = Clause(size)
                        c_main_diag_left_bottom.add_negative(j+i, j)
                        c_main_diag_left_bottom.add_negative(k+i, k)
                        expression.append(c_main_diag_left_bottom)

                        c_main_diag_right_bottom = Clause(size)
                        c_main_diag_right_bottom.add_negative(j+i, size-1-j)
                        c_main_diag_right_bottom.add_negative(k+i, size-1-k)
                        expression.append(c_main_diag_right_bottom)

            c_at_least_one_per_column.add_positive(i, j)

        expression.append(c_at_least_one_per_column)

    return expression


if __name__ == '__main__':
    expression = get_expression(4)
    for clause in expression:
        print(clause)
