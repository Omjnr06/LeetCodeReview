# Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.

def trappingRainwater(heights):

    l,r = 0, len(heights) - 1
    leftmax = heights[l]
    rightmax = heights[r]
    result = 0


    if not heights:
        return 0
    
    while l < r:
        if leftmax < rightmax:
            l += 1
            leftmax = max(leftmax, heights[l])
            result += leftmax - heights[l]

        else:
            r -= 1
            rightmax = max(rightmax, heights[r])
            result += rightmax - heights[r]


    return result