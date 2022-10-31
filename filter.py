import numpy as np
from scipy import signal
from tkinter import *
import tkinter.filedialog
from PIL import Image
class filters(object):

    def __init__(self, boss, set_image):
        self.boss = boss
        self.set_image = set_image
    #appliquer un filtre saisi
    def apply_filter(self):
        filter = np.zeros((3, 3))
        try:
            filter[0][0] = eval(self.boss.cel11.get())
            filter[1][0] = eval(self.boss.cel21.get())
            filter[1][1] = eval(self.boss.cel22.get())
            filter[0][1] = eval(self.boss.cel12.get())
            filter[0][2] = eval(self.boss.cel13.get())
            filter[2][0] = eval(self.boss.cel31.get())
            filter[1][2] = eval(self.boss.cel23.get())
            filter[2][1] = eval(self.boss.cel32.get())
            filter[2][2] = eval(self.boss.cel33.get())
        except:
            print("error")
        else:
            layers = 0
            if self.boss.var_layers.get() == "Green":
                layers = 1
            elif self.boss.var_layers.get() == "Blue":
                layers = 2
            image_matrix = np.array(self.boss.img_f)
            dim = np.shape(image_matrix)
            img_layer = np.zeros((dim[0], dim[1]))
            for i in range(0, dim[0]):
                for j in range(0, dim[1]):
                    img_layer[i][j] = image_matrix[i][j][layers]
            img_layer = signal.convolve2d(img_layer, filter, 'same')
            for i in range(0, dim[0]):
                for j in range(0, dim[1]):
                    if img_layer[i][j] >255:
                        img_layer[i][j] = 255
                    elif img_layer[i][j] < 0:
                        img_layer[i][j] = 0
                    image_matrix[i][j][layers] = img_layer[i][j]
            self.boss.img_f = Image.fromarray(image_matrix)
            self.boss.img_bef = self.boss.img_f
            self.set_image.update_img()


    def change_filter(self, intensity):
        if self.boss.var_filter.get() != "nothing":
            filter = self.boss.var_filter.get()
            filter = self.boss.dict_filter[filter]
            image_matrix = np.array(self.boss.img_f)
            dim = np.shape(image_matrix)
            for layer in range(0, 3):
                img_layer = np.zeros((dim[0], dim[1]))
                for i in range(0, dim[0]):
                    for j in range(0, dim[1]):
                        img_layer[i][j] = image_matrix[i][j][layer]
                img_layer = signal.convolve2d(img_layer, filter, 'same')
                if(self.boss.var_filter.get()=="sobel gradient"):
                    img_layer2 = signal.convolve2d(img_layer, np.transpose(filter), 'same')
                    img_layer = np.sqrt(img_layer**2 + img_layer2**2)
                for i in range(0, dim[0]):
                    for j in range(0, dim[1]):
                        if img_layer[i][j] >255:
                            img_layer[i][j] = 255
                        elif img_layer[i][j] < 0:
                            img_layer[i][j] = 0
                        image_matrix[i][j][layer] = img_layer[i][j]
            self.boss.img_f = Image.fromarray(image_matrix)
            self.boss.img_bef = self.boss.img_f
            self.set_image.update_img()

    #ajouter un drapeau sur une image
    def choose_flag(self):
        self.fen_flag = Toplevel(self.boss)
        self.entry_flag = Entry(self.fen_flag, width=100)
        self.entry_flag.grid(row=0, column=0)
        self.bout_flag = Button(self.fen_flag, text="browser", command=self.browser_flag)
        self.bout_flag.grid(row=0, column=1)
        self.fen_flag.mainloop()

    #chercher un drapeau
    def browser_flag(self):
        self.dir_flag = tkinter.filedialog.askopenfilename(initialdir='/', title="select your flag", filetypes=(("jpeg image", "*.jpeg*"), ("png image", "*.png*"), ("gif image", "*.gif*"), ("all file", "*.*")))
        self.entry_flag.delete(0, END)
        self.entry_flag.insert(0, dir)
        self.fen_flag.destroy()
        self.put_flag()

    #mettre un drapeau sur une image
    def put_flag(self):
        matrix_o = np.array(self.boss.img_f)
        img_flag = Image.open(self.dir_flag)
        img_flag = img_flag.resize((self.boss.img_f.width, self.boss.img_f.height))
        matrix_flag = np.array(img_flag)
        dim = np.shape(matrix_flag)
        for i in range(0, dim[0]):
            for j in range(0, dim[1]):
                for k in range(0, dim[2]):
                    matrix_o[i][j][k] = (matrix_flag[i][j][k] + matrix_o[i][j][k]*2)/3
        self.boss.img_f = Image.fromarray(matrix_o)
        self.boss.img_bef = self.boss.img_f
        self.set_image.update_img()

    #ressortir le canal rouge d'une image
    def red_canal(self):
        matrix = np.array(self.boss.img_f)
        dim = np.shape(matrix)
        for i in range(0, dim[0]):
            for j in range(0, dim[1]):
                matrix[i][j][1] = 0
                matrix[i][j][2] = 0
        self.boss.img_f = Image.fromarray(matrix)
        self.boss.img_bef = self.boss.img_f
        self.set_image.update_img()

    #ressortir le canal blue d'une image
    def blue_canal(self):
        matrix = np.array(self.boss.img_f)
        dim = np.shape(matrix)
        for i in range(0, dim[0]):
            for j in range(0, dim[1]):
                matrix[i][j][0] = 0
                matrix[i][j][1] = 0
        self.boss.img_f = Image.fromarray(matrix)
        self.boss.img_bef = self.boss.img_f
        self.set_image.update_img()

    #ressortir le canal vert d'une image
    def green_canal(self):
        matrix = np.array(self.boss.img_f)
        dim = np.shape(matrix)
        for i in range(0, dim[0]):
            for j in range(0, dim[1]):
                matrix[i][j][0] = 0
                matrix[i][j][2] = 0
        self.boss.img_f = Image.fromarray(matrix)
        self.boss.img_bef = self.boss.img_f
        self.set_image.update_img()

    #ressortir le negatif d'une image
    def negatif(self):
        matrix = np.array(self.boss.img_f)
        dim = np.shape(matrix)
        matrix = 255 - matrix
        self.boss.img_f = Image.fromarray(matrix)
        self.boss.img_bef = self.boss.img_f
        self.set_image.update_img()