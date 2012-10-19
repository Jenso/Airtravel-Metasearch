from django.core.management.base import BaseCommand, CommandError, AppCommand

class Command(BaseCommand):
    option_list = BaseCommand.option_list + ()
    help = "Starts a Tornado Web."
    args = '[optional port number, or ipaddr:port]'

    def handle(self, addrport='', *args, **options):
        import tornad.app
        
