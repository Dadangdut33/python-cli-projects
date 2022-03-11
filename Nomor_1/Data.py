# Fauzan Farhan Antoro - 11200910000004 - 3A - UTS Struktur Data
from tabulate import tabulate
from Json_Handling import *
from datetime import datetime

# Import tabulate for the table
from tabulate import tabulate
from termcolor import colored

class Data_Motor:
    def __init__(self):
        status, dataMotor = getDataPT()
        if not status:
            print("Error:", dataMotor)
            exit()
        self.dataMotor = dataMotor
        self.headers = [colored("ID", "yellow"), colored("Jenis Motor", "yellow"), colored("QTY", "yellow"), colored("Harga", "yellow")]

    def printTable(self):
        arrData = []
        for item in self.dataMotor["dataMotor"]:
            arrData.append([colored(item['id'], "blue"), item["jenis_motor"], item["qty"], "Rp. {:,.2f}―⠀".format(item["harga"])]) # "Rp. {:,.2f}​⠀".format(item["harga"])]

        print(tabulate(arrData, self.headers, tablefmt="fancy_grid", numalign='left')) # fancy_grid

    def pesanMotor(self, arrPesanan):
        for pesanan in arrPesanan:
            id = pesanan[0]
            qty = int(pesanan[1])
            for item in self.dataMotor["dataMotor"]:
                if item["id"] == id:
                    item["qty"] -= qty # Kurangkan datanya
                    self.dataMotor['uang'] += item["harga"] * qty # Tambahkan uangnya
                    break
            # Tidak mungkin tidak ketemu kecuali jsonnya nya diotak atik
            else:
                print("Error:", "ID Motor tidak ditemukan. Harap jangan modifikasi manual id data motor!")
                exit()

    def getDataMotorById(self, id):
        for item in self.dataMotor["dataMotor"]:
            if item["id"] == id:
                return item

    def saveDataMotorDanUang(self):
        updateDataPT(self.dataMotor)

    def resetData(self):
        try:
            resetDataMotor()
            self.dataMotor = getDataPT()[1]
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
            colored("ID", "yellow"), colored("NIK", "yellow"), colored("Nama", "yellow"), colored("Tempat & Tanggal Lahir", "yellow"), 
            colored("jenis_kelamin", "yellow"), colored("Alamat", "yellow"), colored("Agama", "yellow"), colored("Status Nikah", "yellow"), 
            colored("Pekerjaan", "yellow"), colored("Kewarganegaraan", "yellow"), colored("Tanggal Pembelian", "yellow"), colored("Jenis Motor", "yellow"), 
            colored("QTY", "yellow"), colored("Harga", "yellow")
        ]
        self.capacity = len(self.dataHistory["history"])

    def printTable(self):
        arrData = []
        for item in self.dataHistory["history"]:
            arrData.append([colored(item['id'], "blue"), item['pembeli']["nik"], item['pembeli']["nama"], item['pembeli']["ttl"], item['pembeli']["jenis_kelamin"], 
                item['pembeli']["alamat"], item['pembeli']["agama"], item['pembeli']['statusNikah'],item['pembeli']["pekerjaan"], item['pembeli']["kewarganegaraan"], item["tgl_pembelian"],
                item["jenis_motor"], item["qty"], "Rp. {:,.2f}".format(item["harga"])])

        if self.capacity == 0:
            arrData.append(["", "", "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀", "⠀⠀⠀⠀⠀⠀⠀⠀⠀", "", "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀", "⠀⠀⠀⠀⠀⠀", "", "", "", "", "⠀⠀⠀⠀⠀⠀⠀⠀⠀", "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀"])
        
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

    def searchHistory(self, searchfor, key1, key2 = None): # Linear search implementation
        arrData = []
        if key2 is not None:
            for item in self.dataHistory["history"]:
                if searchfor.lower() in str(item["pembeli"][key2]).lower(): # Di lower agar tidak case sensitive
                    arrData.append(item)
        else:
            for item in self.dataHistory["history"]:
                if searchfor.lower() in str(item[key1]).lower(): # Di lower agar tidak case sensitive
                    arrData.append(item)
        return arrData

    def sortHistory(self, type, key1, key2 = None): 
        # Bubble sort implementation

        if key2 is not None:
            n = self.capacity

            # Traverse through all array elements
            for i in range(n-1):
                # Last i elements are already in place
                for j in range(0, n-i-1):
                    # traverse the array from 0 to n-i-1
                    # Swap if the element found is greater
                    # than the next element
                    if type == "desc":
                        if self.dataHistory['history'][j][key1][key2] < self.dataHistory['history'][j+1][key1][key2]:
                            self.dataHistory['history'][j], self.dataHistory['history'][j+1] = self.dataHistory['history'][j+1], self.dataHistory['history'][j]
                    else:
                        if self.dataHistory['history'][j][key1][key2] > self.dataHistory['history'][j+1][key1][key2]:
                            self.dataHistory['history'][j], self.dataHistory['history'][j+1] = self.dataHistory['history'][j+1], self.dataHistory['history'][j]

        else:
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
                        if 'tgl' in key1: # Tgl beli
                            if datetime.strptime(self.dataHistory['history'][j][key1], r"%d-%m-%Y") < datetime.strptime(self.dataHistory['history'][j+1][key1], r"%d-%m-%Y"):
                                self.dataHistory['history'][j], self.dataHistory['history'][j+1] = self.dataHistory['history'][j+1], self.dataHistory['history'][j]
                        else:
                            if self.dataHistory['history'][j][key1] < self.dataHistory['history'][j+1][key1]:
                                self.dataHistory['history'][j], self.dataHistory['history'][j+1] = self.dataHistory['history'][j+1], self.dataHistory['history'][j]
                    else:
                        if 'tgl' in key1: # Tgl beli
                            if datetime.strptime(self.dataHistory['history'][j][key1], r"%d-%m-%Y") > datetime.strptime(self.dataHistory['history'][j+1][key1], r"%d-%m-%Y"):
                                self.dataHistory['history'][j], self.dataHistory['history'][j+1] = self.dataHistory['history'][j+1], self.dataHistory['history'][j]
                        else:    
                            if self.dataHistory['history'][j][key1] > self.dataHistory['history'][j+1][key1]:
                                self.dataHistory['history'][j], self.dataHistory['history'][j+1] = self.dataHistory['history'][j+1], self.dataHistory['history'][j]

if __name__ == "__main__":
    pass
    # Debug
    # data_Motor = Data_Motor()

    # data_Motor.printTable()
    # print(data_Motor.dataMotor)
    # data_Motor.pesanMotor([[1, 2]])
    # data_Motor.printTable()

    # print(data_Motor.dataMotor)
    # history = History()

    # print(history.dataHistory['history'][0])