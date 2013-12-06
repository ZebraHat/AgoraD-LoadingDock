#
## test_runner.py
## custom test runner that bypasses the creation of a database on this side
#

from django.test.simple import DjangoTestSuiteRunner
from loading_dock.management.commands.add_db import Command
from django.core.management import call_command

class LoadFixturesRunner(DjangoTestSuiteRunner):
    """ A test runner to test without database creation """
    def run_tests(self, test_labels, extra_tests=None, **kwargs):

        self.setup_test_environment()
        suite = self.build_suite(test_labels, extra_tests)
        old_config = self.setup_databases()

        print 'Running script'
        call_command('add_db', 'CHASE-PUT-THE-NAME-OF-THE-DATABASE-HERE')

        c = Command()
        c.handle('test_app_postgresql')
        c.handle('test_app_sqlite')

        ###                        ###

        result = self.run_suite(suite)

        self.teardown_databases(old_config)
        self.teardown_test_environment()

        return self.suite_result(suite, result)
