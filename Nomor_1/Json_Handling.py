import json
import os

# Directory
dir_path = os.path.dirname(os.path.realpath(__file__))
history_json_path = dir_path + "\\json\\History.json"
dataPTXYZ_json_path = dir_path + "\\json\\Data_PTXYZ.json"

default_DataMotor = [
    {
        "id": 1,
        "jenis_motor": "Revo F1 110",
        "qty": 30,
        "harga": 12_500_000  
    },
    {
        "id": 2,
        "jenis_motor": "New Supra X 125 F1",
        "qty": 30,
        "harga": 18_500_000  
    },
    {
        "id": 3,
        "jenis_motor": "Revo F1 110",
        "qty": 30,
        "harga": 12_500_000 
    },
    {
        "id": 4,
        "jenis_motor": "New Beat F1",
        "qty": 20,
        "harga": 12_000_000  
    },
    {
        "id": 5,
        "jenis_motor": "Vega ZR",
        "qty": 10,
        "harga": 13_500_000  
    },
    {
        "id": 6,
        "jenis_motor": "Jupiter Z",
        "qty": 20,
        "harga": 14_000_000  
    },
    {
        "id": 7,
        "jenis_motor": "Jupiter MX",
        "qty": 15,
        "harga": 17_000_000  
    },
    {
        "id": 8,
        "jenis_motor": "Satria FU 150",
        "qty": 10,
        "harga": 19_500_000 
    },
    {
        "id": 9,
        "jenis_motor": "Shogun R 125",
        "qty": 5,
        "harga": 14_000_000 
    }
]

default_UangPT_XYZ = 400_000_000
    
__all__ = [
    "resetDataMotor",
    "createDataMotorIfGone",
    "updateDataPT",
    "getDataPT",
    "createEmptyHistory",
    "createHistoryIfGone",
    "getHistory",
    "writeAdd_History",
    "deleteAllHistory",
    "deleteCertainHistory"
]

def resetDataMotor():
    with open(dataPTXYZ_json_path, "w") as file:
        file_data = {
            "dataMotor": default_DataMotor,
            "uang": default_UangPT_XYZ
        }
        json.dump(file_data, file, ensure_ascii=False, indent=4)

def createDataMotorIfGone():
    """
    Create the file if not exists
    """
    if not os.path.exists(dataPTXYZ_json_path):
        try:
            resetDataMotor()
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
        createDataMotorIfGone()
        with open(dataPTXYZ_json_path, 'w', encoding='utf-8') as f:
            json.dump(newData, f, ensure_ascii=False, indent=4)
            is_Success = True
            status = "Data Motor Has Been Updated Successfully"
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
        createDataMotorIfGone()
        with open(dataPTXYZ_json_path, 'r', encoding='utf-8') as f:
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
            "pembeli": {
                "nik": "3313131344550022",
                "nama": "Bambang Supriyadi",
                "ttl": "Jakarta, 12 Desember 1995",
                "jenis_kelamin": "L",
                "alamat": "Jl. Raya Bambang",
                "agama": "Islam",
                "statusNikah": "Sudah Menikah",
                "pekerjaan": "PNS",
                "kewarganegaraan": "Indonesia"
            },
            "tgl_pembelian": "04/11/2021", # Format: DD/MM/YYYY
            "jenis_motor": "Revo F1 110",
            "qty": "2",
            "harga": "28000000"
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
                "pembeli": {
                    "nik": item['pembeli']['nik'],
                    "nama": item['pembeli']['nama'],
                    "ttl": item['pembeli']['ttl'],
                    "jenis_kelamin": item['pembeli']['jenis_kelamin'],
                    "alamat": item['pembeli']['alamat'],
                    "agama": item['pembeli']['agama'],
                    "statusNikah": item['pembeli']['statusNikah'],
                    "pekerjaan": item['pembeli']['pekerjaan'],
                    "kewarganegaraan": item['pembeli']['kewarganegaraan']
                },
                "tgl_pembelian": item['tgl_pembelian'],
                "jenis_motor": item['jenis_motor'],
                "qty": item['qty'],
                "harga": item['harga']
            }
            newHistory['history'].append(old_data)
            countId += 1

        # Add the new data
        toAddNew = {
            "id": countId,
            "pembeli": {
                "nik": new_data['pembeli']['nik'],
                "nama": new_data['pembeli']['nama'],
                "ttl": new_data['pembeli']['ttl'],
                "jenis_kelamin": new_data['pembeli']['jenis_kelamin'],
                "alamat": new_data['pembeli']['alamat'],
                "agama": new_data['pembeli']['agama'],
                "statusNikah": new_data['pembeli']['statusNikah'],
                "pekerjaan": new_data['pembeli']['pekerjaan'],
                "kewarganegaraan": new_data['pembeli']['kewarganegaraan']
            },
            "tgl_pembelian": new_data['tgl_pembelian'],
            "jenis_motor": new_data['jenis_motor'],
            "qty": new_data['qty'],
            "harga": new_data['harga']
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
                "pembeli": {
                    "nik": new_data['pembeli']['nik'],
                    "nama": new_data['pembeli']['nama'],
                    "ttl": new_data['pembeli']['ttl'],
                    "jenis_kelamin": new_data['pembeli']['jenis_kelamin'],
                    "alamat": new_data['pembeli']['alamat'],
                    "agama": new_data['pembeli']['agama'],
                    "statusNikah": new_data['pembeli']['statusNikah'],
                    "pekerjaan": new_data['pembeli']['pekerjaan'],
                    "kewarganegaraan": new_data['pembeli']['kewarganegaraan']
                },
                "tgl_pembelian": new_data['tgl_pembelian'],
                "jenis_motor": new_data['jenis_motor'],
                "qty": new_data['qty'],
                "harga": new_data['harga']
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
                "pembeli": {
                    "nik": item['pembeli']['nik'],
                    "nama": item['pembeli']['nama'],
                    "ttl": item['pembeli']['ttl'],
                    "jenis_kelamin": item['pembeli']['jenis_kelamin'],
                    "alamat": item['pembeli']['alamat'],
                    "agama": item['pembeli']['agama'],
                    "statusNikah": item['pembeli']['statusNikah'],
                    "pekerjaan": item['pembeli']['pekerjaan'],
                    "kewarganegaraan": item['pembeli']['kewarganegaraan']
                },
                "tgl_pembelian": item['tgl_pembelian'],
                "jenis_motor": item['jenis_motor'],
                "qty": item['qty'],
                "harga": item['harga']
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
