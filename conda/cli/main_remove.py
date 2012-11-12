
from os import listdir
from os.path import join
from shutil import rmtree

from config import config


def configure_parser(sub_parsers):
    p = sub_parsers.add_parser(
        'remove',
        description     = "Remove packages from local availability.",
        help            = "Remove packages from local availability. (ADVANCED)",
    )
    p.add_argument(
        "--confirm",
        action  = "store",
        default = "yes",
        choices = ["yes", "no"],
        help    = "ask for confirmation before removing packages (default: yes)",
    )
    p.add_argument(
        '-d', "--dry-run",
        action  = "store_true",
        default = False,
        help    = "display packages to be removed, without actually executing",
    )
    p.add_argument(
        'canonical_names',
        action  = "store",
        metavar = 'canonical_name',
        nargs   = '+',
        help    = "canonical name of package to remove from local availability",
    )
    p.set_defaults(func=execute)


def execute(args):
    conf = config()

    to_remove = set(listdir(conf.packages_dir)) & set(args.canonical_names)

    if not to_remove:
        if len(args.canonical_names) == 1:
            print "Could not find package with canonical name '%s' to remove (already removed or unknown)." % args.canonical_names
        else:
            print 'Could not find packages with canonical names %s to remove.' % args.canonical_names
        return

    print "    The following packages were found and will be removed from local availability:"
    print
    for pkg_name in to_remove:
        print "         %s" % pkg_name
    print

    if args.dry_run: return

    if args.confirm == "yes":
        proceed = raw_input("Proceed (y/n)? ")
        if proceed.lower() not in ['y', 'yes']: return

    for pkg_name in to_remove:
        rmtree(join(conf.packages_dir, pkg_name))


