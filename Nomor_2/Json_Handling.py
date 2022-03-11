import json
import os

# Directory
dir_path = os.path.dirname(os.path.realpath(__file__))
history_json_path = dir_path + "\\json\\History.json"
dataPTPerkutut_json_path = dir_path + "\\json\\Data_PT_Perkutut_Airline.json"

default_DataPTPerkutut = [
    {
        "id": 1,
        "kode_penerbangan": "PAL001",
        "tujuan": "Semarang",
        "harga": 350_000  
    },
    {
        "id": 2,
        "kode_penerbangan": "PAL002",
        "tujuan": "Yogyakarta",
        "harga": 450_000  
    },
    {
        "id": 3,
        "kode_penerbangan": "PAL003",
        "tujuan": "Bali",
        "harga": 700_000 
    },
    {
        "id": 4,
        "kode_penerbangan": "PAL004",
        "tujuan": "Palembang",
        "harga": 500_000  
    },
    {
        "id": 5,
        "kode_penerbangan": "PAL005",
        "tujuan": "Balikpapan",
        "harga": 600_000  
    }
]

default_Uang = 0
    
__all__ = [
    "resetDataPesawat",
    "createDataPesawatIfGone",
    "updateDataPT",
    "getDataPT",
    "createEmptyHistory",
    "createHistoryIfGone",
    "getHistory",
    "writeAdd_History",
    "deleteAllHistory",
    "deleteCertainHistory"
]

def resetDataPesawat():
    with open(dataPTPerkutut_json_path, "w") as file:
        file_data = {
            "dataTiket": default_DataPTPerkutut,
            "uang": default_Uang
        }
        json.dump(file_data, file, ensure_ascii=False, indent=4)

def createDataPesawatIfGone():
    """
    Create the file if not exists
    """
    if not os.path.exists(dataPTPerkutut_json_path):
        try:
            resetDataPesawat()
        except Exception as e:
            print("Error: " + str(e))

def updateDataPT(newData):
    """Update data pt xyz

    Args:
        newData (list): New data to update

    Returns:
        bool: True if success, False if failed
        status: Status text of the operation
    """
    is_Success = False
    status = ""
    try:
        createDataPesawatIfGone()
        with open(dataPTPerkutut_json_path, 'w', encoding='utf-8') as f:
            json.dump(newData, f, ensure_ascii=False, indent=4)
            is_Success = True
            status = "Data Pesawat Has Been Updated Successfully"
    except Exception as e:
        status = str(e)
    finally:
        return is_Success, status

def getDataPT():
    """Get data pt xyz

    Returns:
        is_sucess: Boolean
        status: Data motor if success else error message
    """
    is_Success = False
    status = ""
    try:
        createDataPesawatIfGone()
        with open(dataPTPerkutut_json_path, 'r', encoding='utf-8') as f:
            status = json.load(f)
            is_Success = True
    except Exception as e:
        status = str(e)
    finally:
        return is_Success, status

# -------------------------------------------------
# History
def createEmptyHistory():
    """
    Create empty history file
    """
    try:
        with open(history_json_path, 'w', encoding='utf-8') as f:
            file_data = {
                "history": []
            }

            json.dump(file_data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print("Error: " + str(e))

def createHistoryIfGone():
    """
    Create the json directory if not exists
    """
    if not os.path.exists(history_json_path):
        try:
            createEmptyHistory()
        except Exception as e:
            print("Error: " + str(e))

# Read History
def getHistory():
    """Read history

    Returns:
        bool: True if success, False if failed
        data: Data of the history
    """
    is_Success = False
    data = ""
    try:
        createHistoryIfGone()
        with open(history_json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            is_Success = True
    except FileNotFoundError: # If file still not found create new empty History.json 
        createEmptyHistory()
        data = r"Couldn't found History.Json, History now empty"
    except Exception as e:
        data = str(e)
    finally:
        return is_Success, data

def writeAdd_History(new_data):
    """Write and or add history
    
    # Example of how the data should be written
        new_data = {
            # ID Will be auto generated here
            "nama": "Bambang Supriyadi",
            "kode_penerbangan": "PAL001",
            "kelas": "Ekonomi",
            "tgl_berangkat": "6/9/2022",
            "jam_berangkat": "10:00",
            "jam_datang": "12:00",
            "penumpang_dewasa": 2,
            "penumpang_anak": 1,
            "total": 1000000
        }
    """
    is_Success = False
    status = ""
    try:
        # Get current history, ignore the status
        x, file_data = getHistory()

        # Overwrite the ID and add the new data
        newHistory = {
            "history": []
        }
        countId = 1
        for item in file_data['history']:
            old_data = {
                "id": countId,
                "nama": item['nama'],
                "kode_penerbangan": item['kode_penerbangan'],
                "kelas": item['kelas'],
                "tgl_berangkat": item['tgl_berangkat'],
                "jam_berangkat": item['jam_berangkat'],
                "jam_datang": item['jam_datang'],
                "penumpang_dewasa": item['penumpang_dewasa'],
                "penumpang_anak": item['penumpang_anak'],
                "total": item['total']
            }
            newHistory['history'].append(old_data)
            countId += 1

        # Add the new data
        toAddNew = {
            "id": countId,
            "nama": new_data['nama'],
            "kode_penerbangan": new_data['kode_penerbangan'],
            "kelas": new_data['kelas'],
            "tgl_berangkat": new_data['tgl_berangkat'],
            "jam_berangkat": new_data['jam_berangkat'],
            "jam_datang": new_data['jam_datang'],
            "penumpang_dewasa": new_data['penumpang_dewasa'],
            "penumpang_anak": new_data['penumpang_anak'],
            "total": new_data['total']
        }

        newHistory['history'].append(toAddNew)

        # Overwrite file
        with open(history_json_path,'w', encoding='utf-8') as f:
            json.dump(newHistory, f, ensure_ascii=False, indent = 4)
            is_Success = True
            status = "no error"

    except FileNotFoundError: # If fail to read History.json because of file not found error, then create new one with the new data provided
        with open(history_json_path, 'w', encoding='utf-8') as f:
            toAddNew = {
                "id": 1,
                "nama": new_data['nama'],
                "kode_penerbangan": new_data['kode_penerbangan'],
                "kelas": new_data['kelas'],
                "tgl_berangkat": new_data['tgl_berangkat'],
                "jam_berangkat": new_data['jam_berangkat'],
                "jam_datang": new_data['jam_datang'],
                "penumpang_dewasa": new_data['penumpang_dewasa'],
                "penumpang_anak": new_data['penumpang_anak'],
                "total": new_data['total']
            }
            file_data = {
                "history": [toAddNew]
            }

            json.dump(file_data, f, ensure_ascii=False, indent=4)
            is_Success = True
            status = "no error"
    except Exception as e:
        status = str(e)
    finally:
        return is_Success, status

def updateOverWriteHistory(self, file_data):
    is_Success = False
    status = ""
    try:
        # Overwrite the ID and add the new data
        newHistory = {
            "history": file_data['history']
        }

        # Overwrite file
        with open(history_json_path,'w', encoding='utf-8') as f:
            json.dump(newHistory, f, ensure_ascii=False, indent = 4)
            is_Success = True
            status = "no error"
    except Exception as e:
        status = str(e)
    finally:
        return is_Success, status

def deleteAllHistory(): 
    """Delete all history

    Returns:
        bool: True if success, False if failed
        status: Status text of the operation
    """
    is_Success = False
    status = ""
    try:
        createEmptyHistory()
        status = "All of The History Data Have Been Deleted Successfully"
    except Exception as e:
        status = str(e)
    finally:
        return is_Success, status

def deleteCertainHistory(index):
    """Delete certain history

    Args:
        index (int): Index of the history to delete

    Returns:
        bool: True if success, False if failed
        status: Status text of the operation
    """
    is_Success = False
    status = ""
    try:
        # Get current history, ignore the status
        x, file_data = getHistory()

        # Pop the selected value first
        file_data["history"].pop(index)

        # Then
        # Overwrite the ID and add the new data
        newHistory = {
            "history": []
        }

        countId = 1
        for item in file_data['history']:
            old_data = {
                "id": countId,
                "nama": item['nama'],
                "kode_penerbangan": item['kode_penerbangan'],
                "kelas": item['kelas'],
                "tgl_berangkat": item['tgl_berangkat'],
                "jam_berangkat": item['jam_berangkat'],
                "jam_datang": item['jam_datang'],
                "penumpang_dewasa": item['penumpang_dewasa'],
                "penumpang_anak": item['penumpang_anak'],
                "total": item['total']
            }
            newHistory['history'].append(old_data)
            countId += 1

        # Overwrite file
        with open(history_json_path,'w', encoding='utf-8') as f:
            json.dump(newHistory, f, ensure_ascii=False, indent = 4)
            is_Success = True
            status = "Selected History Has Been Deleted Successfully"
    except Exception as e:
        status = str(e)
    finally:
        return is_Success, status
