import sqlite3

def veritabani_baglanti_ve_tablo():
    conn = sqlite3.connect("atm.db")
    cursor = conn.cursor()

    # Tabloyu oluştur
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS musteriler (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        isim TEXT NOT NULL,
        soyisim TEXT NOT NULL,
        sifre TEXT NOT NULL,
        dogumtarihi TEXT NOT NULL,
        uyruk TEXT NOT NULL,
        bakiye REAL DEFAULT 0.0,
        esnekhesap REAL DEFAULT 0,
        esneklimit REAL DEFAULT 0.0
    )
    """)
    
    conn.commit()
    conn.close()


veritabani_baglanti_ve_tablo()


def musterikaydi():


    musteri={
        'isim': input('Ihr Vorname:'),
        'soyisim': input('Ihr Nachname:'),
        'dogumtarihi': input('Ihr Geburtsdatum (TT.MM.JJJJ):'),
        'uyruk': input('Ihre Staatsangehörigkeit:'),
        'bakiye' : 0,
        'esnekhesap': 0,
        'esneklimit':0,
        'sifre' : input('Bitte legen Sie ein Passwort fest:')
        
        } 
    
    conn = sqlite3.connect("atm.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO musteriler (isim, soyisim, dogumtarihi, uyruk, bakiye, esnekhesap, esneklimit, sifre) 
        VALUES (:isim, :soyisim, :dogumtarihi, :uyruk, :bakiye, :esnekhesap, :esneklimit, :sifre)
    """, musteri)  # Sözlük olarak veri ekleme

    conn.commit()
    conn.close()

    print(f"{musteri['isim']} wurde erfolgreich registriert.")
    a=input('Möchten Sie eine weitere Aktion durchführen? (j/n) ')
    if a=='j':
        return(islemmenusu(musteri['isim'], musteri['sifre']))
    else:
        print(f"{musteri['isim']}, wir wünschen Ihnen einen schönen Tag.")




def parayukleme(isim, sifre):
    

    conn = sqlite3.connect("atm.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM musteriler WHERE isim = ? AND sifre = ?", (isim, sifre))
    musteri = cursor.fetchone()  # Sonuç varsa döndürür, yoksa None olur

    bakiye=musteri[6] 
    esnekhesap = musteri[7]
    esneklimit = musteri[8]

    miktar=float(input('Wie viel Geld möchten Sie einzahlen?:'))



    if esnekhesap==1:
        
        if esneklimit<2000:
            eksimiktar=2000-esneklimit
            if miktar<=eksimiktar:
                esneklimit = miktar + esneklimit
            else:
                esneklimit=2000
                bakiye=miktar-eksimiktar
            print(f'Ihre Transaktion war erfolgreich. Kontostand: {bakiye} EUR. Flexibles Konto: {esneklimit} EUR.')
        else:
            bakiye=bakiye+miktar
            print(f'Ihre Transaktion war erfolgreich. Kontostand: {bakiye} EUR. Flexibles Konto: {esneklimit} EUR.')
    else:
        bakiye=bakiye+miktar
        print(f'Ihre Transaktion war erfolgreich. Kontostand: {bakiye} EUR.')

    cursor.execute("UPDATE musteriler SET bakiye = ?, esneklimit = ? WHERE isim = ? AND sifre = ?", (bakiye, esneklimit, isim, sifre))
    
    conn.commit()
    conn.close()

    a=input('Möchten Sie eine weitere Aktion durchführen? (j/n) ')
    if a=='j':
        return(islemmenusu(isim, sifre))
    else:
        print(f"{musteri['isim']}, wir wünschen Ihnen einen schönen Tag.")




def paracekme(isim, sifre):

    conn = sqlite3.connect("atm.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM musteriler WHERE isim = ? AND sifre = ?", (isim, sifre))
    musteri = cursor.fetchone()  # Sonuç varsa döndürür, yoksa None olur

    bakiye = musteri[6] 
    esnekhesap = musteri[7]
    esneklimit = musteri[8]


    if esnekhesap==1:
        print(f'Ihr Kontostand beträgt: {bakiye} EUR. Flexibles Konto: {esneklimit} EUR.')

    else:
        print(f'Ihr Kontostand beträgt: {bakiye} EUR.')
    
    miktar=float(input('Wie viel Geld möchten Sie abheben?:'))

    if esnekhesap==1:
        if  miktar>bakiye + esneklimit:
            print("Leider ist Ihr Kontostand unzureichend. Bitte geben Sie erneut den gewünschten Auszahlungsbetrag ein.")
            return(paracekme(isim, sifre))
   
        else:
            if miktar>bakiye:
                ekhesap=input('Ihr Kontostand reicht nicht aus. Möchten Sie das flexible Konto nutzen? (j/n):').lower()
                if ekhesap=='j':
                    esneklimit -= (miktar - bakiye) 
                    bakiye = 0 

                    print(f'Ihr Geld wird vorbereitet. Neuer Kontostand: {bakiye} EUR. Flexibles Konto: {esneklimit} EUR')
                else:
                    print(f"Leider ist Ihr Kontostand unzureichend. Kontoinformationen: Kontostand: {bakiye} EUR, Flexsibles Konto: {esneklimit} EUR.")
                    
            else:
                bakiye=bakiye-miktar
                print(f'Ihr Geld wird vorbereitet. Neuer Kontostand: {bakiye} EUR. Flexibles Konto: {esneklimit} EUR ')
    else:
        if miktar>bakiye:
            kontrol=input('Nicht genügend Guthaben. Möchten Sie ein flexibles Konto eröffnen? (j/n): ').lower()
            if kontrol=='j':
                esnekhesap=1
                esneklimit=2000
                print(f"{isim}, Ihr flexibles Konto wurde Ihrem Konto hinzugefügt. Ihr flexibles Konto beträgt {esneklimit} EUR.")
        else:
            bakiye = bakiye-miktar
            print(f'Ihr Geld wird vorbereitet. Neuer Kontostand: {bakiye} EUR.')

    cursor.execute("UPDATE musteriler SET bakiye = ?, esneklimit = ?, esnekhesap = ? WHERE isim = ? AND sifre = ?", (bakiye, esneklimit, esnekhesap, isim, sifre))

    conn.commit()
    conn.close()

    a=input('Möchten Sie eine weitere Aktion durchführen? (j/n)')
    if a=='j':
        return(islemmenusu(isim, sifre))
    else:
        print(f"{isim}, wir wünschen Ihnen einen schönen Tag.")

def sifredegistirme(isim, sifre): 
    conn = sqlite3.connect("atm.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM musteriler WHERE isim = ? AND sifre = ?", (isim, sifre))
    musteri = cursor.fetchone()  # Sonuç varsa döndürür, yoksa None olur
    sifre=musteri[3]

    eskisifre=input('Bitte geben Sie Ihr aktuelles Passwort ein:')
    yenisifre=input('Neues Passwort eingeben:')
    tekraryenisifre=input('Neues Passwort erneut eingeben:')

    if sifre==eskisifre:
        if yenisifre==tekraryenisifre:
            cursor.execute("UPDATE musteriler SET sifre = ? WHERE isim = ? AND sifre = ?", (yenisifre, isim, sifre))
            print('Ihr Passwort wurde erfolgreich geändert.')
        else:
            print('Das neue Passwort stimmt nicht überein. Bitte wiederholen Sie den Vorgang.')
            return(sifredegistirme(isim, sifre))
    else:
        print('Das aktuelle Passwort ist falsch. Bitte erneut versuchen.')
     

    conn.commit()
    conn.close()
    return(anamenu())
    




def islemmenusu(isim, sifre):
    islem=int(input('Welche Aktion möchten Sie durchführen? (1, 2, 3)\n1. Geld abheben\n2. Geld einzahlen\n3. Passwort ändern\n'))
    if islem==1:
        paracekme(isim, sifre)
    elif islem==2:
        parayukleme(isim, sifre)
    elif islem==3:
        sifredegistirme(isim, sifre)
    else:
        print('Ungültige Eingabe. Bitte erneut versuchen.')
        return(islemmenusu(isim, sifre))




def hesapbilgileri():

    isim=input('Bitte geben Sie Ihren Namen ein:')
    sifre=input('Bitte geben Sie Ihr Passwort ein:')

    conn = sqlite3.connect("atm.db")
    cursor = conn.cursor()


    cursor.execute("SELECT * FROM musteriler WHERE isim = ? AND sifre = ?", (isim, sifre))
    musteri = cursor.fetchone()

    conn.close()

    if musteri:
        if musteri[7]==1:
            print(f"Login erfolgreich! Willkommen, {isim}. Kontostand: {musteri[6]} EUR. Flexibles Konto: {musteri[8]} EUR")
            return(islemmenusu(isim, sifre))
        else:
            print(f"Login erfolgreich! Willkommen, {isim}. Kontostand: {musteri[6]} EUR.")
            return(islemmenusu(isim, sifre))

    else:
        print("Falsche Eingabe! Bitte versuchen Sie es erneut.")
        return(anamenu())

def sifremiunuttum():

    isim=input('Bitte geben Sie Ihren Namen ein:')
    dt=input('Bitte geben Sie Ihr Geburtsdatum ein (TT.MM.JJJJ):') 

    conn = sqlite3.connect("atm.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM musteriler WHERE isim = ? AND dogumtarihi = ?", (isim, dt))
    musteri = cursor.fetchone()

    if musteri:

        yenisifre=input('Neues Passwort eingeben:')
        tekraryenisifre=input('Neues Passwort erneut eingeben:')

        if yenisifre==tekraryenisifre:
            cursor.execute("UPDATE musteriler SET sifre = ? WHERE isim = ? AND dogumtarihi = ?", (yenisifre, isim, dt))
            print('Ihr neues Passwort wurde erfolgreich festgelegt.')
        else:
            print("Das wiederholte Passwort stimmt nicht überein. Bitte versuchen Sie es erneut.")
            return(sifremiunuttum())
    else:
        print('Name oder Geburtsdatum falsch. Bitte erneut versuchen.')
        return(sifremiunuttum())
 
    conn.commit()
    conn.close()
    return(anamenu())
    

    
def anamenu():
    islem=int(input('Was möchten Sie tun? (1, 2, 3)\n1. Neues Benutzerkonto erstellen\n2. Benutzeranmeldung\n3. Passwort vergessen\n'))

    if islem==1:
        musterikaydi()
    elif islem==2:
        hesapbilgileri()
    elif islem==3:
        sifremiunuttum()

    else:
        print('Ungültige Eingabe. Bitte erneut versuchen.')
        return(anamenu())

anamenu()
    




    






        
    