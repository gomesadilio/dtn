from datetime import datetime as dt, timedelta as td
import sys
import pyperclip

selected_date = dt.today()

def to_str(some_date):
    return some_date.strftime('%d/%m/%Y')

def to_num(some_date):
    return (some_date - dt(1899,12,30)).days

day, month, year = (0,0,0)

if len(sys.argv) > 1:
    param = list(f"{sys.argv[1]:06}")

    try:
        day, month, year = [int(''.join(param[(k-1)*2: k*2])) for k in range(1, len(param)//2 +1)]
    except Exception:
        print('>Erro ao converter o valor recebido, será usado o dia atual!')

day = day if day else selected_date.day
month = month if month else selected_date.month
year = 2000 + year if year else selected_date.year

try:
    selected_date = selected_date.replace(day= day, month = month, year = year)
except ValueError:
    print('>Erro ao converter o valor recebido, será usado o dia atual!')

next_month = 1 if selected_date.month == 12 else selected_date.month
next_year = selected_date.year +1 if selected_date.month == 12 else selected_date.year

dict_dates = {
    'Data base' : selected_date,
    'Dia anterior' : selected_date - td(days=1),
    'Início do mês' : selected_date.replace(day=1),    
    'Final do mês' : selected_date.replace(day=1, month = next_month, year=next_year) - td(days=1),
    'Início do ano' : selected_date.replace(day=1,month=1),
    'Final do ano' : selected_date.replace(day=31,month=12)
}           

print(f"{'*'*60}\nData solicitada: dia = {selected_date.day}, mês = {selected_date.month}, ano = {selected_date.year}")

cnt = 0
for k, v in dict_dates.items():
    if not cnt:
        print('-' * 60)
        cnt = 1
    else:
        cnt = 0
    print(f"{k: >20} | {to_str(v)} | {to_num(v)}")

pyperclip.copy(to_num(selected_date))
print('\nValor copiado para a àrea de transferência!')
