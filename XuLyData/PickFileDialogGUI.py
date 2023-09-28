from tkinter import Tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename


def pickImage():
    isPicking = True
    while isPicking:
        Tk().withdraw() 
        filename = askopenfilename()
        if not isImage(filename):
            messagebox.showwarning(title="Image only", message="Please select an image!!")
            continue
        else:
            isPicking = False
    return filename

def pickVideo():
    isPicking = True
    while isPicking:
        Tk().withdraw() 
        filename = askopenfilename()
        if not isVideo(filename):
            messagebox.showwarning(title="Video only", message="Please select an video!!")
            continue
        else:
            isPicking = False
    return filename

def pickExcel():
    isPicking = True
    while isPicking:
        Tk().withdraw() 
        filename = askopenfilename()
        if not isExcel(filename):
            messagebox.showwarning(title="Excel only", message="Please select an .xlsx!!")
            continue
        else:
            isPicking = False
    return filename

imgFileExtension = ['.jpg', '.png', '.jpqg']
def isImage(filename):
    for ex in imgFileExtension:
        if ex in filename.lower():
            return True
    return False

videoFileExtension = ['.mp4', '.wav', '.ogg', '.avi']
def isVideo(filename):
    for ex in videoFileExtension:
        if ex in filename.lower():
            return True
    return False
ExcelFileExtension = ['.xlsx', '.csv']
def isExcel(filename):
    for ex in ExcelFileExtension:
        if ex in filename.lower():
            return True
    return False

