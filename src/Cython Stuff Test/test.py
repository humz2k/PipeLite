import timeit

setup='import primes'

code = 'primes.primes(1000)'

print ("The time of execution of above program is :",
       timeit.timeit(setup = setup, stmt = code,
                    number = 500))
