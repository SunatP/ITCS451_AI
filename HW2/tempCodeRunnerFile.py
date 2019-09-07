

# def Action(state: EightPuzzleState, i: int, j: int):
#     possibleAction = copy.deepcopy(state.action_space)

#     # row_upper = i - 1
#     if i - 1 < 0:
#         possibleAction.remove('u')

#     # row_under = i + 1
#     if i + 1 > len(state.board) - 1:
#         possibleAction.remove('d')

#     # col_left = j - 1
#     if j - 1 < 0:
#         possibleAction.remove('l')

#     # col_right = j + 1
#     if j + 1 > len(state.board[0]) - 1:
#         possibleAction.remove('r')

#     return possibleAction
#     pass
