# Number 1: Valid Parentheses
# Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input string is valid.
# An input string is valid if:
# 1. Open brackets must be closed by the same type of brackets.
# 2. Open brackets must be closed in the correct order.
# 3. Every close bracket has a corresponding open bracket of the same type.

def ValidParentheses(str):

    bracketsHash = {"}":"{",")":"(","]":"["}
    stack = []

    for x in str:
        if x in bracketsHash:
            if stack and stack[-1] == bracketsHash[x]:
                stack.pop()
            else:
                return False
            
        else:
            stack.append(x)
    
    if stack:
        return False
    
    return True


# Number 2: Daily Temperatures
# Given an array of integers temperatures represents the daily temperatures, 
# return an array answer such that answer[i] is the number of days you have to wait after the ith day to get a 
# warmer temperature. If there is no future day for which this is possible, keep answer[i] == 0 instead.

def DailyTemperatures(array):

    result = [0] * len(array)
    stack = []

    for x in range(len(array)):
        while stack and array[x] > array[stack[-1]]:
            currIndex = stack.pop()
            result[x] = x - currIndex
        stack.append(currIndex)

    return result

# Number 3: MinStack
# Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.
# Implement the MinStack class:
# MinStack() initializes the stack object.
# void push(int value) pushes the element value onto the stack.
# void pop() removes the element on the top of the stack.
# int top() gets the top element of the stack.
# int getMin() retrieves the minimum element in the stack.
# You must implement a solution with O(1) time complexity for each function.

def _init_(self):
    self.stack = []
    self.minStack = []

def push(self,value):
    self.stack.append(value)

    if self.minStack:
        value = min(value, self.minStack[-1])
    else:
        value = value

    self.minStack.append(value)

def pop(self):
    self.stack.pop()
    self.minStack.pop()

def top(self):
    self.stack[-1]

def getMin(self):
    self.minStack[-1]
    
            
# Number 4: Encode and Decode Strings
# Design an algorithm to encode a list of strings to a string. 
# The encoded string is then sent over the network and is decoded back to the original list of strings.

def encode(array):
    result = ""
    for string in array:
        result = result + len(string) + "*" + string
    
    return result

def decoding(string):
    result = []
    i = 0

    while i < len(string):
        j = i
        while string[j] != "*":
            j += 1

        length = int(string[i:j])
        i = j + 1
        j = i + length

        result.append(str[i:j])

        i = j
    
    return result

            
