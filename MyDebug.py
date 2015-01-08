# -*- coding: utf-8 -*-
r"""

DEBUGGING TOOLSET
=================

:Author:  J. Tolton
    
This toolset is designed to aid in rapid debugging.

Much inspiration was drawn from Peter Norvig's Udacity 
class "Design of Computer Programs"

(www.https://www.udacity.com/course/viewer#!/c-cs212/)

Created on Thu Jan 01 17:40:08 2015
@author: J

"""
from MyDecorator import decorator
from time import clock

__all__ = [
              "tracePrint",
              "suppressErrors",
              "countcalls",
              "trace",
              "timeIt",
              "printInputs",
              "printStuff",
              "UnintendedUseError",
              "disabled"
          ]

def tracePrint(s):
    print s
    return s

@decorator
def suppressErrors(f):
    def wrapper(*args, **kw):
        try: 
            f(*args, **kw)
        except Exception as e:
            print "Something bad happened!"
            print e.message
    return wrapper

@decorator
def countcalls(f):
    "Decorator that makes the function count calls to it, in callcounts[f]."
    def _f(*args):
        callcounts[_f] += 1
        return f(*args)
    callcounts[_f] = 0
    return _f
callcounts = {}


@decorator
def trace(f):
    indent = '   '
    def _f(*args):
        signature = '%s(%s)' % (f.__name__, ', '.join(map(repr, args)))
        print '%s--> %s' % (trace.level*indent, signature)
        trace.level += 1
        try:
            result = f(*args)
            print '%s<-- %s == %s' % ((trace.level-1)*indent,
                                      signature, result)
        finally:
            trace.level -= 1
        return result
    trace.level = 0
    return _f
    
@decorator
def timeIt(f):
    t0 = clock()
    def wrapper(*args, **kw):
        rtn =  f(*args, **kw)
        t1 = clock()
        print ("Time for function call {}({}{}): {}"
                .format(f.__name__,
                        ', '.join(map(repr,args)),
                        ', '.join(map(repr,kw)),
                        t1-t0
                        )
                )
        return rtn
    
    return wrapper
    
@decorator
def printInputs(f):
    def wrapper(*args, **kw):
        print "Function: ", str(f.__name__)
        print "Args: "; printStuff(args)
        print "Kwargs: "; printStuff(kw)
        return f(*args, **kw)
    return wrapper
    
def disabled(f): 
    """Used to disable decorators when not debugging.
    
    Usage during debugging:
       
           decorator = decorator
           @decorator
           def foo(x):
               <something>
           
    E.G.
        >>>foo(5)
        <decorated> 5
        
    Usage when not debugging:
    
            decorator = disabled
            
            @decorator
            def foo(x):
                <something>
        
    E.G.
        >>>foo(5)
        5
    """
    return f
    
def printStuff(things):
    """Print ALLL the things"""
    def printIt(x): print x
    [printIt(thing) for thing in things]

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class UnintendedUseError(Error):
    """Exception raised when input is mathematically valid but
    falls outside intended use of method or function.
    
    Attributes:
        expr -- input expression for which the error occured
        msg -- explanation of the error
    """
    def __init__(self, expr, msg):
        self.expr = expr
        self.msg = msg


