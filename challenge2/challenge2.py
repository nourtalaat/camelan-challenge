# All code is compliant with PEP8 style guidelines

# This program takes in the number of items on auction, as well as a list of
# bidders and their bid amounts then calculates the winners of the bid based
# on the method of 'generalized second-price auction'


def verify_valid_int(num):
    '''Takes a variable `num` and returns the integer value of
    that variable; exits the program if it's not a valid integer'''
    try:
        f_num = float(num)
        num = int(num)
        # Ensuring that the entered value is not a rounded float
        if num != f_num:
            raise ValueError()
        return num
    except ValueError:
        print('Invalid value entered, integer required')
        return None


def verify_valid_name(name):
    '''Taken a variable `name` and returns the input as in if the input
    consists only of alphabetic characters, disregarding spaces; exits
    the program if it's not a valid alphabetic string'''
    # Accounting for spaces, i.e. 'Ahmed Omar'.isalpha() would return False
    # while 'Ahmed'.isalpha() would return True
    for sp in name.split(' '):
        if not sp.isalpha():
            print('Invalid name entered, string required')
            return None
    return name


def calculate_winners(n_items, bidders):
    '''Takes the number of items up for auction and a list of bidders
    as well as their bids, returns the list of bidders with winning
    bids marked with the amount they're supposed to pay (based on
    the GSP method) and non-winning bids marked with "Lost" instead'''
    bidders = [(k,v) for k,v in bidders.items()]
    # Check special case #2 (i.e. no bidders)
    if not bidders:
        return 'No Winners'
    for b in bidders:
        if b[1] < 0:
            return 'Invalid input'
    # Sorting bidders by bid amount then by name (i.e. alphabetic order)
    # Here we have the first key as negative as we'd like to sort by bids
    # in descending order, but at the same time we'd like to sort the names in
    # ascending alphabetic order, hence the negative key for bid amount
    bidders = sorted(bidders, key=lambda x: (-x[1], x[0]))
    b_names, b_amounts = list(zip(*bidders))[0], list(zip(*bidders))[1]
    # Assuming the last bidder (after sorting) pays the amount they bid
    b_amounts_tmp = list(b_amounts)
    b_amounts_tmp.append(b_amounts[-1])
    b_amounts = tuple(b_amounts_tmp)
    # Creating GSP bid amounts
    gsp_bid = list(zip(b_names, b_amounts[1:]))
    # Make a list of the winners through slicing
    # note: n_items > len(bidders) is fine and will not cause an overflow
    winners = gsp_bid[:n_items]
    results = [w for w in winners]
    losers = gsp_bid[n_items:]
    for loser in losers:
        results.append((loser[0], 'Lost'))
    return results


def mock():
    '''Mock endpoint'''
    # Taking and validating the number of items on auction
    n_items = verify_valid_int(input('Number of items: '))
    # Taking and validating the number of bidders
    n_bidders = verify_valid_int(input('Number of bidders: '))
    # Taking in the list of bidders and bid amounts
    bidders = {}
    for i in range(n_bidders):
        b_name = verify_valid_name(input(f'Enter the name of bidder #{i+1}: '))
        # Assuming the bid amount has to be an integer
        b_amount = verify_valid_int(input(f'Enter the bid of bidder #{i+1}: '))
        bidders[b_name] = b_amount
    # Call to the function the does the actual work
    output = calculate_winners(n_items, bidders)
    print(output)


# Call to mock if run from terminal
if __name__ == '__main__':
    mock()
