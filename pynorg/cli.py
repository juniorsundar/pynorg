import argparse
from pynorg.indexer import check, reindex

class NorgCLI():
    def __init__(self, parser):
        self.parser = parser
        self.subparsers = {}

def main():
    global CLI

    CLI = NorgCLI(parser=argparse.ArgumentParser(
        description="Junior's personal Neorg Helper.\n BEWARE: May contain some useful functions."
    ))
    subparsers = CLI.parser.add_subparsers(
        dest="command",
        help="The following built-in and plugins subcommands are available."
    )

    CLI.parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Verbose output. Useful for debugging.",
    )

    # Indexer submodule
    CLI.subparsers["indexer"] = subparsers.add_parser("indexer", help="Indexing module")
    CLI.subparsers["indexer"].add_argument(
        "-c",
        "--check",
        type=str,
        help="Check if cache in provided directory covers all the files in the directory.",
    )
    CLI.subparsers["indexer"].add_argument(
        "-r",
        "--reindex",
        type=str,
        help="Reindex the directory of files not stored in cache. Runs check by default."
    )
    CLI.subparsers["indexer"].set_defaults(func=indexer)

    args = CLI.parser.parse_args()
    
    if args.command:
        args.func(args)
    else:
        CLI.parser.print_help()


def indexer(args):
    global CLI

    if args.check:
        check(args.check)
        return
    elif args.reindex:
        reindex(args.reindex)
        return

    CLI.subparsers["indexer"].print_help() 

