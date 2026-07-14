# Number 1: Min Stack
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
        self.minStack = []

    def push(self,value):

        self.stack.append(value)

        if self.minStack:
            value = min(value, self.minStack[-1])
        else:
            value = value

        self.minStack.append(value)

    def pop(self):
        self.minStack.pop()
        self.stack.pop()

    def top(self):
        return self.stack[-1]
    
    def getMin(self):
        return self.minStack[-1]
    

# Number 2: Encode and Decode Strings
# Design an algorithm to encode a list of strings to a string. 
# The encoded string is then sent over the network and is decoded back to the original list of strings.

def encode(strings):
    result = ""
    for x in strings:
        result = result + len(x) + "*" + x
    
    return result

def decode(string):
    result = []
    i = 0
    while i < len(string):
        j = i

        while string[j] != "*":
            j += 1

        length = int(string[i:j])

        i = j + 1
        j = length + i

        result.append(string[i:j])
        i = j
        i += 1
    return result

