import os
from datetime import datetime
from yattag import Doc

def generate_html_report(number_of_mutants, number_of_test_passed, number_of_test_failed, mutation_score):
    doc, tag, text = Doc().tagtext()

    with tag('html'):
        with tag('head'):
            with tag('title'):
                text('Mutation Testing Report')

        with tag('body'):
            with tag('h1'):
                text('Mutation Testing Report')

            with tag('table', border="1", cellpadding="5"):
                with tag('tr'):
                    with tag('th'):
                        text('Total Mutants')
                    with tag('th'):
                        text('Mutants Passed')
                    with tag('th'):
                        text('Mutants Failed')
                    with tag('th'):
                        text('Mutation Score')

                with tag('tr'):
                    with tag('td'):
                        text(str(number_of_mutants))
                    with tag('td'):
                        text(str(number_of_test_passed))
                    with tag('td'):
                        text(str(number_of_test_failed))
                    with tag('td'):
                        text(f'{mutation_score:.2f}%')

    # Ensure the reports directory exists
    os.makedirs('reports', exist_ok=True)

    # Save the report with a timestamp in the filename
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    report_filename = f'reports/bugbane-{timestamp}.html'
    with open(report_filename, 'w') as report_file:
        report_file.write(doc.getvalue())