from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
from tkinter import simpledialog
from PIL import Image, ImageTk
import sqlite3
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt

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
                        inicio_admin.ventana_inicio_admin(id_usuario, self.username)
                        ventana_login.withdraw()
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
        
    # Método para mostrar la ventana, recibe el id y el nombre de usuario del cliente
    def inicio_cliente(self, id_cliente, username_cliente):     
        self.id_cliente = id_cliente
        self.username_cliente = username_cliente
        
        self.nombre_cliente, self.apellido_cliente = self.obtener_nombre_cliente((id_cliente,))   # desempaquetar nombre y apellido del usuario 
        
        self.obtener_nombre_cliente((id_cliente, )) 
        # ventana inicio cliente - creación y configuración
        inicio = Toplevel()
        inicio.title(f"Inicio - {self.username_cliente}")
        inicio.geometry("1360x760")
        inicio.resizable(False, False)
        inicio.config(bg=color_fondo_cliente)
        inicio.iconbitmap(icono)
        
        def cerrar():
            inicio.destroy()
            ventana_login.destroy()
            
        inicio.protocol("WM_DELETE_WINDOW", cerrar)
        
        # llamar a métodos para la interfaz - estos métodos añaden los widgets necesarios a la ventana 'inicio'
        self.limpiar_cargar_widgets(inicio, "SELECT imagen, nombre_producto, jugador, precio, id_producto FROM productos ORDER BY RANDOM()") # Consulta de inicio
        
    def ventana_y_frames(self, ventana_inicial): 
        # limpiar widgets antes de cargarlos todos de nuevo, ya que este método funciona en conjunto con configurar_scrollbar y colocar_camisetas
        for widget in ventana_inicial.winfo_children():     
            widget.destroy()                              
            
        # ---- FRAMES ---- (colocados en la ventana toplevel 'inicio')
        # busqueda
        frame_busqueda = Frame(ventana_inicial, bg="black", border=1, width=1360, height=80)
        frame_busqueda.pack()
        
        # acceso rapido
        frame_acceso_rapido = Frame(ventana_inicial, bg="black", border=1, width=100, height=760)   # para usar el método .place() en un frame, hay que definir su ancho, su alto
        frame_acceso_rapido.pack(side=LEFT)                                                                # y posicionarlo antes de los demás widgets
        
        # ELEMENTOS de frames
        # -----elementos del frame_busqueda-----
        # barra de busqueda
        self.barra_busqueda = Entry(frame_busqueda, width=50, font=fuente_cliente, justify='center')
        self.barra_busqueda.place(x=400, y=30)
        
        # boton de busqueda
        boton_busqueda = Button(frame_busqueda, image=imagen_buscar, border=0, bg="snow", cursor="hand2", command=lambda : self.busqueda(ventana_inicial))
        boton_busqueda.place(x=870, y=24)
        
        boton_busqueda.bind("<Enter>", lambda e: e.widget.config(bg="light blue", highlightthickness=2, highlightbackground="blue"))
        boton_busqueda.bind("<Leave>", lambda e: e.widget.config(bg="snow", highlightthickness=0))
        
        # volver (cargar de nuevo las camisetas)
        boton_volver = Button(frame_busqueda, image=imagen_volver, bg="black", border=0, cursor="hand2", command=lambda : self.recargar_camisetas(ventana_inicial)) 
        boton_volver.place(x=15, y=15) 
        
        boton_volver.bind("<Enter>", lambda e: e.widget.config(bg="gray", highlightthickness=2, highlightbackground="blue"))
        boton_volver.bind("<Leave>", lambda e: e.widget.config(bg="black", highlightthickness=0))
        
        # botón para modificar la información personal del usuario
        boton_nombre_de_usuario = Button(frame_busqueda, text=f"{self.nombre_cliente} {self.apellido_cliente}", bg="black", fg="white", font=("Century Gothic", 12),
                                         border=0, cursor="hand2", command=lambda : editar_cliente.interfaz_editar_datos_principales(self.id_cliente))
        boton_nombre_de_usuario.place(x=1150, y=25)
        
        boton_nombre_de_usuario.bind("<Enter>", lambda e: e.widget.config(bg="gray", highlightthickness=2, highlightbackground="blue"))
        boton_nombre_de_usuario.bind("<Leave>", lambda e: e.widget.config(bg="black", highlightthickness=0))
                  
        # -----elementos del frame_acceso_rapido-----
        # boton modificar ubicacion cliente
        boton_modificar_ubicacion = Button(frame_acceso_rapido, image=imagen_modificar_ubicacion, cursor="hand2", border=0,
                                           command=lambda : editar_direccion_cliente.interfaz_editar_ubicacion(self.id_cliente))
        boton_modificar_ubicacion.place(x=15, y=120)
        
        boton_modificar_ubicacion.bind("<Enter>", lambda e: e.widget.config(bg="lightblue", highlightthickness=2, highlightbackground="blue"))
        boton_modificar_ubicacion.bind("<Leave>", lambda e: e.widget.config(bg="snow", highlightthickness=0))
        
        # boton filtrar por
        boton_filtrar = Button(frame_acceso_rapido, image=imagen_filtrar, cursor="hand2", border=0, command=lambda : self.ventana_filtro(ventana_inicial))
        boton_filtrar.place(x=15, y=215)
        
        boton_filtrar.bind("<Enter>", lambda e: e.widget.config(bg="lightblue", highlightthickness=2, highlightbackground="blue"))
        boton_filtrar.bind("<Leave>", lambda e: e.widget.config(bg="snow", highlightthickness=0))
        
        # mis compras
        boton_mis_compras = Button(frame_acceso_rapido, image=imagen_compras, cursor="hand2", border=0, command=lambda : self.ver_compras(ventana_inicial))
        boton_mis_compras.place(x=15, y=305)
        
        boton_mis_compras.bind("<Enter>", lambda e: e.widget.config(bg="lightblue", highlightthickness=2, highlightbackground="blue"))
        boton_mis_compras.bind("<Leave>", lambda e: e.widget.config(bg="snow", highlightthickness=0))
        
        # mis favoritos
        boton_favoritos = Button(frame_acceso_rapido, image=imagen_favoritos, cursor="hand2", border=0, command=lambda : self.ver_favoritos(ventana_inicial)) 
        boton_favoritos.place(x=15, y=395)
        
        boton_favoritos.bind("<Enter>", lambda e: e.widget.config(bg="lightblue", highlightthickness=2, highlightbackground="blue"))
        boton_favoritos.bind("<Leave>", lambda e: e.widget.config(bg="snow", highlightthickness=0))
        
        # Términos y condiciones
        boton_terminos = Button(frame_acceso_rapido, image=imagen_acuerdo, cursor="hand2", border=0, command=lambda : terminos.interfaz_terminos(self.nombre_cliente))
        boton_terminos.place(x=15, y=485)
        
        boton_terminos.bind("<Enter>", lambda e: e.widget.config(bg="lightblue", highlightthickness=2, highlightbackground="blue"))
        boton_terminos.bind("<Leave>", lambda e: e.widget.config(bg="snow", highlightthickness=0))
        
        return ventana_inicial      # retornamos la ventana original de inicio con los frames de busqueda y acceso rápido añadidos
        # ---- FIN de los frames ---- Al colocar los frames en la ventana original toplevel antes de declarar el scrollbar, estos van a estar fijos y no van a ser deslizados
        
        
    def configurar_scrollbar(self, ventana_principal, mousewheel=True):
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
        
        if mousewheel:
            # ----- Evento para usar la rueda del mouse -----
            def on_mouse_wheel(event):
                canva.yview_scroll(-1 * int((event.delta / 120)), "units")
                
            # Vincular la rueda del mouse al canvas
            canva.bind_all("<MouseWheel>", on_mouse_wheel)
        
        return frame_widgets    # retornamos un frame con un scrollbar listo para que las camisetas se coloquen acá y sean deslizadas 
        # ---- FIN scrollbar ---- ahora la barra de deslizamiento esta configurada para deslizar por sobre las camisetas
        
        
        # --- colocar camisetas ----
    def colocar_camisetas(self, frame_camisetas, consulta_sql, parametro_sql=()):
        try:
            # lista camisetas
            camisetas = cargar_camisetas.cargar_camisetas(consulta_sql, parametro_sql) 
            
            if camisetas:
            
                fila = 0
                columna = 0 
                
                for imagen_camiseta, descripcion_camiseta, id_camiseta in camisetas: # se declara la variable que contenga la imagen en la función lambda para mantener la referencia
                    camiseta = Button(frame_camisetas, image=imagen_camiseta, border=0, width=300, height=400, bg='white', cursor="hand2",
                                    command=lambda imagen=imagen_camiseta, id=id_camiseta, id_cliente=self.id_cliente : vista_compra.vista_compra(imagen, id, id_cliente))
                    camiseta.grid(row=fila, column=columna, padx=60, pady=10)
                    
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
        
    def obtener_nombre_cliente(self, id_usuario):
        try:
            tabla = coneccion.cursor()
            tabla.execute("SELECT nombre, apellido FROM usuarios WHERE id_usuario = ?", id_usuario) 
            datos = tabla.fetchone()
            return datos
        except sqlite3.OperationalError as e:
            showwarning("Advertencia", f"No pudimos obtener el nombre y apellido del usuario.\n{e}")
            
            
    def limpiar_cargar_widgets(self, ventana, consulta_sql, parametro_sql=()):  # método para recargar la ventana con nuevas camisetas dependiendo de la búsqueda
        ventana = self.ventana_y_frames(ventana) 
        frame_camisetas = self.configurar_scrollbar(ventana)
        if not parametro_sql:
            self.colocar_camisetas(frame_camisetas, consulta_sql)
        else:
            self.colocar_camisetas(frame_camisetas, consulta_sql, parametro_sql)      
    
    def busqueda(self, ventana):    # método para buscar con la bara de búsqueda
        criterio = self.barra_busqueda.get()
        if criterio:
            consulta_sql = '''SELECT imagen, nombre_producto, jugador, precio, id_producto
                              FROM productos
                              WHERE nombre_producto LIKE ?
                              OR marca LIKE ?
                              OR equipo LIKE ?
                              OR jugador LIKE ?
                              OR version LIKE ?
                              ORDER BY RANDOM()
                              '''
            self.limpiar_cargar_widgets(ventana, consulta_sql, parametro_sql=(f"%{criterio}%", f"%{criterio}%", f"%{criterio}%", f"%{criterio}%", f"%{criterio}%"))
            self.barra_busqueda.insert(0, criterio)
                          

    def recargar_camisetas(self, ventana):  # recargar ventana con nuevas camisetas
        consulta_sql = "SELECT imagen, nombre_producto, jugador, precio, id_producto FROM productos ORDER BY RANDOM()"
        self.limpiar_cargar_widgets(ventana, consulta_sql) 
            
    def ver_favoritos(self, ventana):   # ver los productos favoritos del usuario
        consulta_sql = f'''
                SELECT imagen, nombre_producto, jugador, precio, p.id_producto FROM productos p
                INNER JOIN favoritos f
                ON p.id_producto = f.id_producto
                WHERE f.id_usuario = ?
                        '''
        self.limpiar_cargar_widgets(ventana, consulta_sql, (self.id_cliente, ))
        
    def ver_compras(self, ventana): # ver compras del usuario
        consulta_sql = f'''
                SELECT DISTINCT imagen, nombre_producto, jugador, precio, p.id_producto FROM productos p
                JOIN ventas v
                ON p.id_producto = v.id_producto
                WHERE v.id_usuario = ?
                       '''
        self.limpiar_cargar_widgets(ventana, consulta_sql, (self.id_cliente, ))
        
    def ventana_filtro(self, ventana):  # ventana para filtrar camisetas por precio, marca, versión, color y equipo
        ventana_filtrar = Toplevel(ventana)
        ventana_filtrar.title("Filtrar por")
        ventana_filtrar.geometry("300x170")
        ventana_filtrar.resizable(False, False)
        ventana_filtrar.iconbitmap(icono)
                
        campos = ["Precio", "Marca", "Version", "Color", "Equipo"]
        self.entry_campo = ttk.Combobox(ventana_filtrar, values=campos, font=('Century Gothic', 12))
        self.entry_campo.insert(0, campos[0])
        self.entry_campo.config(state='readonly')
        self.entry_campo.pack(pady=10)
                
        orden = ["Ascendente", "Descendente"]
        self.entry_orden = ttk.Combobox(ventana_filtrar, values=orden, font=('Century Gothic', 12))
        self.entry_orden.insert(0, orden[0])
        self.entry_orden.config(state='readonly')
        self.entry_orden.pack(pady=10)
        
        boton_ir = Button(ventana_filtrar, text="Filtrar", bg='gray22', fg='white', font=('Century Gothic', 12), width=15, cursor="hand2",
                          command=lambda : self.filtrar(ventana, ventana_filtrar))
        boton_ir.pack(pady=10)
        
        boton_ir.bind("<Enter>", lambda e: e.widget.config(bg="black", highlightbackground="blue"))
        boton_ir.bind("<Leave>", lambda e: e.widget.config(bg="gray22", highlightthickness=0))
        
    def filtrar(self, ventana_camisetas, ventana_filtrar): # lógica para filtrar
        campo = self.entry_campo.get().lower()
        if self.entry_orden.get() == "Ascendente":
            orden = "ASC"
        elif self.entry_orden.get() == "Descendente":
            orden = "DESC"
        else:
            showwarning("Error al filtrar.", "Orden incorrecto.")
            return 
                           
        ventana_filtrar.destroy()
        consulta_sql = f"SELECT imagen, nombre_producto, jugador, precio, id_producto FROM productos ORDER BY {campo} {orden}" 
        self.limpiar_cargar_widgets(ventana_camisetas, consulta_sql)
                              
        
    
# clase para cargar las imagenes de las camisetas y una descripción (nombre de la camiseta, jugador y precio). 
# Esta clase esta diseñada para que la consulta SQL seleccione 5 campos (imagen, nombre_producto, jugador, precio y id_camiseta)
class CargarCamisetas:  
    def __init__(self):
        self.imagenes_cargadas = []     # Lista para mantener la referencia a las imagenes
        
    def cargar_camisetas(self, consulta_sql, parametro_sql=(), modificar_tamaño=False, tamaño_imagenes=(400, 300)): # Al poner parametros ya definidos, no hay un error si no los pasamos
        try:
            tabla = coneccion.cursor()
            if not parametro_sql:
                tabla.execute(consulta_sql)
            else:
                tabla.execute(consulta_sql, parametro_sql) 
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
        
        
        
class EditarCliente: 
    def obtener_datos_cliente(self, id_usuario):
        try:
            tabla = coneccion.cursor()
            tabla.execute("SELECT nombre, apellido, num_telefono, email, username FROM usuarios WHERE id_usuario = ?", (id_usuario, )) 
            datos_cliente = tabla.fetchone()
            return datos_cliente
        except sqlite3.OperationalError as e:
            showwarning("Advertencia", f"Error al acceder a los datos del cliente.\n{e}")
        
    def interfaz_editar_datos_principales(self, id_usuario):
        nombre, apellido, telefono, email, username = self.obtener_datos_cliente(id_usuario) 
        editar_cliente = Toplevel()
        editar_cliente.title(f"Editar cliente - {nombre} {apellido}") 
        editar_cliente.geometry("510x330")
        editar_cliente.resizable(False, False)
        editar_cliente.config(bg="white")
        editar_cliente.iconbitmap(icono)
        
        label_nombre = Label(editar_cliente, text="Nombre", bg="white", font=("Century Gothic", 12))
        label_nombre.place(x=10, y=10)
        
        self.entry_nombre = Entry(editar_cliente, width=20, font=("Century Gothic", 12), bg="white", border=1)
        self.entry_nombre.place(x=10, y=40)
        
        label_apellido = Label(editar_cliente, text="Apellido", bg="white", font=("Century Gothic", 12))
        label_apellido.place(x=10, y=80)
        
        self.entry_apellido = Entry(editar_cliente, width=20, font=("Century Gothic", 12), bg="white", border=1)
        self.entry_apellido.place(x=10, y=110)
        
        label_telefono = Label(editar_cliente, text="Número de Teléfono", bg="white", font=("Century Gothic", 12))
        label_telefono.place(x=10, y=150)
        
        self.entry_telefono = Entry(editar_cliente, width=20, font=("Century Gothic", 12), bg="white", border=1)
        self.entry_telefono.place(x=10, y=180)
        
        label_email = Label(editar_cliente, text="Email", bg="white", font=("Century Gothic", 12))
        label_email.place(x=10, y=220)
        
        self.entry_email = Entry(editar_cliente, width=25, font=("Century Gothic", 12), bg="white", border=1)
        self.entry_email.place(x=10, y=250)
        
        label_username = Label(editar_cliente, text="Nombre de usuario", bg="white", font=("Century Gothic", 12))
        label_username.place(x=280, y=10)
        
        self.entry_username = Entry(editar_cliente, width=20, font=("Century Gothic", 12), bg="white", border=1)
        self.entry_username.place(x=280, y=40)
        
        # insertar datos iniciales
        self.entry_nombre.insert(0, nombre)
        self.entry_apellido.insert(0, apellido)
        self.entry_telefono.insert(0, telefono)
        self.entry_email.insert(0, email) 
        self.entry_username.insert(0, username)
        
        # botones
        boton_confirmar_cambios = Button(editar_cliente, text="Guardar Cambios", bg="dark blue", fg="white", font=("Century Gothic", 12), width=18, cursor="hand2",
                                         command=lambda : self.editar_datos_principales(id_usuario, editar_cliente))
        boton_confirmar_cambios.place(x=280, y=80)
        
        boton_confirmar_cambios.bind("<Enter>", lambda e: e.widget.config(bg="midnight blue"))
        boton_confirmar_cambios.bind("<Leave>", lambda e: e.widget.config(bg="dark blue"))
        
        boton_restaurar_clave = Button(editar_cliente, text="Restaurar Contraseña", bg="gray22", fg="white", font=("Century Gothic", 12), width=18, cursor="hand2",
                                       command=lambda : self.interfaz_cambiar_clave(id_usuario))
        boton_restaurar_clave.place(x=280, y=120)
        
        boton_restaurar_clave.bind("<Enter>", lambda e: e.widget.config(bg="black"))
        boton_restaurar_clave.bind("<Leave>", lambda e: e.widget.config(bg="gray22"))
        
        # logo
        logo_proyecto = Label(editar_cliente, image=imagen_proyecto, width=250, height=161)
        logo_proyecto.place(x=250, y=160)
         
         
    def editar_datos_principales(self, id_usuario, ventana):
        nuevo_nombre = self.entry_nombre.get()
        nuevo_apellido = self.entry_apellido.get()
        nuevo_telefono = self.entry_telefono.get()
        nuevo_email = self.entry_email.get()
        nuevo_username = self.entry_username.get()
        
        if nuevo_nombre and nuevo_apellido and nuevo_telefono and nuevo_email and nuevo_username:
        
            if "@" not in nuevo_email or nuevo_email.count("@") != 1 or "." not in nuevo_email.split("@")[1]:
                showwarning("Email invalido", "Por favor escriba una dirección de correo electrónico válida.")
                return
                
            if not nuevo_telefono.isnumeric() or len(nuevo_telefono) < 8:
                showwarning("Número de teléfono inválido", "Por favor escriba un número de teléfono correcto.")
                return
            
            if not nuevo_nombre.isalpha():
                showwarning("Nombre inválido", "El nombre no debe contener números ni caracteres especiales.")
                return
            
            if not nuevo_apellido.isalpha():
                showwarning("Apellido inválido", "El apellido no debe contener números ni caracteres especiales.")
                return
            
            if len(nuevo_username) < 4:
                showwarning("Username inválido", "El username debe contener al menos cuatro caracteres.")
                return
            
            confirmar = askyesno("Confirmar", "¿Estás seguro de que deseas modificar tu información de usuario?")
            
            if confirmar:
                try:
                    actualizacion = (nuevo_nombre, nuevo_apellido, nuevo_telefono, nuevo_email, nuevo_username, id_usuario)
                    tabla = coneccion.cursor()
                    tabla.execute("UPDATE usuarios SET nombre = ?, apellido = ?, num_telefono = ?, email = ?, username = ? WHERE id_usuario = ?", actualizacion)
                    coneccion.commit()
                except sqlite3.OperationalError as e:
                    showwarning("Advertencia", f"Error al actualizar la información del usuario.\n{e}")
                    return
                except sqlite3.IntegrityError:  # validar que el nombre de usuario no exista ya en la base de datos
                    showwarning("Advertencia", f"El nombre de usuario '{nuevo_username}' ya existe.\nPor favor elige otro.")
                    return
                except Exception as e2:
                    showwarning("Advertencia", f"Ocurrió un error desconocido al modificar la información de usuario.\n{e2}") 
                
                showinfo("Actualización correcta.", "Los datos se actualizaron correctamente.")
                ventana.destroy()
                
        else:
            showwarning("Advertencia", "Completa todos los campos de texto.")
                
    
    def interfaz_cambiar_clave(self, id_usuario):
        editar_clave = Toplevel()
        editar_clave.title("Restaurar contraseña") 
        editar_clave.geometry("300x150")
        editar_clave.resizable(False, False)
        editar_clave.config(bg="white")
        editar_clave.iconbitmap(icono)
        
        label_clave_original = Label(editar_clave, text="Ingresa tu contraseña actual", bg="white", font=("Century Gothic", 12))
        label_clave_original.pack()
        
        self.entry_clave_original = Entry(editar_clave, width=20, font=("Century Gothic", 12), bg="white", border=1, show="*", justify='center')
        self.entry_clave_original.pack()
        
        label_nueva_clave = Label(editar_clave, text="Ingresa tu nueva contraseña", bg="white", font=("Century Gothic", 12))
        label_nueva_clave.pack()
        
        self.entry_nueva_clave = Entry(editar_clave, width=20, font=("Century Gothic", 12), bg="white", border=1, show="*", justify='center')
        self.entry_nueva_clave.pack()
        
        boton_actualizar = Button(editar_clave, text="Actualizar", bg="gray22", fg="white", font=("Century Gothic", 12), cursor="hand2",
                                  command=lambda : self.cambiar_clave(id_usuario, editar_clave)) 
        boton_actualizar.pack(pady=10)
        
        boton_actualizar.bind("<Enter>", lambda e: e.widget.config(bg="black"))
        boton_actualizar.bind("<Leave>", lambda e: e.widget.config(bg="gray22"))
        
        
    def cambiar_clave(self, id_usuario, ventana):
        clave_actual_introducida = self.entry_clave_original.get()
        nueva_clave = self.entry_nueva_clave.get()
        
        if clave_actual_introducida and nueva_clave:
            if len(nueva_clave) >= 6:
                try:
                    tabla = coneccion.cursor()
                    tabla.execute("SELECT password FROM usuarios WHERE id_usuario = ?", (id_usuario, ))
                    clave_actual_usuario = tabla.fetchone()
                    clave_actual = str(clave_actual_usuario[0]) # convertir a string para comprarar los mismos tipos de datos
                    
                    if clave_actual_introducida == clave_actual: 
                        confirmar = askyesno("Confirmar", "¿Estás seguro que deseas cambiar tu contraseña?")
                        if confirmar:
                            datos_actualizar = (nueva_clave, id_usuario) 
                            tabla.execute("UPDATE usuarios SET password = ? WHERE id_usuario = ?", datos_actualizar)
                            coneccion.commit()
                            showinfo("Actualización correcta", "Actualizaste tu contraseña correctamente.")
                            ventana.destroy()
                    else:
                        showwarning("Contraseña actual incorrecta", "Tu contraseña actual es incorrecta.\nPor favor intenta de nuevo")       
                        return
                    
                except Exception as e:
                    showwarning("Advertencia", f"Error al cambiar contraseña.\n{e}")
                    return
            else:
                showwarning("Contraseña inválida", "La contraseña debe contener al menos 6 caracteres.")       
        else:
            showwarning("Advertencia", "No puedes ingresar contraseñas vacías.")
          

class EditarDireccionCliente:
    def direccion_actual_cliente(self, id_usuario):
        try:
            tabla = coneccion.cursor()
            consulta_ubicacion = '''
                    SELECT ubi.id_ubicacion, provincia, localidad, direccion, codigo_postal FROM ubicacion ubi
                    INNER JOIN usuarios us
                    ON ubi.id_ubicacion = us.id_ubicacion
                    WHERE us.id_usuario = ?
                                 '''
                                 
            tabla.execute(consulta_ubicacion, (id_usuario, )) 
            datos_ubicacion = tabla.fetchone()
            return datos_ubicacion
        except Exception as e:
            showwarning("Advertencia", f"Error al cargar la dirección actual del cliente.\n{e}")
            
    
    def interfaz_editar_ubicacion(self, id_usuario):
        self.id_ubicacion, provincia, localidad, direccion, codigo_postal = self.direccion_actual_cliente(id_usuario)
        editar_ubicacion = Toplevel()
        editar_ubicacion.title(f"Editar ubicación - {provincia}") 
        editar_ubicacion.geometry("480x280")
        editar_ubicacion.resizable(False, False)
        editar_ubicacion.config(bg="white")
        editar_ubicacion.iconbitmap(icono)
        
        label_provincia = Label(editar_ubicacion, text="Provincia", bg="white", font=("Century Gothic", 12))
        label_provincia.place(x=10, y=10)
        
        self.entry_provincia = ttk.Combobox(editar_ubicacion, width=17, font=("Century Gothic", 12), values=provincias)
        self.entry_provincia.place(x=10, y=40)
        
        label_localidad = Label(editar_ubicacion, text="Localidad", bg="white", font=("Century Gothic", 12))
        label_localidad.place(x=10, y=80)
        
        self.entry_localidad = Entry(editar_ubicacion, width=20, font=("Century Gothic", 12), bg="white", border=1)
        self.entry_localidad.place(x=10, y=110)
        
        label_direccion = Label(editar_ubicacion, text="Dirección", bg="white", font=("Century Gothic", 12))
        label_direccion.place(x=10, y=150)
        
        self.entry_direccion = Entry(editar_ubicacion, width=20, font=("Century Gothic", 12), bg="white", border=1)
        self.entry_direccion.place(x=10, y=180)
        
        label_codigo_postal = Label(editar_ubicacion, text="Código postal", bg="white", font=("Century Gothic", 12))
        label_codigo_postal.place(x=10, y=220)
        
        self.entry_codigo_postal = Entry(editar_ubicacion, width=20, font=("Century Gothic", 12), bg="white", border=1)
        self.entry_codigo_postal.place(x=10, y=250)
        
        # insertar datos iniciales
        self.entry_provincia.insert(0, provincia)
        self.entry_provincia.config(state='readonly')
        self.entry_localidad.insert(0, localidad)
        self.entry_direccion.insert(0, direccion)
        self.entry_codigo_postal.insert(0, codigo_postal) 
     
        boton_confirmar_cambios = Button(editar_ubicacion, text="Guardar Cambios", bg="dark blue", fg="white", font=("Century Gothic", 12), width=18, cursor="hand2",
                                         command=lambda : self.editar_ubicacion(editar_ubicacion)) 
        boton_confirmar_cambios.place(x=250, y=210)
        
        boton_confirmar_cambios.bind("<Enter>", lambda e: e.widget.config(bg="midnight blue"))
        boton_confirmar_cambios.bind("<Leave>", lambda e: e.widget.config(bg="dark blue"))
        
        # logo
        logo_proyecto = Label(editar_ubicacion, image=imagen_proyecto, width=250, height=161)
        logo_proyecto.place(x=220, y=20)
                      
    def editar_ubicacion(self, ventana):
        provincia = self.entry_provincia.get()
        localidad = self.entry_localidad.get()
        direccion = self.entry_direccion.get()
        codigo_postal = self.entry_codigo_postal.get()
        
        if localidad and direccion and codigo_postal:
            if not codigo_postal.isnumeric() or len(codigo_postal) < 4:
                showwarning("Advertencia", "Introduce un código postal válido.")
                return
            confirmar = askyesno("Confirmar", "¿Estás seguro que deseas modificar tu ubicación?")
            if confirmar:
                try:
                    datos_actualizar = (provincia, localidad, direccion, codigo_postal, self.id_ubicacion)
                    tabla = coneccion.cursor()
                    tabla.execute("UPDATE ubicacion SET provincia = ?, localidad = ?, direccion = ?, codigo_postal = ? WHERE id_ubicacion = ?", datos_actualizar)
                    coneccion.commit()
                    showinfo("Ubicación actualizada", "Actualizaste tu ubicación correctamente.")
                    ventana.destroy()
                except Exception as e:
                    showwarning("Advertencia", f"Error al modificar la ubicación.\n{e}")
        else:
            showwarning("Advertencia", "No puedes ingresar localizaciones vacías.")
    
    
            
class TerminosCondiciones:
    def interfaz_terminos(self, nombre_cliente):
        terminos = Toplevel()
        terminos.title("Términos y Condiciones")
        terminos.geometry("1360x760")
        terminos.resizable(False, False)
        terminos.iconbitmap(icono)
        
        texto_terminos = f"""Términos y Condiciones
Hola, {nombre_cliente}
        
1. Introducción
Bienvenido a KitsNBA. Al acceder y utilizar nuestra aplicación, aceptas estar sujeto a los siguientes términos y condiciones, que rigen el uso de todos los servicios ofrecidos. Por favor, lee detenidamente estos términos antes de proceder.

2. Aceptación de Términos
Al registrarte y utilizar nuestra aplicación, aceptas los términos y condiciones aquí descritos. Si no estás de acuerdo con alguna parte de estos términos, por favor, no utilices nuestros servicios.

3. Registro de Usuario
Para acceder a ciertas funciones de la aplicación, debes registrarte proporcionando información personal veraz y actualizada. Es tu responsabilidad mantener la confidencialidad de tu cuenta y contraseña, así como de todas las actividades que ocurran bajo tu cuenta.

4. Uso de la Aplicación
Prohibiciones: Está prohibido el uso indebido de nuestra aplicación, incluyendo, pero no limitado a, la transmisión de virus, malware, spam, o cualquier otra actividad ilegal o no autorizada.
Acceso y Seguridad: Nos reservamos el derecho de restringir el acceso a la aplicación o a partes de la misma en cualquier momento y por cualquier motivo.

5. Compras y Pagos
Precios y Disponibilidad: Los precios de los productos están sujetos a cambios sin previo aviso. Nos reservamos el derecho de modificar o descontinuar cualquier producto en cualquier momento.
Proceso de Pago: Todas las compras realizadas a través de la aplicación están sujetas a la aceptación de la forma de pago proporcionada. Aceptamos exclusivamente tarjetas de débito.

6. Envíos y Devoluciones
Tiempos de Envío: Los tiempos de envío son estimados y pueden variar según la ubicación y la disponibilidad del producto.
Política de Devoluciones: Ofrecemos devoluciones y cambios dentro de un plazo de 30 días a partir de la recepción del pedido, siempre que el producto se encuentre en su estado original. Los costos de envío de la devolución corren por cuenta del cliente.

7. Protección de Datos
Nos comprometemos a proteger la privacidad de nuestros usuarios. Todos los datos personales recopilados serán utilizados de acuerdo con nuestra Política de Privacidad.

8. Propiedad Intelectual
Todo el contenido de la aplicación, incluyendo pero no limitado a, logotipos, imágenes, gráficos, y textos, es propiedad de KitsNBA o de nuestros proveedores y está protegido por leyes de derechos de autor y otras leyes de propiedad intelectual.

9. Modificaciones a los Términos
Nos reservamos el derecho de modificar estos términos y condiciones en cualquier momento. Las modificaciones entrarán en vigor inmediatamente después de su publicación en la aplicación. Es tu responsabilidad revisar estos términos periódicamente.

10. Ley Aplicable
Estos términos y condiciones se regirán e interpretarán de acuerdo con las leyes de la República Argentina, y cualquier disputa estará sujeta a la jurisdicción exclusiva de los tribunales de Mendoza.

11. Contacto
Si tienes alguna pregunta sobre estos términos y condiciones, por favor contáctanos a través de kitsnba@gmail.com.
        """
        
        area_texto = Text(terminos, width=1360, height=760, bg='snow', font=('Calibri', 12), wrap='word') 
        area_texto.insert("1.0", texto_terminos)
        area_texto.config(state='disabled')
        area_texto.pack(side='left', anchor='nw')
    
                    
class VistaCompra:      # clase para la vista de compra de una camiseta
    def __init__(self):
        self.informacion_camiseta = []
        
    def obtener_informacion_camiseta(self, id_camiseta):    # obtener todos los datos de la camiseta pasando como parametro el id
        try:
            consulta_sql = "SELECT nombre_producto, precio, marca, equipo, temporada, jugador, version, color, descripcion FROM productos WHERE id_producto = ?"
            parametro_sql = (id_camiseta, )
            tabla = coneccion.cursor()
            tabla.execute(consulta_sql, parametro_sql) 
            info_camiseta = tabla.fetchone()
            return info_camiseta
        except Exception as e:
            showwarning("Advertencia", f"Error en la base de datos al entrar a la ventana de compra.\n{e}") 
        
    def descripcion_camiseta(self, id_camiseta, imagen_camiseta):   # colocar la descripción de la camiseta en pantalla, requiere el id y la imagen 
        producto, precio, marca, equipo, temporada, jugador, version, color, descripcion = self.obtener_informacion_camiseta(id_camiseta) # obtener info de obtener_infomacion_camiseta
        
        frame_descripcion = Frame(self.ventana_compra, bg='white', width=700, height=768, border=0)
        frame_descripcion.pack(side=LEFT)
        
        muestra_camiseta = Label(frame_descripcion, image=imagen_camiseta)
        muestra_camiseta.place(x=10, y=10)
        
        label_producto = Label(frame_descripcion, text=f"Producto: {producto}", bg='white', font=("Calibri", 12))
        label_producto.place(x=350, y=10)
        
        label_marca = Label(frame_descripcion, text=f"Marca: {marca}", bg='white', font=("Calibri", 12))
        label_marca.place(x=350, y=40)
        
        label_equipo = Label(frame_descripcion, text=f"Franquicia: {equipo}", bg='white', font=("Calibri", 12))
        label_equipo.place(x=350, y=70)
        
        label_jugador = Label(frame_descripcion, text=f"Jugador: {jugador}", bg='white', font=("Calibri", 12))
        label_jugador.place(x=350, y=100)
        
        label_temporada = Label(frame_descripcion, text=f"Temporada: {temporada}", bg='white', font=("Calibri", 12))
        label_temporada.place(x=350, y=130)
        
        label_version = Label(frame_descripcion, text=f"Version: {version}", bg='white', font=("Calibri", 12))
        label_version.place(x=350, y=160)
        
        label_color = Label(frame_descripcion, text=f"Color: {color}", bg='white', font=("Calibri", 12))
        label_color.place(x=350, y=190)
         
        area_descripcion = Text(frame_descripcion, bg='white', font=("Calibri", 12), width=40, height=10, border=0, wrap='word')
        area_descripcion.place(x=350, y=220)    
        area_descripcion.insert("1.0", f"Descripción: {descripcion}")
        area_descripcion.config(state='disabled')
        
        label_precio = Label(frame_descripcion, text=f"Precio: {precio}", bg='white', font=("Calibri", 16))
        label_precio.place(x=350, y=460)
        
        # botón de compra
        color = graficos.obtener_colores([producto])[0]
        boton_compra = Button(frame_descripcion, text="Comprar ahora", width=24, bg=color, fg="white", font=("Century Gothic", 16), cursor="hand2",
                              command=lambda imagen=imagen_camiseta: confirmar_compra.vista_confirmar_compra(self.ventana_compra, self.id_cliente, id_camiseta, imagen))
        boton_compra.place(x=10, y=460)
        
        boton_compra.bind("<Enter>", lambda e: e.widget.config(bg=color, highlightthickness=1))
        boton_compra.bind("<Leave>", lambda e: e.widget.config(bg=color, highlightthickness=0))
        
        
        # logo aplicación
        logo = Label(frame_descripcion, image=imagen_proyecto)
        logo.place(x=350, y=505)
        
        return frame_descripcion
    

    def talles_camiseta(self, frame_descripcion, id_camiseta):  # método para colocar los widgets de talles y verificar stock
        try:
            consulta = "SELECT stock_talle FROM stock WHERE id_producto = ?"
            parametro = (id_camiseta, )
            tabla = coneccion.cursor()
            tabla.execute(consulta, parametro)
            talles = tabla.fetchall()
                    
            xs, s, m, l, xl, xxl = talles
            xs, s, m, l, xl, xxl = int(xs[0]), int(s[0]), int(m[0]), int(l[0]), int(xl[0]), int(xxl[0])     # convertir la cantidad de talles disponibles a entero
        
        except Exception as e:
            showwarning("Advertencia", f"Error al cargar la información de talles\n{e}") 
                 
        def cantidades_talles(stock):
            if stock > 5:   # si el stock es mayor a 5, limitar la compra a 5 camisetas por talle
                return ["", 1, 2, 3, 4, 5]
            else:
                return [""] + [i for i in range(1, stock + 1)]
                 
        # listas con la cantidad de camisetas que el usuario puede seleccionar en base al stock actual
        cantidad_xs = cantidades_talles(xs)
        cantidad_s = cantidades_talles(s)
        cantidad_m = cantidades_talles(m)     
        cantidad_l = cantidades_talles(l)
        cantidad_xl = cantidades_talles(xl)
        cantidad_xxl = cantidades_talles(xxl)
            
        # talles    
        # XS
        label_xs = Label(frame_descripcion, text="XS", bg='white', font=("Calibri", 14))
        label_xs.place(x=10, y=560)
        
        self.combo_xs = ttk.Combobox(frame_descripcion, width=1, values=cantidad_xs, font=("Calibri", 14), state='readonly')    
        self.combo_xs.place(x=10, y=590)
        # S
        label_s = Label(frame_descripcion, text="S", bg='white', font=("Calibri", 14))
        label_s.place(x=60, y=560)
        
        self.combo_s = ttk.Combobox(frame_descripcion, width=1, values=cantidad_s, font=("Calibri", 14), state='readonly')    
        self.combo_s.place(x=60, y=590)
        # M
        label_m = Label(frame_descripcion, text="M", bg='white', font=("Calibri", 14))
        label_m.place(x=110, y=560)
        
        self.combo_m = ttk.Combobox(frame_descripcion, width=1, values=cantidad_m, font=("Calibri", 14), state='readonly')    
        self.combo_m.place(x=110, y=590)
        # L
        label_l = Label(frame_descripcion, text="L", bg='white', font=("Calibri", 14))
        label_l.place(x=160, y=560)
        
        self.combo_l = ttk.Combobox(frame_descripcion, width=1, values=cantidad_l, font=("Calibri", 14), state='readonly')    
        self.combo_l.place(x=160, y=590)
        # XL
        label_xl = Label(frame_descripcion, text="XL", bg='white', font=("Calibri", 14))
        label_xl.place(x=210, y=560)
        
        self.combo_xl = ttk.Combobox(frame_descripcion, width=1, values=cantidad_xl, font=("Calibri", 14), state='readonly')    
        self.combo_xl.place(x=210, y=590)
        # XXL
        label_xxl = Label(frame_descripcion, text="XXL", bg='white', font=("Calibri", 14))
        label_xxl.place(x=260, y=560)
        
        self.combo_xxl = ttk.Combobox(frame_descripcion, width=1, values=cantidad_xxl, font=("Calibri", 14), state='readonly')    
        self.combo_xxl.place(x=260, y=590)
        
        # mostrar si hay stock disponible en los talles 
        if xs == 0:
            self.combo_xs.config(state='disabled')
            label_xs.config(fg='red')
        if s == 0:
            self.combo_s.config(state='disabled')
            label_s.config(fg='red')
        if m == 0:
            self.combo_m.config(state='disabled')
            label_m.config(fg='red')
        if l == 0:
            self.combo_l.config(state='disabled')
            label_l.config(fg='red')
        if xl == 0:
            self.combo_xl.config(state='disabled')
            label_xl.config(fg='red')
        if xxl == 0:
            self.combo_xxl.config(state='disabled')
            label_xxl.config(fg='red')
        
    

    def boton_favoritos(self, id_camiseta, id_cliente, frame_descripcion):     # este método coloca el botón de favoritos junto a la descripción de la camiseta
        try:
            tabla = coneccion.cursor()
            tabla.execute("SELECT COUNT(*) FROM favoritos WHERE id_producto = ? AND id_usuario = ?", (id_camiseta, id_cliente)) # verificar si la camiseta está en favoritos
            favorito = tabla.fetchone()[0]  # obtener la primera y unica posicion de la tupla
            # definir botón dependiendo de si se encuentra o no en favoritos
            if favorito:
                boton_añadir_favoritos = Button(frame_descripcion, text="Quitar de favoritos", width=24, bg='red', fg="white", font=("Century Gothic", 16), cursor="hand2",
                                                command=lambda : self.eliminar_favorito(id_camiseta, id_cliente, frame_descripcion))
            else:
                boton_añadir_favoritos = Button(frame_descripcion, text="Añadir a favoritos", width=24, bg='salmon', fg="white", font=("Century Gothic", 16), cursor="hand2",
                                                command=lambda : self.agregar_favorito(id_camiseta, id_cliente, frame_descripcion))
                
            boton_añadir_favoritos.bind("<Enter>", lambda e: e.widget.config(highlightthickness=1))
            boton_añadir_favoritos.bind("<Leave>", lambda e: e.widget.config(highlightthickness=0)) 
                
            boton_añadir_favoritos.place(x=10, y=510)
        except Exception as e:
            showwarning("Advertencia", f"Error al comprobar si el producto se encuentra en favoritos.\n{e}")
            
    def agregar_favorito(self, id_camiseta, id_cliente, frame_descripcion): # agregar producto a favoritos
        confirmar = askyesno("Añadir a favoritos", f"¿Deseas añadir este producto a favoritos?")
        if confirmar:
            try:
                datos = (id_camiseta, id_cliente)
                tabla = coneccion.cursor()
                tabla.execute("INSERT INTO favoritos (id_producto, id_usuario) VALUES (?, ?)", datos)
                coneccion.commit()
                nombre_camiseta = self.obtener_informacion_camiseta(id_camiseta)[0] # obtener primera posición de la tupla
                showinfo("Producto favorito", f"Agregaste '{nombre_camiseta}' a tu lista de favoritos.")
                self.boton_favoritos(id_camiseta, id_cliente, frame_descripcion)
            except Exception as e:
                showwarning("Advertencia", f"Error al agregar el producto a favoritos.\n{e}")
    
    def eliminar_favorito(self, id_camiseta, id_cliente, frame_descripcion): # eliminar producto de favoritos   
        confirmar = askyesno("Eliminar de favoritos", f"¿Deseas eliminar este producto de favoritos?")
        if confirmar:
            try:
                datos = (id_camiseta, id_cliente)
                tabla = coneccion.cursor()
                tabla.execute("DELETE FROM favoritos WHERE id_producto = ? AND id_usuario = ?", datos)
                coneccion.commit()
                nombre_camiseta = self.obtener_informacion_camiseta(id_camiseta)[0] # obtener primera posición de la tupla
                showinfo("Producto favorito", f"Eliminaste '{nombre_camiseta}' de tu lista de favoritos.")
                self.boton_favoritos(id_camiseta, id_cliente, frame_descripcion)
            except Exception as e:
                showwarning("Advertencia", f"Error al agregar el producto a favoritos.\n{e}")
    
    
    def productos_relacionados(self, id_camiseta):  # mostrar productos relacionados junto a la descripción de la camiseta
        datos_camiseta = self.obtener_informacion_camiseta(id_camiseta) 
        # obtener marca y versión de la camiseta actual para encontrar productos similares
        marca = datos_camiseta[2]
        version = datos_camiseta[6]
        
        try:
            # consultas para traer los productos relacionados
            if version == "Swingman":   # si la versión de la camiseta es swingman, vamos a mostrar todas más de estas camisetas sin filtrar por marca, ya que hay menos.
                consulta_productos_relacionados = """
                SELECT imagen, nombre_producto, jugador, precio, id_producto FROM productos WHERE version = ? and id_producto != ? ORDER BY RANDOM() LIMIT 6
                """
                parametros_productos_relacionados = (version, id_camiseta)
            else:
                consulta_productos_relacionados = """
                SELECT imagen, nombre_producto, jugador, precio, id_producto FROM productos WHERE marca = ? and version = ? and id_producto != ? ORDER BY RANDOM() LIMIT 6"""
                parametros_productos_relacionados = (marca, version, id_camiseta)
                
            camisetas = cargar_camisetas.cargar_camisetas(consulta_sql=consulta_productos_relacionados, parametro_sql=parametros_productos_relacionados,
                                                          modificar_tamaño=True, tamaño_imagenes=(280, 350))  
            
             # este frame se va a ubicar a la derecha del frame_descripcion, van a ser compatibles ya que ambos son posicionados con pack
            frame_camisetas = inicio_cliente.configurar_scrollbar(self.ventana_compra, mousewheel=False)  # mousewheel en False es para que la rueda del mouse este desabilitada 
            frame_camisetas.config(border=0, bg='white')
            label_productos_relacionados = Label(frame_camisetas, text="Ver productos relacionados", bg='white', font=("Calibri", 12))
            label_productos_relacionados.grid(row=0, column=0, columnspan=2)
            
            # lógica para colocar camisetas en el frame
            fila = 1
            columna = 0
            
            for imagen, descripcion, id in camisetas:
                camiseta_recomendada = Button(frame_camisetas, image=imagen, bg='white', border=0, cursor='hand2',
                        command=lambda imagen_relacionada=imagen, id_relacionado=id : self.vista_compra(imagen_relacionada, id_relacionado, self.id_cliente, recargar_ventana=True))
                camiseta_recomendada.grid(row=fila, column=columna, padx=20, pady=10)
                
                descripcion_camiseta = Label(frame_camisetas, text=descripcion, bg='white', font=("Calibri", 11))
                descripcion_camiseta.grid(row=fila + 1, column=columna)
                
                if columna == 0:
                    columna += 1
                    
                elif columna == 1:
                    fila += 2
                    columna = 0
    
        except Exception as e:
            showwarning("Advertencia", f"Error al cargar camisetas relacionadas.\n{e}") 
            
            
    def obtener_talles(self):
        talles = {"XS": self.combo_xs.get(),
                  "S": self.combo_s.get(),
                  "M": self.combo_m.get(),
                  "L": self.combo_l.get(),
                  "XL": self.combo_xl.get(),
                  "XXL": self.combo_xxl.get()
                  } 
                                # comprensión de diccionario, guardando únicamente los talles seleccionados por el usuario
        talles_seleccionados = {talle: cantidad for talle, cantidad in talles.items() if cantidad}    
        return talles_seleccionados
        
             
    def vista_compra(self, imagen_camiseta, id_camiseta, id_cliente, recargar_ventana=False):   # crear la ventana de compra
        self.id_cliente = id_cliente
        datos_camiseta = self.obtener_informacion_camiseta(id_camiseta)
        # obtener el nombre del producto, jugador y color de la camiseta para colocarlos en el título de la ventana
        producto = datos_camiseta[0]
        jugador = datos_camiseta[5]
        color = datos_camiseta[7]
        
        if recargar_ventana:    # al elegir un producto relacionado, se recarga la ventana eliminando los frames actuales reemplazandolos por nuevos
            for widget in self.ventana_compra.winfo_children():
                widget.destroy()
        else:   # crear y mostrar la ventana de compra al elegir una camiseta desde la ventana de inicio. 
            self.ventana_compra = Toplevel()
            self.ventana_compra.title(f"Comprar {producto} {jugador} {color}")
            self.ventana_compra.geometry("1366x768")
            self.ventana_compra.resizable(False, False)
            self.ventana_compra.config(bg='white')
            self.ventana_compra.iconbitmap(icono)
        
        frame_descripcion = self.descripcion_camiseta(id_camiseta, imagen_camiseta) # descripción de la camiseta
        self.boton_favoritos(id_camiseta, id_cliente, frame_descripcion)
        self.talles_camiseta(frame_descripcion, id_camiseta)    # cargar talles de la camiseta
        self.productos_relacionados(id_camiseta)    # cargar camisetas relacionadas


class Comprar:
    def __init__(self):
        pass
    
    def vista_confirmar_compra(self, ventana_compra, id_cliente, id_producto, imagen_producto):
        self.id_cliente = id_cliente
        self.id_producto = id_producto 
        talles = vista_compra.obtener_talles()
        
        if not talles:
            showwarning("Advertencia", "Selecciona un talle.")
            return
        
        frame_descripcion, frame_camisetas = ventana_compra.winfo_children()    # obtener lista de widgets de la ventana (frame_descripcion y frame_camisetas (relacionadas))
        frame_descripcion.pack_forget()
        frame_camisetas.pack_forget()
        
        ventana_compra.title("Confirmar compra")
        
        boton_volver = Button(ventana_compra, image=imagen_atras, bg='white', border=0, command=lambda : self.volver(ventana_compra, frame_descripcion, frame_camisetas))
        boton_volver.place(x=0, y=0)
        
        boton_volver.bind("<Enter>", lambda e: e.widget.config(bg="gray", highlightthickness=2, highlightbackground="blue"))
        boton_volver.bind("<Leave>", lambda e: e.widget.config(bg="white", highlightthickness=0))
        
        self.widgets_confirmar_compra(ventana_compra, talles, imagen_producto)
           
     
    def volver(self, ventana_compra, frame_descripcion, frame_camisetas):
        index = 2   # la ventana_compra, inicialmente tiene 2 widgets (2 frames con descripcion[0] y productos relacionados[1]), todos los widgets que se le colocan en el método 
        lista_widgets = ventana_compra.winfo_children() # vista_confirmar_compra, van a estar posicionados a partir de la posición 2. Entonces borramos a partir de esa posición
        while index < len(lista_widgets):
            lista_widgets[index].destroy()
            index += 1
        
        frame_descripcion.pack(side=LEFT)   # mostrar los frames de la ventana anterior
        frame_camisetas.pack(fill=BOTH, expand=1)
            
    
    def widgets_confirmar_compra(self, ventana_compra, talles, imagen_producto):
        nombre, apellido, telefono, email = self.obtener_informacion_cliente() 
        provincia, localidad, direccion, codigo_postal = self.obtener_direccion_cliente()   
        nombre_producto, marca, version, precio = self.obtener_informacion_producto()
        
        fuente = "Calibri"
        
        label_titulo = Label(ventana_compra, text=f"Confirmar compra - {nombre_producto} {version}", bg='white', font=(fuente, 16))
        label_titulo.pack(pady=10)
        
        label_titulo_resumen = Label(ventana_compra, text=f"Resumen del pedido:", bg='white', font=(fuente, 14))
        label_titulo_resumen.pack(anchor='nw', padx=10, pady=30) 
        # información producto
        label_titulo_producto = Label(ventana_compra, text=f"Información del producto:", bg='white', font=(fuente, 14))
        label_titulo_producto.pack(anchor='nw', padx=10)
        
        label_nombre_producto = Label(ventana_compra, text=f"Producto: {nombre_producto}", bg='white', font=(fuente, 14))
        label_nombre_producto.pack(anchor='nw', padx=10) 
        
        label_marca_producto = Label(ventana_compra, text=f"Marca: {marca}", bg='white', font=(fuente, 14))
        label_marca_producto.pack(anchor='nw', padx=10) 
        
        label_version_producto = Label(ventana_compra, text=f"Versión: {version}", bg='white', font=(fuente, 14))
        label_version_producto.pack(anchor='nw', padx=10) 
        
        
        # información usuario
        label_espacio = Label(ventana_compra, text="", bg='white', font=(fuente, 14))
        label_espacio.pack(anchor='nw', padx=10, pady=2)  
        
        label_info_usuario = Label(ventana_compra, text=f"Información del usuario:", bg='white', font=(fuente, 14))
        label_info_usuario.pack(anchor='nw', padx=10)
        
        label_nombre_usuario = Label(ventana_compra, text=f"Nombre/s: {nombre}", bg='white', font=(fuente, 14))
        label_nombre_usuario.pack(anchor='nw', padx=10)  
        
        label_apellido_usuario = Label(ventana_compra, text=f"Apellido/s: {apellido}", bg='white', font=(fuente, 14))
        label_apellido_usuario.pack(anchor='nw', padx=10)  
        
        label_tel_usuario = Label(ventana_compra, text=f"Número de teléfono: {telefono}", bg='white', font=(fuente, 14))
        label_tel_usuario.pack(anchor='nw', padx=10)  
        
        label_email_usuario = Label(ventana_compra, text=f"Email: {email}", bg='white', font=(fuente, 14))
        label_email_usuario.pack(anchor='nw', padx=10)  
        
        # informacion de compra
        label_espacio2 = Label(ventana_compra, text="", bg='white', font=(fuente, 14))
        label_espacio2.pack(anchor='nw', padx=10, pady=2) 
        
        label_info_compra = Label(ventana_compra, text=f"Información de compra:", bg='white', font=(fuente, 14))
        label_info_compra.pack(anchor='nw', padx=10)
        
        talles_seleccionados = list(talles.keys())
        mostrar_talles = ""
        for talle in talles_seleccionados:
            mostrar_talles += f"{talle} ({talles[talle]}) "
         
        label_talle_compra = Label(ventana_compra, text=f"Talle/s: {mostrar_talles}", bg='white', font=(fuente, 14))
        label_talle_compra.pack(anchor='nw', padx=10)
        
        cantidad = []
        for talle in list(talles.values()):
            cantidad.append(int(talle))
            
        label_cantidad_compra = Label(ventana_compra, text=f"Cantidad: {sum(cantidad)}", bg='white', font=(fuente, 14))
        label_cantidad_compra.pack(anchor='nw', padx=10)
        
        label_precio_unitario = Label(ventana_compra, text=f"Precio unitario: {precio}", bg='white', font=(fuente, 14))
        label_precio_unitario.pack(anchor='nw', padx=10)
        
        label_precio_total = Label(ventana_compra, text=f"Precio total: {precio * sum(cantidad)}", bg='white', font=(fuente, 14))
        label_precio_total.pack(anchor='nw', padx=10)
        
        # frame línea
        frame_linea1 = Frame(ventana_compra, bg='black', width=1, height=760)
        frame_linea1.place(x=360, y=0)
        
        # información de dirección del cliente
        label_info_direccion = Label(ventana_compra, text=f"Información de dirección y envío:", bg='white', font=(fuente, 14))
        label_info_direccion.place(x=500, y=85)
        
        label_provincia = Label(ventana_compra, text=f"Provincia: {provincia}", bg='white', font=(fuente, 14))
        label_provincia.place(x=500, y=115) 
        
        label_localidad = Label(ventana_compra, text=f"Localidad: {localidad}", bg='white', font=(fuente, 14))
        label_localidad.place(x=500, y=145)
        
        label_direccion = Label(ventana_compra, text=f"Dirección: {direccion}", bg='white', font=(fuente, 14))
        label_direccion.place(x=500, y=175)  
        
        label_codigo_postal = Label(ventana_compra, text=f"Código postal: {codigo_postal}", bg='white', font=(fuente, 14))
        label_codigo_postal.place(x=500, y=205) 
        
        # notas del usuario
        label_notas = Label(ventana_compra, text=f"Notas del usuario acerca del envío y dirección:", bg='white', font=(fuente, 14))
        label_notas.place(x=500, y=235)
        
        self.mensaje_inicial = """Notas adicionales para el envío
Por favor, utiliza este espacio para agregar cualquier comentario sobre tu disponibilidad para recibir el pedido, o para especificar una dirección de envío alternativa. Asegúrate de que la información que proporciones sea clara y precisa, ya que cualquier error o ambigüedad podría retrasar o afectar la entrega de tu pedido.
        """
        self.area_notas = Text(ventana_compra, width=50, height=9, bg='white', fg='gray', font=(fuente, 12), wrap='word') 
        self.area_notas.insert("1.0", self.mensaje_inicial)
        self.area_notas.place(x=500, y=280)  
        
        def borrar_mensaje(event):
            if self.area_notas.get("1.0", "end-1c"):   # si el texto es el mensaje inicial
                self.area_notas.delete("1.0", "end") 
                self.area_notas.config(fg='black')
        
        self.area_notas.bind("<FocusIn>", borrar_mensaje)
        
        # tiempo estimado de envío
        tiempo_estimado_envio = self.calcular_tiempo_envío()
        label_tiempo_estimado = Label(ventana_compra, text=f"Tiempo de envío estimado: {tiempo_estimado_envio} días", bg='white', font=(fuente, 14))
        label_tiempo_estimado.place(x=550, y=500) 
        
        label_imagen_envio = Label(ventana_compra, image=imagen_envio, bg="white")
        label_imagen_envio.place(x=500, y=500) 
        
        # terminos y condiciones
        label_terminos = Label(ventana_compra, text=f"Antes de realizar la compra, asegúrate\nde haber leído y entendido los", bg='white', font=("Calibri", 14))
        label_terminos.place(x=500, y=560)
    
        boton_terminos = Button(ventana_compra, text=f"Términos y condiciones", bg='white', font=(fuente, 14), border=0, cursor="hand2",
                                command=lambda : terminos.interfaz_terminos(nombre))
        boton_terminos.place(x=555, y=605)
        
        boton_terminos.bind("<Enter>", lambda e: e.widget.config(font=(fuente, 14, "bold", "underline")))
        boton_terminos.bind("<Leave>", lambda e: e.widget.config(font=(fuente, 14)))
    
        # frame línea
        frame_linea2 = Frame(ventana_compra, bg='black', width=1, height=760)
        frame_linea2.place(x=990, y=0)
    
        # muestra camiseta
        label_camiseta = Label(ventana_compra, image=imagen_producto)
        label_camiseta.place(x=1025, y=70) 
        
        # tarjeta de credito
        label_credito = Label(ventana_compra, text="Tarjeta de débito", bg='white', fg='black', font=(fuente, 12)) 
        label_credito.place(x=1110, y=520)
        
        self.parte1 = Entry(ventana_compra, width=7, font=(fuente, 12), justify='center')
        self.parte1.place(x=1020, y=560) 

        self.parte2 = Entry(ventana_compra, width=7, font=(fuente, 12), justify='center')
        self.parte2.place(x=1100, y=560) 

        self.parte3 = Entry(ventana_compra, width=7, font=(fuente, 12), justify='center')
        self.parte3.place(x=1180, y=560) 

        self.parte4 = Entry(ventana_compra, width=7, font=(fuente, 12), justify='center')
        self.parte4.place(x=1260, y=560) 
        
        label_titular = Label(ventana_compra, text="Titular", bg='white', font=(fuente, 12))
        label_titular.place(x=1000, y=600)
        
        self.titular = Entry(ventana_compra, font=(fuente, 12), justify='center', width=25)
        self.titular.place(x=1000, y=630) 
        
        label_venc = Label(ventana_compra, text="Venc.", bg='white', font=(fuente, 12))
        label_venc.place(x=1220, y=600)
        
        self.venc = Entry(ventana_compra, font=(fuente, 12), width=6, justify='center')
        self.venc.place(x=1220, y=630) 
        
        label_cvv = Label(ventana_compra, text="CVV", bg='white', font=(fuente, 12))
        label_cvv.place(x=1290, y=600)
        
        self.cvv = Entry(ventana_compra, font=(fuente, 12), width=6, justify='center')
        self.cvv.place(x=1290, y=630) 
         
    
        #botón confirmar compra
        boton_comprar = Button(ventana_compra, text=f"Confirmar compra", bg='gray22', fg='white', font=(fuente, 14), cursor="hand2",
                               command=lambda : self.confirmar_compra(talles, ventana_compra))
        boton_comprar.place(x=1100, y=675)
        
        boton_comprar.bind("<Enter>", lambda e: e.widget.config(bg="black", highlightthickness=2, highlightbackground="blue"))
        boton_comprar.bind("<Leave>", lambda e: e.widget.config(bg="gray22", highlightthickness=0))
    
    def obtener_informacion_cliente(self):
        try:
            tabla = coneccion.cursor()
            tabla.execute("SELECT nombre, apellido, num_telefono, email FROM usuarios WHERE id_usuario = ?", (self.id_cliente, ))
            datos_cliente = tabla.fetchone()
            return datos_cliente
        except Exception as e:
            showwarning("Advertencia", f"Error al cargar la información de cliente.\n{e}")
            
    def obtener_direccion_cliente(self):
        try:
            tabla = coneccion.cursor()
            consulta = """
            SELECT provincia, localidad, direccion, codigo_postal FROM ubicacion ubi
            JOIN usuarios us
            ON ubi.id_ubicacion = us.id_ubicacion
            WHERE us.id_usuario = ?
            """
            tabla.execute(consulta, (self.id_cliente, ))
            direccion_cliente = tabla.fetchone()
            return direccion_cliente
        except Exception as e:
            showwarning("Advertencia", f"Error al cargar la dirección de cliente.\n{e}")
            
    def obtener_informacion_producto(self):
        try:
            tabla = coneccion.cursor()
            tabla.execute("SELECT nombre_producto, marca, version, precio FROM productos WHERE id_producto = ?", (self.id_producto, ))
            datos_producto = tabla.fetchone()
            return datos_producto
        except Exception as e:
            showwarning("Advertencia", f"Error al cargar la información de producto.\n{e}")
            
            
    def calcular_tiempo_envío(self):
        regiones = {
                    "NOA": ["Jujuy", "Salta", "Tucumán", "Catamarca", "La Rioja", "Santiago del Estero"],
                    "NEA": ["Misiones", "Corrientes", "Chaco", "Formosa"],
                    "Cuyo": ["San Juan", "Mendoza", "San Luis"],
                    "Pampeana": ["Buenos Aires", "Córdoba", "Entre Ríos", "La Pampa", "Santa Fe"],
                    "Patagónica": ["Río Negro", "Neuquén", "Chubut", "Santa Cruz"]
                }          
        
        dias_estimados = 0
        
        provincia_cliente = self.obtener_direccion_cliente()[0]
        
        if provincia_cliente in regiones["Cuyo"]:
            dias_estimados = 1
        elif provincia_cliente in regiones["Pampeana"]:
            dias_estimados = 3
        elif provincia_cliente in regiones["NOA"]:
            dias_estimados = 4
        elif provincia_cliente in regiones["NEA"]:
            dias_estimados = 7
        elif provincia_cliente in regiones["Patagónica"]:
            dias_estimados = 9
        else:
            dias_estimados = "Error al calcular"
            
        return dias_estimados
        
        
    
    def verificar_vencimiento_tarjeta(self, venc):
        try:
            if len(venc) not in [4, 5]:
                return False
            
            if "/" not in venc:
                return False
                
            mes, annio = venc.split("/")
            if not (mes.isdigit() and annio.isdigit()):
                return False
            mes = int(mes)
            annio = int(annio)
            
            if not (1 <= mes <= 12):
                return False
            
            if annio < 24:
                return False
        except ValueError as e:
            showwarning("Advertencia", "El vencimiento es incorrecto.\nPor favor intenta de nuevo ingresando datos correctos.")
        
        return True
        
            
    def confirmar_compra(self, talles, ventana_compra):
        parte1 = self.parte1.get()
        parte2 = self.parte2.get()
        parte3 = self.parte3.get()
        parte4 = self.parte4.get()
        titular = self.titular.get()
        cvv = self.cvv.get()
        venc = self.venc.get()
        
        if not all ([parte1, parte2, parte3, parte4]):
            showwarning("Advertencia", "Completa todos los campos de tu tarjeta de débito")
            return
        
        for parte in [parte1, parte2, parte3, parte4]:
            if not (parte.isnumeric() and len(parte) == 4):
                showwarning("Advertencia", "Cada parte del número de tarjeta debe tener 4 dígitos numéricos.")
                return
                
        if not titular or titular.isnumeric():
            showwarning("Advertencia", "Ingresa un nombre de titular válido.")
            return
        
        if not (cvv.isnumeric() and 3 <= len(cvv) <= 4):
            showwarning("Advertencia", "El CVV debe ser numérico y tener 3 o 4 dígitos.")
            return
            
        if not (self.verificar_vencimiento_tarjeta(venc)):
            showwarning("Advertencia", "La fecha de vencimiento es inválida. Debe estar en formato MM/AA.")
            return
        
        
        nombre_producto = self.obtener_informacion_producto()[0]     # obtener nombre producto
        confirmar = askyesno("Confirmar", f"¿Deseas comprar {nombre_producto}?\nUna vez lo confirmes, se procesará el pago.")
        
        if confirmar:
            self.procesar_compra(talles) 
            ventana_compra.destroy()
                                        
            
    def procesar_compra(self, talles):                      
        # confirmar y procesar compra
        nombre_producto = self.obtener_informacion_producto()[0] 
        try:
            precio_unitario = self.obtener_informacion_producto()[3]     # obtener precio unitario
            notas_cliente = self.area_notas.get("1.0", "end-1c")         # obtener notas adicionales del cliente
            if notas_cliente == self.mensaje_inicial or not notas_cliente:
                notas_cliente = "El cliente no dio notas ni comentarios adicionales."
                tabla = coneccion.cursor()   
                for talle, cantidad in talles.items():
                    cantidad = int(cantidad)
                    precio_total_talle = precio_unitario * cantidad
                    datos = (self.id_producto, self.id_cliente, precio_unitario, precio_total_talle, talle, cantidad, notas_cliente)
                    tabla.execute("INSERT INTO ventas (id_producto, id_usuario, precio_unitario, precio_total, talle, cantidad, notas) VALUES (?, ?, ?, ?, ?, ?, ?)", datos)
                    tabla.execute("UPDATE stock SET stock_talle = stock_talle - ? WHERE id_producto = ? AND talle = ?", (cantidad, self.id_producto, talle))  
                    coneccion.commit()
                                            
                showinfo("¡Felicitaciones!", f"Compraste {nombre_producto}")
                tabla.execute("SELECT MAX(id_venta) FROM ventas")
                id_compra = tabla.fetchone()[0]
                self.descargar_ticket_pdf(id_compra, talles)   
                    
        except Exception as e:
            showwarning("Advertencia", f"Ocurrió un error al procesar el pago. Contacte al administrador.\n{e}")
            return
            
            
    def descargar_ticket_pdf(self, id_compra, talles):
        confirmar_pdf = askyesno("Ticket PDF", "Gracias por tu compra\n¿Deseas descargar el ticket?")
        if confirmar_pdf:
            nombre, apellido, telefono, email = self.obtener_informacion_cliente() 
            provincia, localidad, direccion, codigo_postal = self.obtener_direccion_cliente()   
            nombre_producto, marca, version, precio = self.obtener_informacion_producto()
            
            talles_seleccionados = list(talles.keys())
            mostrar_talles = ""
            for talle in talles_seleccionados:
                mostrar_talles += f"{talle} ({talles[talle]}) "
                
            cantidad = []
            for talle in list(talles.values()):
                cantidad.append(int(talle))
                
            cantidad = sum(cantidad)
            
            escritorio = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
            archivo_pdf = os.path.join(escritorio, f"ticket_compra_{id_compra}.pdf")
            
            # Crear objeto canvas
            c = canvas.Canvas(archivo_pdf, pagesize=letter)
            c.setTitle(f"Ticket de compra - {id_compra}")
            
            # Titulo
            c.setFont("Helvetica-Bold", 18)
            c.drawString(250, 730, "Ticket de Compra")
            
            # Datos del cliente
            c.setFont("Helvetica-Oblique", 16)
            c.drawString(250, 680, "Datos del cliente")
            c.setFont("Helvetica", 16)
            c.drawString(250, 660, f"Nombre: {nombre}")
            c.drawString(250, 640, f"Apellido: {apellido}")
            c.drawString(250, 620, f"Número de teléfono: {telefono}")
            c.drawString(250, 600, f"Email: {email}") 
            
            # Dirección del cliente
            c.setFont("Helvetica-Oblique", 16)
            c.drawString(250, 550, "Dirección del cliente")
            c.setFont("Helvetica", 16)
            c.drawString(250, 530, f"Provincia: {provincia}")
            c.drawString(250, 510, f"Localidad:  {localidad}")
            c.drawString(250, 490, f"Dirección: {direccion}")
            c.drawString(250, 470, f"Código postal: {codigo_postal}") 
            
            # Información de venta
            c.setFont("Helvetica-Oblique", 16)
            c.drawString(250, 420, "Información de venta")
            c.setFont("Helvetica", 16)
            c.drawString(250, 400, f"Producto: {nombre_producto}")
            c.drawString(250, 380, f"Marca: {marca}")
            c.drawString(250, 360, f"Versión: {version}")
            c.drawString(250, 340, f"Talles: {mostrar_talles}")
            c.drawString(250, 320, f"Cantidad: {cantidad}")
            c.drawString(250, 300, f"Precio Unitario: ${precio}")
            c.drawString(250, 280, f"Total: ${precio * cantidad}")
            c.drawString(250, 260, f"Número de Ticket: {id_compra}")

            c.save()
            showinfo("PDF guardado", "Ya puedes ver el ticket de compra.\nSe guardó en tu escritorio.")
    
    
    
# ---------- Sesión de administrador -----------
class InicioAdmin:
    def ventana_inicio_admin(self, id_admin, username):
        self.id_admin = id_admin
        self.username = username
        nombre = self.obtener_nombre_admin()
        
        inicio_admin = Toplevel() 
        inicio_admin.title(f"Sesión de administrador - {self.username}")
        inicio_admin.geometry("890x300")
        inicio_admin.resizable(False, False)
        inicio_admin.config(bg="gray22")
        inicio_admin.iconbitmap(icono) 
        
        def cerrar():
            inicio_admin.destroy()
            ventana_login.destroy()
        
        inicio_admin.protocol("WM_DELETE_WINDOW", cerrar)
        
        # label bienvenida
        label_bienvenida = Label(inicio_admin, text=f"Hola, {nombre}", bg="gray22", fg="white", font=("Century Gothic", 22))
        label_bienvenida.pack(side='top', pady=15)
        
        # añadir administradores, proveedores y clientes
        boton_anadir = Button(inicio_admin, image=imagen_anadir, text="Añadir", compound="top", bg='gray22', border=0, cursor="hand2", fg="white", font=("Century Gothic", 16),
                              command=lambda : add.interfaz_anadir(inicio_admin))
        boton_anadir.place(x=30, y=100)

        boton_anadir.bind("<Enter>", lambda e: e.widget.config(bg="gray", highlightthickness=2, highlightbackground="blue"))
        boton_anadir.bind("<Leave>", lambda e: e.widget.config(bg="gray22", highlightthickness=0))
        
        # editar administradores y proveedores
        boton_editar = Button(inicio_admin, image=imagen_editar, text="Editar", compound="top", bg='gray22', border=0, cursor="hand2", fg="white", font=("Century Gothic", 16),
                              command=lambda : edit.interfaz_editar(inicio_admin))
        boton_editar.place(x=230, y=100)
        
        boton_editar.bind("<Enter>", lambda e: e.widget.config(bg="gray", highlightthickness=2, highlightbackground="blue"))
        boton_editar.bind("<Leave>", lambda e: e.widget.config(bg="gray22", highlightthickness=0))
        
        # añadir stock
        boton_stock = Button(inicio_admin, image=imagen_stock, text="Añadir stock", compound="top", bg='gray22', border=0, cursor="hand2", fg="white", font=("Century Gothic", 16),
                             command=lambda : add_stock.interfaz_mostrar_proveedores(inicio_admin, id_admin))              
        boton_stock.place(x=430, y=100)
        
        boton_stock.bind("<Enter>", lambda e: e.widget.config(bg="gray", highlightthickness=2, highlightbackground="blue"))
        boton_stock.bind("<Leave>", lambda e: e.widget.config(bg="gray22", highlightthickness=0))
        
        # ver gráficos de estadísticas
        boton_graficos = Button(inicio_admin, image=imagen_graficos, text="Gráficos y estadísticas", compound="top", bg='gray22', border=0, cursor="hand2", fg="white",
                                font=("Century Gothic", 16), command=lambda : graficos.ventana_inicio_graficos(inicio_admin))
        boton_graficos.place(x=630, y=100)
        
        boton_graficos.bind("<Enter>", lambda e: e.widget.config(bg="gray", highlightthickness=2, highlightbackground="blue"))
        boton_graficos.bind("<Leave>", lambda e: e.widget.config(bg="gray22", highlightthickness=0))
        
    
    def obtener_nombre_admin(self):
        tabla = coneccion.cursor()
        tabla.execute("SELECT nombre FROM usuarios WHERE id_usuario = ?", (self.id_admin, ))
        nombre_admin = tabla.fetchone()[0]
        return nombre_admin
    
        
class Anadir:
    def interfaz_anadir(self, ventana_primaria):
        x_pos, y_pos = bloquear_ventanas_duplicadas(ventana_primaria, 400, 200)
        
        anadir = Toplevel(ventana_primaria)
        anadir.title("Añadir")
        anadir.geometry(f"620x300+{x_pos}+{y_pos}")
        anadir.resizable(False, False)
        anadir.config(bg="gray22")
        anadir.iconbitmap(icono)
        
        label_anadir = Label(anadir, text=f"Añadir", bg="gray22", fg="white", font=("Century Gothic", 18))
        label_anadir.pack(side='top', pady=10)
        
        # añadir cliente
        boton_anadir_cliente = Button(anadir, image=imagen_anadir_cliente, bg='gray22', border=0, cursor="hand2",
                                      text="Añadir cliente", fg='white', font=("Century Gothic", 12), compound="top",
                                      command=lambda : self.interfaz_anadir_informacion(anadir, admin=False))
        boton_anadir_cliente.place(x=30, y=100)

        boton_anadir_cliente.bind("<Enter>", lambda e: e.widget.config(bg="gray", highlightbackground="blue"))
        boton_anadir_cliente.bind("<Leave>", lambda e: e.widget.config(bg="gray22", highlightthickness=0))
        # añadir proveedor
        boton_anadir_proveedor = Button(anadir, image=imagen_anadir_proveedor, bg='gray22', border=0, cursor="hand2",
                                      text="Añadir proveedor", fg='white', font=("Century Gothic", 12), compound="top",
                                      command=lambda : self.interfaz_anadir_informacion(anadir, admin=False, proveedor=True))
        boton_anadir_proveedor.place(x=230, y=100)

        boton_anadir_proveedor.bind("<Enter>", lambda e: e.widget.config(bg="gray", highlightbackground="blue"))
        boton_anadir_proveedor.bind("<Leave>", lambda e: e.widget.config(bg="gray22", highlightthickness=0))
        # añadir admin
        boton_anadir_admin = Button(anadir, image=imagen_anadir_admin, bg='gray22', border=0, cursor="hand2",
                                      text="Añadir administrador", fg='white', font=("Century Gothic", 12), compound="top",
                                      command=lambda : self.interfaz_anadir_informacion(anadir, admin=True)) 
        boton_anadir_admin.place(x=430, y=100)
        
        boton_anadir_admin.bind("<Enter>", lambda e: e.widget.config(bg="gray", highlightbackground="blue"))
        boton_anadir_admin.bind("<Leave>", lambda e: e.widget.config(bg="gray22", highlightthickness=0))
        
    def interfaz_anadir_informacion(self, interfaz_primaria, admin=True, proveedor=False): # si admin es true, la interfaz registra un administrador, si es false, registra un cliente
        fondo = 'gray22'
        letra = 'white'
        fuente = ("Century Gothic", 12)
        
        x_pos, y_pos = bloquear_ventanas_duplicadas(interfaz_primaria, 400, 200)
        
        interfaz_primaria.withdraw()
        anadir_informacion = Toplevel(interfaz_primaria)
        anadir_informacion.title("Añadir usuario")
        anadir_informacion.geometry(f"620x300+{x_pos}+{y_pos}")
        anadir_informacion.resizable(False, False)
        anadir_informacion.config(bg="gray22", pady=10)
        anadir_informacion.iconbitmap(icono)
        anadir_informacion.protocol("WM_DELETE_WINDOW", lambda : cerrar(anadir_informacion, interfaz_primaria))
        
        # widgets 
        self.label_titulo = Label(anadir_informacion, text="Añadir usuario", bg=fondo, fg=letra, font=("Century Gothic", 14))
        self.label_titulo.grid(row=0, column=0, pady=10, columnspan=3)
        
        label_nombre = Label(anadir_informacion, text="Nombre:", bg=fondo, fg=letra, font=fuente)
        label_nombre.grid(row=1, column=0, sticky='w')

        self.entry_nombre = Entry(anadir_informacion, width=20, font=fuente)
        self.entry_nombre.grid(row=2, column=0, pady=10, padx=8)

        label_apellido = Label(anadir_informacion, text="Apellido:", bg=fondo, fg=letra, font=fuente)
        label_apellido.grid(row=3, column=0, sticky='w')

        self.entry_apellido = Entry(anadir_informacion, width=20, font=fuente)
        self.entry_apellido.grid(row=4, column=0, pady=10, padx=8)

        label_tel = Label(anadir_informacion, text="Número de teléfono:", bg=fondo, fg=letra, font=fuente)
        label_tel.grid(row=1, column=1, sticky='w', padx=20)

        self.entry_tel = Entry(anadir_informacion, width=20, font=fuente)
        self.entry_tel.grid(row=2, column=1, pady=10, sticky='w', padx=20)
            
        label_email = Label(anadir_informacion, text="Email:", bg=fondo, fg=letra, font=fuente)
        label_email.grid(row=3, column=1, sticky='w', padx=20)

        self.entry_email = Entry(anadir_informacion, width=20, font=fuente)
        self.entry_email.grid(row=4, column=1, pady=10, sticky='w', padx=20)
            
        label_username = Label(anadir_informacion, text="Nombre de usuario:", bg=fondo, fg=letra, font=fuente)
        label_username.grid(row=1, column=2, sticky='w', padx=1)

        self.entry_username = Entry(anadir_informacion, width=20, font=fuente)
        self.entry_username.grid(row=2, column=2, pady=10, sticky='w', padx=1)
            
        label_clave = Label(anadir_informacion, text="Contraseña:", bg=fondo, fg=letra, font=fuente)
        label_clave.grid(row=3, column=2, sticky='w', padx=1)

        self.entry_clave = Entry(anadir_informacion, width=20, font=fuente, show='*')
        self.entry_clave.grid(row=4, column=2, pady=10, sticky='w', padx=1)
        
        # configurar widgets dependiendo de si se está introduciendo información de un administrador, proveedor o cliente
        if admin:   # Administrador
            self.boton_ir = Button(anadir_informacion, text="Añadir administrador", bg=fondo, fg=letra, font=fuente, cursor="hand2",
                              command=lambda : self.anadir_admin(anadir_informacion, interfaz_primaria))
            self.boton_ir.grid(row=5, column=1, pady=15)
            
        elif proveedor: # Proveedor
            self.boton_ir = Button(anadir_informacion, text="Añadir proveedor", bg=fondo, fg=letra, font=fuente, cursor="hand2",
                              command=lambda : self.interfaz_anadir_direccion(anadir_informacion, proveedor=True))
            self.boton_ir.grid(row=5, column=0, pady=15, columnspan=2)
            self.label_titulo.config(text="Añadir proveedor")
            self.label_titulo.grid(row=0, column=0, columnspan=2)
            anadir_informacion.geometry("420x290")
            label_apellido.destroy()
            self.entry_apellido.destroy()
            label_username.destroy()
            entry_username.destroy()
            label_clave.destroy()
            self.entry_clave.destroy()
            
            label_nombre_contacto = Label(anadir_informacion, text="Nombre de contacto:", bg=fondo, fg=letra, font=fuente)
            label_nombre_contacto.grid(row=3, column=0, sticky='w')
            
            self.entry_nombre_contacto = Entry(anadir_informacion, width=20, font=fuente)
            self.entry_nombre_contacto.grid(row=4, column=0, pady=10, padx=8)
            
        else:  # Cliente
            self.boton_ir = Button(anadir_informacion, text="Continuar", bg=fondo, fg=letra, font=fuente, cursor="hand2",
                              command=lambda : self.interfaz_anadir_direccion(anadir_informacion, proveedor=False))
            self.boton_ir.grid(row=5, column=1, pady=15)
            
        self.boton_ir.bind("<Enter>", lambda e: e.widget.config(bg="black", highlightbackground="blue"))
        self.boton_ir.bind("<Leave>", lambda e: e.widget.config(bg=fondo, highlightthickness=0))
              
    
    def comprobar_campos(self, proveedor=False):
        # comprobar campos vacíos y tipos de datos para usuarios y proveedores
        self.nombre = self.entry_nombre.get()
        self.email = self.entry_email.get()
        self.telefono = self.entry_tel.get()
        
        if not proveedor:
            self.apellido = self.entry_apellido.get()
            self.username = self.entry_username.get()
            self.clave = self.entry_clave.get()
        
            if not (self.nombre and self.email and self.telefono and self.apellido and self.username and self.clave):
                showwarning("Advertencia", "Por favor, completa todos los campos.")
                return False
            if len(self.clave) < 6:
                showwarning("Advertencia", "La clave de usuario debe contener al menos 6 caracteres.")
                return False
            
        else:    
            self.nombre_contacto = self.entry_nombre_contacto.get()
            if not (self.nombre and self.email and self.telefono and self.nombre_contacto):
                showwarning("Advertencia", "Por favor, completa todos los campos.")
                return False
            
        if not self.telefono.isnumeric():
            showwarning("Advertencia", "Por favor, utiliza un número de teléfono válido.\nLos números deben ir sin espacios.")
            return False
            
        return True
        
        
    def comprobar_direccion(self, proveedor=False):
        # comprobar campos de ubicación vacíos para clientes y proveedores
        self.provincia = self.combo_provincia.get()
        self.localidad = self.entry_localidad.get()
        self.direccion = self.entry_direccion.get()
        
        if not proveedor:
            self.codigo_postal = self.entry_codigo_postal.get()
            if not (self.provincia and self.localidad and self.direccion and self.codigo_postal):
                showwarning("Advertencia", "Por favor completa los campos de ubicación.") 
                return False
            
        else:
            if not (self.provincia and self.localidad and self.direccion):
                showwarning("Advertencia", "Por favor completa los campos de ubicación.") 
                return False           
            
        return True
    
    
    # lógica para añadir un cliente y su ubicación a la base de datos
    def anadir_cliente(self, ventana_primaria):
        if not self.comprobar_direccion(proveedor=False):
            return
        
        try:
            tabla = coneccion.cursor()
            # insertar cliente
            tabla.execute("INSERT INTO usuarios (nombre, apellido, num_telefono, email, username, password, tipo_usuario) VALUES (?, ?, ?, ?, ?, ?, ?)", self.datos_cliente)
            id_usuario = tabla.lastrowid    # lastrowid devuelve la clave primaria del último registro insertado
            direccion = (id_usuario, self.provincia, self.localidad, self.direccion, self.codigo_postal)
            # insertar dirección
            tabla.execute("INSERT INTO ubicacion (id_usuario, provincia, localidad, direccion, codigo_postal) VALUES (?, ?, ?, ?, ?)", direccion)
            id_ubicacion = tabla.lastrowid
            # insertar id de dirección en el cliente
            tabla.execute("UPDATE usuarios SET id_ubicacion = ? WHERE id_usuario = ?", (id_ubicacion, id_usuario))
            coneccion.commit()
            showinfo("Cliente registrado", f"Registraste al cliente {self.nombre} {self.apellido} correctamente.")
            ventana_primaria.destroy()
        except sqlite3.OperationalError as e:
            coneccion.rollback()
            showwarning("Advertencia", f"Error al registrar cliente.\n{e}")
            return
        except sqlite3.IntegrityError:  # validar que el nombre de usuario no exista ya en la base de datos
            coneccion.rollback()
            showwarning("Advertencia", f"El nombre de usuario '{self.username}' ya existe.\nPor favor elige otro.")
            ventana_primaria.deiconify()
            return
        except Exception as e2:
            coneccion.rollback()
            showwarning("Advertencia", f"Ocurrió un error desconocido al registrar cliente.\n{e2}")
            
    # lógica para añadir un proveedor
    def anadir_proveedor(self, ventana_primaria):
        if not self.comprobar_direccion(proveedor=True):
            return
                          # desempaquetar la tupla con la informacion del proveedor
        datos_proveedor = (*self.datos_proveedor, self.provincia, self.localidad, self.direccion)
        
        try:
            tabla = coneccion.cursor()
            tabla.execute("INSERT INTO proveedores (nombre_proveedor, num_telefono, email, nombre_de_contacto, provincia, localidad, direccion) VALUES (?, ?, ?, ?, ?, ?, ?)", datos_proveedor)
            coneccion.commit()
            showinfo("Proveedor registrado", f"Registraste al proveedor '{datos_proveedor[0]}' correctamente.")
            ventana_primaria.destroy()
        except sqlite3.OperationalError as e:
            showwarning("Advertencia", f"Error al registrar proveedor.\n{e}")
            return
        except Exception as e2:
            showwarning("Advertencia", f"Ocurrió un error desconocido al registrar proveedor.\n{e2}")
    
    # lógica para añadir un administrador
    def anadir_admin(self, ventana_primaria, ventana_anterior):
        if not self.comprobar_campos(proveedor=False):
            return
        
        datos_admin = (self.nombre, self.apellido, self.telefono, self.email, self.username, self.clave, "admin")
        
        try:
            tabla = coneccion.cursor()
            tabla.execute("INSERT INTO usuarios (nombre, apellido, num_telefono, email, username, password, tipo_usuario) VALUES (?, ?, ?, ?, ?, ?, ?)", datos_admin)
            coneccion.commit()
            showinfo("Administrador registrado", f"Registraste al administrador '{self.nombre}' correctamente.")
            cerrar(ventana_primaria, ventana_anterior)
        except sqlite3.OperationalError as e:
            showwarning("Advertencia", f"Error al registrar administrador.\n{e}")
            return
        except Exception as e2:
            showwarning("Advertencia", f"Ocurrió un error desconocido al registrar nuevo administrador.\n{e2}")
        
        
    # interfaz para añadir dirección en caso de proveedores o clientes
    def interfaz_anadir_direccion(self, ventana_primaria, proveedor=False): # si proveedor es False, la interfaz va a ser para añadir un cliente
        if not self.comprobar_campos(proveedor):
            return  
        
        fondo = 'gray22'
        letra = 'white'
        fuente = ("Century Gothic", 12)
         
        x_pos, y_pos = bloquear_ventanas_duplicadas(ventana_primaria, 600, 400)
          
        # ventana y widgets
        ventana_primaria.withdraw()
        
        anadir_direccion = Toplevel(ventana_primaria)
        anadir_direccion.title("Añadir dirección de usuario")
        anadir_direccion.geometry(f"400x300+{x_pos}+{y_pos}")
        anadir_direccion.resizable(False, False)
        anadir_direccion.config(bg="gray22", pady=10)
        anadir_direccion.iconbitmap(icono) 
        anadir_direccion.protocol("WM_DELETE_WINDOW", lambda : cerrar(anadir_direccion, ventana_primaria))
       
        
        label_titulo = Label(anadir_direccion, text="Dirección del cliente", bg=fondo, fg=letra, font=("Century Gothic", 14))
        label_titulo.pack(pady=10)
        
        label_provincia = Label(anadir_direccion, text="Provincia:", bg=fondo, fg=letra, font=fuente)
        label_provincia.pack()

        self.combo_provincia = ttk.Combobox(anadir_direccion, width=20, font=fuente, values=provincias, state='readonly')
        self.combo_provincia.pack()

        label_localidad = Label(anadir_direccion, text="Localidad:", bg=fondo, fg=letra, font=fuente)
        label_localidad.pack()

        self.entry_localidad = Entry(anadir_direccion, width=20, font=fuente)
        self.entry_localidad.pack()

        label_direccion = Label(anadir_direccion, text="Dirección:", bg=fondo, fg=letra, font=fuente)
        label_direccion.pack()

        self.entry_direccion = Entry(anadir_direccion, width=20, font=fuente)
        self.entry_direccion.pack()
        
        # configuar widgets dependiendo de si es un proveedor o cliente
        if not proveedor:
            self.datos_cliente = (self.nombre, self.apellido, self.telefono, self.email, self.username, self.clave, "cliente")
            
            anadir_direccion.geometry("400x350")
            
            label_codigo_postal = Label(anadir_direccion, text="Código postal:", bg=fondo, fg=letra, font=fuente)
            label_codigo_postal.pack()

            self.entry_codigo_postal = Entry(anadir_direccion, width=20, font=fuente)
            self.entry_codigo_postal.pack()
            
            self.boton_guardar = Button(anadir_direccion, text="Registrar cliente", bg=fondo, fg=letra, font=fuente, cursor="hand2", 
                                   command=lambda : self.anadir_cliente(anadir_direccion))
        else:
            label_titulo.config(text="Dirección del proveedor") 
            self.datos_proveedor = (self.nombre, self.telefono, self.email, self.nombre_contacto)
            self.boton_guardar = Button(anadir_direccion, text="Registrar proveedor", bg=fondo, fg=letra, font=fuente, cursor="hand2",
                                   command=lambda : self.anadir_proveedor(anadir_direccion))
        
        
        self.boton_guardar.pack(pady=15)
        self.boton_guardar.bind("<Enter>", lambda e: e.widget.config(bg="black", highlightbackground="blue"))
        self.boton_guardar.bind("<Leave>", lambda e: e.widget.config(bg=fondo, highlightthickness=0))
             
             
                           
class Editar(Anadir):   # heredar de la clase Anadir
    def interfaz_editar(self, ventana_primaria):
        x_pos, y_pos = bloquear_ventanas_duplicadas(ventana_primaria, 500, 250)
                
        editar = Toplevel(ventana_primaria)
        editar.title("Editar")
        editar.geometry(f"620x280+{x_pos}+{y_pos}")
        editar.resizable(False, False)
        editar.config(bg="gray22")
        editar.iconbitmap(icono)
        
        label_editar = Label(editar, text=f"Editar", bg="gray22", fg="white", font=("Century Gothic", 18))
        label_editar.place(x=270, y=15)
        
        # editar admin
        boton_editar_admin = Button(editar, image=imagen_editar_admin, bg='gray22', border=0, cursor="hand2",
                                      text="Editar administrador", fg='white', font=("Century Gothic", 12), compound="top", command=lambda : self.interfaz_mostrar_cargados(editar))
        boton_editar_admin.place(x=230, y=80)

        boton_editar_admin.bind("<Enter>", lambda e: e.widget.config(bg="gray", highlightbackground="blue"))
        boton_editar_admin.bind("<Leave>", lambda e: e.widget.config(bg="gray22", highlightthickness=0))
        # editar proveedor
        boton_editar_proveedor = Button(editar, image=imagen_editar_proveedor, bg='gray22', border=0, cursor="hand2",
                                      text="Editar proveedor", fg='white', font=("Century Gothic", 12), compound="top",
                                      command=lambda : self.interfaz_mostrar_cargados(editar, admin=False))
        boton_editar_proveedor.place(x=30, y=80)

        boton_editar_proveedor.bind("<Enter>", lambda e: e.widget.config(bg="gray", highlightbackground="blue"))
        boton_editar_proveedor.bind("<Leave>", lambda e: e.widget.config(bg="gray22", highlightthickness=0))
        # editar producto
        boton_editar_producto = Button(editar, image=imagen_editar_producto, bg='gray22', border=0, cursor="hand2",
                                      text="Editar producto", fg='white', font=("Century Gothic", 12), compound="top",
                                      command=lambda : self.interfaz_mostrar_productos(editar))  
        boton_editar_producto.place(x=460, y=80)
        
        boton_editar_producto.bind("<Enter>", lambda e: e.widget.config(bg="gray", highlightbackground="blue"))
        boton_editar_producto.bind("<Leave>", lambda e: e.widget.config(bg="gray22", highlightthickness=0))
        
    # Interfaz para mostrar los administradores o proveedores registrados en la base de datos
    def interfaz_mostrar_cargados(self, ventana_primaria, admin=True):
        x_pos, y_pos = bloquear_ventanas_duplicadas(ventana_primaria, 500, 200) 
        
        # ventana y widgets
        ventana_primaria.withdraw()
        mostrar_cargados = Toplevel(ventana_primaria)
        mostrar_cargados.title("Registrados")
        mostrar_cargados.geometry(f"350x250+{x_pos}+{y_pos}")
        mostrar_cargados.resizable(False, False)
        mostrar_cargados.config(bg="gray22")
        mostrar_cargados.iconbitmap(icono)
        mostrar_cargados.protocol("WM_DELETE_WINDOW", lambda : cerrar(mostrar_cargados, ventana_primaria))
          
        label_mostrar = Label(mostrar_cargados, text="Administradores registrados", bg="gray22", fg='white', font=("Century Gothic", 12))
        label_mostrar.pack(pady=10)
        
        registrados = self.obtener_registrados(admin)
        combo_registrados = ttk.Combobox(mostrar_cargados, font=("Calibri", 12), values=registrados ,state='readonly')
        combo_registrados.pack()
        
        boton_modificar = Button(mostrar_cargados, text="Modificar", bg="gray22", fg="white", font=("Century Gothic", 12), cursor="hand2",
                                 command=lambda : self.interfaz_editar_admin(combo_registrados.get(), mostrar_cargados))
        boton_modificar.pack(pady=15)
        
        boton_modificar.bind("<Enter>", lambda e: e.widget.config(bg="black", highlightbackground="blue"))
        boton_modificar.bind("<Leave>", lambda e: e.widget.config(bg="gray22", highlightthickness=0))
        
        boton_eliminar = Button(mostrar_cargados, text="Eliminar", bg="gray22", fg="white", font=("Century Gothic", 12), cursor="hand2",
                                command=lambda : self.eliminar_admin(combo_registrados.get(), mostrar_cargados))
        boton_eliminar.pack(pady=15)
        
        boton_eliminar.bind("<Enter>", lambda e: e.widget.config(bg="black", highlightbackground="blue"))
        boton_eliminar.bind("<Leave>", lambda e: e.widget.config(bg="gray22", highlightthickness=0))
        
        if not admin:
            label_mostrar.config(text="Proveedores registrados")
            boton_modificar.config(command=lambda : self.interfaz_editar_proveedor(combo_registrados.get(), mostrar_cargados))
            boton_eliminar.config(command=self.eliminar_proveedor)
            
    # Eliminar proveedor por ID
    def eliminar_proveedor(self):
        id_proveedor = simpledialog.askinteger("Eliminar proveedor", "Ingresa el ID del proveedor que deseas eliminar")
        if id_proveedor:
            confirmar = askyesno("Eliminar proveedor", "¿Estás seguro que deseas eliminar este proveedor?")
            if confirmar:
                try:
                    tabla = coneccion.cursor()
                    tabla.execute("DELETE FROM proveedores WHERE id_proveedor = ?", (id_proveedor, ))
                    coneccion.commit()
                    showinfo("Proveedor eliminado", f"El proveedor con el ID {id_proveedor} ha sido eliminado.")
                except sqlite3.IntegrityError:
                    showwarning("Advertencia", "El stock contiene productos de este proveedor.\nNo se puede eliminar.")
                except sqlite3.OperationalError as e:
                    showwarning("Advertencia", f"Error en la base de datos al eliminar proveedor.{e}")
                except Exception as e2:
                    showwarning("Advertencia", "Error desconocido al eliminar proveedor.")

    # Eliminar administrador por username
    def eliminar_admin(self, username, ventana):
        if not username:
            showwarning("Advertencia", "Selecciona un administrador.")
            return
        confirmar = askyesno("Confirmar", "¿Estás seguro que deseas eliminar a este usuario?")
        if confirmar:
            try:
                tabla = coneccion.cursor()
                tabla.execute("DELETE FROM usuarios WHERE username = ?", (username, ))
                coneccion.commit()
                showinfo("Administrador eliminado", f"Eliminaste al administrador {username}")
                ventana.destroy()
            except sqlite3.OperationalError as e:
                showwarning("Advertencia", f"Error en la base de datos al eliminar administrador.\n{e}")
            except Exception as e2:
                showwarning("Advertencia", f"Error desconocido al eliminar administrador.\n{e2}")
        
    
    # Obtener los administradores o proveedores registrados       
    def obtener_registrados(self, admin=True):
        try:
            tabla = coneccion.cursor()
            if admin:
                tabla.execute('SELECT username FROM usuarios WHERE tipo_usuario = "admin"')
            else:
                tabla.execute('SELECT nombre_proveedor FROM proveedores') 
                
            tuplas_registrados = tabla.fetchall()
            registrados = []
                
            for registrado in tuplas_registrados:
                registrados.append(registrado[0])
                
            return registrados 
        
        except sqlite3.OperationalError as e:
            showwarning("Advertencia", f"Error en la base de datos al cargar administradores.\n{e}")
        except Exception as e2:
            showwarning("Advertencia", f"Error desconocido al cargar administradores.\n{e2}")
        
            
    # Interfaz para modificar la información de los administradores
    def interfaz_editar_admin(self, username_admin, ventana_primaria):
        if not username_admin:
            showwarning("Advertencia", "Selecciona un administrador para modificar.")
            return
        
        ventana_primaria.withdraw()
        super().interfaz_anadir_informacion(ventana_primaria, admin=True, proveedor=False)  # Reutilizar la ventana de la clase Anadir con herencia
        self.label_titulo.config(text="Editar información de administrador")
        self.boton_ir.config(command=lambda : self.editar_admin(ventana_primaria))
        
        # Buscar información cargada en la base de datos
        try:
            tabla = coneccion.cursor()
            tabla.execute("SELECT nombre, apellido, num_telefono, email, username, password FROM usuarios WHERE username = ?", (username_admin, )) 
            datos_admin = tabla.fetchall()
        except sqlite3.OperationalError as e:
            showwarning("Advertencia", f"Error en la base de datos al cargar administradores.\n{e}")
        except Exception as e2:
            showwarning("Advertencia", f"Error desconocido al cargar administradores.\n{e2}")
            
        # Llenar los campos de texto con la información cargada en la base de datos    
        self.entry_nombre.insert(0, datos_admin[0][0])
        self.entry_apellido.insert(0, datos_admin[0][1])
        self.entry_tel.insert(0, datos_admin[0][2])
        self.entry_email.insert(0, datos_admin[0][3])
        self.entry_username.insert(0, datos_admin[0][4])
        self.entry_clave.insert(0, datos_admin[0][5])
        
    # lógica para editar la información de administradores     
    def editar_admin(self, ventana_primaria):
        if super().comprobar_campos(proveedor=False):
            datos_actualizar = (self.nombre, self.apellido, self.telefono, self.email, self.username, self.clave, self.username)
            try:
                tabla = coneccion.cursor()
                tabla.execute("UPDATE usuarios SET nombre = ?, apellido = ?, num_telefono = ?, email = ?, username = ?, password = ? WHERE username = ?", datos_actualizar)
                coneccion.commit()
                showinfo("Información actualizada", "La información del usuario se actualizó correctamente.") 
                ventana_primaria.destroy()
            except sqlite3.OperationalError as e:
                showwarning("Advertencia", f"Error en la base de datos al cargar administradores.\n{e}")
            except sqlite3.IntegrityError:
                showwarning("Advertencia", f"El nombre de usuario elegido ya existe.\nPor favor elige otro.")
            except Exception as e2:
                showwarning("Advertencia", f"Error desconocido al cargar administradores.\n{e2}")
        else:
            showwarning("Advertencia", f"Completa todos los campos.")
        
    # Interfaz para editar la información principal del proveedor
    def interfaz_editar_proveedor(self, nombre_proveedor, ventana_primaria):
        if not nombre_proveedor:
            showwarning("Advertencia", "Selecciona un proveedor.")
            return 

        ventana_primaria.withdraw()
        super().interfaz_anadir_informacion(ventana_primaria, admin=False, proveedor=True)
        self.label_titulo.config(text="Editar información de proveedor")
        self.boton_ir.config(command=lambda : self.mostrar_ventana_direccion(nombre_proveedor, ventana_primaria))
        
        # Buscar información cargada del proveedor en la base de datos
        try:
            tabla = coneccion.cursor()
            tabla.execute("SELECT nombre_proveedor, num_telefono, email, nombre_de_contacto FROM proveedores WHERE nombre_proveedor = ?", (nombre_proveedor, )) 
            datos_proveedor = tabla.fetchall()
        except sqlite3.OperationalError as e:
            showwarning("Advertencia", f"Error en la base de datos al cargar la información del proveedor.\n{e}")
        except Exception as e2:
            showwarning("Advertencia", f"Error desconocido al cargar la información del proveedor.\n{e2}")

        # Colocar la información en los entry
        self.entry_nombre.insert(0, datos_proveedor[0][0])
        self.entry_tel.insert(0, datos_proveedor[0][1])
        self.entry_email.insert(0, datos_proveedor[0][2])
        self.entry_nombre_contacto.insert(0, datos_proveedor[0][3]) 
        
    # Abrir la ventana para editar la dirección del proveedor si los campos de su información principal están todos completos
    def mostrar_ventana_direccion(self, nombre_proveedor, ventana_primaria):
        if self.comprobar_campos(proveedor=True):
            self.interfaz_anadir_direccion(ventana_primaria, proveedor=True)
            self.boton_guardar.config(command=lambda : self.editar_proveedor(ventana_primaria))
            
            # Buscar información de ubicación del proveedor en la base de datos
            try:
                tabla = coneccion.cursor()
                tabla.execute("SELECT provincia, localidad, direccion FROM proveedores WHERE nombre_proveedor = ?", (nombre_proveedor, )) 
                direccion_proveedor = tabla.fetchall()
                
            except sqlite3.OperationalError as e:
                showwarning("Advertencia", f"Error en la base de datos al cargar la información del proveedor.\n{e}")
            except Exception as e2:
                showwarning("Advertencia", f"Error desconocido al cargar la información del proveedor.\n{e2}")
            
            # insertar dirección actual del proveedor
            self.combo_provincia.config(state='normal')
            self.combo_provincia.insert(0, direccion_proveedor[0][0])
            self.combo_provincia.config(state='readonly')
            self.entry_localidad.insert(0, direccion_proveedor[0][1]) 
            self.entry_direccion.insert(0, direccion_proveedor[0][2]) 
            
        else:
            showwarning("Advertencia", "Completa todos los campos.")
         
    # lógica para editar la información del proveedor
    def editar_proveedor(self, ventana_primaria):
        if self.comprobar_direccion(proveedor=True):
            datos_proveedor = (*self.datos_proveedor, self.provincia, self.localidad, self.direccion, self.datos_proveedor[0])
            try:
                tabla = coneccion.cursor()
                tabla.execute("UPDATE proveedores SET nombre_proveedor = ?, num_telefono = ? , email = ?, nombre_de_contacto = ?, provincia = ?, localidad = ?, direccion = ? WHERE nombre_proveedor = ?", datos_proveedor)
                coneccion.commit()
                showinfo("Información actualizada", "La información del proveedor se actualizó correctamente.") 
                ventana_primaria.destroy()
            except sqlite3.OperationalError as e:
                showwarning("Advertencia", f"Error en la base de datos al modificar proveedor.\n{e}")
            except Exception as e2:
                showwarning("Advertencia", f"Error desconocido al modificar proveedor.\n{e2}")
                
    
    # ------- modificar productos -------
    
    def obtener_informacion_productos(self, ordenar_id=False):
    # crear un diccionario con el id de clave y la descripción de valor
        try:
            tabla = coneccion.cursor()
            if not ordenar_id:
                tabla.execute("SELECT id_producto, nombre_producto, jugador, color FROM productos ORDER BY nombre_producto ASC")
            else:
                tabla.execute("SELECT id_producto, nombre_producto, jugador, color FROM productos ORDER BY id_producto ASC")
         
            datos_camiseta = tabla.fetchall()
            
            camisetas = {}
            
            for camiseta in datos_camiseta:
                descripcion = f"{camiseta[0]} - {camiseta[1]} {camiseta[2]} {camiseta[3]}"
                camisetas.update({camiseta[0]: descripcion}) 
                
            return camisetas
                    
        except sqlite3.OperationalError as e:
            showwarning("Advertencia", f"Error al cargar información de productos.\n{e}")
        except Exception as e2:
            showwarning("Advertencia", f"Error desconocido al cargar información de productos.\n{e2}")
            
    # interafaz para mostrar los productos cargados en la base de datos        
    def interfaz_mostrar_productos(self, ventana_primaria):
        x_pos, y_pos = bloquear_ventanas_duplicadas(ventana_primaria, 500, 200)
        
        ventana_primaria.withdraw()
        mostrar_productos = Toplevel(ventana_primaria)
        mostrar_productos.title("Productos registrados")
        mostrar_productos.geometry(f"+{x_pos}+{y_pos}")
        mostrar_productos.resizable(False, False)
        mostrar_productos.config(bg="gray22")
        mostrar_productos.iconbitmap(icono)
        mostrar_productos.protocol("WM_DELETE_WINDOW", lambda : cerrar(mostrar_productos, ventana_primaria))
          
        label_mostrar = Label(mostrar_productos, text="Productos registrados", bg="gray22", fg='white', font=("Century Gothic", 12))
        label_mostrar.pack(pady=10)
        
        self.camisetas = self.obtener_informacion_productos(ordenar_id=True)    # obtener un diccionario con el id y la descripción de los productos
        # combobox con las descripciones para identificar cada producto
        self.combo_descripciones = ttk.Combobox(mostrar_productos, font=("Calibri", 12), width=55, values=list(self.camisetas.values()), justify='center')
        try:
            self.combo_descripciones.insert(0, list(self.camisetas.values())[0])
        except IndexError:  # mostrar esta advertencia si aun no hay ningún registro
            showwarning("Advertencia", "Aún no hay registros.")
            mostrar_productos.destroy()
            return
        
        self.combo_descripciones.config(state="readonly")
        self.combo_descripciones.pack(pady=10)
        
        
        self.boton_modificar = Button(mostrar_productos, text="Modificar", bg="gray22", fg="white", font=("Century Gothic", 12), cursor="hand2",
                                 command=lambda : self.interfaz_editar_producto(mostrar_productos, self.combo_descripciones.get()))
        self.boton_modificar.pack(pady=15)
        
        self.boton_modificar.bind("<Enter>", lambda e: e.widget.config(bg="black", highlightbackground="blue"))
        self.boton_modificar.bind("<Leave>", lambda e: e.widget.config(bg="gray22", highlightthickness=0))
        
        self.label_ordenar = Label(mostrar_productos, text="Ordenar por:", bg="gray22", fg='white', font=("Century Gothic", 12))
        self.label_ordenar.pack(pady=10)
        
        # ordenar combobox por el id del producto o por orden alfabético
        self.ordenes = ["Orden alfábetico", "ID camiseta"]
        
        self.combo_ordenar = ttk.Combobox(mostrar_productos, font=("Calibri", 12), width=25, values=self.ordenes, justify='center',)
        self.combo_ordenar.insert(0, self.ordenes[1])
        self.combo_ordenar.config(state="readonly")
        self.combo_ordenar.pack(pady=10)
        
        self.boton_ordenar = Button(mostrar_productos, text="Ordenar", bg="gray22", fg="white", font=("Century Gothic", 12), cursor="hand2",
                               command=lambda : self.ordenar_camisetas(self.combo_ordenar.get()))
        self.boton_ordenar.pack(pady=15)
        
        self.boton_ordenar.bind("<Enter>", lambda e: e.widget.config(bg="black", highlightbackground="blue"))
        self.boton_ordenar.bind("<Leave>", lambda e: e.widget.config(bg="gray22", highlightthickness=0))
          
    # lógica para ordenar el combobox de los productos    
    def ordenar_camisetas(self, orden):
        if orden == self.ordenes[0]:
            self.camisetas = self.obtener_informacion_productos(ordenar_id=False)
        elif orden == self.ordenes[1]: 
            self.camisetas = self.obtener_informacion_productos(ordenar_id=True)
            
        self.combo_descripciones.config(values=list(self.camisetas.values()))
        
    # este método valida que el usuario haya seleccionado un producto, y si es así, devuelve los datos de dicho producto
    def validar_producto(self, descripcion_producto):
        if not descripcion_producto:
            showwarning("Advertencia", "Selecciona un producto.")
            return
        
        if descripcion_producto in self.camisetas.values():
            id_producto = 0
           
            for id in self.camisetas:
               if self.camisetas[id] == descripcion_producto:
                   id_producto = id
                   
            if not id_producto:
                showwarning("Advertencia", "Producto no encontrado.")
                return
                   
            try:
                tabla = coneccion.cursor()
                consulta = '''
                    SELECT id_producto, nombre_producto, precio, nombre_proveedor, marca, equipo, temporada, jugador, version, color, descripcion FROM productos c
                    JOIN proveedores p
                    ON c.id_proveedor = p.id_proveedor
                    WHERE id_producto = ? 
                '''
                tabla.execute(consulta, (id_producto, ))
                datos_camiseta = tabla.fetchall()
                return datos_camiseta
            except sqlite3.OperationalError as e:
                showwarning("Advertencia", f"Error al cargar información de productos.\n{e}")
            except Exception as e2:
                showwarning("Advertencia", f"Error desconocido al cargar información de productos.\n{e2}")

        else:
            showwarning("Advertencia", "El producto no se encuentra en la lista de camisetas.")
            return
        
    # interfaz para editar el precio y descripción del producto
    def interfaz_editar_producto(self, ventana_primaria, descripcion_producto):
        x_pos, y_pos = bloquear_ventanas_duplicadas(ventana_primaria)
        
        # crear ventana
        ventana_primaria.withdraw()
        self.i_editar_producto = Toplevel(ventana_primaria)
        self.i_editar_producto.title("Productos registrados")
        self.i_editar_producto.geometry(f"+{x_pos}+{y_pos}")
        self.i_editar_producto.resizable(False, False)
        self.i_editar_producto.config(bg="gray22")
        self.i_editar_producto.iconbitmap(icono)
        self.i_editar_producto.protocol("WM_DELETE_WINDOW", lambda : cerrar(self.i_editar_producto, ventana_primaria))
        
        # guardar los datos que retorna el método validar_producto
        datos_camiseta = self.validar_producto(descripcion_producto)[0]
        id, producto, precio, proveedor, marca, equipo, temporada, jugador, version, color, descripcion = datos_camiseta
        
        # llamar al método de la clase CargarCamisetas para cargar la imagen del producto seleccionado
        consulta_sql = f"SELECT imagen, nombre_producto, jugador, precio, id_producto FROM productos WHERE id_producto = ?"
        parametro_sql = (id, )
        imagen_camiseta = cargar_camisetas.cargar_camisetas(consulta_sql, parametro_sql)[0][0] # guardar la imagen de la camiseta contenida en la lista de tuplas
    
        label_imagen = Label(self.i_editar_producto, image=imagen_camiseta)
        label_imagen.grid(row=0, column=0, padx=10, pady=10)
        
        self.boton_modificar_producto = Button(self.i_editar_producto, text="Modificar", bg="gray22", fg="white", font=("Century Gothic", 12), cursor="hand2",
                                 command=lambda : self.editar_producto(id, ventana_primaria))
        self.boton_modificar_producto.grid(row=1, column=0, padx=10, pady=10, sticky='n') 
        
        self.boton_modificar_producto.bind("<Enter>", lambda e: e.widget.config(bg="black", highlightbackground="blue"))
        self.boton_modificar_producto.bind("<Leave>", lambda e: e.widget.config(bg="gray22", highlightthickness=0))
        
        # frame con toda la informacion del producto
        self.frame_informacion = Frame(self.i_editar_producto, bg="gray22") 
        self.frame_informacion.grid(row=0, column=1, padx=50, sticky='n') 
        
        label_precio = Label(self.frame_informacion, text="Precio", bg="gray22", fg='white', font=("Century Gothic", 12))
        label_precio.grid(row=0, column=0, sticky='w', padx=50)
        
        self.entry_precio = Entry(self.frame_informacion, width=20, font=("Century Gothic", 12))
        self.entry_precio.insert(0, precio)
        self.entry_precio.grid(row=1, column=0, sticky='w', padx=50, pady=5) 

        label_informacion = Label(self.frame_informacion, text="Información del producto", bg="gray22", fg='white', font=("Century Gothic", 12))
        label_informacion.grid(row=2, column=0, sticky='w', padx=50)

        listbox_informacion = Listbox(self.frame_informacion, bg="gray22", fg="white", font=("Century Gothic", 12), width=50) 
        listbox_informacion.grid(row=3, column=0, sticky='w', padx=50, pady=10)
        
        # insertar información actual
        listbox_informacion.insert(0, f"Producto: {producto}") 
        listbox_informacion.insert(1, f"Distribuido por: {proveedor}")
        listbox_informacion.insert(2, f"Marca: {marca}")
        listbox_informacion.insert(3, f"Versión: {version}")
        listbox_informacion.insert(4, f"Equipo: {equipo}")
        listbox_informacion.insert(5, f"Temporada: {temporada}")
        listbox_informacion.insert(6, f"Jugador: {jugador}")
        listbox_informacion.insert(7, f"Color: {color}")
        
        listbox_informacion.config(state="disabled")
        
        self.label_descripcion = Label(self.frame_informacion, text="Descripción del producto", bg="gray22", fg='white', font=("Century Gothic", 12))
        self.label_descripcion.grid(row=4, column=0, sticky='w', padx=50)
        
        self.area_descripcion = Text(self.frame_informacion, bg="gray22", fg="white", font=("Century Gothic", 12), width=50, height=10, wrap='word') 
        self.area_descripcion.grid(row=5, column=0, sticky='w', padx=50) 
        self.area_descripcion.insert("1.0", descripcion)
    
    # lógica para editar producto
    def editar_producto(self, id_producto, ventana_primaria):
        precio = self.entry_precio.get()
        descripcion = self.area_descripcion.get("1.0", "end-1c")
        
        if not (precio and descripcion):
            showwarning("Advertencia", "Debes establecer un precio y una descripción.")
            return
        
        try:
            precio = float(precio)
        except ValueError:
            showwarning("Advertencia", "Escribe un precio válido.")
            return
        
        confirmar = askyesno("Modificar producto", "¿Estás seguro que deseas modificar este producto?")
        if confirmar:
            try:
                datos_actualizar = (precio, descripcion, id_producto)
                tabla = coneccion.cursor()
                tabla.execute("UPDATE productos SET precio = ?, descripcion = ? WHERE id_producto = ?", datos_actualizar)
                coneccion.commit()
                showinfo("Producto modificado", f"Modificaste el producto correctamente.\nEl nuevo precio es: ${precio}")
                ventana_primaria.destroy()
            except sqlite3.OperationalError as e:
                showwarning("Advertencia", f"Error en la base de datos al modificar producto.\n{e}")
            except Exception as e2:
                showwarning("Advertencia", f"Error desconocido al modificar producto.\n{e2}")
            
            

class AnadirStock(Editar):  # heredar de la clase Editar
    def interfaz_mostrar_proveedores(self, ventana_primaria, id_admin):
        x_pos, y_pos = bloquear_ventanas_duplicadas(ventana_primaria)
            
        self.id_admin = id_admin    # obtener el id del administrador en la sesión actual
        
        # ventana y widgets
        mostrar_proveedores = Toplevel(ventana_primaria)
        mostrar_proveedores.title("Proveedores registrados")
        mostrar_proveedores.geometry(f"350x180+{x_pos}+{y_pos}")
        mostrar_proveedores.resizable(False, False)
        mostrar_proveedores.config(bg="gray22")
        mostrar_proveedores.iconbitmap(icono)
        
        label_proveedor = Label(mostrar_proveedores, text="Selecciona un proveedor:", bg="gray22", fg='white', font=("Century Gothic", 12))
        label_proveedor.pack(pady=10)
        
        self.proveedores = self.obtener_proveedores()
        self.combo_proveedores = ttk.Combobox(mostrar_proveedores, width=20, font=("Calibri", 12), justify='center', values=list(self.proveedores.values()))
        self.combo_proveedores.insert(0, list(self.proveedores.values())[0]) 
        self.combo_proveedores.config(state='readonly')
        self.combo_proveedores.pack(pady=10)
        
        
        boton_seleccionar = Button(mostrar_proveedores, text="Seleccionar", fg="white", bg="gray22", font=("Century Gothic", 12), cursor="hand2",
                                   command=lambda : self.interfaz_productos_proveedores(mostrar_proveedores)) 
        boton_seleccionar.pack(pady=10)
        
        boton_seleccionar.bind("<Enter>", lambda e: e.widget.config(bg="black", highlightbackground="blue"))
        boton_seleccionar.bind("<Leave>", lambda e: e.widget.config(bg="gray22", highlightthickness=0))
        
    # validar si el usuario seleccionó un proveedor, retorna el id del proveedor seleccionado
    def validar_proveedor(self):
        proveedor = self.combo_proveedores.get()
        if not proveedor:
            showwarning("Advertencia", "Selecciona un proveedor.")
            return
        
        id = 0
        if proveedor in self.proveedores.values():
            for id_proveedor in self.proveedores:
                if self.proveedores[id_proveedor] == proveedor:
                    id = id_proveedor
                    return id 
        
    # obtener todos los proveedores registrados en la base de datos
    def obtener_proveedores(self):
        try:
            tabla = coneccion.cursor()
            tabla.execute("SELECT id_proveedor, nombre_proveedor FROM proveedores")
            tuplas_proveedores = tabla.fetchall()
            proveedores = {}
            for proveedor in tuplas_proveedores:
                proveedores.update({proveedor[0]: f"{proveedor[0]} - {proveedor[1]}"})  
            return proveedores
        except sqlite3.OperationalError as e:
            showwarning("Advertencia", f"Error al cargar proveedores.\n{e}")
        except Exception as e2:
            showwarning("Advertencia", f"Error desconocido al cargar proveedores.\n{e2}")
      
    # obtener información de los productos para crear una descrpción
    def obtener_informacion_productos(self, ordenar_id=False):
        try:
            tabla = coneccion.cursor()
            if not ordenar_id:  # consulta por defecto, si el usuario elige filtrar por orden alfabético
                consulta = '''
                SELECT pp.id_producto, pp.nombre_producto, pp.jugador, pp.color FROM productos p
                JOIN productos_proveedores pp
                ON p.id_producto = pp.id_producto 
                WHERE id_proveedor = ?
                ORDER BY pp.nombre_producto ASC
                '''
            else:   # consulta para filtrar por id
                consulta = '''
                SELECT pp.id_producto, pp.nombre_producto, pp.jugador, pp.color FROM productos p
                JOIN productos_proveedores pp
                ON p.id_producto = pp.id_producto 
                WHERE id_proveedor = ?
                ORDER BY pp.id_producto ASC
                '''
            tabla.execute(consulta, (self.id_proveedor, ))
            datos_camiseta = tabla.fetchall()
            
            # crear un dicionario con el id de las camisetas como clave y su descripción como valor
            camisetas = {}
        
            for camiseta in datos_camiseta:
                descripcion = f"{camiseta[0]} - {camiseta[1]} {camiseta[2]} {camiseta[3]}"  # ejemplo: "11 - Camiseta Minnesota Timberwolves Anthony Edwards Azul"
                camisetas.update({camiseta[0]: descripcion}) 
                
            return camisetas
                    
        except sqlite3.OperationalError as e:
            showwarning("Advertencia", f"Error al cargar información de productos.\n{e}")
        except Exception as e2:
            showwarning("Advertencia", f"Error desconocido al cargar información de productos.\n{e2}")
            
    # utilizar el método de la clase padre para mostrar los productos en un combobox, según el proveedor seleccionado
    def interfaz_productos_proveedores(self, ventana_primaria):
        try:
            self.id_proveedor = self.validar_proveedor()        # obtener id del proveedor
            ventana_primaria.withdraw()                         # ocultar la ventana anterior
            self.interfaz_mostrar_productos(ventana_primaria)   # mostrar la ventana nueva
            # configurar la funcionalidad del botón
            self.boton_modificar.config(text="Confirmar", command=lambda : self.interfaz_anadir_producto(self.combo_descripciones.get(), ventana_primaria))
        # si el proveedor no tiene productos registrados, usamos esta excepción
        except AttributeError:
            showwarning("Error", "No hay registros.")
            return
            
    # interfaz para añadir stock a un producto
    def interfaz_anadir_producto(self, descripcion_producto, ventana_primaria):
        ventana_primaria.withdraw()
        # heredar de la interfaz para editar productos
        self.interfaz_editar_producto(ventana_primaria, descripcion_producto)
        
        
        # modificar los widgets de esta interfaz heredada
        self.area_descripcion.destroy()
        self.label_descripcion.destroy()
        self.boton_modificar_producto.config(text="Añadir", command=lambda : self.anadir_talles(self.i_editar_producto))
        self.frame_talles = Frame(self.i_editar_producto, bg="gray22")
        self.frame_talles.place(x=420, y=340)
        
        self.precio = self.obtener_precio_producto(descripcion_producto)    # obtener precio del producto
        self.entry_precio.delete(0, END)
        self.entry_precio.insert(0, self.precio)
        self.entry_precio.config(state = 'disabled')
        
        # talles   
        cantidades = [1, 2, 3, 4, 5] 
        # XS
        label_xs = Label(self.frame_talles, text="XS", bg='gray22', fg="white", font=("Century Gothic", 14))
        label_xs.grid(row=0, column=0, padx=5, pady=10, sticky='w') 
        
        self.combo_xs = ttk.Combobox(self.frame_talles, width=1, font=("Century Gothic", 14), state='readonly', values=cantidades)    
        self.combo_xs.grid(row=1, column=0, padx=5, pady=10, sticky='w') 
        # S
        label_s = Label(self.frame_talles, text="S", bg='gray22', fg="white", font=("Century Gothic", 14))
        label_s.grid(row=0, column=1, padx=5, pady=10, sticky='w') 
        
        self.combo_s = ttk.Combobox(self.frame_talles, width=1, font=("Century Gothic", 14), state='readonly', values=cantidades)    
        self.combo_s.grid(row=1, column=1, padx=5, pady=10, sticky='w') 
        # M
        label_m = Label(self.frame_talles, text="M", bg='gray22', fg="white", font=("Century Gothic", 14))
        label_m.grid(row=0, column=2, padx=5, pady=10, sticky='w') 
        
        self.combo_m = ttk.Combobox(self.frame_talles, width=1, font=("Century Gothic", 14), state='readonly', values=cantidades)    
        self.combo_m.grid(row=1, column=2, padx=5, pady=10, sticky='w') 
        # L
        label_l = Label(self.frame_talles, text="L", bg='gray22', fg="white", font=("Century Gothic", 14))
        label_l.grid(row=0, column=3, padx=5, pady=10, sticky='w') 
        
        self.combo_l = ttk.Combobox(self.frame_talles, width=1, font=("Century Gothic", 14), state='readonly', values=cantidades)    
        self.combo_l.grid(row=1, column=3, padx=5, pady=10, sticky='w') 
        # XL
        label_xl = Label(self.frame_talles, text="XL", bg='gray22', fg="white", font=("Century Gothic", 14))
        label_xl.grid(row=0, column=4, padx=5, pady=10, sticky='w') 
        
        self.combo_xl = ttk.Combobox(self.frame_talles, width=1, font=("Century Gothic", 14), state='readonly', values=cantidades)    
        self.combo_xl.grid(row=1, column=4, padx=5, pady=10, sticky='w') 
        # XXL
        label_xxl = Label(self.frame_talles, text="XXL", bg='gray22', fg="white", font=("Century Gothic", 14))
        label_xxl.grid(row=0, column=5, padx=5, pady=10, sticky='w') 
        
        self.combo_xxl = ttk.Combobox(self.frame_talles, width=1, font=("Century Gothic", 14), state='readonly', values=cantidades)    
        self.combo_xxl.grid(row=1, column=5, padx=5, pady=10, sticky='w') 
        
        stock_actual = self.obtener_stock_actual() # obtener stock actual del producto
        
        
        # mostrar stock actual
        frame_stock_actual = Frame(self.i_editar_producto, bg="gray22")
        frame_stock_actual.place(x=720, y=350)
        
        label_stock_actual = Label(frame_stock_actual, text="Stock actual", bg='gray22', fg='green', font=("Century Gothic", 12))
        label_stock_actual.grid(row=0, column=0, sticky='w', columnspan=3)   
        
        label_stock_xs = Label(frame_stock_actual, text=f"XS: {stock_actual[0]}   ", bg='gray22', fg='white', font=("Century Gothic", 12))
        label_stock_xs.grid(row=1, column=0, sticky='w')  
        
        label_stock_s = Label(frame_stock_actual, text=f"S: {stock_actual[1]}   ", bg='gray22', fg='white', font=("Century Gothic", 12))
        label_stock_s.grid(row=2, column=0, sticky='w')  
        
        label_stock_m = Label(frame_stock_actual, text=f"M: {stock_actual[2]}   ", bg='gray22', fg='white', font=("Century Gothic", 12))
        label_stock_m.grid(row=1, column=1, sticky='w')  
        
        label_stock_l = Label(frame_stock_actual, text=f"L: {stock_actual[3]}   ", bg='gray22', fg='white', font=("Century Gothic", 12))
        label_stock_l.grid(row=2, column=1, sticky='w')  
        
        label_stock_xl = Label(frame_stock_actual, text=f"XL: {stock_actual[4]}", bg='gray22', fg='white', font=("Century Gothic", 12))
        label_stock_xl.grid(row=1, column=2, sticky='w')  
        
        label_stock_xxl = Label(frame_stock_actual, text=f"XXL: {stock_actual[5]}", bg='gray22', fg='white', font=("Century Gothic", 12))
        label_stock_xxl.grid(row=2, column=2, sticky='w')  
        
        
        
       
        
    # lógica para guardar el pedido en la base de datos, en las tablas compras y stock
    def anadir_talles(self, ventana):
        # validar al menos un talle seleccionado
        if (self.combo_xs.get() or self.combo_s.get() or self.combo_m.get() or self.combo_l.get() or self.combo_xl.get() or self.combo_xxl.get()):
            
            confirmar = askyesno("Realizar pedido", "¿Estás seguro que deseas realizar este pedido?")
            if confirmar:
                # diccionario con el talle seleccionado como clave y la cantidad seleccionada como valor
                talles = {"XS": self.combo_xs.get(),
                        "S": self.combo_s.get(),
                        "M": self.combo_m.get(),
                        "L": self.combo_l.get(),
                        "XL": self.combo_xl.get(),
                        "XXL": self.combo_xxl.get()
                        } 
                
                try:
                    self.precio = float(self.precio)    # convertir el precio a float
                    tabla = coneccion.cursor()
                    for talle, stock in talles.items(): # iterar diccionario
                        if stock:   # si el usuario especificó una cantidad en el talle actual
                            stock = int(stock)  # convertir la cantidad a entero
                            # actualizar la tabla stock con el nuevo stock agregado
                            tabla.execute("UPDATE stock SET stock_talle = stock_talle + ? WHERE id_producto = ? AND talle = ?", (stock, self.id_producto, talle))
                            # registrar el pedido en la tabla compras
                            consulta_compra = "INSERT INTO compras (id_producto, id_usuario, precio_unitario, precio_total, talle, cantidad) VALUES (?, ?, ?, ?, ?, ?)"
                            tabla.execute(consulta_compra, (self.id_producto, self.id_admin, self.precio, self.precio * stock, talle, stock))
                            
                    coneccion.commit()
                    showinfo("Stock actualizado", "El pedido se realizó correctamente.")
                    ventana.destroy()
                except ValueError:
                    showwarning("Advertencia", "Error en los talles seleccionados: Los talles son incompatibles")
                except sqlite3.OperationalError as e:
                    showwarning("Advertencia", f"Error en los datos al realizar el pedido.\n{e}")
                except Exception as e2:
                    showwarning("Advertencia", f"Error al realizar el pedido.\n{e2}")
                           
        else:
            showwarning("Advertencia", "Selecciona al menos un talle.")
            return
            
            
    # obtener stock actual
    def obtener_stock_actual(self):
        try:
            tabla = coneccion.cursor()
            tabla.execute("SELECT stock_talle FROM stock WHERE id_producto = ?", (self.id_producto, ))
            talles = tabla.fetchall()
            stock_talles = []
            for talle in talles:
                stock_talles.append(talle[0])
            return stock_talles
        except sqlite3.OperationalError as e:
            showwarning("Advertencia", f"Error en la base de datos al cargar stock actual.\n{e}")
        except Exception as e2:
            showwarning("Advertencia", f"Error desconocido al cargar stock.\n{e2}")
            

    # obtener precio del producto
    def obtener_precio_producto(self, descripcion_producto):
        try:
            self.id_producto = self.validar_producto(descripcion_producto)[0][0]
            tabla = coneccion.cursor()
            tabla.execute("SELECT precio FROM productos_proveedores WHERE id_producto = ?", (self.id_producto, ))  
            precio = tabla.fetchone()[0]
            return precio
        except sqlite3.OperationalError as e:
            showwarning("Advertencia", f"Error en la base de datos al obtener el ID del producto.\n{e}") 
        except Exception as e2:
            showwarning("Advertencia", f"Error desconocido al obtener el ID del producto.\n{e2}") 
      

class GraficosEstadisticas: # graficos: 1- productos más vendidos, 2- mejores clientes, 3- talles populares, 4- versiones más vendidas, 5- estadísticas
    def ventana_inicio_graficos(self, ventana_primaria):
        x_pos, y_pos = bloquear_ventanas_duplicadas(ventana_primaria) 
        
        inicio_graficos = Toplevel(ventana_primaria)
        inicio_graficos.title("Gráficos y estadísticas")
        inicio_graficos.geometry(f"950x250+{x_pos}+{y_pos}")
        inicio_graficos.resizable(False, False)
        inicio_graficos.config(bg="gray22")
        inicio_graficos.iconbitmap(icono) 
        
        # botones principales
        boton_grafico_productos = Button(inicio_graficos, image=imagen_grafico_productos, bg="gray22", fg="white", font=("Century Gothic", 11), text="Productos más vendidos",
                                         compound='top', border=0, command=self.grafico_top_productos)
        boton_grafico_productos.grid(row=0, column=0, padx=20, pady=50) 
        
        boton_grafico_productos.bind("<Enter>", lambda e: e.widget.config(bg="gray", highlightthickness=1, highlightbackground="blue"))
        boton_grafico_productos.bind("<Leave>", lambda e: e.widget.config(bg="gray22", highlightthickness=0))
        
        boton_grafico_clientes = Button(inicio_graficos, image=imagen_grafico_clientes, bg="gray22", fg="white", font=("Century Gothic", 11), text="Mejores clientes",
                                         compound='top', border=0, command=self.grafico_mejores_clientes)
        boton_grafico_clientes.grid(row=0, column=1, padx=20, pady=50) 
        
        boton_grafico_clientes.bind("<Enter>", lambda e: e.widget.config(bg="gray", highlightthickness=1, highlightbackground="blue"))
        boton_grafico_clientes.bind("<Leave>", lambda e: e.widget.config(bg="gray22", highlightthickness=0))
        
        boton_grafico_talles = Button(inicio_graficos, image=imagen_grafico_talles, bg="gray22", fg="white", font=("Century Gothic", 11), text="Talles populares",
                                         compound='top', border=0, command=self.grafico_talles_vendidos)
        boton_grafico_talles.grid(row=0, column=2, padx=20, pady=50) 
        
        boton_grafico_talles.bind("<Enter>", lambda e: e.widget.config(bg="gray", highlightthickness=1, highlightbackground="blue"))
        boton_grafico_talles.bind("<Leave>", lambda e: e.widget.config(bg="gray22", highlightthickness=0))
        
        boton_grafico_versiones = Button(inicio_graficos, image=imagen_grafico_versiones, bg="gray22", fg="white", font=("Century Gothic", 11), text="Versiones populares",
                                         compound='top', border=0, command=self.grafico_versiones_vendidas)
        boton_grafico_versiones.grid(row=0, column=3, padx=20, pady=50) 
        
        boton_grafico_versiones.bind("<Enter>", lambda e: e.widget.config(bg="gray", highlightthickness=1, highlightbackground="blue"))
        boton_grafico_versiones.bind("<Leave>", lambda e: e.widget.config(bg="gray22", highlightthickness=0))
        
        boton_estadisticas = Button(inicio_graficos, image=imagen_estadiscticas, bg="gray22", fg="white", font=("Century Gothic", 11), text="Estadísticas",
                                         compound='top', border=0)
        boton_estadisticas.grid(row=0, column=4, padx=20, pady=50) 
        
        boton_estadisticas.bind("<Enter>", lambda e: e.widget.config(bg="gray", highlightthickness=1, highlightbackground="blue"))
        boton_estadisticas.bind("<Leave>", lambda e: e.widget.config(bg="gray22", highlightthickness=0))
        
    # ------- Graficar los productos más vendidos -------
    def grafico_top_productos(self):
        top_productos = self.obtener_top_productos()    # id_producto, nombre_producto, ventas
        # separar datos en listas distintas para graficar
        nombres_productos = [f"{producto[1]} (ID: {producto[0]})" for producto in top_productos]
        ventas_totales = [producto[2] for producto in top_productos]
        
        # colores para las barras
        colores = self.obtener_colores(nombres_productos)
        
        # crear grafico de barras verticales
        plt.figure(figsize=(10, 6))
        plt.bar(nombres_productos, ventas_totales, color=colores)
        plt.ylabel("Ventas")
        plt.xlabel("Producto")
        plt.title("Top 10 productos más vendidos")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.show()
        
    def obtener_top_productos(self):
        try:
            tabla = coneccion.cursor()  # obtener las camisetas mas vendidas
            consulta_sql = '''  
            SELECT v.id_producto, p.nombre_producto, sum(v.cantidad) AS ventas_producto FROM ventas v
            JOIN productos p
            ON v.id_producto = p.id_producto
            GROUP BY v.id_producto
            ORDER BY ventas_producto DESC 
            LIMIT 10
            '''
            tabla.execute(consulta_sql)
            informacion_ventas = tabla.fetchall()
            return informacion_ventas
        
        except sqlite3.OperationalError as e:
            showwarning("Advertencia", f"Error en la base de datos al cargar los productos más vendidos.\n{e}")
        except Exception as e2:
            showwarning("Advertencia", f"Error desconocido al cargar los productos más vendidos.\n{e2}")
            
    # obtener los colores de cada equipo para el grafico de barras     
    def obtener_colores(self, nombres_productos):
        colores_equipos = {
    "Atlanta Hawks": "#E03A3E",         # Rojo
    "Boston Celtics": "#007A33",        # Verde
    "Brooklyn Nets": "#000000",         # Negro
    "Charlotte Hornets": "#1D1160",     # Morado Oscuro
    "Chicago Bulls": "#CE1141",         # Rojo
    "Cleveland Cavaliers": "#6F263D",   # Vino
    "Dallas Mavericks": "#00538C",      # Azul Oscuro
    "Denver Nuggets": "#0E2240",        # Azul Profundo
    "Detroit Pistons": "#C8102E",       # Rojo
    "Golden State Warriors": "#1D428A", # Azul
    "Houston Rockets": "#CE1141",       # Rojo
    "Indiana Pacers": "#002D62",        # Azul Marino
    "Los Angeles Clippers": "#C8102E",  # Rojo
    "Los Angeles Lakers": "#552583",    # Púrpura
    "Memphis Grizzlies": "#12173F",     # Azul Marino
    "Miami Heat": "#98002E",            # Rojo
    "Milwaukee Bucks": "#00471B",       # Verde Oscuro
    "Minnesota Timberwolves": "#0C2340",# Azul Marino
    "New Orleans Pelicans": "#0C2340",  # Azul Marino
    "New York Knicks": "#006BB6",       # Azul
    "Oklahoma City Thunder": "#007AC1", # Azul
    "Orlando Magic": "#0077C0",         # Azul
    "Philadelphia 76ers": "#006BB6",    # Azul
    "Phoenix Suns": "#1D1160",          # Púrpura
    "Portland Trail Blazers": "#E03A3E",# Rojo
    "Sacramento Kings": "#5A2D81",      # Púrpura Oscuro
    "San Antonio Spurs": "#C4CED4",     # Gris Claro
    "Toronto Raptors": "#CE1141",       # Rojo
    "Utah Jazz": "#002B5C",             # Azul Marino
    "Washington Wizards": "#002B5C"     # Azul Marino
}
        
        colores = []
        
        for nombre in nombres_productos:
            for equipo in colores_equipos:
                if equipo.lower() in nombre.lower():
                    colores.append(colores_equipos[equipo])
                    break
        
        return colores
    
# ------- Gráfico de clientes con más compras -------
    def grafico_mejores_clientes(self):
        top_clientes = self.obtener_mejores_clientes()
        clientes = [f"{cliente[1]} (Total invertido: {cliente[2]})" for cliente in top_clientes]
        compras = [cliente[0] for cliente in top_clientes]
        
        # Crear gráfico de barras horizontal para el número de compras por cliente
        plt.figure(figsize=(10, 6))
        plt.barh(clientes, compras, color="skyblue")
        plt.xlabel("Camisetas compradas")
        plt.ylabel("Clientes")
        plt.title("Top clientes por número de Compras")
        plt.gca().invert_yaxis()  # Invertir el eje Y para que el cliente con más compras esté arriba
        plt.tight_layout()
        plt.show()


    def obtener_mejores_clientes(self):
        try:
            tabla = coneccion.cursor()  # obtener las compras de clientes, su nombre de usuario y total invertido
            consulta_sql = '''  
            SELECT count(v.id_usuario) AS compras_cliente, username, sum(precio_total) as total_invertido FROM ventas v
            JOIN usuarios u ON v.id_usuario = u.id_usuario
            GROUP BY v.id_usuario
            ORDER BY compras_cliente DESC, total_invertido DESC 
            LIMIT 10
            '''
            tabla.execute(consulta_sql)
            informacion_clientes = tabla.fetchall()
            return informacion_clientes
        
        except sqlite3.OperationalError as e:
            showwarning("Advertencia", f"Error en la base de datos al cargar los clientes.\n{e}")
        except Exception as e2:
            showwarning("Advertencia", f"Error desconocido al cargar los clientes.\n{e2}")
  
    
# ------- Gráfico de talles más vendidos -------
    def grafico_talles_vendidos(self):
        # Ejecutar la consulta SQL para obtener la distribución de talles vendidos
        talles_vendidos = self.obtener_talles_vendidos()  # obtener el talle y sus ventas

        # Separar datos en listas para graficar
        talles = [f"{talle[0]} ({talle[1]} ventas)" for talle in talles_vendidos]
        cantidades = [talle[1] for talle in talles_vendidos]

        # Crear gráfico de pastel
        plt.figure(figsize=(8, 8))
        plt.pie(cantidades, labels=talles, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors, wedgeprops={'width': 0.3})
        plt.title("Distribución de talles vendidos")
        plt.tight_layout()
        plt.show()

    def obtener_talles_vendidos(self):
        try:
            tabla = coneccion.cursor()  # Ejecutar la consulta para obtener la cantidad de cada talle vendido
            consulta_sql = '''
            SELECT talle, count(talle) AS cantidad_vendida
            FROM ventas
            GROUP BY talle
            '''
            tabla.execute(consulta_sql)
            informacion_talles = tabla.fetchall()
            return informacion_talles
        
        except sqlite3.OperationalError as e:
            showwarning("Advertencia", f"Error en la base de datos al cargar la información de talles vendidos.\n{e}")
        except Exception as e2:
            showwarning("Advertencia", f"Error desconocido al cargar la información de talles vendidos.\n{e2}")
   
   # ------- Gráfico de versiones más vendidas -------
    def grafico_versiones_vendidas(self):
        # Ejecutar la consulta SQL para obtener la distribución de versiones vendidos
        versiones_vendidas = self.obtener_versiones_vendidas()  # obtener la versión y sus ventas

        # Separar datos en listas para graficar
        versiones = [f"{version[0]} ({version[1]} ventas)" for version in versiones_vendidas]
        cantidades = [version[1] for version in versiones_vendidas]

        # Crear gráfico de pastel
        plt.figure(figsize=(8, 8))
        plt.pie(cantidades, labels=versiones, autopct='%1.1f%%', startangle=140, colors=['#87CEEB', '#2F4F4F', '#8B0000', '#8A2BE2'])
        plt.title("Distribución de versiones vendidas")
        plt.tight_layout()
        plt.show()
   
   
    def obtener_versiones_vendidas(self):
        try:
            tabla = coneccion.cursor()  # Ejecutar la consulta para obtener la cantidad de cada version vendida
            consulta_sql = '''
            SELECT version, sum(cantidad) FROM ventas v
            JOIN productos p ON v.id_producto = p.id_producto
            GROUP BY version
            '''
            tabla.execute(consulta_sql)
            informacion_versiones = tabla.fetchall()
            return informacion_versiones
        
        except sqlite3.OperationalError as e:
            showwarning("Advertencia", f"Error en la base de datos al cargar la información de talles vendidos.\n{e}")
        except Exception as e2:
            showwarning("Advertencia", f"Error desconocido al cargar la información de talles vendidos.\n{e2}")
   
def cerrar(ventana_actual, ventana_anterior):
    ventana_actual.destroy()
    ventana_anterior.deiconify()
 
# funcion para no mostrar ventanas duplicadas si el usuario intenta abrir varias veces la misma interfaz
def bloquear_ventanas_duplicadas(ventana_primaria, x_pos=550, y_pos=250):    
    for widget in ventana_primaria.winfo_children():   
        if type(widget) is Toplevel:                   # verificar que no existan ventanas anteriores para evitar acumular muchas en la pantalla
            x_pos = widget.winfo_x()                   # obtener la posicion de la ventana antes de eliminarla para asignarsela a la nueva
            y_pos = widget.winfo_y()
            widget.destroy()   
    
    return x_pos, y_pos     # posicion de la ventana eliminada
         
# widgets login
ruta_fondo = "imagenes/leBron-dunk.jpg"
imagen_fondo = Image.open(ruta_fondo)
imagen_fondo = imagen_fondo.resize((300, 500), Image.LANCZOS)
imagen_fondo = ImageTk.PhotoImage(imagen_fondo)
label_fondo = Label(ventana_login, image=imagen_fondo)
label_fondo.place(x=0, y=0, relwidth=1, relheight=1)

# lista provincias
provincias = ["Buenos Aires", "Catamarca", "Chaco", "Chubut", "Córdoba",
                    "Corrientes", "Entre Ríos", "Formosa", "Jujuy", "La Pampa",
                    "La Rioja", "Mendoza", "Misiones", "Neuquén", "Río Negro",
                    "Salta", "San Juan", "San Luis", "Santa Cruz", "Santa Fe",
                    "Santiago del Estero", "Tucumán"]

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
ruta_imagen_modificar_ubicacion = "botones/editar-ubicacion2.png"
imagen_modificar_ubicacion = Image.open(ruta_imagen_modificar_ubicacion)
imagen_modificar_ubicacion = ImageTk.PhotoImage(imagen_modificar_ubicacion)

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

ruta_atras = "botones/atras.png"
imagen_atras = Image.open(ruta_atras)
imagen_atras = ImageTk.PhotoImage(imagen_atras)

ruta_logo_proyecto = "imagenes/logo-png.png"
imagen_proyecto = Image.open(ruta_logo_proyecto)
imagen_proyecto = ImageTk.PhotoImage(imagen_proyecto)

ruta_envio = "botones/envio.png"
imagen_envio = Image.open(ruta_envio)
imagen_envio = ImageTk.PhotoImage(imagen_envio)

ruta_anadir = "botones/anadir1.png"
imagen_anadir = Image.open(ruta_anadir)
imagen_anadir = ImageTk.PhotoImage(imagen_anadir)

ruta_editar = "botones/editar2.png"
imagen_editar = Image.open(ruta_editar)
imagen_editar = ImageTk.PhotoImage(imagen_editar)

ruta_stock = "botones/en-stock.png"
imagen_stock = Image.open(ruta_stock)
imagen_stock = ImageTk.PhotoImage(imagen_stock)

ruta_graficos = "botones/graficos.png"
imagen_graficos = Image.open(ruta_graficos)
imagen_graficos = ImageTk.PhotoImage(imagen_graficos)

ruta_anadir_cliente = "botones/agregar-cliente.png"
imagen_anadir_cliente = Image.open(ruta_anadir_cliente)
imagen_anadir_cliente = ImageTk.PhotoImage(imagen_anadir_cliente)

ruta_anadir_proveedor = "botones/agregar-proveedor.png"
imagen_anadir_proveedor = Image.open(ruta_anadir_proveedor)
imagen_anadir_proveedor = ImageTk.PhotoImage(imagen_anadir_proveedor)

ruta_anadir_admin = "botones/agregar-admin.png"
imagen_anadir_admin = Image.open(ruta_anadir_admin)
imagen_anadir_admin = ImageTk.PhotoImage(imagen_anadir_admin)

ruta_editar_admin = "botones/editar-admin.png"
imagen_editar_admin = Image.open(ruta_editar_admin)
imagen_editar_admin = ImageTk.PhotoImage(imagen_editar_admin)

ruta_editar_proveedor = "botones/editar-proveedor.png"
imagen_editar_proveedor = Image.open(ruta_editar_proveedor)
imagen_editar_proveedor = ImageTk.PhotoImage(imagen_editar_proveedor)

ruta_editar_producto = "botones/editar-producto2.png"
imagen_editar_producto = Image.open(ruta_editar_producto)
imagen_editar_producto = ImageTk.PhotoImage(imagen_editar_producto)

ruta_grafico_productos = "botones/barra-grafica.png"
imagen_grafico_productos = Image.open(ruta_grafico_productos)
imagen_grafico_productos = ImageTk.PhotoImage(imagen_grafico_productos)

ruta_grafico_clientes = "botones/grafico-de-barras.png"
imagen_grafico_clientes = Image.open(ruta_grafico_clientes)
imagen_grafico_clientes = ImageTk.PhotoImage(imagen_grafico_clientes)

ruta_grafico_talles = "botones/grafico-circular.png"
imagen_grafico_talles = Image.open(ruta_grafico_talles)
imagen_grafico_talles = ImageTk.PhotoImage(imagen_grafico_talles)

ruta_grafico_versiones = "botones/carrito-de-pasteles.png"
imagen_grafico_versiones = Image.open(ruta_grafico_versiones)
imagen_grafico_versiones = ImageTk.PhotoImage(imagen_grafico_versiones)

ruta_estadisticas = "botones/estadisticas.png"
imagen_estadiscticas = Image.open(ruta_estadisticas)
imagen_estadiscticas = ImageTk.PhotoImage(imagen_estadiscticas)

# instancias
inicio_cliente = InicioCliente()
cargar_camisetas = CargarCamisetas()
vista_compra = VistaCompra()
editar_cliente = EditarCliente()
editar_direccion_cliente = EditarDireccionCliente()
terminos = TerminosCondiciones()
confirmar_compra = Comprar()
inicio_admin = InicioAdmin()
add = Anadir()
edit = Editar()
add_stock = AnadirStock()
graficos = GraficosEstadisticas()
graficos.ventana_inicio_graficos(ventana_login)
#graficos.obtener_top_productos()
# botón ingresar
ingresar = Login()
boton_ingresar = Button(ventana_login, text="Ingresar", width=8, cursor="hand2", command=ingresar.login)
boton_ingresar.place(x=120, y=280)

# pie de página
label_footer = Label(ventana_login, text="NBA Kits - 2024", fg="snow", bg="gray22", font=("Arial", 10))
label_footer.place(x=100, y=480)


ventana_login.mainloop()