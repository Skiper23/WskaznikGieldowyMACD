import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
def alfa(n,wykladnik):
    pom=2/(n+1)
    return pow(1-pom,wykladnik)

def ema (krok,wartosci):
    emalista=[]
    for aktualnyDzien in range(0,1000):
        licznik = wartosci[aktualnyDzien]
        mianownik = 1
        if (aktualnyDzien<krok):
            for j in range(aktualnyDzien,0,-1):
                licznik+=(alfa(aktualnyDzien+1,aktualnyDzien-j+1))*wartosci[j-1]
                mianownik+=(alfa(aktualnyDzien+1,aktualnyDzien-j+1))
        else:
            for j in range(aktualnyDzien-1,aktualnyDzien-krok,-1):
                licznik+=(alfa(krok,aktualnyDzien-j))*wartosci[j]
                mianownik+=(alfa(krok,aktualnyDzien-j))
        emalista.append(licznik/mianownik)
    return emalista

def przecieciaSignalMacd(signal, macd,data):
    punktyPrezciecia=[]
    szukajsprzedazy=1
    for i in range(1,len(signal)-1):
        if (signal[i]>macd[i] and signal[i+1]<macd[i+1] and szukajsprzedazy==0 and signal[i]<0) or (signal[i]<macd[i] and signal[i+1]>macd[i+1] and szukajsprzedazy==1 and signal[i]>0): #kupno gdy signal<0 sprzedaz gdy signal>0
            punktyPrezciecia.append((signal[i],data[i],i))
            if szukajsprzedazy==1:
                szukajsprzedazy=0
            else:
                szukajsprzedazy=1
    return punktyPrezciecia

def kiedyInwestowac(zysk,wartosci,indeksy):
    sprzedaz=1
    iloscJednostek=1000
    wolnePieniadze=0
    for i in indeksy:
        if sprzedaz==1: 
            zysk=iloscJednostek*wartosci[i]
            zysk+=wolnePieniadze
            iloscJednostek=0
            sprzedaz=0
        else: 
            iloscJednostek=(int)(zysk/wartosci[i])
            wolnePieniadze=zysk-(iloscJednostek*wartosci[i])
            sprzedaz=1
    return zysk

def wykresKursu():
    plt.subplot(211)
    plt.plot(data,wartosci,color="red")
    plt.title('Kurs ETF IWDA')
    plt.xlabel('Data')
    plt.ylabel('Wartosc [$]')
    plt.legend(['Kurs'])

def wykresMACD(tablica):
    plt.subplot(212)
    plt.plot(data,macd, color="blue")
    plt.plot(data,signal, color="red")

    tabx=tablica[:,1]
    tabfloat=tablica[:,0].astype(float)
    tabxsell=tabx[::2]
    tabysell=tabfloat[::2]
    tabxbuy=tabx[1::2]
    tabybuy=tabfloat[1::2]

    plt.plot(tabxsell,tabysell,"ro", color="darkgreen")
    plt.plot(tabxbuy,tabybuy,"ro", color="darkorange")
    plt.title('Wykres wskaznika MACD')
    plt.xlabel('Data')
    plt.ylabel('Odchylenie')
    plt.legend(['MACD','SIGNAL','Sprzedaz',"Kupno"])

dane = pd.read_csv("iwda.csv")
data=dane['Data'].tolist()
wartosci=dane['Zamkniecie'].tolist()
ema12=ema(12,wartosci)
ema26=ema(26,wartosci)
macd=[]
for i,j in zip(ema12,ema26):
    macd.append(i-j)
print(macd)

signal=ema(9,macd)

plt.figure(figsize=(12,9))
wykresKursu()
tablica=np.array(przecieciaSignalMacd(signal,macd,data))
wykresMACD(tablica)
plt.show()

wartoscStartowa=1000*wartosci[0]
indeksy=tablica[:,2].astype(int)
wartoscKoncowa=kiedyInwestowac(wartoscStartowa,wartosci,indeksy)
print('Wartosc poczatkowa 1000 akcji %d' %(wartoscStartowa))
print("Wartosc koncowa 1000 akcji %d" %(wartoscKoncowa))
print("Zysk wynosi: %d" %(wartoscKoncowa - wartoscStartowa))