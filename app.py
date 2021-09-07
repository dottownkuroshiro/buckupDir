import tkinter as tk
from tkinter import ttk, StringVar
import zipfile
import os
from _ast import Pass, Break
from idlelib.idle_test.mock_tk import Entry
import tkinter
from Tools.demo.sortvisu import WIDTH
from tkinter.constants import BOTTOM
from tkinter import filedialog
from pip._internal import self_outdated_check
from test.test_decimal import file
from datetime import datetime
from test.test_unicode_file_functions import filenames
import shutil
from tkinter.scrolledtext import ScrolledText


class Application(tk.Frame):
    def __init__(self,master):
        
        super().__init__(master)
        self.pack()
        master.geometry("600x250")
        master.title("DirBuckup")
        self.create_widgets()
    
    def create_widgets(self):
        
        self.frame_1 = ttk.Frame(self,padding=(10,10))
        self.frame_1.pack()
        
        self.label1 = ttk.Label(self.frame_1, text=" バックアップ元フォルダ")
        self.label1.grid(row=0,column=1)
        
        self.button_1 = ttk.Button(self.frame_1, text="参照", command=self.button_readdir_clicked)
        self.button_1.grid(row=0,column=3)
        
        self.readdir_entry = StringVar()
        self.entry1 = ttk.Entry(self.frame_1, textvariable=self.readdir_entry,width=50)
        self.entry1.grid(row=0,column=2)
        
        self.label2 = ttk.Label(self.frame_1, text=" バックアップ先フォルダ")
        self.label2.grid(row=1,column=1)
        
        self.button_2 = ttk.Button(self.frame_1, text="参照", command=self.button_savedir_clicked)
        self.button_2.grid(row=1,column=3)
        
        self.savedir_entry = StringVar()
        self.entry2 = ttk.Entry(self.frame_1, textvariable=self.savedir_entry,width=50)
        self.entry2.grid(row=1,column=2)
        
        self.button_3 = ttk.Button(self.frame_1, text="バックアップ実行" ,command=self.save_zip)
        self.button_3.grid(row=2,column=3)
        
        self.frame_2 = ttk.Frame(self,padding=(10,10))
        self.frame_2.pack()
        
        
        self.textarea = ScrolledText(self.frame_2, font=("", 8), height=8, width=80)
        self.textarea.grid(row=1,column=0)
        
        self.label2 = ttk.Label(self.frame_2, text=" Log :",width=80)
        self.label2.grid(row=0,column=0)

    
    def button_readdir_clicked(self):
        self.iReadDir = os.path.abspath(os.path.dirname(__file__)) # カレントディレクトリを取得
        self.iReadDirPath = filedialog.askdirectory(initialdir = self.iReadDir) 
        self.readdir_entry.set(self.iReadDirPath)
    
    def button_savedir_clicked(self):
        self.iSaveDir = os.path.abspath(os.path.dirname(__file__)) # カレントディレクトリを取得
        self.iSaveDirPath = filedialog.askdirectory(initialdir = self.iSaveDir)
        self.savedir_entry.set(self.iSaveDirPath)

    def save_zip(self):
        self.folder = self.entry1.get() # entry1のpath取得
        self.textarea.insert(tk.END,"パス" + str(self.folder) +"を取得\n")
        self.folder = os.path.abspath(self.folder) # 絶対パスへ変換
        self.textarea.insert(tk.END,"フルパス" +str(self.folder)+ "に変換\n")
        
        self.now = datetime.now()
        self.now = self.now.strftime("%Y-%m-%d_%H%M%S")
        self.textarea.insert(tk.END,"日時"+str(self.now)+"を取得\n")
        self.num = 0
        
        while True:
            self.zip_filename = os.path.basename(self.folder) + "_"  + str(self.now) + ".zip"
            self.textarea.insert(tk.END,"zip_filename : " + str(self.zip_filename) +"を作成\n")
            if not os.path.exists(self.zip_filename):
                break
            self.num =+1
            self.now = str(self.now) + "(" + self.num +")"
        
        self.backup_zip = zipfile.ZipFile(self.zip_filename, "w")
        
        for foldername, subfolders, filenames in os.walk(self.folder):
            self.backup_zip.write(foldername)
            self.textarea.insert(tk.END,str(foldername)+"を圧縮ファイルに追加\n")
            for filename in filenames:
                new_base = os.path.basename(self.folder) + "_"
                self.textarea.insert(tk.END,str(filename)+"を圧縮ファイルに追加\n")
                if filename.startswith(new_base) and filename.endswith(".zip"):
                    continue # forループへ
                self.backup_zip.write(os.path.join(foldername, filename))
        self.backup_zip.close()
        shutil.move(self.zip_filename,self.entry2.get())
        self.textarea.insert(tk.END,"バックアップ完了")
        
def main():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()


if __name__ == "__main__":
    main()