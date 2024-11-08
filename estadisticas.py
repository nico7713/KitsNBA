import sqlite3
from tkinter.messagebox import *

coneccion = sqlite3.connect("kits-database2.db")

class Estadisticas:
    def __init__(self):
        self.tabla = coneccion.cursor()
        
    def total_camisetas_vendidas(self):
        try:
            self.tabla.execute("SELECT sum(cantidad) FROM ventas")
            cantidad_total = self.tabla.fetchone()[0]
            return cantidad_total
        except Exception as e:
            showwarning("Advertencia", f"Error al cargar estadísticas.\n{e}")
    
    
    def camiseta_mas_vendida(self):
        try:
            consulta = '''
            SELECT nombre_producto, jugador, color, precio, p.id_producto, sum(cantidad) AS ventas_producto FROM ventas v
            JOIN productos p ON v.id_producto = p.id_producto 
            GROUP BY v.id_producto
            ORDER BY ventas_producto DESC, precio_total DESC
            LIMIT 1
            '''
            self.tabla.execute(consulta)
            camiseta = self.tabla.fetchone()
            return camiseta
            
        except Exception as e:
            showwarning("Advertencia", f"Error al cargar estadísticas.\n{e}")
            
    
    def marca_mas_vendida(self):
        try:
            consulta = '''
            SELECT marca, sum(cantidad) AS ventas_marca FROM ventas v
            JOIN productos p ON v.id_producto = p.id_producto
            GROUP BY marca 
            ORDER BY ventas_marca DESC
            LIMIT 1
            '''
            self.tabla.execute(consulta)
            marca = self.tabla.fetchone()
            return marca
            
        except Exception as e:
            showwarning("Advertencia", f"Error al cargar estadísticas.\n{e}")
            
            
    def version_mas_vendida(self):
        try:
            consulta = '''
            SELECT version, sum(cantidad) as ventas_version FROM ventas v
            JOIN productos p ON v.id_producto = p.id_producto
            GROUP BY version
            ORDER BY ventas_version DESC
            LIMIT 1
            '''
            self.tabla.execute(consulta)
            version = self.tabla.fetchone()
            return version
            
        except Exception as e:
            showwarning("Advertencia", f"Error al cargar estadísticas.\n{e}")
        
    def jugador_mas_vendido(self):
        try:
            consulta = '''
            SELECT jugador, sum(cantidad) as ventas_jugador FROM ventas v
            JOIN productos p ON v.id_producto = p.id_producto
            GROUP BY jugador
            ORDER BY ventas_jugador DESC, precio_total DESC
            LIMIT 1
            '''
            self.tabla.execute(consulta)
            jugador = self.tabla.fetchone()
            return jugador
            
        except Exception as e:
            showwarning("Advertencia", f"Error al cargar estadísticas.\n{e}")
            
    
    def equipo_mas_vendido(self):
        try:
            consulta = '''
            SELECT equipo, sum(cantidad) as ventas_equipo FROM ventas v
            JOIN productos p ON v.id_producto = p.id_producto
            GROUP BY equipo
            ORDER BY ventas_equipo DESC, precio_total DESC
            LIMIT 1
            '''
            self.tabla.execute(consulta)
            equipo = self.tabla.fetchone()
            return equipo
            
        except Exception as e:
            showwarning("Advertencia", f"Error al cargar estadísticas.\n{e}")
            
            
    def color_mas_vendido(self):
        try:
            consulta = '''
            SELECT color, sum(cantidad) as ventas_color FROM ventas v
            JOIN productos p ON v.id_producto = p.id_producto
            GROUP BY color
            ORDER BY ventas_color DESC
            LIMIT 1
            '''
            self.tabla.execute(consulta)
            color = self.tabla.fetchone()
            return color
            
        except Exception as e:
            showwarning("Advertencia", f"Error al cargar estadísticas.\n{e}")
            
    def talle_mas_vendido(self):
        try:
            consulta = '''
            SELECT talle, sum(cantidad) AS ventas_talle FROM ventas
            GROUP BY talle
            ORDER BY ventas_talle DESC
            LIMIT 1
            '''
            self.tabla.execute(consulta)
            talle = self.tabla.fetchone()
            return talle
            
        except Exception as e:
            showwarning("Advertencia", f"Error al cargar estadísticas.\n{e}")
    
    
    def camiseta_menos_vendida(self):
        try:
            consulta = '''
            SELECT nombre_producto, jugador, color, precio, p.id_producto, sum(cantidad) AS ventas_producto FROM ventas v
            JOIN productos p ON v.id_producto = p.id_producto 
            GROUP BY v.id_producto
            ORDER BY ventas_producto ASC, precio_total ASC
            LIMIT 1
            '''
            self.tabla.execute(consulta)
            camiseta = self.tabla.fetchone()
            return camiseta
            
        except Exception as e:
            showwarning("Advertencia", f"Error al cargar estadísticas.\n{e}")
    
    def marca_menos_vendida(self):
        try:
            consulta = '''
            SELECT marca, sum(cantidad) AS ventas_marca FROM ventas v
            JOIN productos p ON v.id_producto = p.id_producto
            GROUP BY marca 
            ORDER BY ventas_marca ASC
            LIMIT 1
            '''
            self.tabla.execute(consulta)
            marca = self.tabla.fetchone()
            return marca
            
        except Exception as e:
            showwarning("Advertencia", f"Error al cargar estadísticas.\n{e}")
            
    def version_menos_vendida(self):
        try:
            consulta = '''
            SELECT version, sum(cantidad) as ventas_version FROM ventas v
            JOIN productos p ON v.id_producto = p.id_producto
            GROUP BY version
            ORDER BY ventas_version ASC
            LIMIT 1
            '''
            self.tabla.execute(consulta)
            version = self.tabla.fetchone()
            return version
            
        except Exception as e:
            showwarning("Advertencia", f"Error al cargar estadísticas.\n{e}")
    
    
    def jugador_menos_vendido(self):
        try:
            consulta = '''
            SELECT jugador, sum(cantidad) as ventas_jugador FROM ventas v
            JOIN productos p ON v.id_producto = p.id_producto
            GROUP BY jugador
            ORDER BY ventas_jugador ASC, precio_total ASC
            LIMIT 1
            '''
            self.tabla.execute(consulta)
            jugador = self.tabla.fetchone()
            return jugador
            
        except Exception as e:
            showwarning("Advertencia", f"Error al cargar estadísticas.\n{e}")
            
    def equipo_menos_vendido(self):
        try:
            consulta = '''
            SELECT equipo, sum(cantidad) as ventas_equipo FROM ventas v
            JOIN productos p ON v.id_producto = p.id_producto
            GROUP BY equipo
            ORDER BY ventas_equipo ASC, precio_total ASC
            LIMIT 1
            '''
            self.tabla.execute(consulta)
            equipo = self.tabla.fetchone()
            return equipo
            
        except Exception as e:
            showwarning("Advertencia", f"Error al cargar estadísticas.\n{e}")
            
            
    def color_menos_vendido(self):
        try:
            consulta = '''
            SELECT color, sum(cantidad) as ventas_color FROM ventas v
            JOIN productos p ON v.id_producto = p.id_producto
            GROUP BY color
            ORDER BY ventas_color ASC
            LIMIT 1
            '''
            self.tabla.execute(consulta)
            color = self.tabla.fetchone()
            return color
            
        except Exception as e:
            showwarning("Advertencia", f"Error al cargar estadísticas.\n{e}")
            
    def talle_menos_vendido(self):
        try:
            consulta = '''
            SELECT talle, sum(cantidad) AS ventas_talle FROM ventas
            GROUP BY talle
            ORDER BY ventas_talle ASC
            LIMIT 1
            '''
            self.tabla.execute(consulta)
            talle = self.tabla.fetchone()
            return talle
            
        except Exception as e:
            showwarning("Advertencia", f"Error al cargar estadísticas.\n{e}")
            
    def camiseta_mas_cara(self):
        try:
            consulta = '''
            SELECT nombre_producto, jugador, color, precio, p.id_producto, sum(cantidad) AS ventas_producto FROM ventas v
            JOIN productos p ON v.id_producto = p.id_producto 
            GROUP BY v.id_producto
            ORDER BY precio DESC, ventas_producto DESC
            LIMIT 1
            '''
            self.tabla.execute(consulta)
            camiseta = self.tabla.fetchone()
            return camiseta
            
        except Exception as e:
            showwarning("Advertencia", f"Error al cargar estadísticas.\n{e}")
            
    def camiseta_mas_barata(self):
        try:
            consulta = '''
            SELECT nombre_producto, jugador, color, precio, p.id_producto, sum(cantidad) AS ventas_producto FROM ventas v
            JOIN productos p ON v.id_producto = p.id_producto 
            GROUP BY v.id_producto
            ORDER BY precio ASC, ventas_producto DESC
            LIMIT 1
            '''
            self.tabla.execute(consulta)
            camiseta = self.tabla.fetchone()
            return camiseta
            
        except Exception as e:
            showwarning("Advertencia", f"Error al cargar estadísticas.\n{e}")
            
    def total_recaudado(self):
        try:
            consulta = '''
            SELECT SUM(precio_total) FROM ventas
            '''
            self.tabla.execute(consulta)
            total = self.tabla.fetchone()[0]
            return total
            
        except Exception as e:
            showwarning("Advertencia", f"Error al cargar estadísticas.\n{e}")
            
    
    def top_5_jugadores(self):
        try:
            consulta = '''
            SELECT jugador, sum(cantidad) as ventas_jugador FROM ventas v
            JOIN productos p ON v.id_producto = p.id_producto
            GROUP BY jugador
            ORDER BY ventas_jugador DESC, precio_total DESC
            '''
            self.tabla.execute(consulta)
            jugadores = self.tabla.fetchall()
            return jugadores
            
        except Exception as e:
            showwarning("Advertencia", f"Error al cargar estadísticas.\n{e}")
            
    def top_5_equipos(self):
        try:
            consulta = '''
            SELECT equipo, sum(cantidad) as ventas_equipo FROM ventas v
            JOIN productos p ON v.id_producto = p.id_producto
            GROUP BY equipo
            ORDER BY ventas_equipo DESC, precio_total DESC
            LIMIT 5
            '''
            self.tabla.execute(consulta)
            equipos = self.tabla.fetchall()
            return equipos
            
        except Exception as e:
            showwarning("Advertencia", f"Error al cargar estadísticas.\n{e}")
            
    def mejor_cliente(self):
        try:
            consulta = '''
            SELECT nombre, apellido, username, sum(cantidad) AS compras_cliente FROM usuarios u
            JOIN ventas v ON u.id_usuario = v.id_usuario
            GROUP BY v.id_usuario
            ORDER BY compras_cliente DESC, precio_total DESC
            LIMIT 1
            '''
            self.tabla.execute(consulta)
            cliente = self.tabla.fetchone()
            return cliente
            
        except Exception as e:
            showwarning("Advertencia", f"Error al cargar estadísticas.\n{e}")
            
    def lista_compras(self):
        try:
            consulta = '''
            SELECT c.id_producto, nombre_producto, color, jugador, marca, version, precio_total, talle, cantidad, username
            FROM compras c
            JOIN productos_proveedores p, usuarios u ON c.id_producto = p.id_producto AND c.id_usuario = u.id_usuario
            '''
            self.tabla.execute(consulta)
            lista = self.tabla.fetchall()
            return lista
            
        except Exception as e:
            showwarning("Advertencia", f"Error al cargar estadísticas.\n{e}")
            
            
    def lista_ventas(self):
        try:
            consulta = '''
            SELECT id_venta, pd.id_producto, nombre_producto, jugador, version, color, precio_total, cantidad, talle, username
            FROM productos pd
            JOIN ventas v, usuarios u ON pd.id_producto = v.id_producto AND v.id_usuario = u.id_usuario
            '''
            self.tabla.execute(consulta)
            lista = self.tabla.fetchall()
            return lista
            
        except Exception as e:
            showwarning("Advertencia", f"Error al cargar estadísticas.\n{e}")
            
    
    def informacion_venta(self, id_venta):
        try:
            consulta = '''
            SELECT pd.id_producto, nombre_proveedor, nombre_producto, precio, precio_total, cantidad, talle, marca, version, jugador, color, username, notas
            FROM productos pd
            JOIN ventas v, usuarios u, proveedores p ON pd.id_producto = v.id_producto AND v.id_usuario = u.id_usuario AND pd.id_proveedor = p.id_proveedor
            WHERE id_venta = ?
            '''
            self.tabla.execute(consulta, id_venta)
            lista = self.tabla.fetchall()
            return lista
            
        except Exception as e:
            showwarning("Advertencia", f"Error al cargar estadísticas.\n{e}")
