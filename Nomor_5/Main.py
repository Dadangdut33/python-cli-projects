# System
import os
import time
import re
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
        self.menuMainProg = {0: ["1. Input kata", self.inputKata], 1: ["2. Kembali", self.changeLayoutToMenuAwal]}
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
        print(colored(f"{self.spaceToMid}\t      Data berhasil di Refresh!", "blue"))
        time.sleep(1)

    def searchHistory(self):
        searchDict = {1: "id", 2: "input", 3: "output"}
        skipChoice = False
        while True:
            os.system('clear')
            self.printLogo(menuHistory=True)
            print(colored(f"{self.spaceToMid}Pilih kolom yang ingin dilakukan searching:", "blue"))
            print(colored(f"{self.spaceToMid}Tekan esc untuk kembali ke menu history", "red"))
            print(f"{self.spaceToMid}  1. ID")
            print(f"{self.spaceToMid}  2. Input String")
            print(f"{self.spaceToMid}  3. Output Consonant String Value")

            print(colored(f"{self.spaceToMid}Pilih: ", "yellow"), end="", flush=True)
            if not skipChoice:
                pilihan = ord(getche())

            if pilihan in [49, 50, 51]: # 1 2 3
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
                            colored(item['id'], "yellow"), item['input'], item['output']
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
        sortDict = {1: "id", 2: "input", 3: "output"}
        skipChoice = False
        while True:
            os.system('clear')
            self.printLogo(menuHistory=True)
            print(colored(f"{self.spaceToMid}Pilih kolom yang ingin dilakukan sorting:", "blue"))
            print(colored(f"{self.spaceToMid}Tekan esc untuk kembali ke menu history", "red"))
            print(f"{self.spaceToMid}  1. ID")
            print(f"{self.spaceToMid}  2. Input String")
            print(f"{self.spaceToMid}  3. Output Consonant String Value")

            print(colored(f"{self.spaceToMid}Pilih: ", "yellow"), end="", flush=True)
            if not skipChoice:
                pilihan = ord(getche())

            if pilihan in [49, 50, 51]: # 1 2 3
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
                colored(dataPopped['id'], "blue"), dataPopped['input'], dataPopped['output']
            ]
            
            print(tabulate([dataTable], headers=self.history.headers, tablefmt="fancy_grid", numalign='left'))

            print(colored(f"\n{self.spaceToMid}\tData Paling depan berhasil di Hapus!", "yellow"), end="", flush=True)
            getch()

    def popStackHistory(self):
        if self.history.isEmpty():
            os.system('clear')
            self.printLogo(menuHistory=True)
            print(colored(f"{self.spaceToMid}History kosong! Tidak bisa dilakukan pop belakang (Pop Stack)", "red"))
            time.sleep(1)
        else:
            os.system('clear')
            self.printLogo(menuHistory=True)

            dataPopped = self.history.popStackDataHistory()
            print(f"{self.spaceToMid}\t\tData Paling belakang:")
            dataTable = [
                colored(dataPopped['id'], "blue"), dataPopped['input'], dataPopped['output']
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

    def getConsonantVal(self, inputString):
        x = re.split("a|e|i|o|u", inputString) # Split x into a list of strings without the vocal words

        x = ' '.join(x).split() # Remove any empty strings

        numArr = []
        for letter in x: # Loop through the lists
            total = 0
            for char in letter: # Loop through the word inside the lists
                total += ord(char) - ord('a') + 1 # Convert each char to ASCII value then substract by 'a' and add 1
                # This is so that a = 1, b = 2, c = 3, etc.

            numArr.append(total) # Append the total to the numArr

        # Find the max value in the numArr
        maxNum = 0
        for el in numArr:
            if el > maxNum:
                maxNum = el

        return maxNum

    def inputKata(self):
        stringInput = ""
        inputting = True
        while True:
            if inputting:
                try:
                    os.system('clear')
                    self.printLogo()
                    print(colored(">> Tekan Control + C apabila ingin cancel dan kembali ke menu", "red"))
                    if stringInput != "":
                        print(f">> Input string: {stringInput}")
                    else:
                        stringInput = input(">> Input string: ")
                    if stringInput == "":
                        continue
                    if bool(re.search(r"\d", stringInput.strip())):
                        print(colored(">> Input hanya boleh huruf!", "red"))
                        stringInput = ""
                        time.sleep(1)
                        continue
                    if ' ' in stringInput.strip():
                        print(colored(">> Input tidak boleh mengandung spasi!", "red"))
                        stringInput = ""
                        time.sleep(1)
                        continue
                    if any(ele.isupper() for ele in stringInput.strip()):
                        print(colored(">> Input tidak boleh mengandung huruf besar!", "red"))
                        stringInput = ""
                        time.sleep(1)
                        continue
                            
                    ouput = self.getConsonantVal(stringInput)

                    dataHistory = {
                        "input": stringInput,
                        "output": ouput,
                    }

                    os.system('clear')
                    self.printLogo()
                    dataTable = [
                        "", dataHistory['input'], dataHistory['output']
                    ]
            
                    self.history.addHistory([dataHistory])


                    inputting = False
                except KeyboardInterrupt:
                    break
            
            os.system('clear')
            self.printLogo()
            print(tabulate([dataTable], headers=['', 'Input String', "Output Consonant Value"], tablefmt="fancy_grid", numalign='left'))
            print(colored("\n>> Input lagi? (y/n) ", "yellow"), end="", flush=True)
            konfirmasi = ord(getche())
            if konfirmasi == 121 or konfirmasi == 89: # y
                inputting = True
                stringInput = ""
                continue
            elif konfirmasi == 110 or konfirmasi == 78: # n
                break
            else:
                continue

    def printRules(self):
        print(colored(">> Rules:", "blue"))
        print("1. Input hanya huruf tidak boleh ada spasi\n")
        print("2. Input hanya boleh huruf kecil tidak boleh kapital\n")
        print(colored(">> Cara kerja:", "blue"))
        print("Program akan mencari nilai terbesar dari kata yang\nbukan huruf vokal. Diberi nilai dari a-z adalah 1-26\n")
        print(colored(">> Contoh:", "blue"))
        print("Input\t: zodiacs")
        print("Output\t: 26\n")

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