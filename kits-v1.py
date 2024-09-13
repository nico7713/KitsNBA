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
        
        try:
            # camisetas
            consulta_sql = "SELECT imagen, nombre_producto, jugador, precio, id_producto FROM productos ORDER BY RANDOM()"
            camisetas = cargar_camisetas.cargar_camisetas(consulta_sql) 
            
            x = 225
            y = 100 
            cuadricula = 1
            
            for imagen_camiseta, descripcion_camiseta, id_camiseta in camisetas:                        # se declara la una variable que contenga la imagen en la función lambda para mantener la referencia
                camiseta = Button(frame_widgets, image=imagen_camiseta, border=0, width=300, height=400, bg='white',
                                  command=lambda imagen=imagen_camiseta, id=id_camiseta : vista_compra.vista_compra(imagen, id))
                camiseta.place(x=x, y=y)
                descripcion = Label(frame_widgets, text=descripcion_camiseta, bg='white', font=("Calibri", 12))
                descripcion.place(x=x, y=y + 410)
                
                if cuadricula <= 3:
                    cuadricula += 1
                    x = x + 350
                    
                if cuadricula > 3:
                    cuadricula = 1
                    x = 225
                    y = y + 480
                    
        except Exception as e:
            showwarning("Advertencia", f"Error al momento de iniciar sesión al cargar las camisetas.\n{e}")
                
                
    
# clase para cargar las imagenes de las camisetas y una descripción (nombre de la camiseta, jugador y precio). 
# Esta clase esta diseñada para que la consulta SQL seleccione 4 campos (imagen, nombre_producto, jugador, precio)
class CargarCamisetas:  
    def __init__(self):
        self.imagenes_cargadas = []     # Lista para mantener la referencia a las imagenes
        
    def cargar_camisetas(self, consulta_sql):
        try:
            tabla = coneccion.cursor()
            tabla.execute(consulta_sql) 
            info_camisetas = tabla.fetchall()
            camisetas = []
            
            for camiseta in info_camisetas:
                archivo, producto, jugador, precio, id = camiseta               # desempaquetar la tupla
                
                archivo = "camisetas/" + archivo                                # especificar la ruta de las imagenes correctamente
                imagen_camiseta = Image.open(archivo)                           # crear imagen de la camiseta
                imagen_camiseta = ImageTk.PhotoImage(imagen_camiseta)           # dejar imagen lista para asignarla como un botón
                self.imagenes_cargadas.append(imagen_camiseta)                  # Agregar las variables de las camisetas para mantener la referencia a las imágenes
                
                descripcion_camiseta = f"{producto} {jugador} \n {precio}"      # Crear un título para mostrar debajo de la camiseta
                datos_camiseta = (imagen_camiseta, descripcion_camiseta, id)    # Crear una tupla que guarde la imagen de la camiseta, su descripción y id
                camisetas.append(datos_camiseta)                                # Agregar tupla a la lista camisetas
                
            return camisetas      # devolver las imagenes de las camisetas y su descripción
                
        except Exception as e:
            showwarning("Advertencia", f"Error en la base de datos de KitsNBA al cargar camisetas.\n{e}")
        
                
                
class VistaCompra:      # clase para la vista de compra de una camiseta
    def __init__(self):
        self.informacion_camiseta = []
        
    def obtener_informacion_camiseta(self, id_camiseta):
        try:
            consulta_sql = f"SELECT nombre_producto, precio, marca, equipo, temporada, jugador, version, color FROM productos WHERE id_producto = {id_camiseta}"
            tabla = coneccion.cursor()
            tabla.execute(consulta_sql) 
            info_camiseta = tabla.fetchone()
            return info_camiseta
        except Exception as e:
            showwarning("Advertencia", f"Error en la base de datos al entrar a la ventana de compra.\n{e}") 
        
                           
    def vista_compra(self, imagen_camiseta, id_camiseta):
        producto, precio, marca, equipo, temporada, jugador, version, color = self.obtener_informacion_camiseta(id_camiseta)
        
        ventana_compra = Toplevel()
        ventana_compra.title(f"Comprar {producto} {jugador} {color}")
        ventana_compra.geometry("1366x768")
        ventana_compra.resizable(False, False)
        ventana_compra.config(bg='white')
        
        muestra_camiseta = Label(ventana_compra, image=imagen_camiseta)
        muestra_camiseta.place(x=10, y=10)
        
        label_producto = Label(ventana_compra, text=f"Producto: {producto}", bg='white', font=("Calibri", 12))
        label_producto.place(x=350, y=10)
        
        label_marca = Label(ventana_compra, text=f"Marca: {marca}", bg='white', font=("Calibri", 12))
        label_marca.place(x=350, y=40)
        
        label_equipo = Label(ventana_compra, text=f"Franquicia: {equipo}", bg='white', font=("Calibri", 12))
        label_equipo.place(x=350, y=70)
        
        label_jugador = Label(ventana_compra, text=f"Jugador: {jugador}", bg='white', font=("Calibri", 12))
        label_jugador.place(x=350, y=100)
        
        label_temporada = Label(ventana_compra, text=f"Temporada: {temporada}", bg='white', font=("Calibri", 12))
        label_temporada.place(x=350, y=130)
        
        label_version = Label(ventana_compra, text=f"Version: {version}", bg='white', font=("Calibri", 12))
        label_version.place(x=350, y=160)
        
        label_color = Label(ventana_compra, text=f"Color: {color}", bg='white', font=("Calibri", 12))
        label_color.place(x=350, y=190)
        
        label_precio = Label(ventana_compra, text=f"Precio: {precio}", bg='white', font=("Calibri", 16))
        label_precio.place(x=350, y=240)
        
        # botones de compra y añadir a favoritos
        boton_compra = Button(ventana_compra, text="Comprar ahora", width=24, bg="Green", fg="white", font=("Century Gothic", 16))
        boton_compra.place(x=10, y=460)
        
        boton_añadir_favoritos = Button(ventana_compra, text="Añadir a favoritos", width=24, bg='salmon', fg="white", font=("Century Gothic", 16))
        boton_añadir_favoritos.place(x=10, y=510)
        
        # talles
        cantidades = [1, 2, 3, 4, 5]
            
        # XS
        label_xs = Label(ventana_compra, text="XS", bg='white', font=("Calibri", 14))
        label_xs.place(x=10, y=560)
        
        combo_xs = ttk.Combobox(ventana_compra, width=1, values=cantidades, font=("Calibri", 14))    
        combo_xs.place(x=10, y=590)
        
        # S
        label_s = Label(ventana_compra, text="S", bg='white', font=("Calibri", 14))
        label_s.place(x=60, y=560)
        
        combo_s = ttk.Combobox(ventana_compra, width=1, values=cantidades, font=("Calibri", 14))    
        combo_s.place(x=60, y=590)
        # M
        label_m = Label(ventana_compra, text="M", bg='white', font=("Calibri", 14))
        label_m.place(x=110, y=560)
        
        combo_m = ttk.Combobox(ventana_compra, width=1, values=cantidades, font=("Calibri", 14))    
        combo_m.place(x=110, y=590)
        # L
        label_l = Label(ventana_compra, text="L", bg='white', font=("Calibri", 14))
        label_l.place(x=160, y=560)
        
        combo_l = ttk.Combobox(ventana_compra, width=1, values=cantidades, font=("Calibri", 14))    
        combo_l.place(x=160, y=590)
        # XL
        label_xl = Label(ventana_compra, text="XL", bg='white', font=("Calibri", 14))
        label_xl.place(x=210, y=560)
        
        combo_xl = ttk.Combobox(ventana_compra, width=1, values=cantidades, font=("Calibri", 14))    
        combo_xl.place(x=210, y=590)
        # XXL
        label_xxl = Label(ventana_compra, text="XXL", bg='white', font=("Calibri", 14))
        label_xxl.place(x=260, y=560)
        
        combo_xxl = ttk.Combobox(ventana_compra, width=1, values=cantidades, font=("Calibri", 14))    
        combo_xxl.place(x=260, y=590)
        
        
        try:
            consulta = f"SELECT stock_talle FROM stock WHERE id_producto = {id_camiseta}"
            tabla = coneccion.cursor()
            tabla.execute(consulta)
            talles = tabla.fetchall()
            
            xs, s, m, l, xl, xxl = talles
            
            if xs[0] == 0:
                combo_xs.config(state='disabled')
                label_xs.config(fg='red')
            if s[0] == 0:
                combo_s.config(state='disabled')
                label_s.config(fg='red')
            if m[0] == 0:
                combo_m.config(state='disabled')
                label_m.config(fg='red')
            if l[0] == 0:
                combo_l.config(state='disabled')
                label_l.config(fg='red')
            if xl[0] == 0:
                combo_xl.config(state='disabled')
                label_xl.config(fg='red')
            if xxl[0] == 0:
                combo_xxl.config(state='disabled')
                label_xxl.config(fg='red')
            
        except Exception as e:
            showwarning("Advertencia", f"Error al cargar la información de talles\n{e}")      
            
            
        # productos relacionados
        label_productos_relacionados = Label(ventana_compra, text="Ver más productos", bg='white', font=("Calibri", 12))
        label_productos_relacionados.place(x=900, y=10)  # seleccionar productos relacionados por marca y version
        consulta_productos_relacionados = f"SELECT imagen, nombre_producto, jugador, precio, id_producto FROM productos WHERE marca = '{marca}' and version = '{version}' and id_producto != '{id_camiseta}' ORDER BY RANDOM() LIMIT 4"
        camisetas = cargar_camisetas.cargar_camisetas(consulta_productos_relacionados) 
        
        x = 650
        y = 60
        cuadricula = 1
        
        for imagen, descripcion, id in camisetas:
            camiseta_recomendada = Button(ventana_compra, image=imagen, bg='white', border=0, width=300, height=400)
            camiseta_recomendada.place(x=x, y=y)
            
            descripcion_camiseta = Label(ventana_compra, text=descripcion, bg='white', font=("Calibri", 12))
            descripcion_camiseta.place(x=x, y=y + 410)
            
            if cuadricula == 1:
                cuadricula += 1
                x += 350
                
            elif cuadricula >= 2:
                cuadricula = 1
                x = 650
                y += 480
                
        
                     
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
vista_compra = VistaCompra()


# botón ingresar
ingresar = Login()
boton_ingresar = Button(ventana_login, text="Ingresar", width=8, command=ingresar.login)
boton_ingresar.place(x=120, y=280)

# pie de página
label_footer = Label(ventana_login, text="NBA Kits - 2024", fg="snow", bg="gray22", font=("Arial", 10))
label_footer.place(x=100, y=480)


ventana_login.mainloop()