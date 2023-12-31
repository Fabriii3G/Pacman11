import sys
import threading
import tkinter as tk
import pygame
from natsort import natsorted
#Modelo de objetos de la clase juego
class Juego:
    #Atributos de la clase juego
    def __init__(self, Njuego, Tablero, Nivel, Score, pacman, Fantasmas):
        self.Njuego = Njuego
        self.Tablero = Tablero
        self.Nivel = Nivel
        self.Score = Score
        self.pacman = pacman
        self.fantasmas = Fantasmas
        self.ventana_ispector = None

    #Metodos de la clase juego
    def inicio(self):  # metodo de la ventana principal
        self.window = tk.Tk()
        self.window.minsize(1000, 600)
        self.window.maxsize(1000, 600)
        self.window.title("Pacman")
        self.window.configure(bg="black")
        canva = tk.Canvas(self.window, width=1000, height=600, bg="black")
        foto = tk.PhotoImage(master=canva, file="Fondo.png")
        canva.create_image(500, 299, image=foto)
        canva.pack()
        canva.place(x=0, y=0)
        # Boton Jugar
        self.jugar = tk.PhotoImage(file="Jugar.png")
        boton = tk.Button(self.window, image=self.jugar, bg="black", command=self.iniciar_juego)
        boton.pack()
        boton.place(x=440, y=290)
        # Boton Salon de la Fama
        salon = tk.PhotoImage(file="puntajes.png")
        boton = tk.Button(self.window, image=salon, bg="black", command=self.scoreboard)
        boton.pack()
        boton.place(x=440, y=400)
        # Boton Acerca De
        acerca = tk.PhotoImage(file="Info.png")
        boton = tk.Button(self.window, image=acerca, bg="black", command=self.acerca_de)
        boton.pack()
        boton.place(x=240, y=350)
        # Boton Ayuda
        ayuda = tk.PhotoImage(file="ayuda.png")
        boton = tk.Button(self.window, image=ayuda, bg="black", command=self.ayuda)
        boton.pack()
        boton.place(x=640, y=350)
        self.window.mainloop()

    def iniciar_juego(self): # metodo de la ventana de juego
        self.window.withdraw()
        pygame.init()
        self.pantalla = pygame.display.set_mode((1200, 780))
        pygame.display.set_caption("Pac-Man")
        self.fuente = pygame.font.Font("Minecraftia-Regular.ttf", 15)
        # Label para el puntaje
        label = self.fuente.render("Puntaje: 0", True, (255, 255, 255))
        label_rect = label.get_rect()
        label_rect.topright = (1010, 30)
        # Label para el nivel
        label_nivel = self.fuente.render(f"Nivel: {self.Tablero.nivel}", True, (255, 255, 255))
        label_nivel_rect = label_nivel.get_rect()
        label_nivel_rect.topright = (980, 10)
        # Label que indica si puede comer fantasmas
        label_comer = self.fuente.render(f"Comer fantasmas: {self.Tablero.comer}", True, (255, 255, 255))
        label_comer_rect = label_comer.get_rect()
        label_comer_rect.topright = (1100, 50)
        self.fuente1 = pygame.font.Font("Minecraftia-Regular.ttf", 12)
        # Label para indicar como mutear
        label_music = self.fuente1.render("*Barra espaciadora para mutear*", True, (255, 255, 255))
        label_music_rect = label_comer.get_rect()
        label_music_rect.topright = (1115, 750)
        # Codigo donde se carga la musica
        pygame.mixer.music.load("Pac_man_musica.mp3")
        pygame.mixer.music.play(-1)
        # Variables
        self.pausa = True
        musica = False
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif self.pacman.Estado == "Muerto":
                    pygame.display.quit()
                    sys.exit()
                    self.Tablero.finJuego = True
                    self.window.deiconify()
                elif self.Tablero.fantasmas == []:
                    self.Tablero.finJuego = True
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE: #Detecta tecla escape, poner pausa
                        self.pausa_('')
                        self.Tablero.imprimir_matriz()
                    elif evento.key == pygame.K_j: #Detecta tecla j, modo inspector
                        self.pausa_('')
                        self.inspector()
                    elif evento.key == pygame.K_d: #Detecta tecla d, mover derecha
                        if not self.Tablero.detectar_colision_pared(self.pacman.PosX + 1, self.pacman.PosY) and not self.Tablero.colision_pacman_y_fantasmas() and self.pausa:
                            self.Tablero.colision_pacman_y_fantasmas()
                            self.pacman.mover_derecha()
                            self.Tablero.puntaje()
                            self.capsulaJuego()
                    elif evento.key == pygame.K_a: #Detecta tecla a, mover izquierda
                        if not self.Tablero.detectar_colision_pared(self.pacman.PosX - 1, self.pacman.PosY) and not self.Tablero.colision_pacman_y_fantasmas() and self.pausa:
                            self.Tablero.colision_pacman_y_fantasmas()
                            self.pacman.mover_izquierda()
                            self.Tablero.puntaje()
                            self.capsulaJuego()
                    elif evento.key == pygame.K_w: #Detecta tecla 2, mover arriba
                        if not self.Tablero.detectar_colision_pared(self.pacman.PosX, self.pacman.PosY - 1) and not self.Tablero.colision_pacman_y_fantasmas() and self.pausa:
                            self.Tablero.colision_pacman_y_fantasmas()
                            self.pacman.mover_arriba()
                            self.Tablero.puntaje()
                            self.capsulaJuego()
                    elif evento.key == pygame.K_s: #Detecta tecla s, mover abajo
                        if not self.Tablero.detectar_colision_pared(self.pacman.PosX, self.pacman.PosY + 1) and not self.Tablero.colision_pacman_y_fantasmas() and self.pausa:
                            self.Tablero.colision_pacman_y_fantasmas()
                            self.pacman.mover_abajo()
                            self.Tablero.puntaje()
                            self.capsulaJuego()
                    elif evento.key == pygame.K_SPACE: #Detecta tecla espacio, mutear musica
                        if musica:
                            pygame.mixer.music.stop()
                            musica = False
                        else:
                            pygame.mixer.music.play(-1)
                            musica = True
            # Detecta si esta en pausa
            if self.pausa:
                self.pantalla.fill((0, 0, 0))
                self.dibujar_matriz()
                self.Tablero.actualizar_matriz()
                label = self.fuente.render(f"Puntaje: {self.Tablero.puntos}", True, (255, 255, 255))
                self.pantalla.blit(label, label_rect)
                self.pantalla.blit(label_nivel, label_nivel_rect)
                self.pantalla.blit(label_comer, label_comer_rect)
                self.pantalla.blit(label_music, label_music_rect)
                pygame.display.update()
                reloj = pygame.time.Clock()
                reloj.tick(60)
            # Detecta si el pacman puede comer fantasmas
            if self.Tablero.comerFantasmas:
                label_comer = self.fuente.render(f"Comer fantasmas: {self.Tablero.comer}", True, (255, 255, 255))
                self.pantalla.blit(label_comer, label_comer_rect)
            if not self.Tablero.comerFantasmas:
                label_comer = self.fuente.render(f"Comer fantasmas: {self.Tablero.comer}", True, (255, 255, 255))
                self.pantalla.blit(label_comer, label_comer_rect)
            # Detecta si es el final del juego
            if self.Tablero.finJuego:
                self.Tablero.reiniciar()
                label_nivel = self.fuente.render(f"Nivel: {self.Tablero.nivel}", True, (255, 255, 255))
                self.pantalla.blit(label_nivel, label_nivel_rect)
                # Detecta la lista vacia de fantasmas al final
                if self.Tablero.fantasmas == []:
                    pygame.display.quit()
                    self.juego_acabado()

    def pausa_(self, ev): # metodo de pausa
        self.pausa = not self.pausa
        self.Tablero.pausa = not self.Tablero.pausa
        if self.ventana_ispector:
            self.ventana_ispector.destroy()

    def inspector(self): # metodo de la ventana inspector
        self.ventana_ispector = tk.Toplevel()
        self.ventana_ispector.title("Inspector")
        canvas = tk.Canvas(self.ventana_ispector, width=1000, height=800, bg='black')
        canvas.pack()
        lado = 30
        self.ventana_ispector.bind('<Escape>', self.pausa_)
        for i, fila in enumerate(self.Tablero.matriz):
            for j, valor in enumerate(fila):
                x, y = j * lado + lado // 2, i * lado + lado // 2
                canvas.create_text(x, y, text=valor, fill="white", font=("Arial", 12))
        if self.pausa:
            return
        self.ventana_ispector.mainloop()

    def juego_acabado(self): # metodo de ventana de juego acabado
        self.ventana=tk.Tk()
        self.ventana.minsize(500,500)
        self.ventana.maxsize(500, 500)
        self.ventana.title("Inserta tu nombre")
        canva = tk.Canvas(self.ventana, width=500, height=500, bg="black")
        foto = tk.PhotoImage(master=canva, file="Nickname.png")
        canva.create_image(252, 250, image=foto)
        canva.pack()
        canva.place(x=0, y=0)
        self.nombre = tk.Entry(self.ventana, width=30, bg="white")
        self.nombre.place(x=162, y=311)
        boton = tk.Button(self.ventana, width=6, height=2, text='Enviar', command=lambda: [self.nombre_jugador(), self.scoreboard()])
        boton.place(x=225, y=410)
        self.ventana.focus_set()
        self.ventana.mainloop()

    def nombre_jugador(self):  # metodo que crea y edita el archivo txt
        self.usuario = self.nombre.get()
        print(self.usuario)
        try:
            with open("scoreboard.txt", "a") as file:
                file.write(f"{self.Tablero.puntos}-{self.usuario},")
                file.close()
        except:
            with open("scoreboard.txt", "w") as file:
                file.write(f"{self.Tablero.puntos}-{self.usuario},")

    def scoreboard(self):  # metodo que crea la ventana donde aparecen todos los puntajes
        self.window.withdraw()
        self.windo_Salon = tk.Toplevel()
        self.windo_Salon.title("Salon de la fama")
        self.windo_Salon.minsize(500, 500)
        self.windo_Salon.maxsize(500, 500)
        canva = tk.Canvas(self.windo_Salon, width=500, height=500, bg="black")
        foto = tk.PhotoImage(master=canva, file="Salón de la fama.png")
        canva.create_image(250, 250, image=foto)
        canva.pack()
        canva.place(x=0, y=0)
        try:
            file = open('scoreboard.txt', 'r')
            read = file.read().split(',')
            print(read)
            top = natsorted(read, reverse=True)
            print(top)
            puesto1 = tk.Label(self.windo_Salon, text=f'{top[0]}', width=15, height=2, font=('Arial Black', 10), fg="white",
                               bg="black")
            puesto1.place(x=140, y=80)
            puesto2 = tk.Label(self.windo_Salon, text=f'{top[1]}', width=15, height=2, font=('Arial Black', 10), fg="white",
                               bg="black")
            puesto2.place(x=140, y=120)
            puesto3 = tk.Label(self.windo_Salon, text=f'{top[2]}', width=15, height=2, font=('Arial Black', 10), fg="white",
                               bg="black")
            puesto3.place(x=140, y=160)
        except:
            None
        botonSalir = tk.Button(self.windo_Salon, height=1, width=5, text="Salir", command=self.salir_salon)
        botonSalir.place(x=10, y=10)
        self.windo_Salon.mainloop()

    def capsulaJuego(self): # metodo para el poder de comer fantasmas
        hilo=threading.Thread(target=self.Tablero.capsula)
        hilo.daemon = True
        hilo.start()

    def dibujar_matriz(self): # metodo que grafica la matriz en la ventana de pygame
        pacman_imagen = pygame.image.load("pacman.png")
        fantasmaR_imagen = pygame.image.load("rojo.png")
        fantasmaN_imagen = pygame.image.load("naranja (1).png")
        fantasmaC_imagen = pygame.image.load("celeste (1).png")
        fantasmar_imagen = pygame.image.load("rosado (1).png")
        cereza_imagen = pygame.image.load("cereza (1).png")
        punto_imagen = pygame.image.load("punto.png")
        capsula_imagen = pygame.image.load("capsula (1).png")
        pared_imagen = pygame.image.load("muro (1).png")
        for fila in range(len(self.Tablero.matriz)):
            for columna in range(len(self.Tablero.matriz[0])):
                if self.Tablero.matriz[fila][columna] == 0:
                    self.pantalla.blit(pared_imagen,(columna * 30, fila * 30))
                elif self.Tablero.matriz[fila][columna] == '🟡':
                    self.pantalla.blit(pacman_imagen, (columna * 30, fila * 30))
                elif self.Tablero.matriz[fila][columna] == 1 :
                    self.pantalla.blit(punto_imagen, (columna * 30, fila * 30))
                elif self.Tablero.matriz[fila][columna] == 'R' :
                    self.pantalla.blit(fantasmaR_imagen, (columna * 30, fila * 30))
                elif self.Tablero.matriz[fila][columna] == 'N' :
                    self.pantalla.blit(fantasmaN_imagen, (columna * 30, fila * 30))
                elif self.Tablero.matriz[fila][columna] == 'C':
                    self.pantalla.blit(fantasmaC_imagen, (columna * 30, fila * 30))
                elif self.Tablero.matriz[fila][columna] == 'r' :
                    self.pantalla.blit(fantasmar_imagen, (columna * 30, fila * 30))
                elif self.Tablero.matriz[fila][columna] == 3 :
                    self.pantalla.blit(cereza_imagen, (columna * 30, fila * 30))
                elif self.Tablero.matriz[fila][columna] == 2 :
                    self.pantalla.blit(capsula_imagen, (columna * 30, fila * 30))

    def acerca_de(self):  # metodo de la ventana Acerca De
        self.window.withdraw()
        self.acerca = tk.Toplevel()
        self.acerca.minsize(900, 500)
        self.acerca.maxsize(900, 500)
        self.acerca.title("Acerca De")
        self.acerca.configure(bg="black")
        canva = tk.Canvas(self.acerca, width=900, height=500, bg="black")
        foto = tk.PhotoImage(master=canva, file="acerca.png")
        canva.create_image(450, 250, image=foto)
        canva.pack()
        canva.place(x=0, y=0)
        botonSalir = tk.Button(self.acerca, height=1, width=5, text="Salir", command=self.salir_acerca)
        botonSalir.place(x=428, y=465)
        self.acerca.mainloop()

    def ayuda(self):  # metodo de la ventana Ayuda
        self.window.withdraw()
        self.ayuda = tk.Toplevel()
        self.ayuda.minsize(900, 500)
        self.ayuda.maxsize(900, 500)
        self.ayuda.title("Ayuda")
        self.ayuda.configure(bg="black")
        canva = tk.Canvas(self.ayuda, width=900, height=500, bg="black")
        foto = tk.PhotoImage(master=canva, file="Ayuda_fondo.png")
        canva.create_image(450, 250, image=foto)
        canva.pack()
        canva.place(x=0, y=0)
        botonSalir = tk.Button(self.ayuda, height=1, width=5, text="Salir", command=self.salir_ayuda)
        botonSalir.place(x=10, y=10)
        self.ayuda.mainloop()

    def salir_juego(self): # metodo de retornar a ventana principal
        self.ventanaJuego.withdraw()
        self.window.deiconify()

    def salir_salon(self): # metodo de retornar a ventana principal
        self.windo_Salon.withdraw()
        self.window.deiconify()

    def salir_acerca(self): # metodo de retornar a ventana principal
        self.acerca.withdraw()
        self.window.deiconify()

    def salir_ayuda(self): # metodo de retornar a ventana principal
        self.ayuda.withdraw()
        self.window.deiconify()