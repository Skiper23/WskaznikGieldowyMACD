import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
def alfa(n,wykladnik):
    return pow(2/(n+1),wykladnik)

def ema (krok,wartosci):
    emalista=[]
    for i in range(0,1000):
        licznik = wartosci[i]
        mianownik = 1
        if (i<krok):
            for j in range(i,0,-1):
                licznik+=(1-alfa(i+1,i-j+1))*wartosci[j-1]
                mianownik+=(1-alfa(i+1,i-j+1))
        else:
            for j in range(i,i-krok,-1):
                licznik+=(1-alfa(krok,i-j+1))*wartosci[j]
                mianownik+=(1-alfa(krok,i-j+1))
        emalista.append(licznik/mianownik)
    return emalista

def przecieciaSignalMacd(signal, macd,data):
    punktyPrezciecia=[]
    for i in range(1,len(signal)-1):

        if (signal[i]>macd[i] and signal[i+1]<macd[i+1]) or (signal[i]<macd[i] and signal[i+1]>macd[i+1]):
            punktyPrezciecia.append((signal[i],data[i]))
    return punktyPrezciecia

def kiedyInwestowac(zysk,wartosci,indeksy,signal,macd):
    szukajsprzedazy=1
    iloscJednostek=1000
    for i in indeksy:
        if macd[i+1]>signal[i+1] and szukajsprzedazy==0 and macd[i]<0: #kupuj
            iloscJednostek=(int)(zysk/wartosci[i])
            zysk=zysk-(iloscJednostek*wartosci[i])
            szukajsprzedazy=1
        elif (macd[i+1]<signal[i+1]and szukajsprzedazy==1 and macd[i]>0): #sprzedawaj
            zysk+=iloscJednostek*wartosci[i]
            iloscJednostek=0
            szukajsprzedazy=0
    return zysk




dane = pd.read_csv("iwda.csv")
data=dane['Data'].tolist()
wartosci=dane['Zamkniecie'].tolist()
print(wartosci)
ema12=ema(12,wartosci)
ema26=ema(26,wartosci)

macd=[]
for i,j in zip(ema12,ema26):
    macd.append(i-j)

signal=ema(9,macd)
print(ema12)
print(ema26)
print(macd)
print(signal)
print(data)
plt.subplot(211)
plt.plot(data,wartosci,color="red")
plt.title('Kurs ETF IWDA')
plt.xlabel('Data')
plt.ylabel('Wartosc [$]')
plt.subplot(212)
plt.plot(data,macd, color="blue")
plt.plot(data,signal, color="red")
plt.legend(['Kurs','MACD','SIGNAL'])
plt.title('Wykres wskaznika MACD')
plt.xlabel('Data')
plt.ylabel('Odchylenie')
#print(przecieciaSignalMacd(signal,macd,data))
tablica=np.array(przecieciaSignalMacd(signal,macd,data))
tabx=tablica[:,1]
taby=tablica[:,0]
#RZUTOWAC NP NA INT ARRAY
print(tablica[:,0])
print(tablica[:,1])
plt.plot(tablica[:,1],int(tablica[:,0]),"ro", color="green")
plt.show()
print(data[970])
print(signal[970])
print(macd[970])
wartoscStartowa=1000*wartosci[0];
print(kiedyInwestowac(wartoscStartowa,wartosci,przecieciaSignalMacd(signal, macd,data),signal, macd))
