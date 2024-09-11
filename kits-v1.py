from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
import tkinter.simpledialog
from PIL import Image, ImageTk
import sqlite3

# ventana de inicio
ventana_login = Tk()
ventana_login.title("Login")
ventana_login.geometry("300x500")
ventana_login.resizable(False, False)


# conección a la base de datos
coneccion = sqlite3.connect("kits-database2.db")

class Login:    # Iniciar sesión
    def __init__(self):
        self.username = ""
        self.password = ""
        self.usuarios = []

    def login(self):
        self.username = entry_username.get()
        self.password = entry_password.get()
        
        if self.username and self.password:     # Comprobar datos vacíos
            datos = (self.username, self.password)

            try:
                tabla = coneccion.cursor()          # si los datos son correctos, verificar si el usuario es cliente o administrador.
                tabla.execute("SELECT id_usuario, tipo_usuario FROM usuarios WHERE username = ? AND password = ?", datos)
                self.usuarios = tabla.fetchone()    # tipo de usuario y su id   
                
                if self.usuarios:                   # Verificar si el usuario existe 
                    id_usuario, tipo_usuario = self.usuarios
                    
                    if tipo_usuario == "cliente":
                        # ventana de inicio para clientes
                        inicio_cliente.inicio_cliente(id_usuario, self.username)
                        ventana_login.withdraw()
                    elif tipo_usuario == "admin":
                        # ventana de inicio para administradores
                        pass
                    else:
                        showwarning("Error al iniciar sesión", "Tipo de usuario desconocido.")

                else:
                    showwarning("Advertencia", "Datos de acceso incorrectos.\nPor favor intenta de nuevo.")

            except Exception as e:
                showwarning("Advertencia", f"Ocurrió un error en la base de datos:\n{e}") 

        else:
            showwarning("Advertencia", "Completa los campos de texto.")


          
           
class InicioCliente:    # Ventana que se muestra al iniciar sesión como cliente
    def __init__(self):
        self.nombre_cliente = ""
        self.apellido_cliente = ""
        self.imagenes_guardadas = []
        
    def inicio_cliente(self, id_cliente, username_cliente):
        self.id_cliente = id_cliente
        self.username_cliente = username_cliente
        # ventana inicio cliente
        inicio = Toplevel()
        inicio.title(f"Inicio - {username_cliente}")
        inicio.geometry("1360x760")
        inicio.resizable(False, False)
        inicio.config(bg=color_fondo_cliente)
        
        # scrollbar
        # frame para el canvas
        frame_principal = Frame(inicio)
        frame_principal.pack(fill=BOTH, expand=1)
        
        # canvas
        canva = Canvas(frame_principal, bg="snow")
        canva.pack(side=LEFT, fill=BOTH, expand=1)
          
        # añadir scrollbar al canvas
        scrollbar = ttk.Scrollbar(frame_principal, orient=VERTICAL, command=canva.yview)	
        scrollbar.pack(side=RIGHT, fill=Y) 
        
        # configurar canvas
        canva.configure(yscrollcommand=scrollbar.set)
        canva.bind('<Configure>', lambda e: canva.configure(scrollregion = canva.bbox("all")))

        # crear otro frame adentro del canvas, el cual va a contener todos los widgets
        frame_widgets = Frame(canva, bg="white")

        # añadir nuevo frame al canvas
        canva.create_window((0,0), window=frame_widgets, anchor="nw")
        
        # FRAMES
        # busqueda
        frame_busqueda = Frame(frame_widgets, bg="black", border=1, width=1360, height=80)
        frame_busqueda.pack()
        
        # botones del inicio
        frame_acceso_rapido = Frame(frame_widgets, bg="black", border=1, width=100, height=22760)   # para usar el método .place() en un frame, hay que definir su ancho, su alto
        frame_acceso_rapido.pack(side=LEFT)                                                                # y posicionarlo antes de los demás widgets
        
        
        # ELEMENTOS de frames
        # elementos del frame_busqueda
        # barra de busqueda
        barra_busqueda = Entry(frame_busqueda, width=50, font=fuente_cliente, justify='center')
        barra_busqueda.place(x=400, y=30)
        
        # boton de busqueda
        boton_busqueda = Button(frame_busqueda, image=imagen_buscar)
        boton_busqueda.place(x=870, y=22)
        
        # elementos del frame botones_inicio
        # boton modificar cliente
        boton_modificar_cliente = Button(frame_acceso_rapido, image=imagen_modificar_cliente, border=0)
        boton_modificar_cliente.place(x=15, y=130)
        
        # boton filtrar por
        boton_filtrar = Button(frame_acceso_rapido, image=imagen_filtrar, border=0)
        boton_filtrar.place(x=15, y=225)
        
        # mis compras
        boton_mis_compras = Button(frame_acceso_rapido, image=imagen_compras, border=0)
        boton_mis_compras.place(x=15, y=315)
        
        # mis favoritos
        boton_favoritos = Button(frame_acceso_rapido, image=imagen_favoritos, border=0)
        boton_favoritos.place(x=15, y=405)
        
        # Términos y condiciones
        boton_terminos = Button(frame_acceso_rapido, image=imagen_acuerdo, border=0)
        boton_terminos.place(x=15, y=495)
        
        # camisetas
        consulta_sql = "SELECT imagen FROM productos ORDER BY RANDOM()"
        imagenes_camisetas = cargar_camisetas.cargar_camisetas(consulta_sql) 
        
        
        x = 225
        y = 100 
        cuadricula = 1
        
        for imagen in imagenes_camisetas:   
            camiseta = Button(frame_widgets, image=imagen, border=0, width=300, height=400, bg='white')
            camiseta.place(x=x, y=y)
            print(imagen)
            descripcion_camiseta = Label(frame_widgets, text="zzz")
            descripcion_camiseta.place(x=x, y=y + 410)
            
            if cuadricula <= 3:
                cuadricula += 1
                x = x + 350
                
            if cuadricula > 3:
                cuadricula = 1
                x = 225
                y = y + 480 
                
                
            
            
class CargarCamisetas:  # clase para cargar las imagenes de las camisetas y una descripción
    def __init__(self):
        self.imagenes_cargadas = []     # Lista para mantener la referencia a las imagenes
        
    def cargar_camisetas(self, consulta_sql):
        tabla = coneccion.cursor()
        tabla.execute(consulta_sql) 
        imagenes = tabla.fetchall()
          
        camisetas = []
        
        for imagen in imagenes:
            ruta = "camisetas/" + imagen[0]
            imagen_camiseta = Image.open(ruta)
            #imagen_camiseta = imagen_camiseta.resize((300, 400), Image.LANCZOS)
            imagen_camiseta = ImageTk.PhotoImage(imagen_camiseta)
            
            self.imagenes_cargadas.append(imagen_camiseta)  # Mantener la referencia
            camisetas.append(imagen_camiseta)               # Agregar imagenes de camisetas a la lista
            
        return camisetas    # Devolver las camisetas    
        

                     
# widgets login
ruta_fondo = "imagenes/leBron-dunk.jpg"
imagen_fondo = Image.open(ruta_fondo)
imagen_fondo = imagen_fondo.resize((300, 500), Image.LANCZOS)
imagen_fondo = ImageTk.PhotoImage(imagen_fondo)
label_fondo = Label(ventana_login, image=imagen_fondo)
label_fondo.place(x=0, y=0, relwidth=1, relheight=1)

# entry username
entry_username = Entry(ventana_login, width=30, justify='center')
entry_username.insert(0, "Nombre de usuario")
entry_username.place(x=60, y=200)

# entry password
entry_password = Entry(ventana_login, width=30, justify='center', show="*")
entry_password.insert(0, "Contraseña")
entry_password.place(x=60, y=240)

# colores interfaz
color_fondo_cliente = "snow"
fuente_cliente = ("Century Gothic", 12)

# botones con imagenes
ruta_imagen_modificar_cliente = "botones/usuario-cliente-inicio2.png"
imagen_modificar_cliente = Image.open(ruta_imagen_modificar_cliente)
imagen_modificar_cliente = ImageTk.PhotoImage(imagen_modificar_cliente)

ruta_filtrar = "botones/filtrar.png"
imagen_filtrar = Image.open(ruta_filtrar)
imagen_filtrar = ImageTk.PhotoImage(imagen_filtrar) 

ruta_compras = "botones/bolsa-compras.png"
imagen_compras = Image.open(ruta_compras)
imagen_compras = ImageTk.PhotoImage(imagen_compras)

ruta_favoritos = "botones/me-gusta.png"
imagen_favoritos = Image.open(ruta_favoritos)
imagen_favoritos = ImageTk.PhotoImage(imagen_favoritos)

ruta_acuerdo = "botones/acuerdo.png"
imagen_acuerdo = Image.open(ruta_acuerdo)
imagen_acuerdo = ImageTk.PhotoImage(imagen_acuerdo)

ruta_buscar = "botones/buscar.png"
imagen_buscar = Image.open(ruta_buscar)
imagen_buscar = ImageTk.PhotoImage(imagen_buscar)
 

# instancias
inicio_cliente = InicioCliente()
cargar_camisetas = CargarCamisetas()


# botón ingresar
ingresar = Login()
boton_ingresar = Button(ventana_login, text="Ingresar", width=8, command=ingresar.login)
boton_ingresar.place(x=120, y=280)

# pie de página
label_footer = Label(ventana_login, text="NBA Kits - 2024", fg="snow", bg="gray22", font=("Arial", 10))
label_footer.place(x=100, y=480)


ventana_login.mainloop()