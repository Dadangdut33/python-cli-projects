# System
import os
import time
from datetime import datetime
from sys import exit
try: # Windows
    from msvcrt import getch, getche
except ImportError: # Linux
    def getch():
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    def getche():
        ch = getch()
        print(ch, end='')
        return ch

# User Made
from Data import Data_Tiket, History
from Art import *
from Json_Handling import *

# Ext
from termcolor import colored
from tabulate import tabulate

class MainProgram:
    def __init__(self):
        status, data = getDataPT()
        if not status:
            print("Unexpected error happened! Details: " + data)
            exit()

        self.data_PT_Perkutut = Data_Tiket()
        self.history = History()
        self.isRunning = True
        self.uangSekarang = data["uang"]
        self.showTabelTiket = False
        self.showUang = False
        self.showTableHistory = False

        self.menuAwal = {0: ["\t\t    1. Menu Tiket", self.changeLayoutToMenuMotor], 1: ["\t\t    2. History", self.changeLayoutTOMenuHistory], 2: ["\t\t    3. Exit", self.exitProgram]}
        self.menuTiket = {0: [" 1. Beli", self.beliMotor], 1: [" 2. Reset Data", self.resetData], 2: [" 3. Kembali", self.changeLayoutToMenuAwal]}
        self.spaceToMid = "\t\t\t\t\t\t   "
        self.menuHistory = {0: [f"{self.spaceToMid}1. Search", self.searchHistory], 1: [f"{self.spaceToMid}2. Sort", self.sortHistory], 2: [f"{self.spaceToMid}3. Pop depan (Queue)", self.popQueueHistory], 
                            3: [f"{self.spaceToMid}4. Pop Belakang (Stack)", self.popStackHistory], 4: [f"{self.spaceToMid}5. Refresh Data", self.refreshDataHistory], 5: [f"{self.spaceToMid}6. Kembali", self.changeLayoutToMenuAwal]}
        
        self.menuSekarang = self.menuAwal.copy()
        self.posisiMenuSekarang = 0
        self.posisiMenuSebelumnya = 0

    def refreshDataHistory(self):
        os.system('clear')
        self.history.refreshHistory()
        self.printLogo(menuHistory=True)
        print(colored(f"{self.spaceToMid}\t        Data berhasil di Refresh!", "blue"))
        time.sleep(1)

    def searchHistory(self):
        pilihanWord = ""
        searchDict = {"1": "id", "2": "nama", "3": "kode_penerbangan", "4": "kelas", "5": "tgl_berangkat", 
        "6": "jam_berangkat", "7": "jam_datang", "8": "penumpang_dewasa", "9": "penumpang_anak", "10": "total"}
        skipChoice = False
        while True:
            os.system('clear')
            self.printLogo(menuHistory=True)
            print(colored(f"{self.spaceToMid}\t  Pilih kolom yang ingin dilakukan searching:", "blue"))
            print(colored(f"{self.spaceToMid}\t  Tekan esc untuk kembali ke menu history", "blue"))
            print(f"{self.spaceToMid}\t     1. ID")
            print(f"{self.spaceToMid}\t     2. Nama")
            print(f"{self.spaceToMid}\t     3. Kode Penerbangan")
            print(f"{self.spaceToMid}\t     4. Kelas")
            print(f"{self.spaceToMid}\t     5. Tanggal Berangkat")
            print(f"{self.spaceToMid}\t     6. Jam Berangkat")
            print(f"{self.spaceToMid}\t     7. Jam Datang")
            print(f"{self.spaceToMid}\t     8. Penumpang Dewasa")
            print(f"{self.spaceToMid}\t     9. Penumpang Anak")
            print(f"{self.spaceToMid}\t     10. Total")

            print(colored(f"{self.spaceToMid}\t  Pilih: {pilihanWord}", "yellow"), end="", flush=True)
            if not skipChoice:
                pilihan = ord(getche())


            if pilihan == 13: # enter
                if pilihanWord in searchDict.keys():
                    os.system('clear')
                    self.printLogo(menuHistory=True)
                    try:
                        cari = input(colored(f"{self.spaceToMid}\t  Cari: ", "yellow"))
                    except KeyboardInterrupt:
                        skipChoice = True
                        continue

                    if cari == "":
                        skipChoice = True
                        continue

                    searchGet = self.history.searchHistory(cari, searchDict[pilihanWord])
                    os.system('clear')
                    self.printLogo(menuHistory=True)
                    if len(searchGet) == 0:
                        print(f"{self.spaceToMid}\t\t{cari} tidak ditemukan!")
                    else:
                        searchGetArr = []
                        for item in searchGet:
                            searchGetArr.append([
                                colored(item['id'], "blue"), item['nama'], item['kode_penerbangan'], item['kelas'], item['tgl_berangkat'], item['jam_berangkat'], 
                                item['jam_datang'], item['penumpang_dewasa'], item['penumpang_anak'], "Rp. {:,.2f}".format(item["total"])
                            ])
                        print(f"{self.spaceToMid}\t\t{cari} ditemukan!")
                        print(f"{tabulate(searchGetArr, headers=self.history.headers, tablefmt='fancy_grid')}")

                    skipChoice = False

                    print(colored(f"{self.spaceToMid}Hasil searching berdasarkan {searchDict[pilihanWord]}!", "blue"))
                    print(colored(f"{self.spaceToMid}Tekan apa saja untuk kembali ke menu pencarian...", "yellow"), end="", flush=True)
                    getch()
            elif pilihan == 8: # backspace
                if len(pilihanWord) >= 1:
                    pilihanWord = pilihanWord[:-1]
                else:
                    pilihanWord = ""
            elif pilihan == 27: # esc
                break
            elif len(pilihanWord) < 2:
                if chr(pilihan).isnumeric():
                    pilihanWord += chr(pilihan)

    def sortHistory(self):
        pilihanWord = ""
        sortDict = {"1": "id", "2": "nama", "3": "kode_penerbangan", "4": "kelas", "5": "tgl_berangkat", 
        "6": "jam_berangkat", "7": "jam_datang", "8": "penumpang_dewasa", "9": "penumpang_anak", "10": "total"}
        skipChoice = False
        while True:
            os.system('clear')
            self.printLogo(menuHistory=True)
            print(colored(f"{self.spaceToMid}\t  Pilih kolom yang ingin dilakukan sorting:", "blue"))
            print(colored(f"{self.spaceToMid}\t  Tekan esc untuk kembali ke menu history", "blue"))
            print(f"{self.spaceToMid}\t     1. ID")
            print(f"{self.spaceToMid}\t     2. Nama")
            print(f"{self.spaceToMid}\t     3. Kode Penerbangan")
            print(f"{self.spaceToMid}\t     4. Kelas")
            print(f"{self.spaceToMid}\t     5. Tanggal Berangkat")
            print(f"{self.spaceToMid}\t     6. Jam Berangkat")
            print(f"{self.spaceToMid}\t     7. Jam Datang")
            print(f"{self.spaceToMid}\t     8. Penumpang Dewasa")
            print(f"{self.spaceToMid}\t     9. Penumpang Anak")
            print(f"{self.spaceToMid}\t     10. Total")

            print(colored(f"{self.spaceToMid}\t  Pilih: {pilihanWord}", "yellow"), end="", flush=True)
            if not skipChoice:
                pilihan = ord(getche())

            if pilihan == 13: # enter
                if pilihanWord in sortDict.keys():
                    os.system('clear')
                    self.printLogo(menuHistory=True)
                    print(colored(f"{self.spaceToMid}\t      Ascending/Descending (1/2): ", "yellow"), end="", flush=True)
                    pilihanTipe = ord(getche())
                    if pilihanTipe not in [49, 50]:
                        skipChoice = True
                        continue

                    if pilihanTipe == 49:
                        sortType = "asc"
                    else:
                        sortType = "desc"

                    self.history.sortHistory(sortType, sortDict[pilihanWord])
                    os.system('clear')
                    self.printLogo(menuHistory=True)
                    
                    self.history.printTable()

                    skipChoice = False
                    self.history.refreshHistory() # Reset position

                    sortModel = "descending" if sortType == "desc" else "ascending"
                    print(colored(f"{self.spaceToMid}Hasil sorting ({sortModel}) berdasarkan {sortDict[pilihanWord]}!", "blue"))
                    print(colored(f"{self.spaceToMid}Tekan apa saja untuk kembali ke menu sorting...", "yellow"), end="", flush=True)
                    getch()
                    continue
            elif pilihan == 8: # backspace
                if len(pilihanWord) >= 1:
                    pilihanWord = pilihanWord[:-1]
                else:
                    pilihanWord = ""
            elif pilihan == 27: # esc
                break
            elif len(pilihanWord) < 2:
                if chr(pilihan).isnumeric():
                    pilihanWord += chr(pilihan)

    def popQueueHistory(self):
        if self.history.isEmpty():
            os.system('clear')
            self.printLogo(menuHistory=True)
            print(colored(f"\t\t\t\t\t\t\t\t\t  History kosong! Tidak bisa dilakukan pop depan (Pop Queue)", "red"))
            time.sleep(1)
        else:
            os.system('clear')
            self.printLogo(menuHistory=True)
            
            dataPopped = self.history.popQueueDataHistory()
            print(f"{self.spaceToMid}\t\tData Paling depan:")
            dataTable = [
                colored(dataPopped['id'], "blue"), dataPopped['nama'], dataPopped['kode_penerbangan'], dataPopped['kelas'], dataPopped['tgl_berangkat'], dataPopped['jam_berangkat'], 
                dataPopped['jam_datang'], dataPopped['penumpang_dewasa'], dataPopped['penumpang_anak'], "Rp. {:,.2f}".format(dataPopped["total"])
            ]
            
            print(tabulate([dataTable], headers=self.history.headers, tablefmt="fancy_grid", numalign='left'))

            print(colored(f"\n{self.spaceToMid}\tData Paling depan berhasil di Hapus!", "yellow"), end="", flush=True)
            getch()

    def popStackHistory(self):
        if self.history.isEmpty():
            os.system('clear')
            self.printLogo(menuHistory=True)
            print(colored(f"\t\t\t\t\t\t\t\t\t  History kosong! Tidak bisa dilakukan pop belakang (Pop Stack)", "red"))
            time.sleep(1)
        else:
            os.system('clear')
            self.printLogo(menuHistory=True)

            dataPopped = self.history.popStackDataHistory()
            print(f"{self.spaceToMid}\t\tData Paling belakang:")
            dataTable = [
                colored(dataPopped['id'], "blue"), dataPopped['nama'], dataPopped['kode_penerbangan'], dataPopped['kelas'], dataPopped['tgl_berangkat'], dataPopped['jam_berangkat'], 
                dataPopped['jam_datang'], dataPopped['penumpang_dewasa'], dataPopped['penumpang_anak'], "Rp. {:,.2f}".format(dataPopped["total"])
            ]
            
            print(tabulate([dataTable], headers=self.history.headers, tablefmt="fancy_grid", numalign='left'))

            print(colored(f"\n{self.spaceToMid}\tData Paling belakang berhasil di Hapus!", "yellow"), end="", flush=True)
            getch()

    def printLogo(self, menuHistory=False):        
        if menuHistory:
            tabToMid = " " * 30
            print(colored(tabToMid + "╒" + "═" * 92 + "╕", "blue"), end="")
            print(colored(logoMid, "blue"), end="")
            print(colored("\r" + tabToMid + "│" + " " * 92 + "│", "blue"))
            print(colored(tabToMid + "╘" + "═" * 92 + "╛", "blue"))
        else:
            print(colored("╒" + "═" * 92 + "╕", "blue"), end="")
            print(colored(logo, "blue"), end="")
            print(colored("\r│" + " " * 92 + "│", "blue"))
            print(colored("╘" + "═" * 92 + "╛", "blue"))
        
    def printUang(self):
        print(colored("\t\tUang : Rp. {:,.2f}".format(self.uangSekarang), "cyan"))

    def exitProgram(self, ctrlC = False):
        self.isRunning = False
        os.system('clear')
        if ctrlC: print("Ctrl+C pressed! Program will exit!")
        print(colored(exit_msg, "blue"), end ="")
        time.sleep(1)
        os.system('clear')
        exit()
    
    def changeLayoutToMenuMotor(self):
        self.posisiMenuSebelumnya = 0
        self.posisiMenuSekarang = 0
        self.menuSekarang.clear()
        self.menuSekarang = self.menuTiket.copy()
        self.showTabelTiket = True
        self.showUang = True

    def changeLayoutTOMenuHistory(self):
        self.posisiMenuSebelumnya = 0
        self.posisiMenuSekarang = 0
        self.menuSekarang.clear()
        self.menuSekarang = self.menuHistory.copy()
        self.showTableHistory = True

    def changeLayoutToMenuAwal(self):
        self.posisiMenuSebelumnya = 0
        self.posisiMenuSekarang = 0
        self.menuSekarang.clear()
        self.menuSekarang = self.menuAwal.copy()
        self.showTabelTiket = False
        self.showUang = False
        self.showTableHistory = False

    def averagePrice(self, arr):
        total = 0
        for i in arr:
            total += i
        return total / len(arr)

    def maxPrice(self, arr):
        maxPrice = 0
        for i in arr:
            if i > maxPrice:
                maxPrice = i
        return maxPrice

    def minPrice(self, arr):
        minPrice = arr[0]
        for i in arr:
            if i < minPrice:
                minPrice = i
        return minPrice

    def beliMotor(self):
        sedangBeliTiket = True
        while sedangBeliTiket: # Sedang memesan motor
            sedangMemilihTiket = True
            sedangIsiDetailTiket = True
            sedangPesanTiket = True
            pesanLagi = False
            arrPesananTabel = []
            arrHargaPesananTiket = []
            arrDataHistory = []
            counter = 1
            totalBeli = 0
            while True:
                if sedangMemilihTiket:
                    os.system('clear')
                    self.printLogo()
                    self.data_PT_Perkutut.printTable()
                    print(colored(">> Tekan Control + C apabila ingin cancel proses dan kembali ke menu tiket", "red"))
                    if pesanLagi:
                        print(colored(">> Tekan Escape apabila tidak jadi menambah tiket", "blue"))
                    print(">> Masukkan Pilihan Tiket: ", end="", flush=True)

                    pilihanTiket = ord(getch())

                    if pilihanTiket == 3:
                        return
                    elif pilihanTiket == 27 and pesanLagi: # Escape -> cancel tambah tiket
                        sedangMemilihTiket = False
                        sedangPesanTiket = False
                        sedangIsiDetailTiket = False
                        continue
                    if pilihanTiket not in range(48, 54):
                        continue
                    else:
                        sedangMemilihTiket = False
                        nama, kelas, tgl_berangkat, jam_berangkat, jam_datang, penumpang_dewasa, penumpang_anak= "", "", "", "", "", "", ""

                if sedangIsiDetailTiket:
                    try:
                        os.system('clear')
                        self.printLogo()
                        print(colored(">> Tekan Control + C apabila ingin cancel dan kembali ke menu pilih tiket", "red"))
                        print(colored(">> Masukkan detail pembeli & tiket", "blue"))

                        # Nama
                        if nama != "":
                            print(f"   Nama\t\t\t   : {nama}")
                        else:
                            nama = input("   Nama\t\t\t   : ")
                        if nama == "":
                            nama = ""
                            continue

                        # Kelas
                        if kelas != "":
                            print(f"   Kelas (B/E)\t\t   : {kelas}")
                        else:
                            print("   Kelas (B/E)\t\t   : ", end="", flush=True)
                            kelas = ord(getch())
                            if kelas == "":
                                kelas = ""
                                continue
                            elif kelas not in [66, 98, 69, 101]: 
                                if kelas == 3: # CTRL + C
                                    sedangMemilihTiket = True
                                    kelas = ""
                                    continue
                                kelas = ""
                                continue
                            else:
                                if kelas == 66 or kelas == 98: 
                                    kelas = "Bisnis"
                                else: 
                                    kelas = "Ekonomi"
                                continue

                        # Tgl berangkat
                        if tgl_berangkat != "":
                            print(f"   Tanggal Keberangkatan   : {tgl_berangkat}")
                        else:
                            tgl_berangkat = input("   Tanggal Keberangkatan   : ")
                        if tgl_berangkat == "":
                            tgl_berangkat = ""
                            continue
                        elif len(tgl_berangkat) != 10 or "-" not in tgl_berangkat:
                            tgl_berangkat = ""
                            print(colored("   Tanggal keberangkatan harus dalam format dd-mm-yyyy", "red"))
                            time.sleep(1)
                            continue

                        # Validasi tanggal
                        try:
                            tgl_berangkat_validasi = datetime.strptime(tgl_berangkat, "%d-%m-%Y")
                        except ValueError:
                            tgl_berangkat = ""
                            print(colored("   Tanggal tidak valid!", "red"))
                            print(colored("   Tanggal keberangkatan harus dalam format dd-mm-yyyy", "red"))
                            time.sleep(1)
                            continue

                        # Jam berangkat
                        if jam_berangkat != "":
                            print(f"   Jam Keberangkatan\t   : {jam_berangkat}")
                        else:
                            jam_berangkat = input("   Jam Keberangkatan\t   : ")
                        if jam_berangkat == "":
                            jam_berangkat = ""
                            continue
                        # Jam harus tipe hh:mm:ss
                        elif len(jam_berangkat) != 8 or ":" not in jam_berangkat:
                            jam_berangkat = ""
                            print(colored("   Format jam salah! (hh:mm:ss)", "red"))
                            time.sleep(1)
                            continue

                        jam_berangkat_Validate = jam_berangkat.split(":")
                        if int(jam_berangkat_Validate[0]) > 23 or int(jam_berangkat_Validate[1]) > 59 or int(jam_berangkat_Validate[2]) > 59:
                            jam_berangkat = ""
                            print(colored("   Jam keberangkatan tidak valid!", "red"))
                            time.sleep(1)
                            continue  

                        # Jam datang
                        if jam_datang != "":
                            print(f"   Jam Kedatangan\t   : {jam_datang}")
                        else:
                            jam_datang = input("   Jam Kedatangan\t   : ")
                        if jam_datang == "":
                            jam_datang = ""
                            continue
                        # Jam harus tipe hh:mm:ss
                        elif len(jam_datang) != 8 or ":" not in jam_datang:
                            jam_datang = ""
                            print(colored("   Format jam salah! (hh:mm:ss)", "red"))
                            time.sleep(1)
                            continue
                        # validasi jam menit dan sekon
                        jam_datang_Validate = jam_datang.split(":")
                        if int(jam_datang_Validate[0]) > 23 or int(jam_datang_Validate[1]) > 59 or int(jam_datang_Validate[2]) > 59:
                            jam_datang = ""
                            print(colored("   Jam kedatangan tidak valid!", "red"))
                            time.sleep(1)
                            continue
                        
                        # Penumpang dewasa
                        if penumpang_dewasa != "":
                            print(f"   Jumlah Penumpang Dewasa : {penumpang_dewasa}")
                        else:
                            penumpang_dewasa = input("   Jumlah Penumpang Dewasa : ")
                        if penumpang_dewasa == "":
                            penumpang_dewasa = ""
                            continue
                        elif penumpang_dewasa.isdigit() == False:
                            penumpang_dewasa = ""
                            print(colored("   Jumlah Penumpang Dewasa tidak valid!", "red"))
                            time.sleep(1)
                            continue

                        # Pekerjaan
                        if penumpang_anak != "":
                            print(f"   Jumlah Penumpang Anak   : {penumpang_anak}")
                        else:
                            penumpang_anak = input("   Jumlah Penumpang Anak   : ")
                        if penumpang_anak == "":
                            penumpang_anak = ""
                            continue
                        elif penumpang_anak.isdigit() == False:
                            penumpang_anak = ""
                            print(colored("   Jumlah Penumpang Anak tidak valid!", "red"))
                            time.sleep(1)
                            continue

                        if int(penumpang_dewasa) + int(penumpang_anak) == 0:
                            print(colored("   Jumlah penumpang tidak boleh kosong!", "red"))
                            time.sleep(1)
                            penumpang_dewasa = ""
                            penumpang_anak = ""
                            continue
                    except KeyboardInterrupt:
                        sedangMemilihTiket = True
                        nama, kelas, tgl_berangkat, jam_berangkat, jam_datang, penumpang_dewasa, penumpang_anak= "", "", "", "", "", "", ""
                        continue
                
                if sedangPesanTiket:
                    tiket = self.data_PT_Perkutut.getDataTiketById(pilihanTiket - 48)
                    os.system('clear')
                    self.printLogo()
                    print(colored(">> Tekan Control + C apabila ingin kembali ke menu pilih tiket", "blue"))
                    print(colored(">> Tiket Yang Dipilih", "blue"))
                    print(f"   Kode Penerbangan \t: {tiket['kode_penerbangan']}")
                    print(f"   Tujuan\t\t: {tiket['tujuan']}")
                    print(f"   Harga 1 Tiket \t: {tiket['harga']}")
                    
                    jumlahTiketDewasa = int(tiket['harga']) * int(penumpang_dewasa)
                    jumlahTiketAnak = int(tiket['harga']) * int(penumpang_anak) * 0.6
                    totalHarga = jumlahTiketDewasa + jumlahTiketAnak
                    if kelas == "Bisnis":
                        totalHarga += totalHarga * 0.2

                    print(colored("   Total Harga Tiket \t: {:,.2f}".format(totalHarga), "blue"))

                    print(colored("\n>> Konfirmasi? (y/n) ", "yellow"), end="", flush=True)
                    konfirmasi = ord(getche())
                    if konfirmasi == 121 or konfirmasi == 89: # y
                        sedangPesanTiket = False
                    elif konfirmasi == 110 or konfirmasi == 78: # n
                        sedangMemilihTiket = True
                        sedangIsiDetailTiket = True
                        nama, kelas, tgl_berangkat, jam_berangkat, jam_datang, penumpang_dewasa, penumpang_anak= "", "", "", "", "", "", ""
                        continue
                    else:
                        continue

                    arrPesananTabel.append([colored(counter, "yellow"), nama, tiket['kode_penerbangan'], kelas, tgl_berangkat, jam_berangkat, jam_datang, penumpang_dewasa, penumpang_anak, "Rp. {:,.2f}".format(totalHarga)])
                    arrHargaPesananTiket.append(totalHarga)
                    
                    dataHistory = {
                        "nama": nama,
                        "kode_penerbangan": tiket['kode_penerbangan'],
                        "kelas": kelas,
                        "tgl_berangkat": tgl_berangkat,
                        "jam_berangkat": jam_berangkat,
                        "jam_datang": jam_datang,
                        "penumpang_dewasa": int(penumpang_dewasa),
                        "penumpang_anak": int(penumpang_anak),
                        "total": totalHarga
                    }
                    arrDataHistory.append(dataHistory)
                    totalBeli += totalHarga

                # ------------------------------
                os.system('clear')
                self.printLogo()
                print(tabulate(arrPesananTabel, headers=[colored('No', 'yellow'), "Nama", "Kode Penerbangan", "Kelas", "Tgl Berangkat", "Jam Berangkat", "Jam Datang", "Jumlah Dewasa", "Jumlah Anak-anak", "Total"], tablefmt="grid"))
                
                print(colored(">> Detail:" , "blue"))
                print("   Rata-rata\t\t: Rp. {:,.2f}".format(self.averagePrice(arrHargaPesananTiket)))
                print("   Pembayaran tertinggi\t: Rp. {:,.2f}".format(self.maxPrice(arrHargaPesananTiket)))
                print("   Pembayaran terendah\t: Rp. {:,.2f}".format(self.minPrice(arrHargaPesananTiket)))
                
                print("\n>> Pesan tiket lagi? (y/n) ", end="", flush=True)
                pilihanTiket = ord(getche())
                if pilihanTiket == 121 or pilihanTiket == 89: # y
                    sedangMemilihTiket = True
                    sedangPesanTiket = True
                    sedangIsiDetailTiket = True
                    counter += 1
                    pesanLagi = True
                    nama, kelas, tgl_berangkat, jam_berangkat, jam_datang, penumpang_dewasa, penumpang_anak= "", "", "", "", "", "", ""
                elif pilihanTiket == 110 or pilihanTiket == 78: # n
                    sedangBeliTiket = False

                    self.data_PT_Perkutut.pesanTiket(totalHarga=arrHargaPesananTiket)
                    self.data_PT_Perkutut.updateUang()
                    self.uangSekarang += totalBeli
                    self.history.addHistory(arrDataHistory)
                    print(colored("\n>> Data berhasil tersimpan!", "green"))
                    print(colored("\n>> Tekan apa saja untuk kembali ke menu...", "yellow"), end="", flush=True)
                    getch()
                    break
                else:
                    continue

    def resetData(self):
        # Konfirmasi
        inputSalah = True
        while inputSalah:

            os.system('clear')
            self.printLogo()
            print(colored("Apakah anda yakin ingin mereset data? (y/n) ", "yellow"), end='', flush=True)
        
            pilihan = ord(getche())
            if pilihan not in [89, 121, 78, 110]:
                continue
            else:
                inputSalah = False

            if pilihan == 89 or pilihan == 121:
                self.data_PT_Perkutut.resetData()
                print(colored("\n\n\t\tData berhasil di reset!", "blue"))
                time.sleep(1)
            else:
                print(colored("\n\n\t\tTidak jadi mereset data!", "blue"))
                time.sleep(1)
        
if __name__ == "__main__":
    """
    Run Program
    Menu function mostly uses getch to get input from user.
    Which will then be converted from bytes into ascii codes number
    """
    mainClass = MainProgram()

    while mainClass.isRunning:
        os.system('clear')

        # --------------------------------------------------
        # Header
        mainClass.printLogo(menuHistory = mainClass.showTableHistory)

        # --------------------------------------------------
        # Print table
        if mainClass.showTabelTiket:
            mainClass.data_PT_Perkutut.printTable()

        if mainClass.showTableHistory:
            mainClass.history.printTable()

        # --------------------------------------------------
        # Print Uang
        if mainClass.showUang:
            mainClass.printUang()

        # --------------------------------------------------
        # Menu value
        counter = 0
        for i in mainClass.menuSekarang.values():
            if mainClass.posisiMenuSekarang != counter:
                print("\t\t    " + i[0])
            else:
                print(colored("\t\t     " + i[0] + " ◄", 'yellow'))
            counter += 1

        # 2 getch function because the terminal in vscode is a little different
        # It will produce 0xE0 that will make it impossible to get the key
        # So that's why in order to get the key in vscode terminal, we need to use getch() twice
        # 0xE0 if it's a special key

        # --------------------------------------------------
        # External Terminal (CMD, powershell, etc)
        input_Terminal_Ext = ord(getch())

        # ----------------------------------------------------------------
        # Key press
        # Enter and ctrl + c does not produce 0xE0 so will be checked first in here
        if input_Terminal_Ext == 13: # Key enter
            mainClass.menuSekarang[mainClass.posisiMenuSekarang][1]()
            continue
        # elif input_Terminal_Ext == 3: # CTRL + C
        #     mainClass.exitProgram(ctrlC=True)
        #     break
        elif input_Terminal_Ext == 72: # Key up
            mainClass.posisiMenuSebelumnya = mainClass.posisiMenuSekarang

            mainClass.posisiMenuSekarang -= 1
            if mainClass.posisiMenuSekarang < 0:
                mainClass.posisiMenuSekarang = len(mainClass.menuSekarang) - 1
            continue
            
        elif input_Terminal_Ext == 80: # Key down
            mainClass.posisiMenuSebelumnya = mainClass.posisiMenuSekarang

            mainClass.posisiMenuSekarang += 1
            if mainClass.posisiMenuSekarang > len(mainClass.menuSekarang) - 1:
                mainClass.posisiMenuSekarang = 0    
            continue
        
        # --------------------------------------------------
        # Internal Terminal (vscode)
        input_Terminal_Int = ord(getch())
 
        # ----------------------------------------------------------------
        # Key press
        if input_Terminal_Int == 72: # Key up
            mainClass.posisiMenuSebelumnya = mainClass.posisiMenuSekarang

            mainClass.posisiMenuSekarang -= 1
            if mainClass.posisiMenuSekarang < 0:
                mainClass.posisiMenuSekarang = len(mainClass.menuSekarang) - 1
            
        elif input_Terminal_Int == 80: # Key down
            mainClass.posisiMenuSebelumnya = mainClass.posisiMenuSekarang

            mainClass.posisiMenuSekarang += 1
            if mainClass.posisiMenuSekarang > len(mainClass.menuSekarang) - 1:
                mainClass.posisiMenuSekarang = 0