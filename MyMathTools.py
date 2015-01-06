# -*- coding: utf-8 -*-
r"""
This is a collection of math tools I find useful.

Much inspiration was drawn from Peter Norvig's Udacity 
class "Design of Computer Programs" 
(www.https://www.udacity.com/course/viewer#!/c-cs212/)

Created on Thu Jan 01 17:40:08 2015
@author: J

"""
from MyDevTools.MyDecorator import decorator
from MyDevTools.MyAnalysisTools import histogram
from MyDevTools.MyPerformanceTools import *
from MyDevTools.MyDebug import *
import itertools
import sys

import math

__all__ = [
            "makeInt",
            "root_",
            "has_factors",
            "get_greatest_factor",
            "get_gcf",
            "is_prime",
            "get_factors",
            "get_prime_factors",
            "get_greatest_factor"
        ]


def main():
    values = 14,21,28
    printStuff(get_multiples(*values, stop_value=10000, common=True))
    printStuff(get_factors(*values, prime=True, common=True))
    print '=============='
    print get_gcf(*values, prime=True)
    print get_lcm(*values)
#    printStuff(res)
#    print res
    
def recurse():
    recurse()
    #more_recursion!
    #more_recursion!



def not_recurse():
    return

@decorator
def makeInt(f):
    """Forces the function to return an int"""
    def wrapper(*args,**kw):
        return int(f(*args,**kw))
    return wrapper

@makeInt
def root_(n):
    """Returns the square root of n, rounded up."""
    return math.sqrt(n)+1
    
def has_factors(n, low=None, high=None):
    """Returns True if n is factorable in the specified range."""
    if n == 1: 
        raise MyDevTools.UnintendedUseError(n, "1 is prime")
    if not high: high = n+1
    if low < 2: low = 2    
    search_range = xrange(low, high)
    for num in search_range:
        if n % num == 0 and low < n/num < high:
            print num, n/num
            return True
    return False

def get_gcf(*values, **kw):
    """Returns the greatest common factor of the numbers given."""
    return max(get_factors(*values, **kw))

def get_lcm(*values, **kw):
    return get_multiples(*values, **kw).next()
    
def get_factors(*nums, **kw):
    """Returns all factors of n excluding n."""
    common = kw.get('common',False)
    prime = kw.get('prime',False)
    def factor_(n):    
        assert isinstance(n,int)
        possible_factors = (num for num in xrange(2,root_(n)))
        yield 1
        try:
            while possible_factors:
                p = possible_factors.next()
                q,r = divmod(n, p)        
                try:
                    p_not_a_factor = r != 0
                    assert p_not_a_factor
                except AssertionError:
                    yield p
                    yield q
        finally:
            yield n
    factors = combined_gen([factor_(num) for num in nums])
    common_factors = (factor for factor in factors 
                        if is_common_factor(factor, nums))
    res = common_factors if common else factors
    return ((factor for factor in res if is_prime(factor)) if prime
            else res)


def is_prime(n):
    """Tests to see if n is prime"""
    
    if n == 2: return True
    if n % 2 == 0: 
        return False
    root_n = int(math.sqrt(n))+1
    up_to_root_n = root_n
    quotients = map(lambda divisor: n % divisor, 
                    range(3, up_to_root_n))
    n_is_evenly_divisible = 0 in quotients
    return False if n_is_evenly_divisible else True

def get_n_ary_multiples(nums, stop=None):
    multiples = tuple([get_multiples_of(num, stop) for num in nums])
    return combine_gens(multiples)    
    
def get_multiples(*nums, **kw):
        
        common = kw.get('common',False)
        assert isinstance(common, bool)
    
        def _get_multiples_(n, **kw):
            stop_value = kw.get('stop_value')
            counter = 0
            while True:
                counter += 1
    #            print "counter: {}, n*counter: {}".format(counter, n*counter)
                multiple = n * counter
                if stop_value != None and multiple >= stop_value: break
                yield n * counter
                
        multiples = combined_gen([_get_multiples_(num, **kw) 
                                           for num in nums])
        common_multiples = (multiple for multiple in multiples
                        if is_common_multiple(multiple, nums))
        return common_multiples if common else multiples
        

def is_common_multiple(num, nums):
    return True if sum(map(lambda x: num % x, nums)) == 0 else False

def is_common_factor(num, nums):
    return True if sum(map(lambda x: x % num, nums)) == 0 else False
    
def test():
    assert is_common_multiple(30,(5,10,15))
    assert is_common_factor(2,(32,24))
    assert is_common_factor(1,(32,24))
#def get_lcm()
    
            
if __name__ == '__main__':
    test()
    main()