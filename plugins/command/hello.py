"""A simple hello world command plugin - demonstrates basic command structure."""

from pavilion.config import PavConfig
from pavilion import output
from pavilion.commands.base_classes import Command


class HelloCommand(Command):
    """Say hello and show some basic Pavilion info."""

    def __init__(self):
        super().__init__(
            name='hello',
            description="Say hello and display basic Pavilion configuration info.",
            short_help="Display a greeting and Pavilion info.",
            aliases=['hi', 'greet']
        )

    def _setup_arguments(self, parser):
        parser.add_argument(
            '--name', '-n', action='store', default='World',
            help='Name to greet. Default: World.'
        )
        parser.add_argument(
            '--verbose', '-v', action='store_true', default=False,
            help='Show additional configuration info.'
        )

    def run(self, pav_cfg: PavConfig, args) -> int:
        """Run the hello command."""

        output.fprint(self.outfile, f"Hello, {args.name}!", color=output.GREEN)
        output.fprint(self.outfile, "Welcome to Pavilion 2!")

        if args.verbose:
            output.fprint(self.outfile, "\nPavilion Info:")
            output.fprint(self.outfile, f"  Working Directory: {pav_cfg.working_dir}")
            output.fprint(self.outfile, f"  Config Areas: {list(pav_cfg.configs.keys())}")

        return 0
