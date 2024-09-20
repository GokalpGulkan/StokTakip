import sys
from PyQt5 import *
from PyQt5.QtWidgets import *
from donusumler.anasayfaUİ import *
import sqlite3

#uygulama oluşturma
uygulama=QApplication(sys.argv)
pencere=QMainWindow()
ui=Ui_MainWindow()
ui.setupUi(pencere)
pencere.show()

#Veritabı işlemleri
#baglanti=conn,islem=curs
baglanti=sqlite3.connect("urunler.db")
islem=baglanti.cursor()
table=islem.execute("CREATE TABLE IF NOT EXISTS urunler(urunKodu INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,urunAdi TEXT NOT NULL,birimFiyat INTEGER NOT NULL,stokMiktari INTEGER NOT NULL,urunAciklamasi TEXT NOT NULL,urunMarka TEXT NOT NULL,urunKategori TEXT NOT NULL)")

baglanti.commit()#veritabanına değişiklikleri kayıt et


#kayı ekleme
def kayitekle():
    urunKodu=ui.lineEdit_urunkodu.text()
    urunAdi=ui.lineEdit_urunadi.text()
    birimFiyat=ui.lineEdit_birimfiyat.text()
    stokMiktari=ui.lineEdit_stokmiktari.text()
    urunAciklaması=ui.lineEdit_urunaciklamasi.text()
    urunMarka=ui.comboBox_urunmarka.currentText()
    urunKategori=ui.comboBox_urunkategori.currentText()
    
    try:
        ekle=("INSERT INTO urunler (urunKodu,urunAdi,birimFiyat,stokMiktari,urunAciklamasi,urunMarka,urunKategori) values(?,?,?,?,?,?,?)")
        islem.execute(ekle,(urunKodu,urunAdi,birimFiyat,stokMiktari,urunAciklaması,urunMarka,urunKategori))
        baglanti.commit()
        
        ui.statusbar.showMessage("Kayıt Ekleme İşlemi Başarılı...",2000)
    except Exception as error:
        ui.statusbar.showMessage("Kayıt Ekleme İşlemi Başarısız.Hata Kodu ="+str(error))
        
    kayitlistele()
    

#kayıt listeleme

def kayitlistele():
    ui.tableWidget_bilgi.clear()
    
    ui.tableWidget_bilgi.setHorizontalHeaderLabels(("Ürün Kodu","Ürün Adi","Birim Fiyat","Stok Miktari","Ürün Açıklaması","Ürün Markası","Ürün Kategori"))
     
    sorgu="SELECT * FROM urunler"
    islem.execute(sorgu)   
    
    for indexSatir,kayitNumarasi in enumerate(islem):
        for indexSutun,kayitSutun in enumerate(kayitNumarasi):
            ui.tableWidget_bilgi.setItem(indexSatir,indexSutun,QTableWidgetItem(str(kayitSutun)))

kayitlistele()        
#kategoriye göre listeleme
def kategoriyegörelisteleme():
    listenecekkategori=ui.comboBox_kategoriyegorelistele.currentText()
    
    sorgu="SELECT * FROM urunler WHERE urunKategori=?"
    islem.execute(sorgu,(listenecekkategori,))
    ui.tableWidget_bilgi.clear()
   
    for indexSatir,kayitNumarasi in enumerate(islem):
        for indexSutun,kayitSutun in enumerate(kayitNumarasi):
            ui.tableWidget_bilgi.setItem(indexSatir,indexSutun,QTableWidgetItem(str(kayitSutun)))


#kayıt silme işlemi
def kayitsil():
    sil_mesaj=QMessageBox.question(pencere,"KAYIT SİL","Ürünü silmek istediğine emin misiniz?",\
        QMessageBox.Yes | QMessageBox.No)
    
    if sil_mesaj==QMessageBox.Yes:
        secilenkayit=ui.tableWidget_bilgi.selectedItems()
        silinecekkayit=secilenkayit[0].text()
        
        try:
            sorgu="DELETE FROM urunler WHERE urunKodu='%s'"%(silinecekkayit)
            islem.execute(sorgu)
            
            kayitlistele()

            ui.statusbar.showMessage("ürün silme işlemi başarı ile gerçekleşti",2000)
        
        except Exception as error:
            ui.statusbar.showMessage("Program şöyle bir hata ile karşılaştı="+str(error))
    else:
        ui.statusbar.showMessage("Silme işlemi iptal edildi.",2000)
        
    kayitlistele()

#kayıt güncelleme

def kayitguncelle():
    guncellle_mesaj=QMessageBox.question(pencere,"KAYIT GÜNCELLE","Bu kaydı güncellemek istediğinize emin misiniz?",\
        QMessageBox.Yes | QMessageBox.No)
    
    if guncellle_mesaj==QMessageBox.Yes:
        try:
            urunKodu=ui.lineEdit_urunkodu.text()
            urunAdi=ui.lineEdit_urunadi.text()
            birimFiyat=ui.lineEdit_birimfiyat.text()
            stokMiktari=ui.lineEdit_stokmiktari.text()
            urunAciklaması=ui.lineEdit_urunaciklamasi.text()
            urunMarka=ui.comboBox_urunmarka.currentText()
            urunKategori=ui.comboBox_urunkategori.currentText()
            
            
            #databes tablo isimleri :(urunKodu,urunAdi,birimFiyat,stokMiktari,urunAciklamasi,urunMarka,urunKategori)
            
            if urunAdi=="" and birimFiyat=="" and stokMiktari=="" and urunAciklaması==""and urunMarka=="":
                islem.execute("update urunler set urunKodu= ?  where urunKategori= ?",(urunKodu,urunKategori))
            elif urunAdi=="" and birimFiyat=="" and stokMiktari=="" and urunAciklaması==""and urunKategori=="":
                islem.execute("update urunler set urunMarka= ?  where urunKategori= ?",(urunMarka,urunKategori))
            elif urunAdi=="" and birimFiyat=="" and stokMiktari=="" and urunMarka==""and urunKategori=="":
                islem.execute("update urunler set urunAcıklamasi= ?  where urunKategori= ?",(urunAciklaması,urunKategori))
            elif urunAdi=="" and birimFiyat=="" and urunAciklaması=="" and urunMarka==""and urunKategori=="":
                islem.execute("update urunler set stokMiktarı= ?  where urunKategori= ?",(stokMiktari,urunKategori))
            elif urunAdi=="" and stokMiktari=="" and urunAciklaması=="" and urunMarka==""and urunKategori=="":
                islem.execute("update urunler set birimFiyat= ?  where urunKategori= ?",(birimFiyat,urunKategori))
            elif birimFiyat=="" and stokMiktari=="" and urunAciklaması=="" and urunMarka==""and urunKategori=="":
                islem.execute("update urunler set urunAdi= ?  where urunKategori= ?",(urunAdi,urunKategori))
            else:
                islem.execute("update urunler set urunKodu= ?,urunAdi= ?,birimFiyat= ?,stokMiktari= ?,urunAciklamasi= ?,urunMarka= ? where urunKategori= ?",(urunKodu,urunAdi,birimFiyat,stokMiktari,urunAciklaması,urunMarka,urunKategori))
            baglanti.commit()
            kayitlistele()
            ui.statusbar.showMessage("Kayıt başarılı bir şekilde güncellendi",2000)
        except Exception as error:
            ui.statusbar.showMessage("Kayıt güncellemede hata ile karşılaştı="+str(error))
    else:
        ui.statusbar.showMessage("Güncelleme iptal edildi",2000)

    
        
#butonlara signal gönderme

ui.pushButton_urunekle.clicked.connect(kayitekle)
ui.pushButton_urunlistele.clicked.connect(kayitlistele)
ui.pushButton_kategoriyegorelistele.clicked.connect(kategoriyegörelisteleme)
ui.pushButton_urunsil.clicked.connect(kayitsil)
ui.pushButton_urunguncelle.clicked.connect(kayitguncelle)


sys.exit(uygulama.exec_())