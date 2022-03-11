import json
import os

# Directory
dir_path = os.path.dirname(os.path.realpath(__file__))
history_json_path = dir_path + "\\json\\History.json"
    
__all__ = [
    "createEmptyHistory",
    "createHistoryIfGone",
    "getHistory",
    "writeAdd_History",
    "deleteAllHistory",
    "deleteCertainHistory"
]

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
            "input_a": 1,
            "input_b": 2, 
            "input_c": 3,
            "output": "PAL001",
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
                "input_a": item['input_a'],
                "input_b": item['input_b'],
                "input_c": item['input_c'],
                "output": item['output']
            }
            newHistory['history'].append(old_data)
            countId += 1

        # Add the new data
        toAddNew = {
            "id": countId,
            "input_a": new_data['input_a'],
            "input_b": new_data['input_b'],
            "input_c": new_data['input_c'],
            "output": new_data['output']
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
                "input_a": new_data['input_a'],
                "input_b": new_data['input_b'],
                "input_c": new_data['input_c'],
                "output": new_data['output']
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
                "input_a": item['input_a'],
                "input_b": item['input_b'],
                "input_c": item['input_c'],
                "output": item['output']
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
