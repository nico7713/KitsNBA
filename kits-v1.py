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
        boton_busqueda = Button(frame_busqueda, image=imagen_buscar, border=0, cursor="hand2", command=lambda : busqueda(self))
        boton_busqueda.place(x=870, y=24)
        
        # volver (cargar de nuevo las camisetas)
        boton_volver = Button(frame_busqueda, image=imagen_volver, bg="black", border=0, cursor="hand2", command=lambda : busqueda(self, volver=True)) 
        boton_volver.place(x=15, y=15) 
        
        boton_volver.bind("<Enter>", lambda e: e.widget.config(bg="gray", highlightthickness=2, highlightbackground="blue"))
        boton_volver.bind("<Leave>", lambda e: e.widget.config(bg="black", highlightthickness=0))
        
        # botón para modificar la información personal del usuario
        boton_nombre_de_usuario = Button(frame_busqueda, text=f"{self.nombre_cliente} {self.apellido_cliente}", bg="black", fg="white", font=("Century Gothic", 12),
                                         border=0, cursor="hand2", command=lambda : editar_cliente.interfaz_editar_datos_principales(self.id_cliente))
        boton_nombre_de_usuario.place(x=1150, y=25)
        
        boton_nombre_de_usuario.bind("<Enter>", lambda e: e.widget.config(bg="gray", highlightthickness=2, highlightbackground="blue"))
        boton_nombre_de_usuario.bind("<Leave>", lambda e: e.widget.config(bg="black", highlightthickness=0))
        
        def busqueda(self, volver=False, favoritos=False, compras=False, filtrar=False, filtro=False):
            criterio = self.barra_busqueda.get()
            if criterio and not volver and not favoritos and not compras and not filtrar and not filtro:
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
                
            if favoritos:
                consulta_sql = f'''
                SELECT imagen, nombre_producto, jugador, precio, p.id_producto FROM productos p
                INNER JOIN favoritos f
                ON p.id_producto = f.id_producto
                WHERE f.id_usuario = {self.id_cliente}
                               '''
                               
            if compras:
                consulta_sql = f'''
                SELECT imagen, nombre_producto, jugador, precio, p.id_producto FROM productos p
                JOIN ventas v
                ON p.id_producto = v.id_producto
                WHERE v.id_usuario = {self.id_cliente}
                '''
                
            if filtrar:
                self.ventana_filtrar = Toplevel()
                self.ventana_filtrar.title("Filtrar por")
                self.ventana_filtrar.geometry("300x170")
                self.ventana_filtrar.resizable(False, False)
                self.ventana_filtrar.iconbitmap(icono)
                
                campos = ["Precio", "Marca", "Version", "Color", "Equipo"]
                self.entry_campo = ttk.Combobox(self.ventana_filtrar, values=campos, font=('Century Gothic', 12))
                self.entry_campo.insert(0, campos[0])
                self.entry_campo.config(state='readonly')
                self.entry_campo.pack(pady=10)
                
                orden = ["Ascendente", "Descendente"]
                self.entry_orden = ttk.Combobox(self.ventana_filtrar, values=orden, font=('Century Gothic', 12))
                self.entry_orden.insert(0, orden[0])
                self.entry_orden.config(state='readonly')
                self.entry_orden.pack(pady=10)
            
                boton_ir = Button(self.ventana_filtrar, text="Filtrar", bg='gray22', fg='white', font=('Century Gothic', 12), width=15, command=lambda : busqueda(self, filtro=True))
                boton_ir.pack(pady=10)
            
            if filtro:
                campo = self.entry_campo.get().lower()
                if self.entry_orden.get() == "Ascendente":
                    orden = "ASC"
                if self.entry_orden.get() == "Descendente":
                    orden = "DESC"
                    
                self.ventana_filtrar.destroy()
                consulta_sql = f"SELECT imagen, nombre_producto, jugador, precio, id_producto FROM productos ORDER BY {campo} {orden}" 
            
            if criterio or volver or favoritos or compras or filtro: 
                for widget in ventana_inicial.winfo_children():
                    widget.destroy()
                        
                ventana_inicio = self.ventana_y_frames(ventana_inicial)
                self.barra_busqueda.insert(0, criterio)
                frame_camisetas = self.configurar_scrollbar(ventana_inicio)
                self.colocar_camisetas(frame_camisetas, consulta_sql)
            
              
        # elementos del frame_acceso_rapido
        # boton modificar ubicacion cliente
        boton_modificar_ubicacion = Button(frame_acceso_rapido, image=imagen_modificar_ubicacion, cursor="hand2", border=0,
                                           command=lambda : editar_direccion_cliente.interfaz_editar_ubicacion(self.id_cliente))
        boton_modificar_ubicacion.place(x=15, y=120)
        
        boton_modificar_ubicacion.bind("<Enter>", lambda e: e.widget.config(bg="lightblue", highlightthickness=2, highlightbackground="blue"))
        boton_modificar_ubicacion.bind("<Leave>", lambda e: e.widget.config(bg="snow", highlightthickness=0))
        
        # boton filtrar por
        boton_filtrar = Button(frame_acceso_rapido, image=imagen_filtrar, cursor="hand2", border=0, command=lambda : busqueda(self, filtrar=True))
        boton_filtrar.place(x=15, y=215)
        
        boton_filtrar.bind("<Enter>", lambda e: e.widget.config(bg="lightblue", highlightthickness=2, highlightbackground="blue"))
        boton_filtrar.bind("<Leave>", lambda e: e.widget.config(bg="snow", highlightthickness=0))
        
        # mis compras
        boton_mis_compras = Button(frame_acceso_rapido, image=imagen_compras, cursor="hand2", border=0, command=lambda : busqueda(self, compras=True))
        boton_mis_compras.place(x=15, y=305)
        
        boton_mis_compras.bind("<Enter>", lambda e: e.widget.config(bg="lightblue", highlightthickness=2, highlightbackground="blue"))
        boton_mis_compras.bind("<Leave>", lambda e: e.widget.config(bg="snow", highlightthickness=0))
        
        # mis favoritos
        boton_favoritos = Button(frame_acceso_rapido, image=imagen_favoritos, cursor="hand2", border=0, command=lambda : busqueda(self, favoritos=True)) 
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
                except Exception as e2:
                    showwarning("Advertencia", f"Ocurrió un error desconocido al actualizar la información del usuario.\n{e2}")
                    return
                
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
            if not codigo_postal.isnumeric():
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

# botón ingresar
ingresar = Login()
boton_ingresar = Button(ventana_login, text="Ingresar", width=8, cursor="hand2", command=ingresar.login)
boton_ingresar.place(x=120, y=280)

# pie de página
label_footer = Label(ventana_login, text="NBA Kits - 2024", fg="snow", bg="gray22", font=("Arial", 10))
label_footer.place(x=100, y=480)


ventana_login.mainloop()