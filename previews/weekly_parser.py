from previews.models import Weekly, PUBLISHERS
from previews.parser import Parser


class WeeklyParser(Parser):
    preparse_url = 'https://api.shortboxed.com/'

    pulishers = filter(lambda x: x.get('load_weekly'), PUBLISHERS)
