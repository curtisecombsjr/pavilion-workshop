"""Command to list recently run tests."""

from argparse import Namespace
from datetime import datetime

from pavilion.config import PavConfig
from pavilion import output
from pavilion import cmd_utils
from pavilion import filters
from pavilion.test_ids import SeriesID
from pavilion.commands.base_classes import Command


class RecentCommand(Command):
    """List the most recently run tests."""

    def __init__(self):
        super().__init__(
            name='recent',
            description="List the most recently run tests with their status.",
            short_help="List recent tests.",
            aliases=['latest']
        )

    def _setup_arguments(self, parser):
        parser.add_argument(
            '-n', '--count', action='store', type=int, default=10,
            help='Number of recent tests to show. Default: 10.'
        )
        parser.add_argument(
            '--state', '-s', action='store', default=None,
            help='Only show tests in this state.'
        )
        parser.add_argument(
            '--test', '-t', action='store', default=None,
            help='Only show tests with this name pattern.'
        )
        parser.add_argument(
            '--verbose', '-v', action='store_true', default=False,
            help='Show additional details.'
        )
        filters.add_test_filter_args(parser, sort_keys=[])

    def run(self, pav_cfg: PavConfig, args: Namespace) -> int:
        """Run the recent tests command."""

        # Build filter query
        filter_parts = []
        if args.state:
            filter_parts.append(f"state={args.state}")
        if args.test:
            filter_parts.append(f"test={args.test}")

        filter_query = ' AND '.join(filter_parts) if filter_parts else None

        # Get tests sorted by creation time (newest first)
        tests = cmd_utils.arg_filtered_tests(
            pav_cfg,
            tests=[],
            series=[SeriesID("all")],
            filter_query=filter_query,
            sort_by='-created',
            limit=args.count,
            verbose=self.errfile
        )

        test_data = tests.data
        if not test_data:
            output.fprint(self.outfile, "No tests found.", color=output.YELLOW)
            return 0

        # Display results
        output.fprint(self.outfile, f"\nRecent Tests (last {len(test_data)}):", color=output.BOLD)
        output.fprint(self.outfile, "=" * 70)

        for test in test_data:
            test_id = test.get('id', '?')
            test_name = str(test.get('name', 'unknown'))
            result = test.get('result')
            status = str(result) if result else str(test.get('state', 'unknown'))
            created = test.get('created', '')

            # Color based on pass/fail
            if status in ('PASS', 'PASSED'):
                color = output.GREEN
            elif status in ('FAIL', 'FAILED', 'ERROR'):
                color = output.RED
            else:
                color = output.YELLOW

            output.fprint(self.outfile, f"  [{test_id}] {test_name:32s} {status}", color=color)

            if args.verbose:
                output.fprint(self.outfile, f"           created: {created}")

        output.fprint(self.outfile, "=" * 70)

        return 0
