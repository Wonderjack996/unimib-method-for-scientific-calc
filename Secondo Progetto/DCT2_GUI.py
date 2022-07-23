import numpy as np
import tkinter as tk
import tkinter.font as tkFont
import tkinter.filedialog as fDialog
import imageio
import cv2
from tkinter import messagebox
from scipy.fft import dct, idct
from PIL import Image, ImageTk

class App:

    def __init__(self, root):

        self.chosen_image_path = ""
        self.compressed_image_path = "" 
        self.f_value = ""
        self.d_value = ""
        self.var_f = tk.StringVar()
        self.var_d = tk.StringVar()
        
        # Main window
        root.title("Progetto 2 MCS")
        width=600
        height=450
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        # Testo per l'immagine caricata
        self.load_label=tk.Label(root)
        ft = tkFont.Font(family='Times',size=18)
        self.load_label["font"] = ft
        self.load_label["fg"] = "#333333"
        self.load_label["justify"] = "left"
        self.load_label["anchor"] = "w"
        self.load_label["text"] = "Chosen file: "
        self.load_label.place(x=30,y=30,width=400,height=36)

        # Bottone load
        load_button=tk.Button(root)
        load_button["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=23)
        load_button["font"] = ft
        load_button["fg"] = "#000000"
        load_button["justify"] = "center"
        load_button["anchor"] = "center"
        load_button["text"] = "Load image"
        load_button.place(x=200,y=90,width=188,height=44)
        load_button["command"] = self.load_command
        
        # Testo per l'intero F
        f_label = tk.Label(root)
        ft = tkFont.Font(family='Times',size=18)
        f_label["font"] = ft
        f_label["fg"] = "#333333"
        f_label["justify"] = "center"
        f_label["anchor"] = "center"
        f_label["text"] = "Integer F: "
        f_label.place(x=150,y=180,width=150,height=25)

        # Entry per il valore F
        f_entry = tk.Entry(root, textvariable=self.var_f)
        ft = tkFont.Font(family='Times',size=16)
        f_entry["font"] = ft
        f_entry.place(x=300,y=180,width=100,height=25)

        # Testo per l'intero D
        d_label = tk.Label(root)
        ft = tkFont.Font(family='Times',size=18)
        d_label["font"] = ft
        d_label["fg"] = "#333333"
        d_label["justify"] = "center"
        d_label["anchor"] = "center"
        d_label["text"] = "Integer d: "
        d_label.place(x=150,y=240,width=150,height=25)
        
        # Entry per il valore D
        d_entry = tk.Entry(root, textvariable=self.var_d)
        ft = tkFont.Font(family='Times',size=16)
        d_entry["font"] = ft
        d_entry.place(x=300,y=240,width=100,height=25)

        # Bottone per la compressione delle immagini
        compress_button=tk.Button(root)
        compress_button["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=28)
        compress_button["font"] = ft
        compress_button["fg"] = "#000000"
        compress_button["justify"] = "center"
        compress_button["anchor"] = "center"
        compress_button["text"] = "Compress image"
        compress_button.place(x=150,y=330,width=300,height=55)
        compress_button["command"] = self.compress_command
        

    def load_command(self):
        '''
        Funzione per il salvataggio del path dell'immagine originale.

        :param self: variabili e funzioni della classe App
        '''

        self.chosen_image_path = fDialog.askopenfilename(initialdir = "/", title = "Select an image", 
                                    filetypes = (("Images", "*.bmp"),("All files", "*.*")))  
        
        index = self.chosen_image_path.rfind("/") + 1
        filename = self.chosen_image_path[index:]
        if filename:
            self.load_label["text"] = "Chosen file: " + filename
        

    def compress_command(self):
        '''
        Funzione per la compressione di immagini in toni di grigio.

        :param self: variabili e funzioni della classe App
        '''

        # Controlla se gli input sono corretti
        correct_inputs = self.check_inputs()

        # Se gli input sono corretti si procede alla compressione dell'immagine
        if (correct_inputs):

            # Legge l'immagine originale dal path memorizzato
            image = cv2.imread(self.chosen_image_path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Converte l'immagine in scala di grigi
            image_pil = Image.fromarray(image)
            image_greyscale = image_pil.convert('L')
            image_matrix = np.array(image_greyscale)

            # Recupera altezza e larghezza dell'immagine
            height = image_matrix.shape[0]
            width = image_matrix.shape[1]

            # Se l'altezza non è multiplo di f, si tronca al maggior valore multiplo di f
            if (height % self.f_value != 0):
                height = height - (height % self.f_value)

            # Se la larghezza non è multiplo di f, si tronca al maggior valore multiplo di f
            if (width % self.f_value != 0):
                width = width - (width % self.f_value)

            # Comprime l'immagine in base ad altezza e larghezza troncate
            image_matrix_truncated = image_matrix[0:height , 0:width]
            height = image_matrix_truncated.shape[0]
            width = image_matrix_truncated.shape[1]

            # Crea blocchi F x F
            blocks = self.create_blocks(height, width, image_matrix_truncated)

            # Trasforma i blocchi con DCT2 e IDCT2
            compressed_blocks = self.compress_blocks(blocks)

            # Ricostruisce la matrice con i valori calcolati
            image_matrix_compressed = self.rebuild_image_matrix(height, width, image_matrix_truncated, compressed_blocks)

            # Trasforma la matrice in un'immagine
            image_compressed = Image.fromarray(image_matrix_compressed.astype('uint8'))
            image_compressed = image_compressed.convert('L')

            # Salva l'immagine compressa
            index = self.chosen_image_path.rfind("/") + 1
            path = self.chosen_image_path[:index]
            self.compressed_image_path = path + "compressed_image.bmp"
            imageio.imsave(self.compressed_image_path, image_compressed)

            # Mostra a schermo l'immagine originale e quella compressa
            self.show_images()


    def check_inputs(self):
        '''
        Funzione per controllare che tutti gli input siano corretti.

        :param self: variabili e funzioni della classe App
        :return: True se tutti gli input sono corretti, False altrimenti
        '''

        if (self.chosen_image_path == ""):
            messagebox.showerror(title="Errore", message="Nessuna immagine selezionata")
            return False
        if (self.var_f.get() == ""):
            messagebox.showerror(title="Errore", message="Il campo per il valore F non può essere vuoto")
            return False
        if (self.var_d.get() == ""):
            messagebox.showerror(title="Errore", message="Il campo per il valore d non può essere vuoto")
            return False

        try:
            self.f_value = int(self.var_f.get())
        except:
            messagebox.showerror(title="Errore", message="Il valore F deve essere intero")
            return False
        if (self.f_value < 0):
            messagebox.showerror(title="Errore", message="Il valore F deve essere maggiore o uguale a 0")
            return False

        # Legge l'immagine originale dal path memorizzato
        image = cv2.imread(self.chosen_image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Recupera altezza e larghezza dell'immagine
        image_pil = Image.fromarray(image)
        image_matrix = np.array(image_pil)
        height = image_matrix.shape[0]
        width = image_matrix.shape[1]
        if (self.f_value > height or self.f_value > width):
            messagebox.showerror(title="Errore", message="Il valore F non può essere maggiore dell'altezza o della larghezza dell'immagine")
            return False 

        try:
            self.d_value = int(self.var_d.get())
        except:
            messagebox.showerror(title="Errore", message="Il valore d deve essere intero")
            return False
        if (self.d_value < 0 or self.d_value > (2 * self.f_value - 2)):
            messagebox.showerror(title="Errore", message="Valore dell'intero d errato")
            return False
        return True


    def create_blocks(self, height, width, image_matrix_truncated):
        '''
        Funzione per la creazione di blocchi F x F.

        :param self: variabili e funzioni della classe App
        :param height: altezza dell'immagine originale
        :param width: larghezza dell'immagine originale
        :param image_matrix_truncated: matrice dell'immagine troncata
        :return blocks: blocchi F x F
        '''

        # Crea blocchi F x F
        blocks = []
        for i in range(0, height, self.f_value):
            for j in range(0, width, self.f_value):

                # Prende i valori di un blocco F x F
                values = image_matrix_truncated[i:i+self.f_value, j:j+self.f_value]

                # Crea un blocco F x F con i precedenti valori
                block = np.array(values).reshape(self.f_value, self.f_value)

                # Aggiunge il blocco alla lista dei blocchi
                blocks.append(block)

        return blocks

    
    def compress_blocks(self, blocks):
        '''
        Funzione per la compressione e decompressione dei blocchi.

        :param self: variabili e funzioni della classe App
        :param blocks: blocchi F x F
        :return compressed_blocks: blocchi F X F ottenuti con DCT2 e IDCT2,
        con frequenze tagliate in base al valore d, e con i valori arrotondati
        all'intero più vicino compreso tra 0 e 255
        '''

        # Trasforma i blocchi con DCT2 e IDCT2
        compressed_blocks = []
        for k in range(len(blocks)):   

                # Recupera un singolo blocco dalla lista dei blocchi
                block = blocks[k]

                # Esegue la DCT2 sul singolo blocco
                c = dct(dct(block.T, norm='ortho').T, norm='ortho')

                # Elimina le frequenze per i + j >= d
                for i in range(0, self.f_value):
                    for j in range(0, self.f_value):
                        if (i + j >= self.d_value):
                            c[i][j] = 0

                # Esegue la IDCT2 sul singolo blocco
                f = idct(idct(c.T, norm='ortho').T, norm='ortho')

                # Arrotonda i valori di f all'intero più vicino
                f = np.rint(f)

                # Mette a 0 i numeri negativi e a 255 quelli maggiori di 255 
                for i in range(0, self.f_value):
                    for j in range(0, self.f_value):
                        if (f[i][j] < 0):
                            f[i][j] = 0
                        if (f[i][j] > 255):
                            f[i][j] = 255
                
                # Aggiunge il blocco compresso alla lista dei blocchi compressi
                compressed_blocks.append(f)

        return compressed_blocks

    
    def rebuild_image_matrix(self, height, width, image_matrix_compressed, blocks):
        '''
        Funzione per ricostruire la matrice di blocchi F x F
        in vista della composizione dell'immagine compressa.

        :param self: variabili e funzioni della classe App
        :param height: altezza dell'immagine originale
        :param width: larghezza dell'immagine originale
        :param image_matrix_compressed: matrice dell'immagine da restituire
        :param blocks: blocchi F x F compressi
        :return image_matrix_compressed: matrice dell'immagine con i blocchi compressi
        '''

        # Ricostruisce la matrice dell'immagine con i valori calcolati
        k = 0
        for i in range(0, height, self.f_value):
            for j in range(0, width, self.f_value):
                image_matrix_compressed[i:i+self.f_value, j:j+self.f_value] = blocks[k]
                k += 1
        return image_matrix_compressed


    def show_images(self):
        '''
        Funzione per mostrare affinacate l'immagine originale e quella ricostruita.

        :param self: variabili e funzioni della classe App
        '''

        # Finestra per mostrare affiancate le immagini (originale e ricostruita) 
        window_images = tk.Tk()
        window_images.title("Images")

        # Divisione della finestra in due colonne
        window_images.grid_columnconfigure(0, weight=1)
        window_images.grid_columnconfigure(1, weight=1)

        # Testo per l'immagine originale
        original_image_label = tk.Label(window_images)
        original_image_label["fg"] = "#333333"
        original_image_label["justify"] = "left"
        original_image_label["anchor"] = "w"
        original_image_label["text"] = "Immagine originale"
        original_image_label.configure(font=('Times',20,'bold'))
        original_image_label.grid(row=0, column=0, pady=5)

        # Aggiunta dell'immagine originale
        original_image_cv = cv2.imread(self.chosen_image_path)
        original_image_cv = cv2.cvtColor(original_image_cv, cv2.COLOR_BGR2RGB)
        # Ridimensionamento dell'immagine originale se troppo grande
        scaled = False
        while not scaled:
            if (original_image_cv.shape[1] > 1280 or original_image_cv.shape[0] > 720):
                scale_percent = 90
                width = int(original_image_cv.shape[1] * scale_percent / 100)
                height = int(original_image_cv.shape[0] * scale_percent / 100)
                dimensions = (width, height)
                original_image_cv = cv2.resize(original_image_cv, dimensions, interpolation = cv2.INTER_CUBIC)
            else:
                scaled = True
        original_image = ImageTk.PhotoImage(Image.fromarray(original_image_cv), master=window_images)
        original_image_label = tk.Label(window_images, image=original_image)
        original_image_label.grid(row=1, column=0, padx=5)
        
        # Testo per l'immagine ricostruita
        compressed_image_label = tk.Label(window_images)
        compressed_image_label["fg"] = "#333333"
        compressed_image_label["justify"] = "left"
        compressed_image_label["anchor"] = "w"
        compressed_image_label["text"] = "Immagine ricostruita"
        compressed_image_label.configure(font=('Times',20,'bold'))
        compressed_image_label.grid(row=0, column=1, pady=5)

        # Aggiunta dell'immagine ricostruita
        compressed_image_cv = cv2.imread(self.compressed_image_path)
        compressed_image_cv = cv2.cvtColor(compressed_image_cv, cv2.COLOR_BGR2RGB)
        # Ridimensionamento dell'immagine ricostruita se troppo grande
        scaled = False
        while not scaled:
            if (compressed_image_cv.shape[1] > 1280 or compressed_image_cv.shape[0] > 720):
                scale_percent = 90
                width = int(compressed_image_cv.shape[1] * scale_percent / 100)
                height = int(compressed_image_cv.shape[0] * scale_percent / 100)
                dimensions = (width, height)
                compressed_image_cv = cv2.resize(compressed_image_cv, dimensions, interpolation = cv2.INTER_CUBIC)
            else:
                scaled = True
        compressed_image = ImageTk.PhotoImage(Image.fromarray(compressed_image_cv), master=window_images)
        compressed_image_label = tk.Label(window_images, image=compressed_image)
        compressed_image_label.grid(row=1, column=1, padx=5)

        window_images.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
