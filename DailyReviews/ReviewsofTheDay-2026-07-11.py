# Number 1: Car Fleet:
# There are `n` cars at given miles away from the starting mile 0, traveling to reach the mile `target`.
# You are given two integer arrays `position` and `speed`, both of length `n`, where `position[i]` is the starting mile of the `ith` car and `speed[i]` is the speed of the `ith` car in miles per hour.
# A car cannot pass another car, but it can catch up and then travel next to it at the speed of the slower car.
# A **car fleet** is a single car or a group of cars driving next to each other. The speed of the car fleet is the **minimum** speed of any car in the fleet.
# If a car catches up to a car fleet at the mile `target`, it will still be considered as part of the car fleet.
# Return the number of car fleets that will arrive at the destination.

def carFleet(target,position,speed):
    pairs = sorted(zip(position,speed),reverse=True)
    stack = []

    for p,s in pairs:
        stack.append(float(target-p)/s)
        if len(stack) >= 2 and stack[-1] <= stack[-2]:
            stack.pop()

    return len(stack)

# Number 2: Daily Temperatures
# Given an array of integers temperatures represents the daily temperatures, return an array answer such that answer[i] 
# is the number of days you have to wait after the ith day to get a warmer temperature. 
# If there is no future day for which this is possible, keep answer[i] == 0 instead.

def DailyTemperatures(temperatures):
    result = [0] * len(temperatures)
    stack = []

    for x in range(len(temperatures)):
        while stack and temperatures[x] > temperatures[stack[-1]]:
            currentIndex = stack.pop()
            result[x] = x - currentIndex
        stack.append(currentIndex)
    return result


# Number 3: Postfix Notation
# You are given an array of strings `tokens` that represents an arithmetic expression in a Reverse Polish Notation.
# Evaluate the expression. Return *an integer that represents the value of the expression*.
# **Note** that:
# - The valid operators are `'+'`, `'-'`, `'*'`, and `'/'`.
# - Each operand may be an integer or another expression.
# - The division between two integers always **truncates toward zero**.
# - There will not be any division by zero.
# - The input represents a valid arithmetic expression in a reverse polish notation.
# - The answer and all the intermediate calculations can be represented in a **32-bit** integer.

def RPN(tokens):
    stack = []

    for x in tokens:
        if x == "+":
            stack.append(stack.pop() + stack.pop())
        elif x == "*":
            stack.append(stack.pop() * stack.pop())
        elif x == "-":
            a,b = stack.pop(), stack.pop()
            stack.append(b-a)
        elif x == "/":
            a,b = stack.pop(),stack.pop()
            stack.append(int(float(b)/a))
        else:
            stack.append(int(x))
    return stack[0]

# Number 3: TopKFreqElements
# Given an integer array nums and an integer k, return the k most frequent elements. You may return the answer in any order.

import heapq
def TopKFreqElements(nums, k):

    hashmap = {}
    result = []

    for x in range(len(nums)):
        if x in hashmap:
            hashmap[x] = 1 + hashmap.get(nums,0)

    heap = []

    for x in hashmap.keys():
        heapq.heappush(heap, (hashmap[x],x))
        if len(heap) > k:
            heapq.heappop(heap)

    for x in range(k):
        result.append(heapq.heappop(heap)[1])

    return result
