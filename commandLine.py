import argparse
import sys

def build_parser():
    parser = argparse.ArgumentParser(description='Bugbane - A comprehensive Mutation Testing Tool for Python Source Code',
                                     fromfile_prefix_chars='@')
    
    parser.add_argument('--source-file', '-s', type=str, nargs='+', help='target module or package to mutate')
    parser.add_argument('--unit-test-', '-t', type=str, nargs='+',
                        help='test class, test method, module or package with unit tests for the target')
    
    parser.add_argument('--show-mutants', '-m', action='store_true', help='show all mutant source codes')
    
    parser.add_argument('--list-operators', '-l', action='store_true', help='list available mutation operators')
    return parser
    