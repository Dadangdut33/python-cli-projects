# Fauzan Farhan Antoro - 11200910000004 - 3A - UTS Struktur Data
from Json_Handling import *
from datetime import datetime

# Import tabulate for the table
from tabulate import tabulate
from termcolor import colored

class Data_Tiket:
    def __init__(self):
        status, dataMotor = getDataPT()
        if not status:
            print("Error:", dataMotor)
            exit()
        self.dataTiket = dataMotor
        self.headers = [colored("ID", "yellow"), colored("Kode Penerbangan", "yellow"), colored("Tujuan", "yellow"), colored("Harga", "yellow")]

    def printTable(self):
        arrData = []
        for item in self.dataTiket["dataTiket"]:
            arrData.append([colored(item['id'], "blue"), item["kode_penerbangan"], item["tujuan"], "Rp. {:,.2f}―⠀".format(item["harga"])])

        print(tabulate(arrData, self.headers, tablefmt="fancy_grid", numalign='left')) # fancy_grid

    def pesanTiket(self, totalHarga): # Cukup update uang saja
        for hargaPesanan in totalHarga:
            self.dataTiket['uang'] += hargaPesanan

    def getDataTiketById(self, id):
        for item in self.dataTiket["dataTiket"]:
            if item["id"] == id:
                return item

    def updateUang(self):
        updateDataPT(self.dataTiket)

    def resetData(self):
        try:
            resetDataPesawat()
            self.dataTiket = getDataPT()[1]
        except:
            print("Error:", getDataPT()[1])

class History:
    def __init__(self):
        status, dataHistory = getHistory() 
        if not status:
            print("Error:", dataHistory) 
            exit()
        self.dataHistory = dataHistory
        self.headers = [
            colored("ID", "yellow"), colored("Nama", "yellow"), colored("Kode Penerbangan", "yellow"), colored("Kelas", "yellow"), 
            colored("Tgl\nBerangkat", "yellow"), colored("Jam Berangkat", "yellow"), colored("Jam Datang", "yellow"), colored("Jumlah Dewasa", "yellow"), 
            colored("Jumlah Anak-anak", "yellow"), colored("Total", "yellow")
        ]
        self.capacity = len(self.dataHistory["history"])

    def printTable(self):
        arrData = []
        for item in self.dataHistory["history"]:
            arrData.append([
                colored(item['id'], "blue"), item['nama'], item['kode_penerbangan'], item['kelas'], item['tgl_berangkat'], item['jam_berangkat'], 
                item['jam_datang'], item['penumpang_dewasa'], item['penumpang_anak'], "Rp. {:,.2f}".format(item["total"])
            ])

        if self.capacity == 0:
            arrData.append(["", "", "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀", "⠀⠀⠀⠀⠀⠀⠀⠀⠀", "", "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀", "⠀⠀⠀⠀⠀⠀", "", "", ""])
        
        print(tabulate(arrData, self.headers, tablefmt="fancy_grid", numalign='left')) # fancy_grid

    def refreshHistory(self):
        self.dataHistory = getHistory()[1]
        self.capacity = len(self.dataHistory["history"])

    def addHistory(self, data):
        for dataHistory in data:
            status, statusText = writeAdd_History(dataHistory)
            if not status:
                print("Error:", statusText)

    def isEmpty(self):
        if len(self.dataHistory["history"]) == 0:
            return True
        else:
            return False

    def popQueueDataHistory(self): # Queue popping implementation
        # Get the first item of history
        firstItem = self.dataHistory["history"][0]
        # Delete the first item of history
        deleteCertainHistory(0)
        # Refresh the history
        self.refreshHistory()
        # Return the first item
        return firstItem

    def popStackDataHistory(self): # Stack popping implementation
        # Get the last item of history
        lastItem = self.dataHistory["history"][-1]
        # Delete the last item of history
        deleteCertainHistory(self.capacity - 1)
        # Refresh the history
        self.refreshHistory()
        # Return the last item
        return lastItem

    def searchHistory(self, searchfor, key): # Linear search implementation
        arrData = []
        for item in self.dataHistory["history"]:
            if searchfor.lower() in str(item[key]).lower(): # Di lower agar tidak case sensitive
                arrData.append(item)
        return arrData

    def sortHistory(self, type, key): 
        # Bubble sort implementation
        n = self.capacity
        # Traverse through all array elements
        for i in range(n-1):
        # range(n) also work but outer loop will repeat one time more than needed.
            # Last i elements are already in place
            for j in range(0, n-i-1):
                # traverse the array from 0 to n-i-1
                # Swap if the element found is greater
                # than the next element
                if type == "desc":
                    if 'tgl' in key: # Tgl berangkat
                        if datetime.strptime(self.dataHistory['history'][j][key], r"%d-%m-%Y") < datetime.strptime(self.dataHistory['history'][j+1][key], r"%d-%m-%Y"):
                            self.dataHistory['history'][j], self.dataHistory['history'][j+1] = self.dataHistory['history'][j+1], self.dataHistory['history'][j]
                    else:
                        if self.dataHistory['history'][j][key] < self.dataHistory['history'][j+1][key]:
                            # Keep the id the same as it is. For some reason this is the only way to keep the id the same
                            self.dataHistory['history'][j], self.dataHistory['history'][j+1] = self.dataHistory['history'][j+1], self.dataHistory['history'][j]
                else:
                    if 'tgl' in key: # Tgl berangkat
                        if datetime.strptime(self.dataHistory['history'][j][key], r"%d-%m-%Y") > datetime.strptime(self.dataHistory['history'][j+1][key], r"%d-%m-%Y"):
                            self.dataHistory['history'][j], self.dataHistory['history'][j+1] = self.dataHistory['history'][j+1], self.dataHistory['history'][j]
                    else:
                        if self.dataHistory['history'][j][key] > self.dataHistory['history'][j+1][key]:
                            # Keep the id the same as it is. For some reason this is the only way to keep the id the same
                            self.dataHistory['history'][j], self.dataHistory['history'][j+1] = self.dataHistory['history'][j+1], self.dataHistory['history'][j]