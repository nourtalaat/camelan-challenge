# All code is compliant with PEP8 style guidelines

import json
from challenge2 import calculate_winners

# The goal of this script is to load, run, and evaluate predefined test cases


def load(fname):
    '''Loads JSON from file'''
    test_cases = None
    with open(fname, 'r') as tc_file:
        test_cases = json.load(tc_file)
    return test_cases


def run(test_case):
    '''Runs each test case'''
    n_items = test_case['input']['n_items']
    bidders = test_case['input']['bidders']
    result = calculate_winners(n_items, bidders)
    expected_output = test_case['expected_output']
    # Try/except used to handle cases with 'No Winners' output
    try:
        expected_output = [(k, v) for k, v in expected_output.items()]
    except AttributeError:
        pass
    return (expected_output == result)


def test_eval(fname):
    '''Loads, runs, and evaluates each test case'''
    test_cases = load(fname)
    count = len(test_cases)
    passed = 0
    for i in range(len(test_cases)):
        test_case = test_cases[i]
        if run(test_case):
            print(f'Passed #{i+1}')
            passed += 1
        else:
            print(f'Failed #{i+1}')
    print(f'Passed {passed}/{count} test cases')


# Runs base test cases from text file if called from terminal
if __name__ == '__main__':
    test_eval('challenge2_test_cases.json')
