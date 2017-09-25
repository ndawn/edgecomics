from previews.models import Monthly, Weekly
from previews.models import PUBLISHERS
import os.path
import time
from edgecomics.settings import MEDIA_ROOT, MEDIA_URL
import json
import locale
import xlwt


def get_default_style():
    style = xlwt.XFStyle()

    style.font = 'Calibri'

    return style


class XLSGenerator(xlwt.Workbook):
    def __init__(
            self,
            mode,
            session_timestamp,
            price_threshold=550,
            xls_dir='xls',
            style=get_default_style(),
            title_under_threshold='Предзаказы %s',
            title_above_threshold='Сборники %s',
    ):
        super().__init__()

        self.mode = mode
        self.session_timestamp = session_timestamp
        self.price_threshold = price_threshold
        self.xls_dir = xls_dir
        self.style = style
        self.title_under_threshold = title_under_threshold
        self.title_above_threshold = title_above_threshold
        self.titles = self.columns + self.additional_columns[self.mode]

        locale.setlocale(locale.LC_TIME, 'ru_RU.utf-8')

    columns = [
        ('Наименование', 'title'),
        ('Наличие', '100'),
        ('Вход', 'bought'),
        ('Цена', 'round(entry.price * entry.discount)'),
        ('Старая', 'price'),
        ('Ссылка', 'entry.cover_list["full"]'),
        ('Вес', 'weight'),
    ]

    additional_columns = {
        'monthly': [
            ('Superior', 'round(entry.price * entry.discount_superior)'),
            ('Дата выхода', 'entry.release_date.strftime("%-d %B %Y")'),
            ('Описание', 'description'),
        ],
        'weekly': [],
    }

    shift_x = 1
    shift_y = 1

    def generate(self):
        for publisher in PUBLISHERS:
            if self.mode == 'monthly':
                values_under_threshold = Monthly.objects.filter(
                    session_timestamp=self.session_timestamp,
                    publisher=publisher['full_name'],
                    price__lt=self.price_threshold,
                )
                values_above_threshold = Monthly.objects.filter(
                    session_timestamp=self.session_timestamp,
                    publisher=publisher['full_name'],
                    price__gte=self.price_threshold,
                )
            elif self.mode == 'weekly':
                values_under_threshold = Weekly.objects.filter(
                    session_timestamp=self.session_timestamp,
                    publisher=publisher['full_name'],
                )
                values_above_threshold = []

            self._write_sheet(self.title_under_threshold % (publisher['short_name']),
                              values_under_threshold)

            self._write_sheet(self.title_above_threshold % (publisher['short_name']),
                              values_above_threshold)

        return self._save()

    def _write_sheet(self, title, values):
        if values:
            sheet = self.add_sheet(title)

            sheet.write(0, 0, title)
            self._write_titles(sheet)
            self._write_values(sheet, values)

    def _write_titles(self, sheet):
        for col in range(len(self.titles)):
            sheet.write(self.shift_x,
                        col + self.shift_y,
                        self.titles[col][0])

    def _write_values(self, sheet, values):
        for row in range(len(values)):
            entry = values[row]

            while isinstance(entry.cover_list, str):
                entry.cover_list = json.loads(entry.cover_list)

            for col in range(len(self.titles)):
                self._write_attr(sheet,
                                 entry,
                                 self.titles[col][1],
                                 row + 1 + self.shift_x,
                                 col + self.shift_y)

    @staticmethod
    def _write_attr(sheet, entry, column, x, y):
        if hasattr(entry, column):
            cell = getattr(entry, column)
        else:
            cell = eval(column)

        sheet.write(x, y, cell)

    def _save(self):
        url = os.path.join(self.xls_dir,
                           '%s_%s.xls' % (self.mode, time.strftime('%Y-%m-%d_%H:%M:%S')))

        path = os.path.join(MEDIA_ROOT, url)

        super().save(path)

        return os.path.join(MEDIA_URL, url)
