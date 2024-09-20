import subprocess

#Dönüştürülecek UI dosyalarını listeye ekleyin.

tasarimlar=[
    "tasarimlar/anasayfa.ui",
       
]


#Her UI dosyasını py dosyasına dönüştürün
for tasarim in tasarimlar:
    
    py_dosya=f"donusumler/{tasarim.split("/")[-1].replace(".ui","Uİ")}.py"
    
    
    #pyuic5 komutunu oluşturun
    komut=["pyuic5",tasarim,"-o",py_dosya]
    
    
    try:
        #subprocess modülü ile komutu çalıştırın
        subprocess.run(komut,check=True,shell=True)
        print(f"{tasarim} dönüştürüldü")
    except subprocess.CalledProcessError:
        print(f"{tasarim} hata")
        