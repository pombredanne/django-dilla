from django.core.management.base import BaseCommand
from optparse import make_option
from dilla import Dilla
import sys


class Command(BaseCommand):
    help = Dilla.__doc__

    option_list = BaseCommand.option_list + (
    make_option('--cycles',
        action='store',
        dest='cycles',
        default=1,
        help='Number of spam cycles to perform. Default: 1'),
    make_option('--apps',
        action='store',
        dest='apps',
        default=None,
        help='Comma-separated apps to spam. Default: settings.DILLA_APPS'),
    )

    def handle(self, *args, **options):
        if options['apps'] is not None:
            apps = options['apps'].split(",")
        else:
            apps = None

        self.stdout.write('Dilla is going to spam your database. \
                Do you wish to proceed? (Y/N)')
        confirm = sys.stdin.readline().replace('\n', '').upper()
        if not confirm == 'Y':
            self.stdout.write('Aborting.\n')
            sys.exit(1)

        d = Dilla(apps=apps, \
                cycles=int(options['cycles']))

        apps, affected, filled, omitted = d.run()

        self.stdout.write("Dilla finished!\n\
        %d app(s) spammed %d row(s) affected, \
        %d field(s) filled, %d field(s) ommited.\nThank you!)" % \
                (apps, affected, filled, omitted)
                )
