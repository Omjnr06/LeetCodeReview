# Given an array of integers heights representing the 
#  histogram's bar height where the width of each bar is 1, return the area of the largest rectangle in the histogram.

def longestRectangle(heights):
    maxArea = 0
    stack = [] # (index,height)

    for x in range(len(heights)):
        start = x
        while stack and stack[x][1] > heights[x]:
            index, height = stack.pop()
            maxArea = max(maxArea, (height * (x - index)))
            start = index
        stack.append((start,heights[x]))

    for i,h in stack:
        maxArea = max(maxArea, (h * (len(stack)- i)))

    return maxArea