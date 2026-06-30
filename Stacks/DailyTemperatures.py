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
            