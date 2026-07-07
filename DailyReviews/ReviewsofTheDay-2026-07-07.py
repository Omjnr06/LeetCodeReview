# Number 1: MinStack
# Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.
# Implement the MinStack class:
# MinStack() initializes the stack object.
# void push(int value) pushes the element value onto the stack.
# void pop() removes the element on the top of the stack.
# int top() gets the top element of the stack.
# int getMin() retrieves the minimum element in the stack.
# You must implement a solution with O(1) time complexity for each function.

class MinStack:
    def __init__(self):
        self.stack = []
        self.minStack  = []
    
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
        return self.stack[-1]
    
    def getMin(self):
        return self.minStack[-1]
    
# Number 2: Daily Temperatures
# Given an array of integers temperatures represents the daily temperatures, 
# return an array answer such that answer[i] is the number of days you have to 
# wait after the ith day to get a warmer temperature. If there is no future day for which this is possible, 
# keep answer[i] == 0 instead.

def DailyTemps(temperatures):

    result = [0] * (len(temperatures))
    stack = []

    for x in range(len(temperatures)):
        while stack and temperatures[x] > temperatures[stack[-1]]:
            currentIndex = stack.pop()
            result[x] = x - currentIndex
        stack.append(currentIndex)

    return result

# Number 3: Encode and Decode Strings
#Design an algorithm to encode a list of strings to a string. 
# The encoded string is then sent over the network and is decoded back to the original list of strings.

def encoding(strings):
    result = ""
    for x in strings:
        result = result + len(x) + "*" + x

    return result

def decoding(strings):
    result = []
    i = 0
    while i < len(strings):
        j = i

        while strings[j] != "*":
            j +=1

        length = int(strings[i:j])
        i + j + 1
        j = i + length

        result.append(strings[i:j])
        i = j
    return result









