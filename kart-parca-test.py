import time
import random

def lcd_yazdir(metin1, metin2=""):
    print("\n=== LCD Ekran ===")
    print(metin1)
    print(metin2)
    print("=================")

class YeryuzuHaritasi:
    def __init__(self):
        self.harita_verisi = []

    def lidar_verisi_olustur(self):
        veri = {"x": random.uniform(-100, 100), "y": random.uniform(-100, 100), "z": random.uniform(0, 50)}
        self.harita_verisi.append(veri)
        return veri

    def kamera_goruntusu_cek(self):
        return {"goruntu_verisi": "Simüle Edilmiş Görüntü"}

    def harita_olustur(self):
        lidar_verisi = self.lidar_verisi_olustur()
        kamera_verisi = self.kamera_goruntusu_cek()
        return {"lidar": lidar_verisi, "kamera": kamera_verisi}

class UcakTelemetri:
    def __init__(self):
        self.hiz = 0
        self.irtifa = 0
        self.pil_durumu = 100
        self.yon = 0  

    def hiz_olc(self):
        self.hiz += random.uniform(-0.5, 0.5)
        self.hiz = max(0, min(self.hiz, 5.56))
        return self.hiz

    def irtifa_olc(self):
        self.irtifa += random.uniform(-0.5, 1)
        self.irtifa = max(0, self.irtifa)
        return self.irtifa

    def pil_durumu_olc(self):
        self.pil_durumu -= random.uniform(0.05, 0.3)
        self.pil_durumu = max(0, self.pil_durumu)
        return self.pil_durumu

    def yon_olc(self):
        self.yon += random.randint(-5, 5)
        self.yon = self.yon % 360
        return self.yon

class UcakKontrol:
    def __init__(self):
        self.motor_sag = 0
        self.motor_sol = 0
        self.inis_takimlari_acik = True
        self.kanat_acisi = 0
        self.fayda_yuk_kanat_sag = 0
        self.fayda_yuk_kanat_sol = 0
        self.ucak_agirlik = 12.0
        self.max_kanat_yuk = 3.5

    def motor_gucu_ayarla(self, sag_guc, sol_guc):
        self.motor_sag = max(0, min(sag_guc, 100))
        self.motor_sol = max(0, min(sol_guc, 100))

    def inis_takimlarini_degistir(self, durum):
        self.inis_takimlari_acik = durum

    def kanat_acisi_ayarla(self, aci):
        self.kanat_acisi = max(-45, min(aci, 45))

    def fayda_yuk_ekle(self, kanat, agirlik):
        if kanat == "sag":
            self.fayda_yuk_kanat_sag = min(agirlik, self.max_kanat_yuk)
        elif kanat == "sol":
            self.fayda_yuk_kanat_sol = min(agirlik, self.max_kanat_yuk)
        toplam_yuk = self.fayda_yuk_kanat_sag + self.fayda_yuk_kanat_sol

    def toplam_agirlik(self):
        toplam_yuk = self.fayda_yuk_kanat_sag + self.fayda_yuk_kanat_sol
        return self.ucak_agirlik + toplam_yuk

class GorevBilgisayari:
    def __init__(self):
        self.telemetri = UcakTelemetri()
        self.kontrol = UcakKontrol()
        self.yeryuzu_haritasi = YeryuzuHaritasi()
        self.ucus_modu = "Kalkış"

    def ucus_modu_guncelle(self):
        if self.telemetri.irtifa < 10:
            self.ucus_modu = "Kalkış"
        else:
            self.ucus_modu = "Uçuş"
            if self.kontrol.inis_takimlari_acik:
                self.kontrol.inis_takimlarini_degistir(False)

    def hata_kontrolu(self):
        if self.telemetri.pil_durumu < 15:
            print("Acil Uyarı: Pil çok düşük!")
        if self.telemetri.hiz > 5.56:
            print("Acil Uyarı: Aşırı hız!")
        toplam_yuk = self.kontrol.fayda_yuk_kanat_sag + self.kontrol.fayda_yuk_kanat_sol
        if toplam_yuk > 6.0:
            print("Acil Uyarı: Kanatlardaki yük sınırı aşıldı!")

    def gorev_dongusu(self, hedef_irtifa, hedef_hiz, agirlik):
        while True:
            hiz = self.telemetri.hiz_olc()
            irtifa = self.telemetri.irtifa_olc()
            pil = self.telemetri.pil_durumu_olc()
            yon = self.telemetri.yon_olc()

            self.ucus_modu_guncelle()
            self.hata_kontrolu()

            lidar_kamera_veri = self.yeryuzu_haritasi.harita_olustur()

            lcd_yazdir(
                f"Hız: {hiz:.2f} m/s | İrtifa: {irtifa:.1f} m",
                f"Pil: %{pil:.1f} | Mod: {self.ucus_modu} | Yön: {yon}°"
            )

            if self.ucus_modu == "Kalkış":
                self.kontrol.motor_gucu_ayarla(100, 100)
            elif self.ucus_modu == "Uçuş":
                self.kontrol.motor_gucu_ayarla(70, 70)

            time.sleep(1)

            if irtifa >= hedef_irtifa and hiz >= hedef_hiz:
                print(f"Başarıyla hedef irtifa ({hedef_irtifa} m) ve hız ({hedef_hiz} m/s) sağlandı.")
                break

def kontrol_paneli():
    gorev = GorevBilgisayari()

    hedef_irtifa = float(input("Hedef irtifayı girin (metre cinsinden): "))
    hedef_hiz = float(input("Hedef hızı girin (m/s cinsinden): "))
    agirlik = float(input("Uçağın ağırlığını girin (kg cinsinden): "))

    kanat_sag_agirlik = float(input("Sağ kanada yük ekleyin (kg cinsinden): "))
    kanat_sol_agirlik = float(input("Sol kanada yük ekleyin (kg cinsinden): "))

    gorev.kontrol.fayda_yuk_ekle("sag", kanat_sag_agirlik)
    gorev.kontrol.fayda_yuk_ekle("sol", kanat_sol_agirlik)

    gorev.gorev_dongusu(hedef_irtifa, hedef_hiz, agirlik)

kontrol_paneli()
