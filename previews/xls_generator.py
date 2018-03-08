from previews.models import Monthly, Weekly
from previews.models import PUBLISHERS
import os
import time
from edgecomics.settings import MEDIA_ROOT, MEDIA_URL
import json
import locale
import xlsxwriter


def get_default_style(wb):
    style = wb.add_format()

    style.set_font('Calibri')

    return style


class XLSGenerator:
    def __init__(
            self,
            mode,
            session_timestamp,
            file_name=None,
            price_threshold=550,
            xls_dir='xls',
            style=None,
            title_under_threshold='Синглы %s',
            title_above_threshold='Сборники %s',
    ):
        self.mode = mode
        self.session_timestamp = session_timestamp
        self.file_name = '%s_%s.xlsx' % (self.mode, self.session_timestamp) if file_name is None else file_name
        self.price_threshold = price_threshold
        self.xls_dir = xls_dir
        self.title_under_threshold = title_under_threshold
        self.title_above_threshold = title_above_threshold
        self.titles = self.columns + self.additional_columns[self.mode]

        self.file_path = os.path.join(
            MEDIA_ROOT,
            self.xls_dir,
            self.file_name,
        )

        self.workbook = xlsxwriter.Workbook(self.file_path)

        self.style = style if style is not None else get_default_style(self.workbook)

        if os.path.exists(self.file_path):
            os.remove(self.file_path)

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
                ).order_by('title')
                values_above_threshold = Monthly.objects.filter(
                    session_timestamp=self.session_timestamp,
                    publisher=publisher['full_name'],
                    price__gte=self.price_threshold,
                ).order_by('title')
            elif self.mode == 'weekly':
                values_under_threshold = Weekly.objects.filter(
                    session_timestamp=self.session_timestamp,
                    publisher=publisher['full_name'],
                ).order_by('title')
                values_above_threshold = []

            self._write_sheet(
                self.title_under_threshold % (publisher['short_name']),
                values_under_threshold,
            )

            self._write_sheet(
                self.title_above_threshold % (publisher['short_name']),
                values_above_threshold,
            )

        self.workbook.close()

        return os.path.join(MEDIA_URL, self.xls_dir, self.file_name)

    def _write_sheet(self, title, values):
        if values:
            sheet = self.workbook.add_worksheet(title)

            sheet.write(0, 0, title, self.style)

            self._write_titles(sheet)
            self._write_values(sheet, values)

    def _write_titles(self, sheet):
        for col in range(len(self.titles)):
            sheet.write(
                self.shift_x,
                col + self.shift_y,
                self.titles[col][0],
                self.style,
            )

    def _write_values(self, sheet, values):
        for row in range(len(values)):
            entry = values[row]

            while isinstance(entry.cover_list, str):
                entry.cover_list = json.loads(entry.cover_list)

            for col in range(len(self.titles)):
                self._write_attr(
                    sheet,
                    entry,
                    self.titles[col][1],
                    row + 1 + self.shift_x,
                    col + self.shift_y,
                )

    def _write_attr(self, sheet, entry, column, x, y):
        if hasattr(entry, column):
            cell = getattr(entry, column)
        else:
            try:
                cell = eval(column)
            except (ValueError, AttributeError, SyntaxError):
                cell = ''

        sheet.write(x, y, cell, self.style)
