import os
import time
import win32api
import customtkinter as ctk
from tkinter import StringVar
from PIL import Image
from CTkToolTip import CTkToolTip
from CTkMessagebox import CTkMessagebox
from distutils.dir_util import copy_tree
import threading


class JExplorer:

    widthIconsLength = 7
    lastWidthIconsLength = 0
    absPath = r""
    lastAbsPath = r""
    buttonPressed = ""
    buttonPresses = 0
    lastButtonObj = None
    badopitons = ["$RECYCLE.BIN", "$Recycle.Bin", "System Volume Information", "desktop.ini"]
    iconsPath = "icons/"
    folder_icon = ctk.CTkImage(light_image=Image.open(iconsPath + "open-folder.png"), dark_image=Image.open(iconsPath + "open-folder.png"), size=(50, 50))
    small_folder_icon = ctk.CTkImage(light_image=Image.open(iconsPath + "open-folder.png"), dark_image=Image.open(iconsPath + "open-folder.png"), size=(15, 15))
    disk_icon = ctk.CTkImage(light_image=Image.open(iconsPath + "harddisk.png"), dark_image=Image.open(iconsPath + "harddisk.png"), size=(80, 80))
    file_icon = ctk.CTkImage(light_image=Image.open(iconsPath + "file.png"), dark_image=Image.open(iconsPath + "file.png"), size=(50, 50))
    small_file_icon = ctk.CTkImage(light_image=Image.open(iconsPath + "file.png"), dark_image=Image.open(iconsPath + "file.png"), size=(15, 15))
    copy_icon = ctk.CTkImage(light_image=Image.open(iconsPath + "copy.png"), dark_image=Image.open(iconsPath + "copy.png"), size=(20, 20))
    paste_icon = ctk.CTkImage(light_image=Image.open(iconsPath + "paste.png"), dark_image=Image.open(iconsPath + "paste.png"), size=(20, 20))
    rename_icon = ctk.CTkImage(light_image=Image.open(iconsPath + "rename.png"), dark_image=Image.open(iconsPath + "rename.png"), size=(20, 20))
    delete_icon = ctk.CTkImage(light_image=Image.open(iconsPath + "delete.png"), dark_image=Image.open(iconsPath + "delete.png"), size=(20, 20))
    creatnew_icon = ctk.CTkImage(light_image=Image.open(iconsPath + "new.png"), dark_image=Image.open(iconsPath + "new.png"), size=(20, 20))
    left_icon = ctk.CTkImage(light_image=Image.open(iconsPath + "left.png"), dark_image=Image.open(iconsPath + "left.png"), size=(25, 25))
    right_icon = ctk.CTkImage(light_image=Image.open(iconsPath + "right.png"), dark_image=Image.open(iconsPath + "right.png"), size=(25, 25))
    home_icon = ctk.CTkImage(light_image=Image.open(iconsPath + "home.png"), dark_image=Image.open(iconsPath + "home.png"), size=(25, 25))
    currentItems = []
    isCopy = False
    copyitem = None
    copydata = None

    def detect_window_resizing(self):
        while 1:
            try:
                time.sleep(0.1)
                self.top.update()
                if self.top.winfo_width() > 1600:
                    self.widthIconsLength = int(str(self.top.winfo_width())[:-2])-2
                else:
                    self.widthIconsLength = int(str(self.top.winfo_width())[:-2])-1
                if self.widthIconsLength != self.lastWidthIconsLength:
                    self.lastWidthIconsLength = self.widthIconsLength
                    if self.absPath == r"":
                        pass
                    else:
                        self.re_align_window()
                else:
                    pass
            except:
                pass

    def creat_new(self):
        if self.absPath == r"" :
            CTkMessagebox(self.top, title="Error!", message=f"Can't create new item here!!", icon="cancel")
        else:
            if CTkMessagebox(self.top, title="Warning!", message=f"What do you want to create new?", option_1="File", option_2="Folder", icon="question").get() == "Folder":
                foldername = ctk.CTkInputDialog(title="Required", text="Type a name for new folder").get_input()
                if os.path.exists(self.absPath + foldername):
                    CTkMessagebox(self.top, title="Error!", message=f"Folder with name '{foldername}' already exists!", icon="cancel")
                else:
                    os.mkdir(self.absPath + foldername)
            else:
                filename = ctk.CTkInputDialog(title="Required", text="Type a name for new file").get_input()
                if os.path.exists(self.absPath + filename):
                    CTkMessagebox(self.top, title="Error!", message=f"File with name '{filename}' already exists!", icon="cancel")
                else:
                    open(self.absPath + filename, 'w').write("")
            self.layerSearch(self.absPath)

    def rename(self, _):
        item = self.remove_newline(_)
        itempath = self.absPath + _
        if item in self.listDisks():
            CTkMessagebox(self.top, title="Fatal error!", message=f"Can't rename disk '{item}' or any other disks!!", icon="cancel")
        else:
            newname = ctk.CTkInputDialog(title="Required", text="Type a new name you want to change to").get_input()
            if os.path.exists(self.absPath + newname):
                CTkMessagebox(self.top, title="Error!", message=f"Name '{newname}' already exists!", icon="cancel")
            else:
                os.rename(itempath, self.absPath + newname)
            self.layerSearch(self.absPath)

    def copy(self, _):
        self.copyitem = self.absPath + self.remove_newline(_)
        if self.copyitem in self.listDisks():
            CTkMessagebox(self.top, title="Fatal error!", message=f"Can't copy disk '{self.copyitem}' or any other disks!!", icon="cancel")
        else:
            self.isCopy = True
            if os.path.isdir(self.copyitem):
                self.copydata = self.copyitem
            else:
                self.copydata = open(self.copyitem, "rb").read()
            self.selected(self.remove_newline(_) + " - copy", iscopy=True)
            self.paste_button.configure(state="normal")

    def paste(self):
        item = self.copyitem.split("\\")[-1]
        self.itempath = self.absPath + item

        if self.isCopy:
            if os.path.exists(self.itempath):
                i = 1
                while 1:
                    new_item_name = self.itempath + " (" + str(i) + ")"
                    if not os.path.exists(new_item_name):
                        self.itempath = new_item_name
                        break

            self.paste_button.configure(state="disabled")
            if os.path.isdir(self.copyitem):
                new_dir = self.absPath + self.copyitem.split("\\")[-1]
                os.mkdir(new_dir)
                copy_tree(self.copydata, new_dir)
            else:
                open(self.itempath, "wb").write(self.copydata)
            self.layerSearch(self.absPath)

    def delete(self, _):
        item = self.remove_newline(_)
        itempath = self.absPath + item
        if item in self.listDisks() or len(self.absPath) <= 3:
            CTkMessagebox(self.top, title="Fatal error!", message=f"Can't delete any disk !!", icon="cancel")
        else:
            try:
                if CTkMessagebox(self.top, title="Warning!", message=f"You will delete '{item}'\nAre you sure!!", option_1="Ok!", option_2="Cancel", icon="cancel").get() == "Ok!":
                    if os.path.isdir(itempath):
                        try:
                            os.rmdir(itempath)
                        except OSError:
                            CTkMessagebox(self.top, title="Access error!", message=f"Can't delete, maybe folder is not empty!", icon="cancel")
                    else:
                        os.remove(itempath)
                    self.layerSearch(self.absPath)
                    self.reset_selected()
            except PermissionError:
                CTkMessagebox(self.top, title="Access error!", message=f"Access is denied", icon="cancel")

    def listDisks(self):
        drives = win32api.GetLogicalDriveStrings()
        drives = drives.split('\000')[:-1]
        return drives

    def clear_window(self):
        for _ in self.currentItems:
            _.grid_forget()
        self.currentItems = []

    def re_align_window(self):
        columsNO = 0
        rowNO = 0
        for _ in self.currentItems:
            _.grid(row=rowNO, column=columsNO, padx=6, pady=5, sticky="n")
            columsNO += 1
            if columsNO >= self.widthIconsLength:
                columsNO = 0
                rowNO += 1

    def remove_newline(self, text):
        if "\n" in text:
            text = text.replace("\n", "")
        return text

    def calc_abs_path(self, current):
        self.lastAbsPath = self.absPath
        if self.absPath == r"":
            self.absPath += self.remove_newline(current)
        else:
            self.absPath += self.remove_newline(current) + "\\"
        return self.absPath

    def return_forward(self, *args):
        if self.lastAbsPath == r"" or self.absPath == r"" or self.lastAbsPath == self.absPath or len(self.absPath) > len(self.lastAbsPath):
            pass
        else:
            self.clear_window()
            self.layerSearch(self.lastAbsPath)
            self.display_path(self.lastAbsPath)
            forward = self.lastAbsPath.split("\\")
            for _ in forward:
                if _ == "":
                    forward.pop(forward.index(_))
            self.calc_abs_path(forward[-1])
            self.reset_selected()

    def return_back(self, *args):
        if self.absPath == r"":
            pass
        else:
            self.clear_window()
            self.lastAbsPath = self.absPath
            back = self.absPath.split("\\")
            self.absPath = r""
            for _ in back:
                if _ == "":
                    back.pop(back.index(_))
            if len(back) > 1:
                for _ in back[:-1]:
                    self.absPath += _ + "\\"
                self.layerSearch(self.absPath)
                self.display_path(self.absPath)
            else:
                self.home_menu()
            self.reset_selected()

    def home_menu(self):
        self.absPath = r""
        self.clear_window()
        for disk in self.listDisks():
            self.new_button(disk, row=0, column=self.listDisks().index(disk), image=self.disk_icon)
        self.display_path("Home")
        self.reset_selected()

    def layerSearch(self, dest):
        columsNO = 0
        rowNO = 0
        try:
            newItems = os.listdir(dest)
            self.clear_window()
            for dir in range(0, len(newItems)):
                if newItems[dir] in self.badopitons:
                    continue
                if os.path.isfile(self.absPath + newItems[dir]) or os.path.isfile(self.lastAbsPath + newItems[dir]):
                    self.new_button(destination=newItems[dir], row=rowNO, column=columsNO, image=self.file_icon)
                else:
                    self.new_button(destination=newItems[dir], row=rowNO, column=columsNO, image=self.folder_icon)
                columsNO += 1
                if columsNO >= self.widthIconsLength:
                    columsNO = 0
                    rowNO += 1
            self.display_path(self.absPath)
        except PermissionError:
            CTkMessagebox(self.top, title="Access error!", message=f"Access is denied", icon="cancel")
            self.return_back()

    def display_path(self, path):
        self.pathString.set(value="")
        self.pathString.set(value=path)

    def selected(self, item, iscopy=False):
        if "\n" in item:
            item = self.remove_newline(item)
        if iscopy:
            item = item.replace(" - copy", "")
            nitem = " " + self.remove_newline(item) + " - copy"
        else:
            nitem = item
        if os.path.isdir(self.absPath + self.remove_newline(item)):
            self.selected_label.configure(text=nitem, image=self.small_folder_icon)
        else:
            self.selected_label.configure(text=nitem, image=self.small_file_icon)

    def reset_selected(self):
        if not self.isCopy:
            try:
                self.selected_label.destroy()
            except:
                pass
            self.selected_label = ctk.CTkLabel(self.top, text="", width=785, height=20, fg_color=self.top.cget("fg_color"), font=("roboto", 14), compound="left")
            self.selected_label.grid(row=1, column=0, pady=2)
            self.buttonPressed = ""

    def entry_search(self, *args):
        try:
            if not self.path_entry.get() == "":
                self.absPath = self.path_entry.get()
                self.layerSearch(self.path_entry.get())
        except:
            CTkMessagebox(self.top, title="Path error", message="Wrong path or invalid syntax!", icon="cancel")

    def gui(self):
        self.top = ctk.CTk()
        self.top.minsize(width=800, height=600)
        self.top.title("J-Explorer")
        self.top.bind("<Alt-Left>", self.return_back)
        self.top.bind("<Alt-Right>", self.return_forward)
        self.top.bind("<Delete>", lambda e:self.delete(self.buttonPressed))
        self.top.bind("<F2>", lambda e:self.rename(self.buttonPressed))
        self.top.bind("<Control-c>", lambda e:self.copy(self.buttonPressed))
        self.top.bind("<Control-v>", self.paste)

        self.ubber_left_tools_frame = ctk.CTkFrame(self.top, height=30, fg_color=self.top.cget("fg_color"))
        self.ubber_left_tools_frame.grid(row=0, column=0, sticky="w", pady=5)

        self.home_button = ctk.CTkButton(self.ubber_left_tools_frame, text="", fg_color=self.ubber_left_tools_frame.cget("fg_color"),
                                         image=self.home_icon, width=10, corner_radius=25, command=self.home_menu)
        self.home_button.pack(side="left", anchor="w")
        CTkToolTip(self.home_button, message="Home")
        self.back_button = ctk.CTkButton(self.ubber_left_tools_frame, text="", fg_color=self.ubber_left_tools_frame.cget("fg_color"),
                                         image=self.left_icon, width=10, corner_radius=25, command=self.return_back)
        self.back_button.pack(side="left", anchor="w")
        CTkToolTip(self.back_button, message="Back")
        self.lastview_button = ctk.CTkButton(self.ubber_left_tools_frame, text="", fg_color=self.ubber_left_tools_frame.cget("fg_color"),
                                             image=self.right_icon, width=10, corner_radius=25, command=self.return_forward)
        self.lastview_button.pack(side="left", anchor="w")
        CTkToolTip(self.lastview_button, message="Last opened page")

        self.ubber_right_tools_frame = ctk.CTkFrame(self.top, height=30, fg_color=self.top.cget("fg_color"))
        self.ubber_right_tools_frame.grid(row=0, column=0, sticky="e", pady=5)

        self.createnew_button = ctk.CTkButton(self.ubber_right_tools_frame, text="", image=self.creatnew_icon, fg_color=self.ubber_right_tools_frame.cget("fg_color"),
                                              width=20, corner_radius=25, command=self.creat_new)
        self.createnew_button.pack(side="right", anchor="e")
        CTkToolTip(self.createnew_button, message="Create new file/folder")
        self.copy_button = ctk.CTkButton(self.ubber_right_tools_frame, text="", image=self.copy_icon, fg_color=self.ubber_right_tools_frame.cget("fg_color"),
                                         width=20, corner_radius=25, command=lambda:self.copy(self.buttonPressed))
        self.copy_button.pack(side="right", anchor="e")
        CTkToolTip(self.copy_button, message="Copy")
        self.paste_button = ctk.CTkButton(self.ubber_right_tools_frame, text="", image=self.paste_icon, fg_color=self.ubber_right_tools_frame.cget("fg_color"),
                                          width=20, corner_radius=25, state="disabled", command=self.paste)
        self.paste_button.pack(side="right", anchor="e")
        CTkToolTip(self.paste_button, message="Paste")
        self.rename_button = ctk.CTkButton(self.ubber_right_tools_frame, text="", image=self.rename_icon, fg_color=self.ubber_right_tools_frame.cget("fg_color"),
                                           width=20, corner_radius=25, command=lambda:self.rename(self.buttonPressed))
        self.rename_button.pack(side="right", anchor="e")
        CTkToolTip(self.rename_button, message="Rename")
        self.delete_button = ctk.CTkButton(self.ubber_right_tools_frame, text="", image=self.delete_icon, fg_color=self.ubber_right_tools_frame.cget("fg_color"),
                                           width=20, corner_radius=25, command=lambda:self.delete(self.buttonPressed))
        self.delete_button.pack(side="right", anchor="e")
        CTkToolTip(self.delete_button, message="Delete")

        self.selected_label = ctk.CTkLabel(self.top, text="", width=785, height=20, fg_color=self.top.cget("fg_color"), font=("roboto", 14), compound="left")
        self.selected_label.grid(row=1, column=0, pady=2)

        self.finder_frame = ctk.CTkScrollableFrame(self.top, width=770, height=500, corner_radius=0)
        self.finder_frame.grid(row=2, column=0, sticky="nsew")


        self.pathString = StringVar(value="Home")
        self.path_entry = ctk.CTkEntry(self.top, width=785, height=20, fg_color=self.finder_frame.cget("fg_color"), font=("roboto", 14), textvariable=self.pathString, border_width=0)
        self.path_entry.grid(row=3, column=0, sticky="nsew")
        self.path_entry.bind("<Return>", self.entry_search)

        self.home_menu()

        self.top.update()
        x_cordinate = int((self.top.winfo_screenwidth() / 2) - (self.top.winfo_width() / 2))
        y_cordinate = int((self.top.winfo_screenheight() / 2) - (self.top.winfo_height() / 2))
        self.top.geometry("{}+{}".format(x_cordinate, y_cordinate - 50))

        self.top.columnconfigure(0, weight=1)
        self.top.rowconfigure(2, weight=1)
        self.top.after(100, threading.Thread(target=self.detect_window_resizing, daemon=True).start)
        self.top.mainloop()

    def new_button(self, destination, row, column, image):
        if len(destination) > 10:
            indicator = 0
            ndest = ""
            for l in destination:
                if indicator == 10:
                    ndest += "\n" + l
                    indicator = 0
                else:
                    ndest += l
                indicator += 1
        else:
            ndest = destination
        if os.path.isdir(self.absPath + destination):
            item = ctk.CTkButton(self.finder_frame, text=ndest, image=image, fg_color=self.finder_frame.cget("fg_color"), width=100, compound="top", corner_radius=15,
                                  command=lambda: self.button_action(item, ndest, logic="open"))
        else:
            item = ctk.CTkButton(self.finder_frame, text=ndest, image=image, fg_color=self.finder_frame.cget("fg_color"), width=100, compound="top", corner_radius=15,
                                  command=lambda: self.button_action(item, ndest, logic="run"))
        item.grid(row=row, column=column, padx=6, pady=5, sticky="n")
        self.currentItems.append(item)

    def button_action(self, obj, btn, logic="open"):
        if btn != self.buttonPressed or self.buttonPresses == 0:
            try:
                if self.lastButtonObj:
                    self.lastButtonObj.configure(fg_color="#2b2b2b")
            except:
                pass
            self.lastButtonObj = obj
            self.buttonPressed = btn
            self.buttonPresses = 0
            self.buttonPresses += 1
            obj.configure(fg_color="#144871")
            self.selected(btn)
        else:
            try:
                if self.lastButtonObj:
                    self.lastButtonObj.configure(fg_color="#2b2b2b")
            except:
                pass
            self.lastButtonObj = None
            self.buttonPresses = 0
            if logic == "open":
                self.layerSearch(self.calc_abs_path(btn))
            else:
                os.startfile(self.absPath + self.remove_newline(btn))


if __name__ == "__main__":
    wf = JExplorer()
    wf.gui()