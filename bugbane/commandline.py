import argparse
import sys


from bugbane import controller, views, operators, utils

    
def main(argv):
    parser = build_parser()
    run_mutpy(parser)


def build_parser():
    DEF_TIMEOUT_FACTOR = 5
    parser = argparse.ArgumentParser(description='Mutation testing tool for Python 3.x source code. ',
                                     fromfile_prefix_chars='@')
    
    parser.add_argument('--target', '-t', type=str, nargs='+', help='target module or package to mutate')
    parser.add_argument('--unit-test', '-u', type=str, nargs='+',
                        help='test class, test method, module or package with unit tests')
    parser.add_argument('--runner', type=str, choices=['unittest', 'pytest'], default='unittest',
                        metavar='RUNNER', help='test runner')
    parser.add_argument('--report', '-r', type=str, help='generate YAML report', metavar='REPORT_FILE')
    parser.add_argument('--report-html', type=str, help='generate HTML report', metavar='DIR_NAME')
    parser.add_argument('--timeout-factor', '-f', type=float, default=DEF_TIMEOUT_FACTOR,
                        help='max timeout factor (default {})'.format(DEF_TIMEOUT_FACTOR))
    parser.add_argument('--show-mutants', '-m', action='store_true', help='show mutants source code')
    parser.add_argument('--quiet', '-q', action='store_true', help='quiet mode')
    parser.add_argument('--debug', action='store_true', help='dubug mode')
    parser.add_argument('--colored-output', '-c', action='store_true', help='try print colored output')
    parser.add_argument('--disable-stdout', '-d', action='store_true',
                        help='try disable stdout during mutation '
                             '(this option can damage your tests if you interact with sys.stdout)')
    parser.add_argument('--experimental-operators', '-e', action='store_true', help='use experimental operators')
    parser.add_argument('--operator', '-o', type=str, nargs='+',
                        help='use only selected operators', metavar='OPERATOR')
    parser.add_argument('--disable-operator', type=str, nargs='+', default=[],
                        help='disable selected operators', metavar='OPERATOR')
    parser.add_argument('--list-operators', '-l', action='store_true', help='list available operators')
    parser.add_argument('--path', '-p', type=str, metavar='DIR', help='extend Python path')
    parser.add_argument('--percentage', type=int, metavar='PERCENTAGE', default=100,
                        help='percentage of the generated mutants (mutation sampling)')
    parser.add_argument('--coverage', action='store_true',
                        help='mutate only covered code')
    parser.add_argument('--order', type=int, metavar='ORDER', default=1, help='mutation order')
    parser.add_argument('--hom-strategy', type=str, metavar='HOM_STRATEGY', help='HOM strategy',
                        default='FIRST_TO_LAST')
    parser.add_argument('--list-hom-strategies', action='store_true', help='list available HOM strategies')
    parser.add_argument('--mutation-number', type=int, metavar='MUTATION_NUMBER',
                        help='run only one mutation (debug purpose)')
    return parser


def run_mutpy(parser):
    cfg = parser.parse_args()
    if cfg.list_operators:
        list_operators()
    elif cfg.list_hom_strategies:
        list_hom_strategies()
    elif cfg.target and cfg.unit_test:
        mutation_controller = build_controller(cfg)
        mutation_controller.run()
    else:
        parser.print_usage()


def build_controller(cfg):
    runner_cls = get_runner_cls(cfg.runner)
    built_views = build_views(cfg)
    mutant_generator = build_mutator(cfg)
    target_loader = utils.ModulesLoader(cfg.target, cfg.path)
    test_loader = utils.ModulesLoader(cfg.unit_test, cfg.path)
    return controller.MutationController(
        runner_cls=runner_cls,
        target_loader=target_loader,
        test_loader=test_loader,
        views=built_views,
        mutant_generator=mutant_generator,
        timeout_factor=cfg.timeout_factor,
        disable_stdout=cfg.disable_stdout,
        mutate_covered=cfg.coverage,
        mutation_number=cfg.mutation_number,
    )


def get_runner_cls(runner):
    if runner == 'unittest':
        from bugbane.test_runners import UnittestTestRunner
        return UnittestTestRunner
    elif runner == 'pytest':
        from bugbane.test_runners import PytestTestRunner
        return PytestTestRunner
    raise ValueError('Unknown runner: {0}'.format(runner))


def build_mutator(cfg):
    operators_set = set()

    if cfg.experimental_operators:
        operators_set |= operators.experimental_operators

    name_to_operator = build_name_to_operator_map()

    if cfg.operator:
        operators_set |= {get_operator(name, name_to_operator)
                          for name in cfg.operator}
    else:
        operators_set |= operators.standard_operators

    operators_set -= {get_operator(name, name_to_operator)
                      for name in cfg.disable_operator}

    if cfg.order == 1:
        return controller.FirstOrderMutator(operators_set, cfg.percentage)
    else:
        hom_strategy = build_hom_strategy(cfg)
        return controller.HighOrderMutator(operators_set, cfg.percentage, hom_strategy=hom_strategy)


def build_hom_strategy(cfg):
    if cfg.order < 1:
        print('Order should be > 0.')
        sys.exit(-1)
    try:
        name_to_hom_strategy = {hom_strategy.name: hom_strategy for hom_strategy in controller.hom_strategies}
        return name_to_hom_strategy[cfg.hom_strategy](order=cfg.order)
    except KeyError:
        print('Unsupported HOM strategy {}! Use --list-hom-strategies to show strategies.'.format(cfg.hom_strategy))
        sys.exit(-1)


def get_operator(name, name_to_operator):
    try:
        return name_to_operator[name]
    except KeyError:
        print('Unsupported operator {}! Use -l to show all operators.'.format(name))
        sys.exit(-1)


def build_name_to_operator_map():
    result = {}
    for operator in operators.standard_operators | operators.experimental_operators:
        result[operator.name()] = operator
        result[operator.long_name()] = operator
    return result


def build_views(cfg):
    views_list = []

    if cfg.quiet:
        views_list.append(views.QuietTextView(cfg.colored_output))
    else:
        views_list.append(views.TextView(cfg.colored_output, cfg.show_mutants))

    if cfg.report:
        views_list.append(views.YAMLReportView(cfg.report))

    if cfg.report_html:
        views_list.append(views.HTMLReportView(cfg.report_html))

    if cfg.debug:
        views_list.append(views.DebugView())

    return views_list


def list_operators():
    print('Standard mutation operators:')
    for operator in utils.sort_operators(operators.standard_operators):
        print(' - {:3} - {}'.format(operator.name(), operator.long_name()))
    print('Experimental mutation operators:')
    for operator in utils.sort_operators(operators.experimental_operators):
        print(' - {:3} - {}'.format(operator.name(), operator.long_name()))


def list_hom_strategies():
    print('HOM strategies:')
    for strategy in controller.hom_strategies:
        print(' - {}'.format(strategy.name))


# #This code is a Python script for a mutation testing tool called mutpy. It defines a command-line interface using the argparse module, and runs a mutation controller with the specified configuration.

# The main() function is the entry point to the program, and it is responsible for parsing the command-line arguments and running the run_mutpy() function with the parsed arguments.

# The build_parser() function creates an instance of argparse.ArgumentParser with various options and arguments that can be passed to the program. The run_mutpy() function then calls parser.parse_args() to parse the command-line arguments and create a configuration object cfg.

# The run_mutpy() function then checks the value of various options in the configuration object to determine what actions to take. If the list_operators option is set, the list_operators() function is called to display a list of available mutation operators. If the list_hom_strategies option is set, the list_hom_strategies() function is called to display a list of available higher-order mutation strategies. Otherwise, the build_controller() function is called to create a MutationController object with the specified configuration and run it.

# The build_controller() function creates a MutationController object with the specified configuration, test runner, mutant generator, and views. It also sets the timeout_factor, disable_stdout, mutate_covered, and mutation_number attributes based on the configuration.

# The get_runner_cls() function returns the test runner class based on the value of the runner option in the configuration object. It currently supports the unittest and pytest runners.

# The build_mutator() function creates a mutant generator with the specified mutation operators, percentage, and higher-order mutation strategy. It first creates a set of mutation operators to use, based on the value of various options in the configuration object. If the experimental_operators option is set, it adds the experimental operators to the set. Otherwise, it adds the standard operators. It then removes any operators that were explicitly disabled using the disable_operator option. If the operator option is set, it adds the specified operators to the set. Finally, it creates a FirstOrderMutator or HighOrderMutator object, depending on the value of the order option.

# The build_hom_strategy() function creates a higher-order mutation strategy object based on the value of the hom_strategy option in the configuration object. It first checks that the order option is greater than 0. It then creates a dictionary mapping strategy names to strategy classes, and looks up the strategy class based on the name in the configuration object. It creates an instance of the strategy class with the specified order and returns it.