
from tkinter import *
from PIL import Image, ImageTk
import numpy as np
import set_image
import img_caract
import filter


class my_appli(Frame):
    def __init__(self, boss):
        Frame.__init__(self)
        self.master = boss
        self.set_img = set_image.set_img(self)
        self.img_caract = img_caract.img_carct(self, self.set_img)
        self.filter = filter.filters(self, self.set_img)
        self.list_filter = ["nothing", "smoothing", "net", "emphasis", "sobel gradient", "border"] #liste des filtres
        self.list_layers = ["Red", "Green", "Blue"]  #differntes couches pour appliquer les filtres
        self.var_layers = StringVar(self)               #variable tkinter pour l'OptionnMenu des filtre saisies
        self.var_layers.set(self.list_layers[0])
        self.var_filter = StringVar(self)               #variable tkinter pour l'OptionMenu de la liste de filtre
        self.var_filter.set(self.list_filter[0])
        #dimension de ma zone de travail
        self.x_can = 500
        self.y_can = 400

        self.can = Canvas(self, width=self.x_can, height=self.y_can, relief=GROOVE, bd=10, scrollregion=(0, 0, 1000, 1000))
        self.can.grid(row=1, column=1, rowspan=7)
        #image initiale
        self.img_f = Image.open("test.jpg")
        self.img_f = self.img_f.resize((400, 300))
        self.img_bef = self.img_f
        self.img_orig = self.img_f
        self.img = ImageTk.PhotoImage(self.img_f)
        self.can.create_image(10, 10, anchor=NW, image=self.img)

        self.yscroll = Scrollbar(self, command=self.can.yview, orient=VERTICAL)
        self.xscroll = Scrollbar(self, command=self.can.xview, orient=HORIZONTAL)
        self.can.configure(yscrollcommand=self.yscroll, xscrollcommand=self.xscroll)
        self.yscroll.grid(row=1, column=2, sticky=NS, rowspan=7)
        self.xscroll.grid(row=8, column=1, sticky=EW)

        #block de bouton
        self.button_ctrl = Frame(self)
        self.button_ctrl.grid(row=0, column=0)

        self.bout_redim = Button(self.button_ctrl, text="resize", command=self.set_img.redim, relief=GROOVE, background="grey", activebackground="black", activeforeground="white")
        self.bout_redim.grid(row=0, column=0, sticky=N)
        self.transform = Menubutton(self.button_ctrl, text="transform", relief=GROOVE, background="grey", activebackground="black", activeforeground="white")
        self.transform.grid(row=0, column=1)
        self.me = Menu(self.transform)
        self.me.add_command(label="add flag", command=self.filter.choose_flag)
        self.me.add_command(label="red canal", command=self.filter.red_canal)
        self.me.add_command(label="blue canal", command=self.filter.blue_canal)
        self.me.add_command(label="green canal", command=self.filter.green_canal)
        self.me.add_command(label="negatif", command=self.filter.negatif)
        self.transform.configure(menu=self.me)
        self.bout_save = Button(self.button_ctrl, text="save", command=self.set_img.save_, relief=GROOVE, background="grey", activebackground="black", activeforeground="white")
        self.bout_save.grid(row=0, column=2, sticky=E)


        #block importer un fichier
        self.import_file = Frame(self)
        self.import_file.grid(row=0, column=1, columnspan=2)
        Label(self.import_file, text="import image:").grid(row=0, column=0, sticky=E)
        self.cd = Entry(self.import_file, width=50)
        self.cd.grid(row=0, column=1)
        self.browser = Button(self.import_file, text="browser", command=self.set_img.browserfiles, relief=GROOVE, background="grey", activebackground="black", activeforeground="white")
        self.browser.grid(row=0, column=2)
        self.cd.bind('<Return>', self.set_img.change_dir)

        #block de reglage
        self.grille = Frame(self)
        self.grille.grid(row=1, column=0)

        self.param_eclair = Scale(self.grille, length=170, from_=-5, to=5, tickinterval=1, orient=HORIZONTAL, label="brightness", command=self.img_caract.update_eclair, activebackground="green", relief=SUNKEN)
        self.param_eclair.grid(row=1, column=0, sticky=N)
        self.eclair = 0

        self.param_contrast = Scale(self.grille, length=170, from_=-5, to=5, tickinterval=1, orient=HORIZONTAL, label="contrast", command=self.img_caract.update_contrast, activebackground="green", relief=SUNKEN)
        self.param_contrast.grid(row=2, column=0)
        self.contrast = 0

        self.param_gamma = Scale(self.grille, length=170, from_=-5, to=5, tickinterval=1, orient=HORIZONTAL,
                                    label="gamma", command=self.img_caract.update_gamma, activebackground="green", relief=SUNKEN)
        self.param_gamma.grid(row=3, column=0)
        self.gamma = 0


        #block de filtre
        self.gener_filter = Frame(self)
        self.gener_filter.grid(row=1, column=3)

        Label(self.gener_filter, text='filter: ').grid(row=1, column=1)
        self.menu_filter = OptionMenu(self.gener_filter, self.var_filter, *self.list_filter)
        self.menu_filter.config(font=('Helvetica 9'), background="blue")
        self.menu_filter.grid(row=2, column=1)
        self.menu_filter.bind('<Configure>', self.filter.change_filter)



        Label(self.gener_filter, text="generate a filter:").grid(row=4, column=1)
        self.menu_layer = OptionMenu(self.gener_filter, self.var_layers, *self.list_layers)
        self.menu_layer.grid(row=5, column=1)
        self.menu_layer.config(font=('Helvetice 9'), background = "blue")
        self.gener_filter_matrix = Frame(self.gener_filter)
        self.gener_filter_matrix.grid(row=6, column=1)
        # creation du tableau
        self.cel11 = Entry(self.gener_filter_matrix, width=5)
        self.cel12 = Entry(self.gener_filter_matrix, width=5)
        self.cel13 = Entry(self.gener_filter_matrix, width=5)
        self.cel21 = Entry(self.gener_filter_matrix, width=5)
        self.cel22 = Entry(self.gener_filter_matrix, width=5)
        self.cel23 = Entry(self.gener_filter_matrix, width=5)
        self.cel31 = Entry(self.gener_filter_matrix, width=5)
        self.cel32 = Entry(self.gener_filter_matrix, width=5)
        self.cel33 = Entry(self.gener_filter_matrix, width=5)

        self.cel11.grid(row=0, column=0)
        self.cel21.grid(row=1, column=0)
        self.cel31.grid(row=2, column=0)
        self.cel12.grid(row=0, column=1)
        self.cel22.grid(row=1, column=1)
        self.cel32.grid(row=2, column=1)
        self.cel13.grid(row=0, column=2)
        self.cel23.grid(row=1, column=2)
        self.cel33.grid(row=2, column=2)

        self.bout_apply = Button(self.gener_filter, text="apply the filter", command=self.filter.apply_filter, relief=GROOVE, background="grey", activebackground="red", activeforeground="white")
        self.bout_apply.grid(row=7, column=1)

        self.Button_refresh = Button(self, text="original", command=self.set_img.refresh, relief=GROOVE, background="green", activebackground="red", activeforeground="white")
        self.Button_refresh.grid(row=3, column=3)

        #dictionnaire des filtres enregistrés
        self.dict_filter = {}
        self.dict_filter["smoothing"] = np.ones((3, 3))*1/9
        self.dict_filter["net"] = np.zeros((3, 3))
        self.dict_filter["emphasis"] = np.zeros((3, 3))
        self.dict_filter["sobel gradient"] = np.zeros((3, 3))
        self.dict_filter["border"] = np.ones((3, 3)) *(-1)
        self.dict_filter["luminosity"] = np.ones((3, 3)) * (-1/9)
        self.dict_filter["contrast"] = np.ones((3, 3)) * (-1/9)

        self.dict_filter["net"][0][1] = -1
        self.dict_filter["net"][1][0] = -1
        self.dict_filter["net"][1][2] = -1
        self.dict_filter["net"][2][1] = -1
        self.dict_filter["net"][1][1] = 5

        self.dict_filter["emphasis"][0][1] = -0.5
        self.dict_filter["emphasis"][1][0] = -0.5
        self.dict_filter["emphasis"][1][2] = -0.5
        self.dict_filter["emphasis"][2][1] = -0.5
        self.dict_filter["emphasis"][1][1] = 3

        self.dict_filter["sobel gradient"][0][0] = -1
        self.dict_filter["sobel gradient"][1][0] = -2
        self.dict_filter["sobel gradient"][2][0] = -1
        self.dict_filter["sobel gradient"][0][2] = 1
        self.dict_filter["sobel gradient"][1][2] = 2
        self.dict_filter["sobel gradient"][2][2] = 1
        self.dict_filter["border"][1][1] = 8


#programme principal
if __name__ == '__main__':
    fen = Tk()
    fen.resizable(width=0, height=0)
    appli = my_appli(boss=fen)
    appli.pack()
    fen.mainloop()
