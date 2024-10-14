import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
import time as tm

# Funkcja zliczająca unikalne wartości w podanym indeksie danych
def data_count(data, index):
    data_dict = {}
    for i in data:
        item = i[index]
        if item not in data_dict:
            data_dict[item] = 1
        else:
            data_dict[item] += 1
    return data_dict

# Funkcja obliczająca średnią wartość w podanym indeksie danych
def average_count(data, index):
    sum = 0
    for i in data:
        sum += float(i[index])
    return sum / len(data)

# Funkcja obliczająca średnią wartość transakcji w zależności od godziny
def average_transaction_by_time(data):
    data_dict = {}
    count = 0
    for i in data:
        count += 1
        item = i[4][len(i[4])-5:]
        if item not in data_dict:
            data_dict[item] = float(i[2])
        else:
            data_dict[item] += float(i[2])

    for i in data_dict:
        data_dict[i] = round(data_dict[i] / count, 2)
    return data_dict

# Funkcja rysująca wykres słupkowy
def draw_bar(data, title, x_name, y_name):
    data = dict(sorted(data.items(), key=lambda x: x[1], reverse=True))
    items = data.keys()
    items_number = data.values()
    y_min = min(items_number) * 0.99
    y_max = max(items_number) * 1.01

    mean_value = sum(items_number) / len(items_number)
    std = (sum((x - mean_value) ** 2 for x in items_number) / len(items_number)) * 0.5

    colors = []
    for i in items_number:
        if i >= max(items_number) * 0.99:
            colors.append((250 / 255, 163 / 255, 129 / 255))
        elif i <= min(items_number) * 1.01:
            colors.append((220 / 255, 219 / 255, 168 / 255))
        else:
            colors.append((245 / 255, 205 / 255, 167 / 255))


    plt.figure(figsize=(10, 6))
    plt.title(title)
    plt.xlabel(x_name)
    plt.ylabel(y_name)
    plt.bar(items, items_number, color=colors)
    plt.ylim(y_min, y_max)
    plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
    plt.xticks(rotation=45)
    plt.grid(True, axis='y')
    plt.tight_layout()
    plt.show()

# Funkcja rysująca wykres kołowy
def draw_pie(data, title):
    items = data.keys()
    items_number = data.values()

    plt.figure(figsize=(10, 6))
    plt.title(title)
    plt.pie(items_number, labels=items, colors=[(220/255, 219/255, 168/255), (245/255, 205/255, 167/255)],
            wedgeprops={"edgecolor":"black", 'linewidth': 0.6}, startangle=90, autopct='%1.1f%%')
    plt.tight_layout()
    plt.show()

# Funkcja rysująca wykres liniowy
def draw_plot(data, title, x_name, y_name):
    items = data.keys()
    items_number = data.values()
    y_min = min(items_number) * 0.99
    y_max = max(items_number) * 1.01

    plt.figure(figsize=(10, 6))
    plt.title(title)
    plt.xlabel(x_name)
    plt.ylabel(y_name)
    plt.plot(items, items_number, linewidth=5, color=(117/255, 219/255, 205/255))
    plt.ylim(y_min, y_max)
    plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
    plt.xticks(rotation=45)
    plt.grid(True, axis='y')
    plt.tight_layout()
    plt.show()

# Odczyt danych z pliku
with open('data.TXT', "r") as file:
    data = file.read().split("\n")

# Dzielimy dane na listy
mylist = []
for i in data:
    mylist.append(i.split("\t"))

# Oddzielamy nagłówki od danych
mylist = mylist[1:]


start = tm.time()

# Zbieranie statystyk
countries_count = data_count(mylist, 1)
transaction_types = data_count(mylist, 3)
industry_count = data_count(mylist, 6)
destination_country_count = data_count(mylist, 7)
reported_by_authority_count = data_count(mylist, 8)
source_of_money_count = data_count(mylist, 9)
tax_country_count = data_count(mylist, 13)

amount_count = average_count(mylist, 2)
risk_count = average_count(mylist, 10)
shell_companies_count = average_count(mylist, 11)

transactions_by_time = average_transaction_by_time(mylist)

# Wyświetlanie wyników analizy
print(f"Kraje: {countries_count}")
print(f"Typy transakcji: {transaction_types}")
print(f"Przemysł: {industry_count}")
print(f"Kraj docelowy: {destination_country_count}")
print(f"Źródło pieniędzy: {source_of_money_count}")
print(f"Zgłoszone przez władze: {reported_by_authority_count}")
print(f"Kraj będący rajem podatkowym: {tax_country_count}")

print(f"Kwota (USD): {amount_count}")
print(f"Ocena ryzyka prania pieniędzy: {risk_count}")
print(f"Zaangażowane spółki fasadowe: {shell_companies_count}")

# Rysowanie wykresów
draw_bar(countries_count, "Liczba transakcji według krajów", "Kraje", "Liczba transakcji")
draw_bar(transaction_types, "Liczba transakcji według typów", "Typ transakcji", "Liczba transakcji")
draw_bar(industry_count, "Liczba transakcji według branż", "Branże", "Liczba transakcji")
draw_bar(destination_country_count, "Liczba transakcji według krajów docelowych", "Kraj docelowy", "Liczba transakcji")
draw_bar(tax_country_count, "Liczba transakcji do rajów podatkowych", "Kraje podatkowe", "Liczba transakcji")

draw_pie(reported_by_authority_count,  "Zgłoszone przez władze")
draw_pie(source_of_money_count,  "Źródła pieniędzy")

draw_plot(transactions_by_time, "Średnia kwota transakcji w zależności od godziny", "Godzina", "Średnia kwota transakcji (USD)")

end = tm.time()

print(f"Time: {end - start}")

