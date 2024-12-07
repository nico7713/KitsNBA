import requests
import tkinter.messagebox as msg

class JugadoresDestacados:
    def __init__(self):
        self.jugadores_api = {      # ids de los jugadores en api-nba
            "LeBron James": 265,
            "Stephen Curry": 124,
            "Giannis Antetokounmpo": 20,
            "James Harden": 216,
            "Kevin Durant": 153,
            "Jayson Tatum": 882,
            "Nikola Jokic": 279,
            "Luka Doncic": 963
        }
        
        self.jugadores_web_nba = {  # ids de los jugadores en nba.com
            "LeBron James": 2544,
            "Stephen Curry": 201939,
            "Giannis Antetokounmpo": 203507,
            "James Harden": 201935,
            "Kevin Durant": 201142,
            "Jayson Tatum": 1628369,
            "Nikola Jokic": 203999,
            "Luka Doncic": 1629029
        }
        
        
    def jugador_destacado(self, nombre_jugador):    # devolver mensaje del rendimiento del jugador con un link
        
        if nombre_jugador in self.jugadores_api.keys():
            
            try:
                x_rapidapi_key = "36280a3f5cmsh192975a3b31d253p18fe69jsn88a5fe0a5979"   # api key
                x_rapidapi_host = "api-nba-v1.p.rapidapi.com"                           # api host
                
                headers = {
                    "X-RapidAPI-Key": x_rapidapi_key,
                    "X-RapidAPI-Host": x_rapidapi_host
                }
                
                # Obtener datos de los partidos de la temporada actual del jugador
                url_partidos = (
                    f"https://api-nba-v1.p.rapidapi.com/players/statistics?"
                    f"id={self.jugadores_api[nombre_jugador]}&season={2024}"    # Buscar el jugador por su id y temporada actual
                )
                
                respuesta = requests.get(url_partidos, headers=headers)
                respuesta.raise_for_status()        # Levantar un error HTTP si la respuesta es incorrecta
                
                partidos = respuesta.json()         # Convertir la respuesta del servidor a formato json
                
                if partidos['response']:            # Si la respuesta no está vacía
                    ultimo_partido = partidos['response'][-1]   # Obtener estadísticas del último partido
                    puntos = ultimo_partido['points']           # Obtener puntos del jugador en el último partido

                    if puntos >= 25:    # Si el jugador tiene 25 o más puntos, devolver un mensaje con un enlace
                        mensaje = f"¡{puntos} puntos de {nombre_jugador} en el último partido!"
                        enlace = f"https://www.nba.com/player/{self.jugadores_web_nba[nombre_jugador]}/{nombre_jugador.replace(' ', '-').lower()}/videos"
                        return mensaje, enlace
                    else:
                        return None
                
                else:
                    return None
                
            # Posibles Excepciones    
            except requests.exceptions.RequestException as e:
                msg.showwarning("Advertencia", f"Error en la solicitud al servidor:\n{e}")
            except requests.exceptions.HTTPError as e2:
                msg.showwarning("Advertencia", f"Error HTTP:\n{e2}")
            except requests.exceptions.ConnectionError:
                msg.showwarning("Advertencia", "Error de conexión. Comprueba tu conexión a internet.")
            except requests.exceptions.Timeout:
                msg.showwarning("Advertencia", "Tiempo de espera agotado.")
            except KeyError:
                msg.showwarning("Advertencia", f"Error al cargar toda la información de la interfaz.")
            except ValueError:
                msg.showwarning("Advertencia", "Se recibió un valor inesperado del servidor.")
            except Exception as e3:
                msg.showwarning("Advertencia", f"Error desconocido: {e3}")
                
        else:
            return None