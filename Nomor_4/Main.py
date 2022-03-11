# System
import os
import time
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
from Data import History
from Art import *
from Json_Handling import *
 
# Ext
from termcolor import colored
from tabulate import tabulate

class MainProgram:
    def __init__(self):
        self.history = History()
        self.isRunning = True
        self.showTableHistory = False
        self.showRules = False

        self.menuAwal = {0: ["1. Main Program", self.changeLayoutToMenuMainProgram], 1: ["2. History", self.changeLayoutTOMenuHistory], 2: ["3. Exit", self.exitProgram]}
        self.menuMainProg = {0: ["1. Input", self.inputAngka], 1: ["2. Kembali", self.changeLayoutToMenuAwal]}
        self.spaceToMid = ""
        self.menuHistory = {0: [f"{self.spaceToMid}1. Search", self.searchHistory], 1: [f"{self.spaceToMid}2. Sort", self.sortHistory], 2: [f"{self.spaceToMid}3. Pop depan (Queue)", self.popQueueHistory], 
                            3: [f"{self.spaceToMid}4. Pop Belakang (Stack)", self.popStackHistory], 4: [f"{self.spaceToMid}5. Refresh Data", self.refreshDataHistory], 5: [f"{self.spaceToMid}6. Kembali", self.changeLayoutToMenuAwal]}
        
        self.menuSekarang = self.menuAwal.copy()
        self.posisiMenuSekarang = 0
        self.posisiMenuSebelumnya = 0

    def refreshDataHistory(self):
        os.system('clear')
        self.history.refreshHistory()
        self.printLogo(menuHistory=True)
        print(colored(f"{self.spaceToMid}\t     Data berhasil di Refresh!", "blue"))
        time.sleep(1)

    def searchHistory(self):
        searchDict = {1: "id", 2: "barisan_tayangan", 3: "barisan_cek_awal", 4: "barisan_cek_akhir", 5: "output"}
        skipChoice = False
        while True:
            os.system('clear')
            self.printLogo(menuHistory=True)
            print(colored(f"{self.spaceToMid}Pilih kolom yang ingin dilakukan sorting:", "blue"))
            print(colored(f"{self.spaceToMid}Tekan esc untuk kembali ke menu history", "red"))
            print(f"{self.spaceToMid}  1. ID")
            print(f"{self.spaceToMid}  2. Barisan Tayangan")
            print(f"{self.spaceToMid}  3. Cek Awal")
            print(f"{self.spaceToMid}  4. Cek Akhir")
            print(f"{self.spaceToMid}  5. Output")
            print(colored(f"{self.spaceToMid}Pilih: ", "yellow"), end="", flush=True)
            if not skipChoice:
                pilihan = ord(getche())

            if pilihan in [49, 50, 51, 52, 53]: # 1 2 3 4 5
                os.system('clear')
                self.printLogo(menuHistory=True)
                try:
                    cari = input((f"{self.spaceToMid}>> Cari: "))
                except KeyboardInterrupt:
                    skipChoice = True
                    continue

                if cari == "":
                    skipChoice = True
                    continue

                searchGet = self.history.searchHistory(cari, searchDict[pilihan - 48])
                os.system('clear')
                self.printLogo(menuHistory=True)
                if len(searchGet) == 0:
                    print(f"{self.spaceToMid}>> \"{cari}\" tidak ditemukan!")
                else:
                    searchGetArr = []
                    for item in searchGet:
                        searchGetArr.append([
                            colored(item['id'], "blue"), item['barisan_tayangan'], item['barisan_cek_awal'], item['barisan_cek_akhir'], item['output']
                        ])
                    print(f"{self.spaceToMid}>> \"{cari}\" ditemukan!")
                    print(f"{tabulate(searchGetArr, headers=self.history.headers, tablefmt='fancy_grid')}")

                skipChoice = False

                print(colored(f"{self.spaceToMid}>> Hasil searching berdasarkan {searchDict[pilihan - 48]}!", "blue"))
                print(colored(f"{self.spaceToMid}Tekan apa saja untuk kembali ke menu pencarian...", "yellow"), end="", flush=True)
                getch()

            elif pilihan == 27: # esc
                break

    def sortHistory(self):
        sortDict = {1: "id", 2: "barisan_tayangan", 3: "barisan_cek_awal", 4: "barisan_cek_akhir", 5: "output"}
        skipChoice = False
        while True:
            os.system('clear')
            self.printLogo(menuHistory=True)
            print(colored(f"{self.spaceToMid}Pilih kolom yang ingin dilakukan sorting:", "blue"))
            print(colored(f"{self.spaceToMid}Tekan esc untuk kembali ke menu history", "red"))
            print(f"{self.spaceToMid}  1. ID")
            print(f"{self.spaceToMid}  2. Barisan Tayangan")
            print(f"{self.spaceToMid}  3. Cek Awal")
            print(f"{self.spaceToMid}  4. Cek Akhir")
            print(f"{self.spaceToMid}  5. Output")

            print(colored(f"{self.spaceToMid}Pilih: ", "yellow"), end="", flush=True)
            if not skipChoice:
                pilihan = ord(getche())

            if pilihan in [49, 50, 51, 52, 53]:
                    os.system('clear')
                    self.printLogo(menuHistory=True)
                    print(colored(f"{self.spaceToMid}Ascending/Descending (1/2): ", "yellow"), end="", flush=True)
                    pilihanTipe = ord(getche())
                    if pilihanTipe not in [49, 50]:
                        skipChoice = True
                        continue

                    if pilihanTipe == 49:
                        sortType = "asc"
                    else:
                        sortType = "desc"

                    self.history.sortHistory(sortType, sortDict[pilihan - 48])
                    os.system('clear')
                    self.printLogo(menuHistory=True)
                    
                    self.history.printTable()

                    skipChoice = False
                    self.history.refreshHistory() # Reset position

                    sortModel = "descending" if sortType == "desc" else "ascending"
                    print(colored(f"{self.spaceToMid}Hasil sorting ({sortModel}) berdasarkan {sortDict[pilihan - 48]}!", "blue"))
                    print(colored(f"{self.spaceToMid}Tekan apa saja untuk kembali ke menu sorting...", "yellow"), end="", flush=True)
                    getch()
                    continue
            elif pilihan == 27: # esc
                break

    def popQueueHistory(self):
        if self.history.isEmpty():
            os.system('clear')
            self.printLogo(menuHistory=True)
            print(colored(f"{self.spaceToMid}History kosong! Tidak bisa dilakukan pop depan (Pop Queue)", "red"))
            time.sleep(1)
        else:
            os.system('clear')
            self.printLogo(menuHistory=True)
            
            dataPopped = self.history.popQueueDataHistory()
            print(f"{self.spaceToMid}\t\tData Paling depan:")
            dataTable = [
                colored(dataPopped['id'], "blue"), dataPopped['barisan_tayangan'], dataPopped['barisan_cek_awal'], dataPopped['barisan_cek_akhir'], dataPopped['output']
            ]
            
            print(tabulate([dataTable], headers=self.history.headers, tablefmt="fancy_grid", numalign='left'))

            print(colored(f"\n{self.spaceToMid}\tData Paling depan berhasil di Hapus!", "yellow"), end="", flush=True)
            getch()

    def popStackHistory(self):
        if self.history.isEmpty():
            os.system('clear')
            self.printLogo(menuHistory=True)
            print(f"{self.spaceToMid}History kosong! Tidak bisa dilakukan pop belakang (Pop Stack)")
            time.sleep(1)
        else:
            os.system('clear')
            self.printLogo(menuHistory=True)

            dataPopped = self.history.popStackDataHistory()
            print(f"{self.spaceToMid}\t\tData Paling belakang:")
            dataTable = [
                colored(dataPopped['id'], "blue"), dataPopped['barisan_tayangan'], dataPopped['barisan_cek'], dataPopped['output']
            ]
            
            print(tabulate([dataTable], headers=self.history.headers, tablefmt="fancy_grid", numalign='left'))

            print(colored(f"\n{self.spaceToMid}\tData Paling belakang berhasil di Hapus!", "yellow"), end="", flush=True)
            getch()

    def printLogo(self, menuHistory=False):
        print(colored("╒" + "═" * 51 + "╕", "blue"), end="")
        print(colored(logo, "blue"), end="")
        print(colored("\r│" + " " * 51 + "│", "blue"))
        print(colored("╘" + "═" * 51 + "╛", "blue"))

    def exitProgram(self, ctrlC = False):
        self.isRunning = False
        os.system('clear')
        if ctrlC: print("Ctrl+C pressed! Program will exit!")
        print(colored(exit_msg, "blue"), end ="")
        time.sleep(1)
        os.system('clear')
        exit()
    
    def changeLayoutToMenuMainProgram(self):
        self.posisiMenuSebelumnya = 0
        self.posisiMenuSekarang = 0
        self.menuSekarang.clear()
        self.menuSekarang = self.menuMainProg.copy()
        self.showRules = True

    def changeLayoutTOMenuHistory(self):
        self.posisiMenuSebelumnya = 0
        self.posisiMenuSekarang = 0
        self.menuSekarang.clear()
        self.menuSekarang = self.menuHistory.copy()
        self.showTableHistory = True
        self.showRules = False

    def changeLayoutToMenuAwal(self):
        self.posisiMenuSebelumnya = 0
        self.posisiMenuSekarang = 0
        self.menuSekarang.clear()
        self.menuSekarang = self.menuAwal.copy()
        self.showTableHistory = False
        self.showRules = False

    def getOutput(self, arrTayangan, arrCekAwal, arrCekAkhir):
        outputArr = []
        for i in range(len(arrCekAwal)):
            if arrCekAwal[i] == arrCekAkhir[i]:
                outputArr.append(arrTayangan[arrCekAwal[i] - 1])
            else:
                outputArr.append(sum(arrTayangan[arrCekAwal[i] - 1 : arrCekAkhir[i]]))
        return outputArr

    def getStringValue(self, arr):
        stringValue = ""
        for i in range(len(arr)):
            stringValue += str(arr[i]) + ", "
        return stringValue[:-2] # Remove last ,

    def inputAngka(self):
        inputting = True
        banyakHari = jumlahTeman = ""
        arrBanyakTayangan = []
        arrCekAwal = []
        arrCekAkhir = []
        check = True
        while True:
            if inputting:
                try:
                    os.system('clear')
                    self.printLogo()
                    print(colored(">> Tekan Control + C apabila ingin cancel dan kembali ke menu", "red"))
                    # --------------------------------
                    if banyakHari != "":
                        print(f">> Input berapa banyak hari tayangan: {banyakHari}")
                    else:
                        banyakHari = input(">> Input berapa banyak hari tayangan: ")
                        if banyakHari == "":
                            continue
                        try:
                            banyakHari = int(banyakHari)
                        except ValueError:
                            print(colored(">> Input harus berupa angka!", "red"))
                            banyakHari = ""
                            time.sleep(1)
                            continue
                        if banyakHari < 1 or banyakHari > 10:
                            print(colored(">> Input harus berupa angka 1-100!", "red"))
                            banyakHari = ""
                            time.sleep(1)
                            continue

                        loopAmount = banyakHari
                        tempCnt = 0
                        while tempCnt < loopAmount:
                            try:
                                os.system('clear')
                                self.printLogo()
                                print(colored(">> Tekan Control + C apabila ingin cancel dan kembali ke menu input hari tayangan", "red"))
                                temp1 = ""
                                print(f">> Barisan tayangan : {self.getStringValue(arrBanyakTayangan)}")
                                temp1 = input(f">> Input banyak tayangan di hari ke-{tempCnt + 1}: ")
                                if temp1 == "":
                                    continue
                                try:
                                    temp1 = int(temp1)
                                except ValueError:
                                    print(colored(">> Input harus berupa angka!", "red"))
                                    time.sleep(1)
                                    continue
                                if temp1 < 1 or temp1 > 100:
                                    print(colored(">> Input harus berupa angka 1-100!", "red"))
                                    time.sleep(1)
                                    continue

                                arrBanyakTayangan.append(temp1)
                                tempCnt += 1

                            except KeyboardInterrupt:
                                check = False
                                jumlahTeman = banyakHari= ""
                                arrBanyakTayangan = []
                                arrCekAwal = []
                                arrCekAkhir = []
                                break
                        else:
                            continue

                    if not check:
                        check = True
                        continue

                    print(f">> Barisan tayangan : {self.getStringValue(arrBanyakTayangan)}")

                    # --------------------------------
                    if jumlahTeman != "":
                        print(f">> Input banyak jumlah teman: {jumlahTeman}")
                    else:
                        jumlahTeman = input(">> Input banyak jumlah teman: ")
                        if jumlahTeman == "":
                            continue
                        try:
                            jumlahTeman = int(jumlahTeman)
                        except ValueError:
                            print(colored(">> Input harus berupa angka!", "red"))
                            jumlahTeman = ""
                            time.sleep(1)
                            continue
                        if jumlahTeman < 1 or jumlahTeman > 10:
                            print(colored(">> Input harus berupa angka 1-100!", "red"))
                            jumlahTeman = ""
                            time.sleep(1)
                            continue

                        loopAmount = jumlahTeman
                        tempCnt = 0
                        while tempCnt < jumlahTeman:
                            try:
                                os.system('clear')
                                self.printLogo()
                                print(colored(">> Tekan Control + C apabila ingin cancel dan kembali ke menu input hari tayangan", "red"))
                                temp1 = ""
                                temp2 = ""
                                print(f">> Barisan pengecekan hari awal oleh teman : {self.getStringValue(arrCekAwal)}")
                                print(f">> Barisan pengecekan hari akhir oleh teman : {self.getStringValue(arrCekAkhir)}")

                                # ------------------------------
                                temp1 = input(f">> Cek hari awal oleh teman ke-{tempCnt + 1}: ")
                                if temp1 == "":
                                    continue
                                try:
                                    temp1 = int(temp1)
                                except ValueError:
                                    print(colored(">> Input harus berupa angka!", "red"))
                                    time.sleep(1)
                                    continue
                                if temp1 < 1 or temp1 > banyakHari:
                                    print(colored(f">> Input harus berupa angka 1-{banyakHari}!", "red"))
                                    time.sleep(1)
                                    continue

                                temp2 = input(f">> Cek hari akhir oleh teman ke-{tempCnt + 1}: ")
                                if temp2 == "":
                                    continue
                                try:
                                    temp2 = int(temp2)
                                except ValueError:
                                    print(colored(">> Input harus berupa angka!", "red"))
                                    time.sleep(1)
                                    continue
                                if temp2 < 1 or temp2 > banyakHari:
                                    print(colored(f">> Input harus berupa angka 1-{banyakHari}!", "red"))
                                    time.sleep(1)
                                    continue
                                elif temp2 < temp1:
                                    print(colored(">> Input hari akhir tidak bisa lebih kecil dari input hari awal!", "red"))
                                    time.sleep(1)
                                    continue

                                arrCekAwal.append(temp1)
                                arrCekAkhir.append(temp2)
                                tempCnt += 1
                            except KeyboardInterrupt:
                                check = False
                                jumlahTeman = banyakHari= ""
                                arrBanyakTayangan = []
                                arrCekAwal = []
                                arrCekAkhir = []
                                break
                        else:
                            continue

                    if not check:
                        check = True
                        continue

                    print(f">> Barisan pengecekan hari awal oleh teman : {self.getStringValue(arrCekAwal)}")
                    print(f">> Barisan pengecekan hari akhir oleh teman : {self.getStringValue(arrCekAkhir)}")

                    
                    ouput = self.getOutput(arrBanyakTayangan, arrCekAwal, arrCekAkhir)

                    dataHistory = {
                        "barisan_tayangan": self.getStringValue(arrBanyakTayangan),
                        "barisan_cek_awal": self.getStringValue(arrCekAwal),
                        "barisan_cek_akhir": self.getStringValue(arrCekAkhir),
                        "output": self.getStringValue(ouput),
                    }

                    os.system('clear')
                    self.printLogo()
                    dataTable = [
                        dataHistory['barisan_tayangan'], dataHistory['barisan_cek_awal'], dataHistory['barisan_cek_akhir'], dataHistory['output']
                    ]
            
                    self.history.addHistory([dataHistory])

                    inputting = False
                except KeyboardInterrupt:
                    break
            
            os.system('clear')
            self.printLogo()
            print(tabulate([dataTable], headers=[colored("Barisan Tayangan", "yellow"), colored("Cek Awal", "yellow"), colored("Cek Akhir", "yellow"), colored("Output", "yellow")], tablefmt="fancy_grid", numalign='left'))
            print(colored("\n>> Hitung lagi? (y/n) ", "yellow"), end="", flush=True)
            konfirmasi = ord(getche())
            if konfirmasi == 121 or konfirmasi == 89: # y
                inputting = True
                banyakHari = jumlahTeman = ""
                arrBanyakTayangan = []
                arrCekAwal = []
                arrCekAkhir = []
                continue
            elif konfirmasi == 110 or konfirmasi == 78: # n
                break
            else:
                continue

    def printRules(self):
        print(colored(">> Rules:", "blue"))
        print("1. Input banyak tayangan hanya boleh 1-100")
        print("2. Input jumlah tayangan per hari hanya boleh 1-100")
        print("3. Input hari pengecekan oleh teman adalah 1-N dimana N nya adalah banyak hari tayangan")
        print("4. Input hari pengecekan awal tidak boleh lebih besar dari hari akhir\n")
        print(colored(">> Cara kerja:", "blue"))
        print("Program akan menghitung jumlah tayangan pada periode hari awal dan akhir\n")
        print(colored(">> Contoh:", "blue"))
        print("Banyak hari tayangan\t: 5")
        print("Jumlah view\t\t: 2, 5, 1, 9, 7")
        print("Jumlah teman\t\t: 9")
        print("Cek hari awal\t\t: 1, 1, 2, 4")
        print("Cek hari akhir\t\t: 1, 3, 5, 5")
        print("Output\t\t\t: 2, 8, 22, 16\n")


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
        if mainClass.showTableHistory:
            mainClass.history.printTable()

        # --------------------------------
        if mainClass.showRules:
            mainClass.printRules()

        # --------------------------------------------------
        # Menu value
        counter = 0
        for i in mainClass.menuSekarang.values():
            if mainClass.posisiMenuSekarang != counter:
                print("\t\t  " + i[0])
            else:
                print(colored("\t\t   " + i[0] + " ◄", 'yellow'))
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