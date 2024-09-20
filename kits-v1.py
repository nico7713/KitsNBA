from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
import tkinter.simpledialog
from PIL import Image, ImageTk
import sqlite3

# ventana de inicio
icono = "icono-logo.ico"
ventana_login = Tk()
ventana_login.title("Login")
ventana_login.geometry("300x500")
ventana_login.resizable(False, False)
ventana_login.iconbitmap(icono) 


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


          
           
class InicioCliente:    # Clase para mostrar la ventana de inicio al iniciar sesión como cliente
    def __init__(self):
        self.nombre_cliente = ""
        self.apellido_cliente = ""
        
    # Método para mostrar la ventana, recibe el id y el nombre de usuario del cliente, más una consulta sql usada para buscar
    def inicio_cliente(self, id_cliente, username_cliente, consulta_sql = "SELECT imagen, nombre_producto, jugador, precio, id_producto FROM productos ORDER BY RANDOM()"):     
        self.id_cliente = id_cliente
        self.username_cliente = username_cliente
        
        # ventana inicio cliente - creación y configuración
        inicio = Toplevel()
        inicio.title(f"Inicio - {self.username_cliente}")
        inicio.geometry("1360x760")
        inicio.resizable(False, False)
        inicio.config(bg=color_fondo_cliente)
        inicio.iconbitmap(icono)
        
        # llamar a métodos para la interfaz - estos métodos añaden los widgets necesarios a la ventana 'inicio'
        ventana_inicio = self.ventana_y_frames(inicio)
        frame_camisetas = self.configurar_scrollbar(ventana_inicio)
        self.colocar_camisetas(frame_camisetas, consulta_sql)
        
    def ventana_y_frames(self, ventana_inicial): 
        # ---- FRAMES ---- (colocados en la ventana toplevel 'inicio')
        # busqueda
        frame_busqueda = Frame(ventana_inicial, bg="black", border=1, width=1360, height=80)
        frame_busqueda.pack()
        
        # acceso rapido
        frame_acceso_rapido = Frame(ventana_inicial, bg="black", border=1, width=100, height=760)   # para usar el método .place() en un frame, hay que definir su ancho, su alto
        frame_acceso_rapido.pack(side=LEFT)                                                                # y posicionarlo antes de los demás widgets
        
        # ELEMENTOS de frames
        # elementos del frame_busqueda
        # barra de busqueda
        self.barra_busqueda = Entry(frame_busqueda, width=50, font=fuente_cliente, justify='center')
        self.barra_busqueda.place(x=400, y=30)
        
        # boton de busqueda
        boton_busqueda = Button(frame_busqueda, image=imagen_buscar, border=0, cursor="hand2", command=lambda : busqueda(self, False))
        boton_busqueda.place(x=870, y=24)
        
        # volver (cargar de nuevo las camisetas)
        boton_volver = Button(frame_busqueda, image=imagen_volver, bg='black', border=0, cursor="hand2", command=lambda : busqueda(self, True))
        boton_volver.place(x=15, y=15) 
        
        boton_volver.bind("<Enter>", lambda e: e.widget.config(bg="lightblue", highlightthickness=2, highlightbackground="blue"))
        boton_volver.bind("<Leave>", lambda e: e.widget.config(bg="black", highlightthickness=0))
        
        def busqueda(self, volver=False):
            criterio = self.barra_busqueda.get()
            if criterio and not volver:
                consulta_sql = f'''
                SELECT imagen, nombre_producto, jugador, precio, id_producto
                FROM productos
                WHERE marca LIKE "%{criterio}%"
                OR jugador LIKE "%{criterio}%"
                OR equipo LIKE "%{criterio}%"
                OR version LIKE "%{criterio}%"
                OR nombre_producto LIKE "%{criterio}%"
                ORDER BY RANDOM() 
                                '''
            if volver:
                consulta_sql = "SELECT imagen, nombre_producto, jugador, precio, id_producto FROM productos ORDER BY RANDOM()"
            
            if criterio or volver: 
                for widget in ventana_inicial.winfo_children():
                    widget.destroy()
                        
                ventana_inicio = self.ventana_y_frames(ventana_inicial)
                self.barra_busqueda.insert(0, criterio)
                frame_camisetas = self.configurar_scrollbar(ventana_inicio)
                self.colocar_camisetas(frame_camisetas, consulta_sql)
            
              
        # elementos del frame_acceso_rapido
        # boton modificar cliente
        boton_modificar_cliente = Button(frame_acceso_rapido, image=imagen_modificar_cliente, cursor="hand2", border=0)
        boton_modificar_cliente.place(x=15, y=120)
        
        boton_modificar_cliente.bind("<Enter>", lambda e: e.widget.config(bg="lightblue", highlightthickness=2, highlightbackground="blue"))
        boton_modificar_cliente.bind("<Leave>", lambda e: e.widget.config(bg="snow", highlightthickness=0))
        
        # boton filtrar por
        boton_filtrar = Button(frame_acceso_rapido, image=imagen_filtrar, cursor="hand2", border=0)
        boton_filtrar.place(x=15, y=215)
        
        boton_filtrar.bind("<Enter>", lambda e: e.widget.config(bg="lightblue", highlightthickness=2, highlightbackground="blue"))
        boton_filtrar.bind("<Leave>", lambda e: e.widget.config(bg="snow", highlightthickness=0))
        
        # mis compras
        boton_mis_compras = Button(frame_acceso_rapido, image=imagen_compras, cursor="hand2", border=0)
        boton_mis_compras.place(x=15, y=305)
        
        boton_mis_compras.bind("<Enter>", lambda e: e.widget.config(bg="lightblue", highlightthickness=2, highlightbackground="blue"))
        boton_mis_compras.bind("<Leave>", lambda e: e.widget.config(bg="snow", highlightthickness=0))
        
        # mis favoritos
        boton_favoritos = Button(frame_acceso_rapido, image=imagen_favoritos, cursor="hand2", border=0)
        boton_favoritos.place(x=15, y=395)
        
        boton_favoritos.bind("<Enter>", lambda e: e.widget.config(bg="lightblue", highlightthickness=2, highlightbackground="blue"))
        boton_favoritos.bind("<Leave>", lambda e: e.widget.config(bg="snow", highlightthickness=0))
        
        # Términos y condiciones
        boton_terminos = Button(frame_acceso_rapido, image=imagen_acuerdo, cursor="hand2", border=0)
        boton_terminos.place(x=15, y=485)
        
        boton_terminos.bind("<Enter>", lambda e: e.widget.config(bg="lightblue", highlightthickness=2, highlightbackground="blue"))
        boton_terminos.bind("<Leave>", lambda e: e.widget.config(bg="snow", highlightthickness=0))
        
        return ventana_inicial      # retornamos la ventana original de inicio con los frames de busqueda y acceso rápido añadidos
        # ---- FIN de los frames ---- Al colocar los frames en la ventana original toplevel antes de declarar el scrollbar, estos van a estar fijos y no van a ser deslizados
        
        
    def configurar_scrollbar(self, ventana_principal):
        # ---- scrollbar ---- (esta barra va a deslizar por las camisetas) 
        # frame para el canvas
        frame_principal = Frame(ventana_principal)
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
        
         # ----- Evento para usar la rueda del mouse -----
        def on_mouse_wheel(event):
            canva.yview_scroll(-1 * int((event.delta / 120)), "units")
            
        # Vincular la rueda del mouse al canvas
        canva.bind_all("<MouseWheel>", on_mouse_wheel)
        
        return frame_widgets    # retornamos un frame con un scrollbar listo para que las camisetas se coloquen acá y sean deslizadas 
        # ---- FIN scrollbar ---- ahora la barra de deslizamiento esta configurada para deslizar por sobre las camisetas
        
        
        # --- colocar camisetas ----
    def colocar_camisetas(self, frame_camisetas, consulta_sql):
        try:
            # lista camisetas
            camisetas = cargar_camisetas.cargar_camisetas(consulta_sql) 
            
            if camisetas:
            
                fila = 0
                columna = 0 
                
                for imagen_camiseta, descripcion_camiseta, id_camiseta in camisetas: # se declara la variable que contenga la imagen en la función lambda para mantener la referencia
                    camiseta = Button(frame_camisetas, image=imagen_camiseta, border=0, width=300, height=400, bg='white', cursor="hand2",
                                    command=lambda imagen=imagen_camiseta, id=id_camiseta : vista_compra.vista_compra(imagen, id))
                    camiseta.grid(row=fila, column=columna, padx=60, pady=10)
                    
                    camiseta.bind("<Enter>", lambda e: e.widget.config(bg="lightblue", highlightbackground="blue"))
                    camiseta.bind("<Leave>", lambda e: e.widget.config(bg="white"))
                    
                    descripcion = Label(frame_camisetas, text=descripcion_camiseta, bg='white', font=("Calibri", 12))
                    descripcion.grid(row=fila + 1, column=columna)
                    
                    if columna < 2:
                        columna += 1
                        
                    elif columna == 2:
                        columna = 0
                        fila += 2
                        
            else:
                sin_resultados = Label(frame_camisetas, text=":/\nLo sentimos, no se encontraron resultados.", bg="white", font=("Calibri", 28))
                sin_resultados.pack(padx=300 ,pady=300)
                    
        except Exception as e:
            showwarning("Advertencia", f"Error al momento de iniciar sesión al cargar las camisetas.\n{e}")
            
        # ---- FIN camisetas ----
        
    
# clase para cargar las imagenes de las camisetas y una descripción (nombre de la camiseta, jugador y precio). 
# Esta clase esta diseñada para que la consulta SQL seleccione 4 campos (imagen, nombre_producto, jugador, precio)
class CargarCamisetas:  
    def __init__(self):
        self.imagenes_cargadas = []     # Lista para mantener la referencia a las imagenes
        
    def cargar_camisetas(self, consulta_sql, modificar_tamaño=False, tamaño_imagenes=(400, 300)):    # Al poner parametros ya definidos, no hay un error si no los pasamos
        try:
            tabla = coneccion.cursor()
            tabla.execute(consulta_sql) 
            info_camisetas = tabla.fetchall()
            camisetas = []
            
            for camiseta in info_camisetas:
                archivo, producto, jugador, precio, id = camiseta               # desempaquetar la tupla
                
                archivo = "camisetas/" + archivo                                # especificar la ruta de las imagenes correctamente
                imagen_camiseta = Image.open(archivo)                           # crear imagen de la camiseta
                if modificar_tamaño:                                            # Modificar el tamaño de la camiseta si el usuario lo especificó
                    imagen_camiseta = imagen_camiseta.resize(tamaño_imagenes, Image.LANCZOS)
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
            consulta_sql = f"SELECT nombre_producto, precio, marca, equipo, temporada, jugador, version, color, descripcion FROM productos WHERE id_producto = {id_camiseta}"
            tabla = coneccion.cursor()
            tabla.execute(consulta_sql) 
            info_camiseta = tabla.fetchone()
            return info_camiseta
        except Exception as e:
            showwarning("Advertencia", f"Error en la base de datos al entrar a la ventana de compra.\n{e}") 
        
                           
    def vista_compra(self, imagen_camiseta, id_camiseta):
        producto, precio, marca, equipo, temporada, jugador, version, color, descripcion = self.obtener_informacion_camiseta(id_camiseta)
        
        ventana_compra = Toplevel()
        ventana_compra.title(f"Comprar {producto} {jugador} {color}")
        ventana_compra.geometry("1366x768")
        ventana_compra.resizable(False, False)
        ventana_compra.config(bg='white')
        ventana_compra.iconbitmap(icono)
        
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
         
        area_descripcion = Text(ventana_compra, bg='white', font=("Calibri", 12), width=40, height=10, border=0, wrap='word')
        area_descripcion.place(x=350, y=220)    
        area_descripcion.insert("1.0", f"Descripción: {descripcion}")
        area_descripcion.config(state='disabled')
        
        label_precio = Label(ventana_compra, text=f"Precio: {precio}", bg='white', font=("Calibri", 16))
        label_precio.place(x=350, y=460)
        
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
        
        combo_xs = ttk.Combobox(ventana_compra, width=1, values=cantidades, font=("Calibri", 14), state='readonly')    
        combo_xs.place(x=10, y=590)
        
        # S
        label_s = Label(ventana_compra, text="S", bg='white', font=("Calibri", 14))
        label_s.place(x=60, y=560)
        
        combo_s = ttk.Combobox(ventana_compra, width=1, values=cantidades, font=("Calibri", 14), state='readonly')    
        combo_s.place(x=60, y=590)
        # M
        label_m = Label(ventana_compra, text="M", bg='white', font=("Calibri", 14))
        label_m.place(x=110, y=560)
        
        combo_m = ttk.Combobox(ventana_compra, width=1, values=cantidades, font=("Calibri", 14), state='readonly')    
        combo_m.place(x=110, y=590)
        # L
        label_l = Label(ventana_compra, text="L", bg='white', font=("Calibri", 14))
        label_l.place(x=160, y=560)
        
        combo_l = ttk.Combobox(ventana_compra, width=1, values=cantidades, font=("Calibri", 14), state='readonly')    
        combo_l.place(x=160, y=590)
        # XL
        label_xl = Label(ventana_compra, text="XL", bg='white', font=("Calibri", 14))
        label_xl.place(x=210, y=560)
        
        combo_xl = ttk.Combobox(ventana_compra, width=1, values=cantidades, font=("Calibri", 14), state='readonly')    
        combo_xl.place(x=210, y=590)
        # XXL
        label_xxl = Label(ventana_compra, text="XXL", bg='white', font=("Calibri", 14))
        label_xxl.place(x=260, y=560)
        
        combo_xxl = ttk.Combobox(ventana_compra, width=1, values=cantidades, font=("Calibri", 14), state='readonly')    
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
            
        try:
            # productos relacionados
            label_productos_relacionados = Label(ventana_compra, text="Ver más productos", bg='white', font=("Calibri", 12))
            label_productos_relacionados.place(x=900, y=10)  # seleccionar productos relacionados por marca y version
            consulta_productos_relacionados = f"SELECT imagen, nombre_producto, jugador, precio, id_producto FROM productos WHERE marca = '{marca}' and version = '{version}' and id_producto != '{id_camiseta}' ORDER BY RANDOM() LIMIT 4"
            camisetas = cargar_camisetas.cargar_camisetas(consulta_sql=consulta_productos_relacionados, modificar_tamaño=True, tamaño_imagenes=(280, 350)) 
            
            x = 720
            y = 60
            cuadricula = 1
            
            for imagen, descripcion, id in camisetas:
                camiseta_recomendada = Button(ventana_compra, image=imagen, bg='white', border=0)
                camiseta_recomendada.place(x=x, y=y)
                
                descripcion_camiseta = Label(ventana_compra, text=descripcion, bg='white', font=("Calibri", 12))
                descripcion_camiseta.place(x=x, y=y + 410)
                
                if cuadricula == 1:
                    cuadricula += 1
                    x += 350
                    
                elif cuadricula >= 2:
                    cuadricula = 1
                    x = 720
                    y += 480
        except Exception as e:
            showwarning("Advertencia", f"Error al cargar camisetas relacionadas.\n{e}") 
                
        
                     
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

ruta_volver = "botones/volver2.png"
imagen_volver = Image.open(ruta_volver)
imagen_volver = ImageTk.PhotoImage(imagen_volver)
 

# instancias
inicio_cliente = InicioCliente()
cargar_camisetas = CargarCamisetas()
vista_compra = VistaCompra()


# botón ingresar
ingresar = Login()
boton_ingresar = Button(ventana_login, text="Ingresar", width=8, cursor="hand2", command=ingresar.login)
boton_ingresar.place(x=120, y=280)

# pie de página
label_footer = Label(ventana_login, text="NBA Kits - 2024", fg="snow", bg="gray22", font=("Arial", 10))
label_footer.place(x=100, y=480)


ventana_login.mainloop()