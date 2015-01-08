# -*- coding: utf-8 -*-
r"""
This is a collection of math tools I find useful.

Much inspiration was drawn from Peter Norvig's Udacity 
class "Design of Computer Programs" 
(www.https://www.udacity.com/course/viewer#!/c-cs212/)

Created on Thu Jan 01 17:40:08 2015
@author: J

"""
import numpy as np
from MyDevTools.MyDecorator import decorator
from MyDevTools.MyAnalysisTools import histogram
from MyDevTools.MyPerformanceTools import unpack
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

@timeIt
def main():
    test()
#    for i in xrange(1000):
#    values = 11,12,13,14,15,17,19,20
#    print have_common_factors(*values)
#    a = list(get_factors(*values))
    
    print sorted(list(get_factors(20)))
#    print get_lcm(*values, stop_value=100000, common=True)
#    printStuff(get_factors(*values, prime=True, common=True))
#    print '=============='
#    print get_gcf(*values, prime=True)
#    print get_lcm(*values)
#    printStuff(res)
#    print res

def test():
    assert not is_prime(8)
    assert not is_prime(4)
    assert is_prime(4)

@decorator
def makeInt(f):
    """Forces the function to return an int"""
    def wrapper(*args,**kw):
        return int(f(*args,**kw))
    return wrapper

@timeIt
def have_common_factors(*nums):
    vals = [set(get_factors(i, common=True)) for i in nums]
    lens = map(lambda x: len(x), vals)
    index = lens.index(max(lens))
    master = vals.pop(index)
    vals = reduce(lambda x,y: x | y, vals)
    return True if vals - master == set([]) else False

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
    """Returns the greatest common factor of the numbers given.
    
    Parameters
    ----------
    
    prime --
        returns prime gcf"""
    return max(get_factors(*values, **kw))

def get_lcm(*values, **kw):
    """Returns least common multiple of values
    
    Key Word Parameters
    -------------------
    """
    return get_multiples(*values, common=True).next()

#@timeIt    
def get_factors(*nums, **kw):
    """Factors inputs, returns iterator.
        
        Parameters
        ----------
        
        nums : *ints; or list or tuple of ints
            The numbers to be factored
            
        common : boolean, optional
            Output yields only common factors
        
        prime : boolean, optional
            Output yields only prime factors
        """
    common = kw.get('common',False)
    prime = kw.get('prime',False)
    def factor_(n):    
        assert isinstance(n,int)
        h = has_fac = np.vectorize(lambda x: n % x == False)        
        p = possible_factors = np.array(xrange(1,n+1))
        v = h(p)
        i = indicies = p[v]
        return frozenset(i)
    factor_sets = [factor_(n) for n in nums]
    assert isinstance(factor_sets[0], frozenset)
    factors = reduce(lambda x,y: x | y, factor_sets)
    common_factors = reduce(lambda x,y: x & y, factor_sets)
    res = common_factors if common else factors
    if prime:
        fast_primes = np.vectorize(lambda x: is_prime(x))
        _nums = np.array([num for num in res])      
        try:
            return _nums[fast_primes(_nums)]        
        except IndexError:
            print "Error"
            return res
    return (factor for factor in res)


def is_prime(n):
    """Tests to see if n is prime"""
    
    if n in (1, 2, 3):
        return True
       
    if not n % 2:
        return False
    nums = np.array(xrange(3,n,2))    
    find_quotients = np.vectorize(lambda divisor: n % divisor == 0)
    return not nums[find_quotients(nums)].any()
           
def get_multiples(*nums, **kw):
        """Returns iterator of multiples of nums
        
        Parameters
        ----------
        *args
        nums --
            *list or *tuple or ints

        **kw
        common --
            returns only 
            
        """
        
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
    """Returns true if num is multiple of nums
    
    Parameters
    ----------
    num --
        int
        
    nums --
        list or tuple of ints"""
    return True if sum(map(lambda x: num % x, nums)) == 0 else False

def is_common_factor(num, nums):
    """Returns true if num is factor of nums
    
    Parameters
    ----------
    num --
        int
        
    nums --
        list or tuple of ints"""
    return True if sum(map(lambda x: x % num, nums)) == 0 else False
    
def test():
    assert is_common_multiple(30,(5,10,15))
    assert is_common_factor(2,(32,24))
    assert is_common_factor(1,(32,24))
#def get_lcm()
    
            
if __name__ == '__main__':
    test()
    main()