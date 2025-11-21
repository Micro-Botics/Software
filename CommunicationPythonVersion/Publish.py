import machine
import network


def publisj(json_entry_file):
    """
    como primer parámetro se recibe infomación sobre servidor, suponer que la conexión ya está establecida. tiene forma de una lista:
    (MQTT_HOST_IP,PORT,CLIENT_ID)
    Publicar topics en el servidor, usar json proporcionado y añadir MAC del esp como nombre principal para el topic(MAC_DE_ESP/JSON_Content),
    debe publicar JSON en su topic correspondiente cuando recibe un JSON.
    """
    return json_entry_file
