# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 21:06:07 2017

@author: steen_000
"""
import timeit

#==============================================================================
# input_list = range(100)
# def div_by_five(num):
#     if num % 5 == 0:
#         return True
#     else:
#         return False
# 
# xyz =(i for i in input_list if div_by_five(i))
#==============================================================================

print(timeit.timeit('''input_list = range(100)
def div_by_five(num):
    if num %5 == 0:
        return True
    else:
        return False

xyz =(i for i in input_list if div_by_five(i))''',number=5000))
