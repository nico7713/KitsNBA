from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
import tkinter.simpledialog
from PIL import Image, ImageTk
import sqlite3
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

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
        boton_busqueda = Button(frame_busqueda, image=imagen_buscar, border=0, cursor="hand2", command=lambda : self.busqueda(ventana_inicial))
        boton_busqueda.place(x=870, y=24)
        
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
        
        boton_ir = Button(ventana_filtrar, text="Filtrar", bg='gray22', fg='white', font=('Century Gothic', 12), width=15, command=lambda : self.filtrar(ventana, ventana_filtrar))
        boton_ir.pack(pady=10)
        
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
        boton_confirmar_cambios = Button(editar_cliente, text="Guardar Cambios", bg="dark blue", fg="white", font=("Century Gothic", 12), width=18,
                                         command=lambda : self.editar_datos_principales(id_usuario, editar_cliente))
        boton_confirmar_cambios.place(x=280, y=80)
        
        boton_restaurar_clave = Button(editar_cliente, text="Restaurar Contraseña", bg="gray22", fg="white", font=("Century Gothic", 12), width=18,
                                       command=lambda : self.interfaz_cambiar_clave(id_usuario))
        boton_restaurar_clave.place(x=280, y=120)
        
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
                    showwarning("Advertencia", f"El nombre de usuario '{nuevo_username}' ya existe.\nPor favor elije otro.")
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
        
        boton_actualizar = Button(editar_clave, text="Actualizar", bg="gray22", fg="white", font=("Century Gothic", 12),
                                  command=lambda : self.cambiar_clave(id_usuario, editar_clave)) 
        boton_actualizar.pack(pady=10)
        
        
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
        
        provincias = ["Buenos Aires", "Mendoza", "Santa Fe", "Chubut", "Cordoba", "Río Negro", "La Rioja", "Corrientes"]
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
     
        boton_confirmar_cambios = Button(editar_ubicacion, text="Guardar Cambios", bg="dark blue", fg="white", font=("Century Gothic", 12), width=18,
                                         command=lambda : self.editar_ubicacion(editar_ubicacion)) 
        boton_confirmar_cambios.place(x=250, y=210)
        
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
        boton_compra = Button(frame_descripcion, text="Comprar ahora", width=24, bg="Green", fg="white", font=("Century Gothic", 16), cursor="hand2",
                              command=lambda imagen=imagen_camiseta: confirmar_compra.vista_confirmar_compra(self.ventana_compra, self.id_cliente, id_camiseta, imagen))
        boton_compra.place(x=10, y=460)
        
        
        # logo aplicación
        logo = Label(frame_descripcion, image=imagen_proyecto)
        logo.place(x=350, y=505)
        
        return frame_descripcion
    
    def talles_camiseta(self, frame_descripcion, id_camiseta):  # método para colocar los widgets de talles y verificar stock
        # talles 
        cantidades = ["", 1, 2, 3, 4, 5]
            
        # XS
        label_xs = Label(frame_descripcion, text="XS", bg='white', font=("Calibri", 14))
        label_xs.place(x=10, y=560)
        
        self.combo_xs = ttk.Combobox(frame_descripcion, width=1, values=cantidades, font=("Calibri", 14), state='readonly')    
        self.combo_xs.place(x=10, y=590)
        # S
        label_s = Label(frame_descripcion, text="S", bg='white', font=("Calibri", 14))
        label_s.place(x=60, y=560)
        
        self.combo_s = ttk.Combobox(frame_descripcion, width=1, values=cantidades, font=("Calibri", 14), state='readonly')    
        self.combo_s.place(x=60, y=590)
        # M
        label_m = Label(frame_descripcion, text="M", bg='white', font=("Calibri", 14))
        label_m.place(x=110, y=560)
        
        self.combo_m = ttk.Combobox(frame_descripcion, width=1, values=cantidades, font=("Calibri", 14), state='readonly')    
        self.combo_m.place(x=110, y=590)
        # L
        label_l = Label(frame_descripcion, text="L", bg='white', font=("Calibri", 14))
        label_l.place(x=160, y=560)
        
        self.combo_l = ttk.Combobox(frame_descripcion, width=1, values=cantidades, font=("Calibri", 14), state='readonly')    
        self.combo_l.place(x=160, y=590)
        # XL
        label_xl = Label(frame_descripcion, text="XL", bg='white', font=("Calibri", 14))
        label_xl.place(x=210, y=560)
        
        self.combo_xl = ttk.Combobox(frame_descripcion, width=1, values=cantidades, font=("Calibri", 14), state='readonly')    
        self.combo_xl.place(x=210, y=590)
        # XXL
        label_xxl = Label(frame_descripcion, text="XXL", bg='white', font=("Calibri", 14))
        label_xxl.place(x=260, y=560)
        
        self.combo_xxl = ttk.Combobox(frame_descripcion, width=1, values=cantidades, font=("Calibri", 14), state='readonly')    
        self.combo_xxl.place(x=260, y=590)
        
        # mostrar si hay stock disponible en los talles
        try:
            consulta = "SELECT stock_talle FROM stock WHERE id_producto = ?"
            parametro = (id_camiseta, )
            tabla = coneccion.cursor()
            tabla.execute(consulta, parametro)
            talles = tabla.fetchall()
            
            xs, s, m, l, xl, xxl = talles
            
            if xs[0] == 0:
                self.combo_xs.config(state='disabled')
                label_xs.config(fg='red')
            if s[0] == 0:
                self.combo_s.config(state='disabled')
                label_s.config(fg='red')
            if m[0] == 0:
                self.combo_m.config(state='disabled')
                label_m.config(fg='red')
            if l[0] == 0:
                self.combo_l.config(state='disabled')
                label_l.config(fg='red')
            if xl[0] == 0:
                self.combo_xl.config(state='disabled')
                label_xl.config(fg='red')
            if xxl[0] == 0:
                self.combo_xxl.config(state='disabled')
                label_xxl.config(fg='red')
            
        except Exception as e:
            showwarning("Advertencia", f"Error al cargar la información de talles\n{e}") 
    
    
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
        label_info_direccion.place(x=500, y=135)
        
        label_provincia = Label(ventana_compra, text=f"Provincia: {provincia}", bg='white', font=(fuente, 14))
        label_provincia.place(x=500, y=165) 
        
        label_localidad = Label(ventana_compra, text=f"Localidad: {localidad}", bg='white', font=(fuente, 14))
        label_localidad.place(x=500, y=195)
        
        label_direccion = Label(ventana_compra, text=f"Dirección: {direccion}", bg='white', font=(fuente, 14))
        label_direccion.place(x=500, y=225)  
        
        label_codigo_postal = Label(ventana_compra, text=f"Código postal: {codigo_postal}", bg='white', font=(fuente, 14))
        label_codigo_postal.place(x=500, y=255) 
        
        # notas del usuario
        label_notas = Label(ventana_compra, text=f"Notas del usuario acerca del envío y dirección:", bg='white', font=(fuente, 14))
        label_notas.place(x=500, y=285)
        
        self.mensaje_inicial = """Notas adicionales para el envío
Por favor, utiliza este espacio para agregar cualquier comentario sobre tu disponibilidad para recibir el pedido, o para especificar una dirección de envío alternativa. Asegúrate de que la información que proporciones sea clara y precisa, ya que cualquier error o ambigüedad podría retrasar o afectar la entrega de tu pedido.
        """
        self.area_notas = Text(ventana_compra, width=50, height=9, bg='white', fg='gray', font=("Calibri", 12), wrap='word') 
        self.area_notas.insert("1.0", self.mensaje_inicial)
        self.area_notas.place(x=500, y=320)  
        
        def borrar_mensaje(event):
            if self.area_notas.get("1.0", "end-1c"):   # si el texto es el mensaje inicial
                self.area_notas.delete("1.0", "end") 
                self.area_notas.config(fg='black')
        
        self.area_notas.bind("<FocusIn>", borrar_mensaje)
        
        # terminos y condiciones
        label_terminos = Label(ventana_compra, text=f"Antes de realizar la compra, asegúrate\nde haber leído y entendido los", bg='white', font=("Calibri", 14))
        label_terminos.place(x=500, y=540)
    
        boton_terminos = Button(ventana_compra, text=f"Términos y condiciones", bg='white', font=("Calibri", 14), border=0, cursor="hand2",
                                command=lambda : terminos.interfaz_terminos(nombre))
        boton_terminos.place(x=555, y=585)
        
        boton_terminos.bind("<Enter>", lambda e: e.widget.config(font=("Calibri", 14, "bold", "underline")))
        boton_terminos.bind("<Leave>", lambda e: e.widget.config(font=("Calibri", 14)))
    
        # frame línea
        frame_linea2 = Frame(ventana_compra, bg='black', width=1, height=760)
        frame_linea2.place(x=990, y=0)
    
        # muestra camiseta
        label_camiseta = Label(ventana_compra, image=imagen_producto)
        label_camiseta.place(x=1025, y=100) 
        
        # tarjeta de credito
        label_credito = Label(ventana_compra, text="Tarjeta de débito", bg='white', fg='black', font=("Arial", 12)) 
        label_credito.place(x=1110, y=550)
        
        self.parte1 = Entry(ventana_compra, width=7, font=("Arial", 12))
        self.parte1.place(x=1020, y=590) 

        self.parte2 = Entry(ventana_compra, width=7, font=("Arial", 12))
        self.parte2.place(x=1100, y=590) 

        self.parte3 = Entry(ventana_compra, width=7, font=("Arial", 12))
        self.parte3.place(x=1180, y=590) 

        self.parte4 = Entry(ventana_compra, width=7, font=("Arial", 12))
        self.parte4.place(x=1260, y=590) 
    
        #botón confirmar compra
        boton_comprar = Button(ventana_compra, text=f"Confirmar compra", bg='gray22', fg='white', font=(fuente, 14), cursor="hand2",
                               command=lambda : self.confirmar_compra(talles, ventana_compra))
        boton_comprar.place(x=1100, y=640)
        
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
            WHERE id_usuario = ?
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
            
    def confirmar_compra(self, talles, ventana_compra):
        parte1 = self.parte1.get()
        parte2 = self.parte2.get()
        parte3 = self.parte3.get()
        parte4 = self.parte4.get()
        
        if parte1 and parte2 and parte3 and parte4:
            if parte1.isnumeric() and len(parte1) == 4 and parte2.isnumeric() and len(parte2) == 4 and parte3.isnumeric() and len(parte3) == 4 and parte4.isnumeric() and len(parte4) == 4:
                nombre_producto = self.obtener_informacion_producto()[0]     # obtener nombre producto
                confirmar = askyesno("Confirmar", f"¿Deseas comprar {nombre_producto}?\nUna vez lo confirmes, se procesará el pago.")
                if confirmar:
                    try:
                        precio_unitario = self.obtener_informacion_producto()[3]     # obtener precio unitario
                        notas_cliente = self.area_notas.get("1.0", "end-1c")    # obtener notas adicionales del cliente
                        if notas_cliente == self.mensaje_inicial:
                            notas_cliente = "El cliente no dio notas ni comentarios adicionales."
                        tabla = coneccion.cursor()   
                        for talle, cantidad in talles.items():
                            cantidad = int(cantidad)
                            precio_total_talle = precio_unitario * cantidad
                            datos = (self.id_producto, self.id_cliente, precio_unitario, precio_total_talle, talle, cantidad, notas_cliente)
                            tabla.execute("INSERT INTO ventas (id_producto, id_usuario, precio_unitario, precio_total, talle, cantidad, notas) VALUES (?, ?, ?, ?, ?, ?, ?)", datos)
                            tabla.execute(f"UPDATE stock SET stock_talle = stock_talle - {cantidad} WHERE id_producto = ? AND talle = ?", (self.id_producto, talle))  
                            coneccion.commit()
                            
                        showinfo("¡Felicitaciones!", f"Compraste {nombre_producto}")
                        tabla.execute("SELECT MAX(id_venta) FROM ventas")
                        id_compra = tabla.fetchone()[0]
                        self.descargar_ticket_pdf(id_compra, talles) 
                        ventana_compra.destroy()
                        
                    except Exception as e:
                        showwarning("Advertencia", f"Ocurrió un error al procesar el pago. Contacte al administrador.\n{e}")
            else:
                showwarning("Advertencia", "Tarjeta de débito inválida.")
        else:
            showwarning("Advertencia", "Completa los campos de entrada correspondientes.")
            
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
            c.drawString(250, 260, f"Ticket: {id_compra}")

            c.save()
            showinfo("PDF guardado", "Ya puedes ver el ticket de compra.\nSe guardó en tu escritorio.")
    
                             
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
 

# instancias
inicio_cliente = InicioCliente()
cargar_camisetas = CargarCamisetas()
vista_compra = VistaCompra()
editar_cliente = EditarCliente()
editar_direccion_cliente = EditarDireccionCliente()
terminos = TerminosCondiciones()
confirmar_compra = Comprar()

# botón ingresar
ingresar = Login()
boton_ingresar = Button(ventana_login, text="Ingresar", width=8, cursor="hand2", command=ingresar.login)
boton_ingresar.place(x=120, y=280)

# pie de página
label_footer = Label(ventana_login, text="NBA Kits - 2024", fg="snow", bg="gray22", font=("Arial", 10))
label_footer.place(x=100, y=480)


ventana_login.mainloop()