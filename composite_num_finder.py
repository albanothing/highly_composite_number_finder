# Highly composite number finder by Alessandro do Carmo Silva

import matplotlib.pyplot as plt
from time import process_time as pt

# Adds thousands separators to integers
def AddThousandSeparators( num: int, minimum_digits: int = 6, separator: str = ' ' ) -> str:
    if type(num) != str: num = str(num)
    if len(num) < minimum_digits: return num
    digits = []
    for idx, digit in enumerate( num[::-1][:-1] ):
        digits.append( digit )
        if ( idx + 1 ) % 3 == 0: digits.append( separator )
    return num[0] + ''.join( digits[::-1] )

composite_numbers = { 1: 1 } # Key = HCN, Value = number of divisors
def_search_max    = 10_080
upper_bound       = float( 'inf' )
search_start      = 1
while True:
    while True:
        search_max = input( 'Input largest number to search: ' ).replace(' ','')
        if search_max == '':
            search_max = def_search_max
            print( f'Empty input. Will use default value of { AddThousandSeparators( def_search_max, 5 ) }.' )
        try:
            search_max = int( search_max )
            if not 0 < search_max < upper_bound: raise
        except: print( 'Invalid number\n' )
        else:   break

    print( 'Searching...' )
    start_time = pt()
    if search_max < search_start:
        del_list = []
        for key in composite_numbers:
            if key > search_max: del_list.append( key )
        for key in del_list:
            del composite_numbers[key]
        del del_list
    elif search_max > search_start:
        largest_divisor_count_so_far = max( composite_numbers.values() )
        for num in range( search_start + 1, search_max + 1 ):
            idx = 2
            largest_divisor = num // 2
            divisors_count = 2 # Every number is divisible by itself and 1
            while idx <= largest_divisor:
                if num % idx == 0: divisors_count += 1
                idx += 1
            if divisors_count > largest_divisor_count_so_far:
                largest_divisor_count_so_far = composite_numbers[num] = divisors_count
    stop_time = pt()
    if   search_max >= search_start: text_core = f'{ AddThousandSeparators( 1 if search_start == 1 else search_start + 1 ) } and { AddThousandSeparators( search_max ) } (inclusive) searched in'
    else                           : text_core = f'{ AddThousandSeparators( search_max ) } and { AddThousandSeparators( search_start ) } wiped in'
    print( f'Space of highly composite numbers between { text_core } { AddThousandSeparators( int( ( stop_time - start_time ) * 1000 ) ) } milliseconds.' )
    search_start = search_max

    numbers              = [ str(num) for num in composite_numbers.keys() ]
    divisors             = list( composite_numbers.values() )
    largest_composite    = numbers[-1]
    bottom_spacing_ratio = len( largest_composite ) / 60 + 0.05
    plt.bar            ( numbers, divisors, color = 'blue', width = 0.8, zorder = 3           )
    plt.grid           ( axis = 'y', color = 'grey', zorder = 0                               )
    plt.xticks         ( rotation = 90                                                        )
    plt.subplots_adjust( bottom = bottom_spacing_ratio                                        )
    plt.title          ( f'Chart of the highly composite numbers up to { largest_composite }' )
    plt.ylabel         ( 'Number of divisors'                                                 )
    plt.show           (                                                                      )

    while True:
        run_again = input( 'Continue searching?(Y/N)\n' ).strip().lower().replace('true','True').replace('yes','True').replace('y','True').replace('false','False').replace('no','False').replace('n','False')
        if run_again == '': continue
        if run_again[-1] == '.': run_again = run_again[:-1]
        try:    run_again = eval( run_again )
        except: print( 'Invalid input.' )
        else:   break
    if not run_again: break
