import pandas as pd

#read csv

df = pd.read_csv("zadanie1.csv")
df['data_urodzenia']=pd.to_datetime(df['data_urodzenia'],format='%d.%m.%Y')
df_po_1999 = df[(df['data_urodzenia']>'1999-12-31')]
print("W danych osób urodzonych po '1999-12-31' jest ",df_po_1999['data_urodzenia'].count())

lista_imion = df['imie'].tolist()

kobiety=[]
for imie in lista_imion:
    if imie[-1:]=='a' and imie not in kobiety:
        kobiety.append(imie)
print("Wszystkie imiona żeńskie w danych to :",set(kobiety))