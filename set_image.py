import tkinter.filedialog
from tkinter import *
from PIL import Image, ImageTk
class set_img(object):
    def __init__(self, boss):
        self.boss = boss

    #redimensionner une image
    def redim(self):
        self.fen_r = Toplevel(self.boss)
        self.fen_r.title("redimensionnement")
        Label(self.fen_r, text="width: ").grid(row=0, column=0, sticky=W)
        Label(self.fen_r, text="height: ").grid(row=0, column=1, sticky=W)
        self.enter_width = Entry(self.fen_r)
        self.enter_width.grid(row=1, column=0)
        self.enter_height = Entry(self.fen_r)
        self.enter_height.grid(row=1, column=1)
        Button(self.fen_r, text="appliquer", command=self.apply_redim).grid(row=2, column=1, sticky=E)
        self.fen_r.mainloop()

    #rafraichir l'affichage a l'image originale
    def refresh(self):
        self.boss.param_eclair.set(0)
        self.boss.param_gamma.set(0)
        self.boss.param_contrast.set(0)
        self.boss.img_f = self.boss.img_orig
        self.boss.img_bef = self.boss.img_f
        self.boss.var_filter.set(self.boss.list_filter[0])
        self.update_img()

    #appliquer le redimensionnement
    def apply_redim(self):
        width, height = 100, 100
        try:
            width, height = int(self.enter_width.get()), int(self.enter_height.get())
        except:
            print("error")
        else:
            self.boss.img_f = self.boss.img_f.resize((width, height))
            self.boss.img_bef = self.boss.img_f
            self.update_img()
        self.fen_r.destroy()

    #changer d'image
    def change_dir(self, event):
        dir = self.boss.cd.get()
        self.boss.img_f = Image.open(dir)
        self.boss.img_bef = self.boss.img_f
        self.boss.img_orig = self.boss.img_bef
        self.boss.var_filter.set(self.boss.list_filter[0])
        self.update_img()

    #fenetre de changement d'image
    def browserfiles(self):
        dir = tkinter.filedialog.askopenfilename(initialdir="/", title="select your image", filetypes=(("jpeg image", "*.jpeg*"), ("png image", "*.png*"), ("gif image", "*.gif*"), ("all file", "*.*")))
        dir = str(dir)
        self.boss.img_f = Image.open(dir)
        self.boss.img_bef = self.boss.img_f
        self.boss.img_orig = self.boss.img_bef
        self.boss.cd.delete(0, END)
        self.boss.cd.insert(0, dir)
        self.boss.var_filter.set(self.boss.list_filter[0])
        self.update_img()

    #mettre a jour l'affichage
    def update_img(self):
        self.boss.img = ImageTk.PhotoImage(self.boss.img_f)
        self.boss.can.delete("all")
        self.boss.can.create_image(10, 10, anchor=NW, image=self.boss.img)

        # fenetre d'enregistrement

    def save_(self):
        self.fen_s = Toplevel(self.boss)
        self.fen_s.title("save_file")
        Label(self.fen_s, text="direction_complete:").grid(row=0, column=0, sticky=E)
        self.directory_s = Entry(self.fen_s, width=75)
        self.directory_s.grid(row=0, column=1, sticky=W)
        Button(self.fen_s, text="enregistrer", command=self.save_img).grid(row=1, column=1, sticky=E)
        self.fen_s.mainloop()

        # enregistrement de l'image

    def save_img(self):
        try:
            self.boss.img_f.save(self.directory_s.get(), "jpeg")
        except:
            print("error")
        self.fen_s.destroy()
