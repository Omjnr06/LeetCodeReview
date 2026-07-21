# #1: ThreeSUM
# Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.
# Notice that the solution set must not contain duplicate triplets.

def ThreeSum(nums):
    
    result = []
    nums.sort()

    for x in range(len(nums)):
        l = x + 1
        r = len(nums) - 1

        if x > 0 and nums[x] == nums[x-1]:
            continue

        while l < r:
            threeSum = nums[x] + nums[l] + nums[r]
            if threeSum > 0:
                r -= 1
            elif threeSum < 0:
                l += 1

            else:
                result.append([nums[x],nums[l],nums[r]])
                l += 1

                while l < r and nums[l] == nums[l -1]:
                    l += 1
        
        return result
                
# #2: Longest Rectangle in Histogram
# Given an array of integers heights representing the  histogram's bar height where the width of each bar is 1, return the area of the largest rectangle in the histogram.
                
def longestRectangleinHistogram(heights):

    maxArea = 0
    stack = []

    for x in range(len(heights)):
        
        start = x

        while stack and stack[x][1] > heights[x]:
            index,height = stack.pop()
            maxArea = max(maxArea,height * (x - index))
            start = index
        
        stack.append(start,heights[x])


    for i,h in stack:
        maxArea = max(maxArea, h * (len(stack) - i))

    return maxArea


# #3: Valid Parentheses
# Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input string is valid.
# An input string is valid if:
# 1. Open brackets must be closed by the same type of brackets.
# 2. Open brackets must be closed in the correct order.
# 3. Every close bracket has a corresponding open bracket of the same type.

def validParentheses(s):
    stack = []
    bracketsHash = {")":"(","}":"{","]":"["}

    for x in s:
        if x in bracketsHash:
            if stack[-1] == bracketsHash[x]:
                stack.pop()
            else:
                return False
        stack.append(x)

    
    if stack:
        return False
    
    return True





