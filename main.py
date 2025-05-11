from datetime import datetime as dt, timedelta as td
import sys
import locale
import tabulate
import pyperclip
from colorama import init, Fore, Back, Style

init(autoreset=True)
locale.setlocale(locale.LC_ALL, "pt_BR.utf8")

colors = {
    "green": Fore.GREEN,
    "blue": Fore.CYAN,
    "red": Back.YELLOW + Fore.BLACK,
    "alternate": Fore.LIGHTBLACK_EX,
    "reset": Style.RESET_ALL,
    "none": "",
}

fmts = [
    "plain",
    "simple",
    "grid",
    "simple_grid",
    "rounded_grid",
    "heavy_grid",
    "mixed_grid",
    "double_grid",
    "fancy_grid",
    "colon_grid",
    "pipe",
    "orgtbl",
    "jira",
    "presto",
    "pretty",
    "psql",
    "rst",
    "outline",
    "simple_outline",
    "rounded_outline",
    "heavy_outline",
    "mixed_outline",
    "double_outline",
    "fancy_outline",
]


class DataNum:
    def __init__(self, text=None):
        self.text = str(text) if text is not None else dt.today().strftime("%d%m%y")
        self.digits = len(self.text)
        self.configure_params()
        self.date = dt(self.year, self.month, self.day)
        self.num = self.to_num(self.date)
        self.weekday = self.date.weekday()
        self.dayname = self.date.strftime("%a")
        self.str = self.to_str(self.date)
        self.weekyear = f"{self.date.isocalendar()[1]}/{self.date.isocalendar()[0]}"
        self.dayyear = (self.date - self.date.replace(day=1, month=1)).days + 1

    def __str__(self):
        return f"""
        original = {self.text}
        digits   = {self.digits}
        day      = {self.day}
        month    = {self.month}
        year     = {self.year}
        date     = {self.date.date()}
        num      = {self.num}
        weekday  = {self.weekday}
        dayname  = {self.dayname}
        str      = {self.str}
        weekyear = {self.weekyear}
        dayyear  = {self.dayyear}
        """

    def configure_params(self):
        start_date = dt.today()

        match self.digits:
            case 0:
                self.day = start_date.day
                self.month = start_date.month
                self.year = start_date.year
            case 2:
                self.day = int(self.text)
                self.month = start_date.month
                self.year = start_date.year
            case 4:
                self.day = int(self.text[:2])
                self.month = int(self.text[2:])
                self.year = start_date.year
            case 5:
                tmp_date = self.to_date(int(self.text))
                self.day = tmp_date.day
                self.month = tmp_date.month
                self.year = tmp_date.year
            case 6:
                self.day = int(self.text[:2])
                self.month = int(self.text[2:4])
                self.year = 2000 + int(self.text[4:])
            case 8:
                self.day = int(self.text[:2])
                self.month = int(self.text[2:4])
                self.year = int(self.text[4:])
            case _:
                raise ValueError(f"Formato de data '{self.text}' inválido.")

    def to_num(self, date):
        number = int((date - dt(1899, 12, 30)).days)
        return f"{number:_}"

    def to_date(self, num):
        return dt(1899, 12, 30) + td(days=num)

    def to_str(self, date):
        return date.strftime("%d/%m/%Y")

    def month_range(self):
        n_days = (
            (self.date.replace(day=1) + td(days=32)).replace(day=1)
            - self.date.replace(day=1)
        ).days
        month_list = [self.date.replace(day=1) + td(days=x) for x in range(n_days)]
        return list(map(lambda x: self.day_info(x), month_list))

    def one_date(self):
        return [[x.replace(colors["red"], "") for x in self.day_info(self.date)]]

    def day_info(self, p_date):
        visual_date = self.to_str(p_date)
        visual_weekday = p_date.strftime("%a")
        visual_num = self.to_num(p_date)
        visual_week_year = p_date.isocalendar()[1]
        visual_day_year = (p_date - p_date.replace(day=1, month=1)).days + 1

        day_num = int(p_date.strftime("%d"))

        color = ""

        if p_date == self.date:
            color = "red"
        elif visual_weekday == "sáb":
            color = "blue"
        elif visual_weekday == "dom":
            color = "green"
        else:
            color = "none"

        str_template = f"{colors[color]}%s{colors['reset']}"

        visual_date = str_template % visual_date
        visual_weekday = str_template % visual_weekday
        visual_num = str_template % visual_num
        visual_week_year = str_template % visual_week_year
        visual_day_year = str_template % visual_day_year

        return [
            visual_date,
            visual_weekday,
            visual_num,
            visual_week_year,
            visual_day_year,
        ]

    def pretty_list(self, date_lists):
        table = tabulate.tabulate(
            date_lists,
            headers=["Data", "Dia", "Número", "Semana", "Dias"],
            tablefmt="outline" if len(date_lists) > 1 else 'fancy_outline',
            numalign="center",
            stralign="center",
        )

        print(table)


if __name__ == "__main__":
    params = sys.argv[1:]
    date_param = None
    options = []

    for param in params:
        if param.isdigit():
            date_param = param
        elif param.isalpha():
            options.extend(list(param))

    try:
        obj = DataNum(date_param)
    except ValueError as e:
        print(f"Erro: {e}")
        sys.exit(1)
    except Exception:
        obj = DataNum()

    if "m" in options:
        year_month = "< " + str.capitalize(obj.date.strftime("%B/%Y")) + " >"
        print(f">>{year_month:=^49}<<")

        obj.pretty_list(obj.month_range())
    else:
        obj.pretty_list(obj.one_date())

    if "c" in options:
        try:
            pyperclip.copy(str(int(obj.num.replace("_", ""))))
        except pyperclip.PyperclipException:
            print(
                Fore.YELLOW
                + "Aviso: Não foi possível copiar para a área de transferência. Certifique-se de ter o pyperclip instalado."
                + Style.RESET_ALL
            )

    # print(obj)
