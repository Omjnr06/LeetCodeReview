# Number 1: Longest Consecutive Sequence
# Given an unsorted array of integers `nums`, return *the length of the longest consecutive elements sequence.*

# You must write an algorithm that runs in `O(n)` time.

def LongestSequence(nums):

    numsSet = set(nums)
    count = 0

    for x in numsSet:
        if x - 1 not in numsSet:
            length = 1

        while x + length in numsSet:
            length += 1
        
        count = max(count,length)

    return count

# Number 2: Valid SUdoku
# Determine if a 9 x 9 Sudoku board is valid. Only the filled cells need to be validated according to the following rules:
# Each row must contain the digits 1-9 without repetition.
# Each column must contain the digits 1-9 without repetition.
# Each of the nine 3 x 3 sub-boxes of the grid must contain the digits 1-9 without repetition.
# Note:

# A Sudoku board (partially filled) could be valid but is not necessarily solvable.
# Only the filled cells need to be validated according to the mentioned rules.

from collections import defaultdict
def ValidSudoku(board):

    rows = defaultdict(set())
    cols = defaultdict(set())
    squares = defaultdict(set())

    for r in range(len(board)):
        for c in range(len(board[0])):

            if board[r][c] == ".":
                continue

            if board[r][c] in rows[r] or board[r][c] in cols[c] or board[r][c] in squares[(r//3,c//3)]:
                return False
            
            rows[r].add(board[r][c])
            cols[c].add(board[r][c])
            squares[(r//3,c//3)].add(board[r][c])
    return True


# Number 3: Valid Parentheses
# Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input string is valid.

# An input string is valid if:

# 1. Open brackets must be closed by the same type of brackets.
# 2. Open brackets must be closed in the correct order.
# 3. Every close bracket has a corresponding open bracket of the same type.

def ValidParentheses(s):
    stack = []
    bracketsHash = {"}":"{","]":"[",")":"("}

    for x in s:
        if stack and x in bracketsHash:
            if stack[-1] == bracketsHash[x]:
                stack.pop()
            else:
                return False
        else:
            stack.append(x)
    
    if stack:
        return False
    
    return True

# NUmber 4 Daily Temperatures
# Given an array of integers temperatures represents the daily temperatures, 
# return an array answer such that answer[i] is the number of days you have to wait after the ith day to get 
# a warmer temperature. If there is no future day for which this is possible, keep answer[i] == 0 instead.

def DailyTemperatures(temperatures):

    result = [0] * (len(temperatures))
    stack = []

    for x in range(len(temperatures)):
        while stack and temperatures[x] > temperatures[stack[-1]]:
            currentIndex = stack.pop()
            result[x] = x - currentIndex
        stack.append(currentIndex)

    return result




