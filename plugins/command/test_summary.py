"""Command to show a summary of test statuses."""

from argparse import Namespace
from collections import Counter

from pavilion.config import PavConfig
from pavilion import output
from pavilion import filters
from pavilion.test_ids import SeriesID
from pavilion import cmd_utils
from pavilion.commands.base_classes import Command


class TestSummaryCommand(Command):
    """Show a summary count of tests by status."""

    def __init__(self):
        super().__init__(
            name='test-summary',
            description="Show a summary count of tests grouped by status.",
            short_help="Show test status summary.",
            aliases=['summary', 'test-status']
        )

    def _setup_arguments(self, parser):
        parser.add_argument(
            '--label', '-L', action='store', default=None,
            help='Only show tests from this config label.'
        )
        parser.add_argument(
            '--state', '-s', action='store', default=None,
            help='Only count tests in this state.'
        )
        filters.add_test_filter_args(parser, sort_keys=[])

    def run(self, pav_cfg: PavConfig, args: Namespace) -> int:
        """Run the test summary command."""

        # Build filter query
        filter_parts = []
        if args.state:
            filter_parts.append(f"state={args.state}")
        if args.filter:
            filter_parts.append(args.filter)

        filter_query = ' AND '.join(filter_parts) if filter_parts else None

        # Get tests
        tests = cmd_utils.arg_filtered_tests(
            pav_cfg,
            tests=[],
            series=[SeriesID("all")],
            filter_query=filter_query,
            sort_by=None,
            limit=None,
            verbose=self.errfile
        )

        test_data = tests.data
        if not test_data:
            output.fprint(self.outfile, "No tests found.", color=output.YELLOW)
            return 0

        # Count by result (PASS/FAIL/...)
        result_counts = Counter()
        for test in test_data:
            result = test.get('result')
            key = str(result) if result else str(test.get('state', 'unknown'))
            result_counts[key] += 1

        # Display results
        output.fprint(self.outfile, "\nTest Status Summary:", color=output.BOLD)
        output.fprint(self.outfile, "-" * 40)

        for status, count in sorted(result_counts.items()):
            if status in ('PASS', 'PASSED'):
                color = output.GREEN
            elif status in ('FAIL', 'FAILED', 'ERROR'):
                color = output.RED
            else:
                color = output.YELLOW

            output.fprint(self.outfile, f"  {status:20s}: {count}", color=color)

        output.fprint(self.outfile, "-" * 40)
        output.fprint(self.outfile, f"  {'TOTAL':20s}: {len(test_data)}", color=output.BOLD)

        return 0
