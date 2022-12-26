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

# Merges an array of strings into a string formatted into an aligned table ready for printing
def AlignedStringTable( array, capitalize = False, brackets = '', separator = ',', full_stop = '.', characters_per_line_limit = 200, alignment = 'center', is_table = True, vertical_separator = '|', horizontal_separator = '-', corner = 'o' ):
    if type(alignment) == str:
        alignment = alignment.lower()
    if is_table == True:
        if len(horizontal_separator) > 1:
            horizontal_separator = horizontal_separator[0]
        elif len(horizontal_separator) < 1:
            horizontal_separator = ' '
        separator = vertical_separator
        full_stop = vertical_separator
    final_string = ''
    array_lenght = len(array)
    separator_length = len(separator)
    bracket_length = len(brackets)
    while len(corner) != separator_length:
        if len(corner) < separator_length:
            corner += corner[0]
        else:
            corner = corner[:-1]
    left_bracket = ''
    right_braket = ''
    if bracket_length > 0 and bracket_length % 2 == 0:
        splitter = bracket_length / 2 - 0.5
        for idx in enumerate(brackets):
            idx = idx[0]
            if idx < splitter:
                left_bracket += brackets[idx]
            elif idx > splitter:
                right_braket += brackets[idx]
    else:
        bracket_length = bracket_length * 2
        left_bracket = brackets
        right_braket = brackets
    strings_per_line = characters_per_line_limit
    if is_table == True:
        strings_per_line -= separator_length
    max_length = 0
    spacing = ''
    merged_strings_count = 0
    strings_in_current_line = 1
    for string in array:
        if len(string) > max_length:
            max_length = len(string)
    max_item_length = max( 1, max_length + bracket_length )
    if alignment in { 'center', 'left_with_extra_spacing' }:
        max_item_length += 1
    if array_lenght > 1 or is_table == True:
        max_item_length += separator_length
    is_single_line =  is_table == False and max_item_length * array_lenght <= strings_per_line
    if not is_single_line:
        strings_per_line = max( 1, int( strings_per_line / max_item_length ) )
    strings_in_next_line = min( array_lenght, strings_per_line )
    for string in array:
        if capitalize == True:
            string = string.capitalize()
        is_first_in_array = merged_strings_count == 0
        is_first_in_line = merged_strings_count % strings_per_line == 0
        is_last_in_line = ( merged_strings_count + 1 ) % strings_per_line == 0
        is_last_in_array = merged_strings_count == array_lenght - 1
        char_diff = max_length - len(string)
        spacing = ' ' + ' ' * char_diff
        if is_first_in_line:
            strings_in_next_line = min( array_lenght - merged_strings_count, strings_per_line )
        if is_last_in_array:
            end_of_string = full_stop
        elif is_last_in_line:
            end_of_string = separator + '\n'
        else:
            end_of_string = separator
        if alignment == 'center':
            spacing_length = len(spacing)
            left_spacing = ' ' * ( 1 + spacing_length // 2 )
            right_spacing = ' ' * ( spacing_length // 2 + spacing_length % 2 )
            string = left_spacing + left_bracket + string + right_braket + right_spacing + end_of_string
        elif alignment == 'right':
            string = spacing + left_bracket + string + right_braket + end_of_string
        elif alignment == 'left_with_extra_spacing':
            string = ' ' + left_bracket + string + right_braket + spacing + end_of_string
        else:
            string = left_bracket + string + right_braket + spacing + end_of_string
        if is_table == True:
            if is_first_in_array == True:
                horizontal_lines_to_draw = strings_in_next_line
            else:
                horizontal_lines_to_draw = strings_in_current_line
            horizontal_line = ( corner + horizontal_separator * ( 1 + max_item_length - separator_length ) ) * horizontal_lines_to_draw + corner
            if is_first_in_array == True:
                string = horizontal_line + '\n' + separator + string
            elif is_first_in_line == True:
                string = separator + string
            if is_last_in_array == True:
                string += '\n' + horizontal_line
            elif is_last_in_line == True:
                string += horizontal_line + '\n'
        if is_last_in_line == True:
            strings_in_current_line = 0
        strings_in_current_line += 1
        merged_strings_count += 1
        final_string += string
    return final_string

# Initializing variables and setting up some default settings
composite_numbers    = { 1: 1 } # Dictionary that will store the the highly composite numbers as the algorithm finds them. Key = HCN, Value = number of divisors.
oeis_reference_table = { 1: 1, 2: 2, 4: 3, 6: 4, 12: 6, 24: 8, 36: 9, 48: 10, 60: 12, 120: 16, 180: 18, 240: 20, 360: 24, 720: 30, 840: 32, 1260: 36, 1680: 40, 2520: 48, 5040: 60, 7560: 64, 10080: 72, 15120: 80, 20160: 84, 25200: 90, 27720: 96, 45360: 100, 50400: 108, 55440: 120, 83160: 128, 110880: 144, 166320: 160, 221760: 168, 277200: 180, 332640: 192, 498960: 200, 554400: 216, 665280: 224, 720720: 240, 1081080: 256, 1441440: 288, 2162160: 320 } # Reference table of HCNs avaliable on the OEIS website. Used only for comparisons and meant to evaluate the correctness of the implementation of the different search algorithms. Number of divisors was not originally present on the OEIS table, it was obtained via Wolfram Alpha queries instead.
def_search_max       = 10_080
def_search_method    = 'conjecture'
upper_bound          = float( 'inf' )
search_start         = 1
while True:
    # Search method selection
    while True:
        search_method = input( 'Input search method (options: "naive", "less naive", "conjecture"): ' ).strip().lower()
        if   search_method == ''           : search_method = def_search_method; print( f'Empty input. Will use default search method; "{ def_search_method }".' ); break
        elif 'naive'       in search_method: search_method = 'naive'          ;                                                                                    break
        elif 'less naive'  in search_method: search_method = 'less naive'     ;                                                                                    break
        elif 'conjecture'  in search_method: search_method = 'conjecture'     ;                                                                                    break
        else: print ( 'Invalid method.\n' )
    # Search range selection
    while True:
        search_max = input( 'Input largest number to search: ' ).replace(' ','')
        if search_max == '':
            search_max = def_search_max
            print( f'Empty input. Will use default value of { AddThousandSeparators( def_search_max, 5 ) }.' )
        try:
            search_max = int( search_max )
            if not 0 < search_max < upper_bound: raise
        except: print( 'Invalid number.\n' )
        else:   break

    # HCN searching algorithm proper starts here
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
        largest_composite            = max( composite_numbers.keys()   )
        largest_divisor_count_so_far = max( composite_numbers.values() )

        # Naive method, just checks every number in the interval directly (or alternatively, every other number)
        if search_method in { 'naive', 'less naive' }:
            for num in range( search_start + 1 if search_start % 2 == 1 else search_start, search_max + 1, 2 if search_method == 'less naive' else 1 ):
                idx = 2
                largest_divisor = num // 2
                divisors_count = 2 # Every number is divisible by itself and 1
                while idx <= largest_divisor:
                    if num % idx == 0: divisors_count += 1
                    idx += 1
                if divisors_count > largest_divisor_count_so_far:
                    largest_composite = num
                    largest_divisor_count_so_far = composite_numbers[num] = divisors_count
        
        # Experimental method which assumes that every highly complex number above 1 is a result of no more than 3 sums of any combination of the 10 previous highly complex numbers (including repeated sums of the same number, for example; 1 + 1 = 2)
        # This is a conjecture and I can not offer a mathematical proof of this being true, but this method is much faster and matches the results of the naive methods up to at least 55_440
        # I have also checked it's results against the sequence table of HCNs up to 2_162_160 provided by the Online Encyclopedia of Integer Sequences, there too the results of this algorithm are in agreement. See: http://oeis.org/A002182/list (Accessed on 26th of December 2022 at 6:30 GMT-3)
        elif search_method in { 'conjecture', }:
            while True:
                prospective_hcns = set()
                previous_hcns    = tuple( composite_numbers.keys() )[-10:]
                for hcn1 in previous_hcns:
                    for hcn2 in previous_hcns:
                        prospective1 = hcn1 + hcn2
                        if largest_composite < prospective1 <= search_max: prospective_hcns.add( prospective1 )
                        for hcn3 in previous_hcns:
                            prospective2 = prospective1 + hcn3
                            if largest_composite < prospective2 <= search_max: prospective_hcns.add( prospective2 )
                if len( prospective_hcns ) == 0: break
                for num in sorted( prospective_hcns ):
                    idx = 2
                    largest_divisor = num // 2
                    divisors_count = 2
                    while idx <= largest_divisor:
                        if num % idx == 0: divisors_count += 1
                        idx += 1
                    if divisors_count > largest_divisor_count_so_far:
                        largest_composite = num
                        largest_divisor_count_so_far = composite_numbers[num] = divisors_count
                        break
                else: break

    # Prints time stats
    stop_time = pt()
    if   search_max >= search_start: text_core = f'{ AddThousandSeparators( 1 if search_start == 1 else search_start + 1 ) } and { AddThousandSeparators( search_max ) } (inclusive) searched in'
    else                           : text_core = f'{ AddThousandSeparators( search_max ) } and { AddThousandSeparators( search_start ) } wiped in'
    print( f'Space of highly composite numbers between { text_core } { AddThousandSeparators( int( ( stop_time - start_time ) * 1000 ) ) } milliseconds.' )

    # Search for divergences between the recorded results and the OEIS reference table
    divergences = [ list(), list(), False, False ] # Keys from reference not found on results - Keys from results not found on reference - Ordering of keys is in disagreement - Values are in disagreement
    comparison_stop = min( max( composite_numbers.keys() ), max( oeis_reference_table.keys() ) )
    shortest_length = min( len( composite_numbers.keys() ), len( oeis_reference_table.keys() ) )
    for key in oeis_reference_table.keys():
        if key not in composite_numbers.keys(): divergences[0].append(key)
        if key == comparison_stop: break
    for key in composite_numbers.keys():
        if key not in oeis_reference_table.keys(): divergences[1].append(key)
        if key == comparison_stop: break
    if tuple( composite_numbers.keys()   )[:shortest_length] != tuple( oeis_reference_table.keys()   )[:shortest_length]: divergences[2] = True
    if tuple( composite_numbers.values() )[:shortest_length] != tuple( oeis_reference_table.values() )[:shortest_length]: divergences[3] = True
    if all( ( len( divergences[0] + divergences[1] ) == 0, divergences[2] == False, divergences[3] == False ) ): print( 'No divergences found between results and OEIS reference table.' )
    else:
        print( 'Attention: Divergences found between results and OEIS reference table!\n\nDivergences:' )
        if len( divergences[0] ) > 0:                                              print( 'These numbers are listed as HCNs on the reference table, but are absent on the results table;\n' + ', '.join( [ str( num ) for num in divergences[0] ] ) + '.' )
        if len( divergences[1] ) > 0:                                              print( 'These numbers are listed as HCNs on the results table, but are absent on the reference table;\n' + ', '.join( [ str( num ) for num in divergences[1] ] ) + '.' )
        if len( divergences[0] + divergences[1] ) == 0 and divergences[2] == True: print( 'The ordering of the HCNs is in disagreement between the two tables.'                                                                                           )
        if                                                 divergences[3] == True: print( 'The listing of the numbers of divisors is in disagreement between the two tables.'                                                                             )

    # Prints table of HCNs and their divisor counts
    nums_table = [ 'Highly composite numbers', 'Number of divisors' ]
    for num, divisor in composite_numbers.items():
        nums_table.append( AddThousandSeparators( num    , 4 ) )
        nums_table.append( AddThousandSeparators( divisor, 4 ) )
    table_length = len( max( nums_table, key = len ) ) * 2 + 6
    print( '\n' + AlignedStringTable( nums_table, characters_per_line_limit = table_length, corner = '+' ) )

    # Charts out the HCNs
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
    search_start = search_max
