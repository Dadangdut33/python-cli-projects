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
from Data import Data_Motor, History
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

        self.data_PT_XYZ = Data_Motor()
        self.history = History()
        self.isRunning = True
        self.uangSekarang = data["uang"]
        self.showTabelMotor = False
        self.showUang = False
        self.showTableHistory = False

        self.menuAwal = {0: ["1. Menu Motor", self.changeLayoutToMenuMotor], 1: ["2. History", self.changeLayoutTOMenuHistory], 2: ["3. Exit", self.exitProgram]}
        self.menuMotor = {0: [" 1. Beli", self.beliMotor], 1: [" 2. Reset Data", self.resetData], 2: [" 3. Kembali", self.changeLayoutToMenuAwal]}
        self.spaceToMid = "\t\t\t\t\t\t\t\t\t   "
        self.menuHistory = {0: [f"{self.spaceToMid}1. Search", self.searchHistory], 1: [f"{self.spaceToMid}2. Sort", self.sortHistory], 2: [f"{self.spaceToMid}3. Pop depan (Queue)", self.popQueueHistory], 
                            3: [f"{self.spaceToMid}4. Pop Belakang (Stack)", self.popStackHistory], 4: [f"{self.spaceToMid}5. Refresh Data", self.refreshDataHistory], 5: [f"{self.spaceToMid}6. Kembali", self.changeLayoutToMenuAwal]}
        
        self.menuSekarang = self.menuAwal.copy()
        self.posisiMenuSekarang = 0
        self.posisiMenuSebelumnya = 0

    def refreshDataHistory(self):
        os.system('clear')
        self.history.refreshHistory()
        self.printLogo(menuHistory=True)
        print(f"{self.spaceToMid}\t\t  Data berhasil di Refresh!")
        time.sleep(1)

    def searchHistory(self):
        pilihanWord = ""
        searchDict = {"1": ["id", None], "2": ["pembeli", "nik"], "3": ["pembeli", "nama"], "4": ["pembeli", "ttl"], "5": ["pembeli", "jenis_kelamin"], 
        "6": ["pembeli", "alamat"], "7": ["pembeli", "agama"], "8": ["pembeli", "pekerjaan"], "9": ["pembeli", "statusNikah"], "10": ["pembeli", "pekerjaan"], 
        "11": ["tgl_pembelian", None], "12": ["jenis_motor", None], "13": ["qty", None], "14": ["harga", None]}
        skipChoice = False
        while True:
            os.system('clear')
            self.printLogo(menuHistory=True)
            print(colored(f"{self.spaceToMid}\t  Pilih kolom yang ingin dilakukan searching:", "blue"))
            print(colored(f"{self.spaceToMid}\t  Tekan esc untuk kembali ke menu history", "red"))
            print(f"{self.spaceToMid}\t     1. ID")
            print(f"{self.spaceToMid}\t     2. NIK")
            print(f"{self.spaceToMid}\t     3. Nama")
            print(f"{self.spaceToMid}\t     4. TTL")
            print(f"{self.spaceToMid}\t     5. Jenis Kelamin")
            print(f"{self.spaceToMid}\t     6. Alamat")
            print(f"{self.spaceToMid}\t     7. Agama")
            print(f"{self.spaceToMid}\t     8. Pekerjaan")
            print(f"{self.spaceToMid}\t     9. Status Nikah")
            print(f"{self.spaceToMid}\t     10. Kewarganegaraan")
            print(f"{self.spaceToMid}\t     11. Tanggal Pembelian")
            print(f"{self.spaceToMid}\t     12. Jenis Motor")
            print(f"{self.spaceToMid}\t     13. Qty")
            print(f"{self.spaceToMid}\t     14. Harga")

            print(colored(f"{self.spaceToMid}\t  Pilih: {pilihanWord}", "yellow"), end="", flush=True)
            if not skipChoice:
                pilihan = ord(getche())


            if pilihan == 13: # enter
                if pilihanWord in searchDict.keys():
                    os.system('clear')
                    self.printLogo(menuHistory=True)
                    try:
                        cari = input((f"{self.spaceToMid}\t  Cari: "))
                    except KeyboardInterrupt:
                        skipChoice = True
                        continue

                    if cari == "":
                        skipChoice = True
                        continue

                    searchGet = self.history.searchHistory(cari, searchDict[pilihanWord][0], searchDict[pilihanWord][1])
                    os.system('clear')
                    self.printLogo(menuHistory=True)
                    if len(searchGet) == 0:
                        print(f"{self.spaceToMid}\t\t      {cari} tidak ditemukan!")
                    else:
                        searchGetArr = []
                        for item in searchGet:
                            searchGetArr.append([
                                colored(item['id'], "blue"), item['pembeli']["nik"], item['pembeli']["nama"], item['pembeli']["ttl"], item['pembeli']["jenis_kelamin"], 
                                item['pembeli']["alamat"], item['pembeli']["agama"], item['pembeli']["pekerjaan"], item['pembeli']["kewarganegaraan"], item["tgl_pembelian"],
                                item["jenis_motor"], item["qty"], "Rp. {:,.2f}".format(item["harga"])
                            ])
                        print(f"{self.spaceToMid}\t\t      {cari} ditemukan!")
                        print(f"{tabulate(searchGetArr, headers=self.history.headers, tablefmt='fancy_grid')}")

                    skipChoice = False
                    searchType = searchDict[pilihanWord][0] if searchDict[pilihanWord][1] is None else searchDict[pilihanWord][1]

                    print(colored(f"{self.spaceToMid}\tHasil searching berdasarkan {searchType}!", "blue"))
                    print(colored(f"{self.spaceToMid}\tTekan apa saja untuk kembali ke menu pencarian...", "yellow"), end="", flush=True)
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
        sortDict = {"1": ["id", None], "2": ["pembeli", "nik"], "3": ["pembeli", "nama"], "4": ["pembeli", "ttl"], "5": ["pembeli", "jenis_kelamin"], 
        "6": ["pembeli", "alamat"], "7": ["pembeli", "agama"], "8": ["pembeli", "pekerjaan"], "9": ["pembeli", "statusNikah"], "10": ["pembeli", "pekerjaan"], 
        "11": ["tgl_pembelian", None], "12": ["jenis_motor", None], "13": ["qty", None], "14": ["harga", None]}
        skipChoice = False
        while True:
            os.system('clear')
            self.printLogo(menuHistory=True)
            print(colored(f"{self.spaceToMid}\t  Pilih kolom yang ingin dilakukan sorting:", "blue"))
            print(colored(f"{self.spaceToMid}\t  Tekan esc untuk kembali ke menu history", "red"))
            print(f"{self.spaceToMid}\t     1. ID")
            print(f"{self.spaceToMid}\t     2. NIK")
            print(f"{self.spaceToMid}\t     3. Nama")
            print(f"{self.spaceToMid}\t     4. TTL")
            print(f"{self.spaceToMid}\t     5. Jenis Kelamin")
            print(f"{self.spaceToMid}\t     6. Alamat")
            print(f"{self.spaceToMid}\t     7. Agama")
            print(f"{self.spaceToMid}\t     8. Pekerjaan")
            print(f"{self.spaceToMid}\t     9. Status Nikah")
            print(f"{self.spaceToMid}\t     10. Kewarganegaraan")
            print(f"{self.spaceToMid}\t     11. Tanggal Pembelian")
            print(f"{self.spaceToMid}\t     12. Jenis Motor")
            print(f"{self.spaceToMid}\t     13. Qty")
            print(f"{self.spaceToMid}\t     14. Harga")

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

                    self.history.sortHistory(sortType, sortDict[pilihanWord][0], sortDict[pilihanWord][1])
                    os.system('clear')
                    self.printLogo(menuHistory=True)
                    
                    self.history.printTable()
                    
                    skipChoice = False
                    self.history.refreshHistory() # Reset position

                    sortDictType = sortDict[pilihanWord][0] if sortDict[pilihanWord][1] is None else sortDict[pilihanWord][1]
                    sortModel = "descending" if sortType == "desc" else "ascending"


                    print(colored(f"{self.spaceToMid}\tHasil sorting ({sortModel}) berdasarkan {sortDictType}!", "blue"))
                    print(colored(f"{self.spaceToMid}\tTekan apa saja untuk kembali ke menu sorting...", "yellow"), end="", flush=True)
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
            print(f"{self.spaceToMid}\t\t      Data Paling depan:")
            dataTable = [
                colored(dataPopped['id'], "blue"), dataPopped['pembeli']["nik"], dataPopped['pembeli']["nama"], dataPopped['pembeli']["ttl"], dataPopped['pembeli']["jenis_kelamin"], 
                dataPopped['pembeli']["alamat"], dataPopped['pembeli']["agama"], dataPopped['pembeli']["pekerjaan"], dataPopped['pembeli']["kewarganegaraan"], dataPopped["tgl_pembelian"],
                dataPopped["jenis_motor"], dataPopped["qty"], "Rp. {:,.2f}".format(dataPopped["harga"])
            ]
            
            print(tabulate([dataTable], headers=self.history.headers, tablefmt="fancy_grid", numalign='left'))

            print(colored(f"\n{self.spaceToMid}\t\tData Paling depan berhasil di Hapus!", "blue"), end="", flush=True)
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
            print(f"{self.spaceToMid}\t\t      Data Paling belakang:")
            dataTable = [
                colored(dataPopped['id'], "blue"), dataPopped['pembeli']["nik"], dataPopped['pembeli']["nama"], dataPopped['pembeli']["ttl"], dataPopped['pembeli']["jenis_kelamin"], 
                dataPopped['pembeli']["alamat"], dataPopped['pembeli']["agama"], dataPopped['pembeli']["pekerjaan"], dataPopped['pembeli']["kewarganegaraan"], dataPopped["tgl_pembelian"],
                dataPopped["jenis_motor"], dataPopped["qty"], "Rp. {:,.2f}".format(dataPopped["harga"])    
            ]
            
            print(tabulate([dataTable], headers=self.history.headers, tablefmt="fancy_grid", numalign='left'))

            print(colored(f"\n{self.spaceToMid}\t\tData Paling belakang berhasil di Hapus!", "blue"), end="", flush=True)
            getch()

    def printLogo(self, menuHistory=False):
        if menuHistory:
            tabToMid = " " * 75
            print(colored(tabToMid + "╒" + "═" * 54 + "╕", "blue"), end="")
            print(colored(logoMid, "blue"), end="")
            print(colored("\r" + tabToMid + "│" + " " * 54 + "│", "blue"))
            print(colored(tabToMid + "╘" + "═" * 54 + "╛", "blue"))
        else:
            print(colored("╒" + "═" * 57 + "╕", "blue"), end="")
            print(colored(logo, "blue"), end="")
            print(colored("\r│" + " " * 57 + "│", "blue"))
            print(colored("╘" + "═" * 57 + "╛", "blue"))        

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
        self.menuSekarang = self.menuMotor.copy()
        self.showTabelMotor = True
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
        self.showTabelMotor = False
        self.showUang = False
        self.showTableHistory = False

    def beliMotor(self):
        sedangBeliMotor = True
        while sedangBeliMotor: # Sedang memesan motor
            nik, nama, ttl, jenis_kelamin, alamat, agama, statusNikah, pekerjaan, kewarganegaraan = "", "", "", "", "", "", "", "", ""
            while True: # Input data kustomer
                try:
                    os.system('clear')
                    self.printLogo()
                    print(colored(">> Tekan Control + C apabila ingin cancel dan kembali ke menu", "red"))
                    print(colored(">> Masukkan data pelanggan", "yellow"))
                    # NIK
                    if nik != "":
                        print(f"   NIK \t\t      : {nik}")
                    else:
                        nik = input("   NIK \t\t      : ")
                    if nik == "":
                        nik = ""
                        continue
                    elif nik.isdigit() == False:
                        print(colored("   NIK harus berupa angka!", "red"))
                        nik = ""
                        time.sleep(1)
                        continue
                    elif len(nik) != 16:
                        print(colored("   NIK invalid! Harus berupa 16 digit!", "red"))
                        nik = ""
                        time.sleep(1)
                        continue

                    # Nama
                    if nama != "":
                        print(f"   Nama\t\t      : {nama}")
                    else:
                        nama = input("   Nama\t\t      : ")
                    if nama == "":
                        nama = ""
                        continue

                    # TTL
                    if ttl != "":
                        print(f"   Tempat & Tgl Lahir : {ttl}")
                    else:
                        ttl = input("   Tempat & Tgl Lahir : ")
                    if ttl == "":
                        ttl = ""
                        continue

                    # Jenis Kelamin
                    if jenis_kelamin != "":
                        print(f"   Jenis Kelamin (P/L): {jenis_kelamin}")
                    else:
                        print("   Jenis Kelamin (P/L): ", end="", flush=True)
                        jenis_kelamin = ord(getche().upper())
                        if jenis_kelamin not in [80, 112, 76, 108]:
                            if jenis_kelamin == 3: # Ctrl + C
                                return
                            jenis_kelamin = ""
                            continue
                        else:
                            if jenis_kelamin == 80 or jenis_kelamin == 112:
                                jenis_kelamin = "Perempuan"
                            else:
                                jenis_kelamin = "Laki-laki"
                            continue

                    # Alamat
                    if alamat != "":
                        print(f"   Alamat\t      : {alamat}")
                    else:
                        alamat = input("   Alamat\t      : ")
                    if alamat == "":
                        alamat = ""
                        continue
                    
                    # Agama
                    if agama != "":
                        print(f"   Agama \t      : {agama}")
                    else:
                        agama = input("   Agama \t      : ")
                    if agama == "":
                        agama = ""
                        continue
                    
                    # Status Nikah
                    if statusNikah != "":
                        print(f"   Status Nikah\t      : {statusNikah}")
                    else:
                        statusNikah = input("   Status Nikah\t      : ")
                    if statusNikah == "":
                        statusNikah = ""
                        continue

                    # Pekerjaan
                    if pekerjaan != "":
                        print(f"   Pekerjaan \t      : {pekerjaan}")
                    else:
                        pekerjaan = input("   Pekerjaan\t      : ")
                    if pekerjaan == "":
                        pekerjaan = ""
                        continue

                    # Kewarganegaraan
                    if kewarganegaraan != "":
                        print(f"   Kewarganegaraan    : {kewarganegaraan}")
                    else:
                        kewarganegaraan = input("   Kewarganegaraan    : ")
                    if kewarganegaraan == "":
                        kewarganegaraan = ""
                        continue

                    print("\n>> Data pelanggan berhasil dimasukkan!")
                    time.sleep(1)
                    break
                except KeyboardInterrupt:
                    return

            sedangMemilihMotor = True
            sedangPesanMotor = True
            pesanLagi = False
            arrPesananTabel = []
            arrPesananMotor = []
            arrDataHistory = []
            counter = 1
            totalBeli = 0
            while True:
                if sedangMemilihMotor:
                    os.system('clear')
                    self.printLogo()
                    self.data_PT_XYZ.printTable()
                    print(colored(">> Tekan Control + C apabila ingin cancel dan isi ulang data pembeli", "red"))
                    if pesanLagi:
                        print(colored(">> Tekan Escape apabila tidak jadi menambah motor", "blue"))
                    print(colored(">> Masukkan Pilihan Motor: ", "yellow"), end="", flush=True)

                    pilihanMotor = ord(getch())

                    if pilihanMotor == 3:
                        break
                    elif pilihanMotor == 27 and pesanLagi:
                        sedangMemilihMotor = False
                        sedangPesanMotor = False
                        continue
                    if pilihanMotor not in range(48, 58):
                        continue
                    else:
                        sedangMemilihMotor = False
                
                if sedangPesanMotor:
                    dataMotor = self.data_PT_XYZ.getDataMotorById(pilihanMotor - 48)
                    os.system('clear')
                    self.printLogo()
                    print(colored(">> Tekan Control + C apabila ingin kembali ke menu pilih motor", "red"))
                    print(colored(">> Data Motor Yang Dipilih", "yellow"))
                    print(f"   jenis Motor \t: {dataMotor['jenis_motor']}")
                    print(f"   Stok Tersedia: {dataMotor['qty']}")
                    print(f"   Harga \t: {dataMotor['harga']}")
                    
                    try:
                        jumlahPesan = input(colored("\n>> Masukkan jumlah motor yang ingin dibeli: ", "yellow"))
                    except KeyboardInterrupt:
                        break

                    if jumlahPesan == "":
                        print(colored("   Jumlah motor tidak boleh kosong!", "red"))
                        time.sleep(1)
                        continue
                    elif jumlahPesan.isdigit() == False:
                        print(colored("   Jumlah motor harus berupa angka!", "red"))
                        time.sleep(1)
                        continue
                    elif int(jumlahPesan) > dataMotor['qty']:
                        print(colored("   Jumlah motor melebihi stok tersedia!", "red"))
                        time.sleep(1)
                        continue
                    elif int(jumlahPesan) <= 0:
                        print(colored("   Jumlah motor harus lebih dari 0!", "red"))
                        time.sleep(1)
                        continue
                    
                    harga = int(dataMotor['harga']) * int(jumlahPesan)
                    tanggal_Pembelian = datetime.now().strftime("%d-%m-%Y")
                    arrPesananTabel.append([colored(counter, "blue"), nama, tanggal_Pembelian, dataMotor['jenis_motor'], jumlahPesan, harga])
                    arrPesananMotor.append([dataMotor['id'], jumlahPesan])
                    
                    sedangPesanMotor = False

                    dataHistory = {
                        "pembeli": {
                            "nik": nik,
                            "nama": nama,
                            "ttl": ttl,
                            "jenis_kelamin": jenis_kelamin,
                            "alamat": alamat,
                            "agama": agama,
                            "statusNikah": statusNikah,
                            "pekerjaan": pekerjaan,
                            "kewarganegaraan": kewarganegaraan
                        },
                        "tgl_pembelian": tanggal_Pembelian,
                        "jenis_motor": dataMotor['jenis_motor'],
                        "qty": jumlahPesan,
                        "harga": harga
                    }
                    arrDataHistory.append(dataHistory)
                    totalBeli += harga

                # ------------------------------
                os.system('clear')
                self.printLogo()
                print(tabulate(arrPesananTabel, headers=[colored('No', "yellow"), colored('Pembeli', "yellow"), colored('Tgl Pembelian', "yellow"), colored('Jenis Motor', "yellow"), colored('QTY', "yellow"), colored('Harga', "yellow")], tablefmt="grid"))
                print(colored("\n>> Pesan motor lagi? (y/n) ", "yellow"), end="", flush=True)
                pilihanMotor = ord(getche())
                if pilihanMotor == 121 or pilihanMotor == 89: # y
                    sedangMemilihMotor = True
                    sedangPesanMotor = True
                    counter += 1
                    pesanLagi = True
                elif pilihanMotor == 110 or pilihanMotor == 78: # n
                    sedangBeliMotor = False

                    self.data_PT_XYZ.pesanMotor(arrPesananMotor)
                    self.uangSekarang += totalBeli
                    self.data_PT_XYZ.saveDataMotorDanUang()
                    self.history.addHistory(arrDataHistory)
                    print(colored("\n>> Data berhasil tersimpan!", "blue"))
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
            print(colored("Apakah anda yakin ingin mereset data? (y/n) ", "red"), end='', flush=True)
        
            pilihan = ord(getche())
            if pilihan not in [89, 121, 78, 110]:
                continue
            else:
                inputSalah = False

            if pilihan == 89 or pilihan == 121:
                self.data_PT_XYZ.resetData()
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
        if mainClass.showTabelMotor:
            mainClass.data_PT_XYZ.printTable()

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
                print(colored("\t\t     " + i[0] + " ◄", "yellow"))
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