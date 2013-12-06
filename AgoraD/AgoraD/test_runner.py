#
## test_runner.py
## custom test runner that runs the introspection stuff on the auto-generated databases
#

from django.test.simple import DjangoTestSuiteRunner
from django.core.management import call_command


class LoadFixturesRunner(DjangoTestSuiteRunner):
    """ A test runner to test without database creation """
    def run_tests(self, test_labels, extra_tests=None, **kwargs):

        self.setup_test_environment()
        suite = self.build_suite(test_labels, extra_tests)
        old_config = self.setup_databases()

        print 'Running script'
        print call_command('add_db')
        call_command('add_db', 'test_app_postgresql')
        call_command('add_db', 'test_app_sqlite')

        ###                        ###

        result = self.run_suite(suite)

        self.teardown_databases(old_config)
        self.teardown_test_environment()

        return self.suite_result(suite, result)
