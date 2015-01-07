# -*- coding: utf-8 -*-
r"""
This toolset is designed to enhance scripting performance.

Much inspiration was drawn from Peter Norvig's Udacity 
class "Design of Computer Programs" 
(www.https://www.udacity.com/course/viewer#!/c-cs212/)

Created on Thu Jan 01 17:40:08 2015
@author: J

"""

from MyDevTools.MyDecorator import decorator
from MyDevTools.MyDataTypes import histogram, get_histogram, loop

__all__ = [

            "memo",
            "combined_gen",
            "get_histogram",
            "n_ary"

]

def main():
    stuff = [range(10) for x in range(10)]
    stuff2 = [3,(1,2,3),(22,45,20),[range(7)]]
    print unpack(*stuff)
#    print unpack(*stuff2)
#    print unpack('five', 'four', 'three', (22,5,10))
#    print unpack('five', 'four', 'three', (22,5,10), string_safe=False)
#    @sequence(stop=50)  
    pass
    
    

@decorator
def memo(f):
    """Decorator that caches the return value for each call to f(args).
    Then when called again with same args, we can just look it up."""
    cache = {}
    def _f(*args):
        try:
            return cache[args]
        except KeyError:
            result = f(*args)
            cache[args] = result
            return result
        except TypeError:
            # some element of args can't be a dict key
            return f(*args)
    _f.cache = cache
    return _f


def combined_gen(args, non_redundant=True):
    cache = {}
    redundant = not non_redundant
    while non_redundant and args:
        for arg in args:
            try:
                res = arg.next()
                cache[res]
            except StopIteration:
                args = tuple(new_arg for new_arg in args if new_arg != arg)                
            except KeyError:
                cache[res] = res
                yield res
    while redundant:
        for arg in args:
            yield arg.next()
            


@decorator
def n_ary(f):
    """Given binary function f(x, y), return an n_ary function such
    that f(x, y, z) = f(x, f(y,z)), etc. Also allow f(x) = x."""
    def n_ary_f(x, *args):
        return x if not args else f(x, n_ary_f(*args))
    return n_ary_f

def unpack(*items, **kw):
    
    string_safe = kw.get('string_safe', True)
    assert isinstance(string_safe, bool)
    
    def intList(n):
        return [n] if isinstance(n, (int,float)) else n
    items = map(intList, items)
        
    def _unpack(items):
        try:
    #        print items[0], len(items[0])
            return (items if isinstance(item, str) or len(items[0]) <= 1
                else unpack(items[0][:1]) + unpack(items[0][1:]))
        except TypeError:
            return items
    cache = []
    try:
        for item in items:
            if isinstance(item, str) and string_safe:
                cache += [item]
            else:
                cache += _unpack(item)
        return cache
    except:
        return items

@decorator            
def sequence(start=0, stop=False, step=1):
    @decorator
    def decorator(f):
        def wrapper(*args, **kw):
            return (term for term in (f(n) for n in count(start, step)
                    if stop if n < stop))
        return wrapper
    return decorator
    
if __name__=='__main__':
    main()
