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
from MyDevTools.MyPerformanceTools import starunpack, memo
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

#@timeIt
def main():
    test()
#    print list(get_factors(4, complete_factorization=True, prime=True))
#    for i in range(1,21):
#        print i, list(get_factors(i, complete_factorization=True))
    accum = []
    for i in range(1,11):
        print i, prime_cut(i)
        accum.append(prime_cut(i))

    nums = {}    
    res = []    
    for lst in accum:
        for item in lst:
            try:
                nums[item]
                if lst.count(item) > nums[item]:
                    nums[item] = lst.count(item)
            except:
                nums[item] = lst.count(item)
    for k,v in nums.items():
        res += [k**v]
    print res
    print reduce(lambda x,y: x*y, res)
    
        
#    for i in xrange(1000):
#    values = 11,12,13,14,15,17,19,20
#    print have_common_factors(*values)
#    a = list(get_factors(*values))
    
#    print sorted(list(get_factors(20)))
#    assert not is_prime(4)
#    print is_prime(4)
##    assert is_prime(4)
#    a = list(get_factors(*xrange(1,11), complete_factorization=True,
#    prime=True))
#    a = sorted(a)
#    b = reduce(lambda x,y: x*y, a)
#    print a
#    print b
#    print list((get_factors(22, prime=True, 
#                            complete_factorization=True)))
                            
#    print sorted(p_factor(sorted(list(get_factors(16)))))
#    print p_factor(16)
#    a = get_factors(*xrange(1,11), prime_factorization=True)
#    print reduce(lambda x,y: x*y, a)
#    for i in xrange(1,11):
#        print i, get_factors(i, prime_factorization=True)
                            
#    for i in range(1,11):
#        print i, tree_factor(i)
#    print get_lcm(*values, stop_value=100000, common=True)
#    printStuff(get_factors(*values, prime=True, common=True))
#    print '=============='
#    print get_gcf(*values, prime=True)
#    print get_lcm(*values)
#    printStuff(res)
#    print res


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
    common = kw.get('common')
    prime = kw.get('prime')
    complete_factorization = kw.get('complete_factorization')
    prime_factorization = kw.get('prime_factorization')
    
#    @trace
    def p_factor(n):
#        print n
        if is_prime(n):
            return n
        n = sorted(list(get_factors(n)))
        n = n[:-1]

#        @trace
        @memo
        def _p_factor(n):
            val = n        
            if len(val) == 1 and is_prime(val[0]):
                return sorted(list(get_factors(*val)))
            elif len(val) == 1:
#                val = sorted(list(get_factors(*val)))
                return p_factor(*val)
            elif len(val)>2:
                return _p_factor(val[1:2]) + _p_factor(val[2:])
            else:
                return _p_factor(val[:1]) + _p_factor(val[1:])
                
        return _p_factor(n)
    
    if prime_factorization:
#        factorizations = []
#        for n in nums:
#            factorizations += [p_factor(n)]
        n = nums[0]
        return p_factor(n)

    @memo
    def factor_(n):    
        assert isinstance(n,int)
        h = has_fac = np.vectorize(lambda x: n % x == False)        
        p = possible_factors = np.array(xrange(1,n+1))
        v = h(p)
        res = p[v]
#        print res, complete_factorization
        return frozenset(res) if not complete_factorization else res

#                    
    factor_sets = ([factor_(n) for n in nums] 
                    if not prime_factorization
                        else [p_factor(n) for n in nums]
    )

   
#    print factor_sets, complete_factorization
    res = None
    if not complete_factorization:
        assert isinstance(factor_sets[0], (frozenset))
        factors = reduce(lambda x,y: x | y, factor_sets)
        common_factors = reduce(lambda x,y: x & y, factor_sets)
        res = common_factors if common else factors
    else:
        res = [[elem for elem in arr]
                        for arr in factor_sets]
#        print res
        res = starunpack(res)
#        print res
    if prime:
        fast_primes = np.vectorize(lambda x: is_prime(x))
        _nums = np.array([num for num in res])      
        try:
            res = _nums[fast_primes(_nums)]        
#            print res
            return (r for r in res)
        except IndexError:
            print "Error"
            return res
#    print "made it"
    return (fac for fac in res)


def is_prime(n):
    """Tests to see if n is prime"""
    try:
        assert n != 0
    except:
        "0 is not prime not composite, cannot return a value"
        raise ZeroDivisionError
        
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

def prime_cut(n):
    if is_prime(n):
        return [n]
    factors = sorted(get_factors(n, prime=True))[1:]
    accum = []
#    print factors
    for factor in factors:
        val = n
#        print "  ", factor
        for i in range(10):
            val, r = divmod(val,factor)
            if r:
                break
            accum.append(factor)
    return accum               

def test():
    assert is_common_multiple(30,(5,10,15))
    assert is_common_factor(2,(32,24))
    assert is_common_factor(1,(32,24))
    assert not is_prime(8)
    assert not is_prime(4)
#    assert is_prime(4)
    

#def get_lcm()

#@trace
#def tree_factor(n):
#    try:
#        if is_prime(n):
#            return n
#        else:
#            print "made it1"
#            factors = sorted(list(get_factors(n)))
#            return tree_factor(factors[:1]) + tree_factor(factors[1:]) 
#    except:
#        if len(n) == 1 and is_prime(n[0]):
#            return n
#        else:
#            print "made it2"
#            factors = sorted(list(get_factors(*n)))
#            return tree_factor(factors[1:2]) + tree_factor(factors[2:]) 
            
if __name__ == '__main__':
    test()
    main()