"""Command to show disk usage of test runs."""

import os
from pathlib import Path
from argparse import Namespace

from pavilion.config import PavConfig
from pavilion import output
from pavilion.commands.base_classes import Command


class DiskUsageCommand(Command):
    """Show disk usage of test runs and builds."""

    def __init__(self):
        super().__init__(
            name='disk-usage',
            description="Show disk usage of Pavilion test runs, builds, and series.",
            short_help="Show disk usage.",
            aliases=['du', 'disk']
        )

    def _setup_arguments(self, parser):
        parser.add_argument(
            '--label', '-l', action='store', default=None,
            help='Only show usage for this config label.'
        )
        parser.add_argument(
            '--human-readable', '-H', action='store_true', default=True,
            help='Show sizes in human-readable format (KB, MB, GB). Default: True.'
        )
        parser.add_argument(
            '--detailed', '-d', action='store_true', default=False,
            help='Show detailed breakdown.'
        )

    @staticmethod
    def _get_dir_size(path: Path) -> int:
        """Get total size of a directory in bytes."""
        total = 0
        if path.exists():
            for dirpath, dirnames, filenames in os.walk(path):
                for f in filenames:
                    fp = Path(dirpath) / f
                    if fp.exists():
                        total += fp.stat().st_size
        return total

    @staticmethod
    def _format_size(size_bytes: int, human_readable: bool = True) -> str:
        """Format byte size to human readable string."""
        if not human_readable:
            return f"{size_bytes} bytes"

        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"

    def run(self, pav_cfg: PavConfig, args: Namespace) -> int:
        """Run the disk usage command."""

        output.fprint(self.outfile, "\nPavilion Disk Usage:", color=output.BOLD)
        output.fprint(self.outfile, "=" * 60)

        total_usage = 0

        # Determine which config areas to check
        if args.label:
            if args.label not in pav_cfg.configs:
                output.fprint(self.errfile, f"Unknown config label: {args.label}", color=output.RED)
                return 1
            config_areas = [(args.label, pav_cfg.configs[args.label])]
        else:
            config_areas = pav_cfg.configs.items()

        # Check each config area
        for label, config in config_areas:
            working_dir = config.get('working_dir', Path('/'))
            
            output.fprint(self.outfile, f"\nConfig Area: {label}", color=output.CYAN)
            output.fprint(self.outfile, f"  Working Dir: {working_dir}")

            # Test runs
            test_runs_dir = working_dir / 'test_runs'
            test_runs_size = self._get_dir_size(test_runs_dir)
            total_usage += test_runs_size
            output.fprint(self.outfile, f"  Test Runs:     {self._format_size(test_runs_size, args.human_readable)}")

            # Builds
            builds_dir = working_dir / 'builds'
            builds_size = self._get_dir_size(builds_dir)
            total_usage += builds_size
            output.fprint(self.outfile, f"  Builds:        {self._format_size(builds_size, args.human_readable)}")

        # Series directory (global)
        series_dir = pav_cfg.working_dir / 'series'
        series_size = self._get_dir_size(series_dir)
        total_usage += series_size
        output.fprint(self.outfile, f"\nSeries:          {self._format_size(series_size, args.human_readable)}")

        # Total
        output.fprint(self.outfile, "\n" + "-" * 60)
        output.fprint(self.outfile, f"TOTAL USAGE:     {self._format_size(total_usage, args.human_readable)}", color=output.BOLD)
        output.fprint(self.outfile, "=" * 60)

        return 0
