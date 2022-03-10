import timeit


setup = '''
def primes(nb_primes):

  if nb_primes > 1000:
    nb_primes = 1000

  len_p = 0
  n = 2
  p = []

  while len_p < nb_primes:
    for i in p:
      if n % i == 0:
        break
    else:
        p.append(n)
        len_p += 1
    n += 1

  result_as_list = [prime for prime in p[:len_p]]
  return result_as_list
'''

stmt = 'primes(1000)'


print ("The time of execution of above program is :",
       timeit.timeit(setup = setup, stmt = stmt,
                    number = 100))
