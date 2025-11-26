import machine
import network
import json
import time
from umqtt.simple import MQTTClient


def get_device_mac():
    """
    Obtiene la dirección MAC del ESP32.
    Retorna el MAC en formato string (ej: "aabbccddeeff").
    """
    mac = machine.unique_id()
    return ''.join('{:02x}'.format(b) for b in mac)


def do_subscribe(mqtt_config, topics_json):
    """
    Función de subscribe. Se subscribe a los topics en el servidor MQTT.
    
    Parámetros:
    -----------
    mqtt_config : dict
        Configuración MQTT con claves:
        - 'host': dirección IP del servidor MQTT
        - 'port': puerto del servidor MQTT (default: 1883)
        - 'client_id': ID del cliente MQTT
        - 'user': usuario MQTT (opcional)
        - 'password': contraseña MQTT (opcional)
    
    topics_json : dict o list
        JSON que indica a qué topics subscribirse.
        - Si es dict con clave 'topics': lista de topics deseados
        - Si es una lista: lista de topics deseados
        - Si está vacío: se devuelven todos los topics asociados al MAC
    
    Retorna:
    --------
    dict : Información de los topics suscritos con su contenido
        Formato: {
            'mac': 'aabbccddeeff',
            'subscribed_topics': ['MAC/topic1', 'MAC/topic2'],
            'messages': {
                'MAC/topic1': 'mensaje_recibido',
                'MAC/topic2': 'mensaje_recibido'
            }
        }
    """
    
    # Obtener MAC del ESP32
    device_mac = get_device_mac()
    
    # Normalizar entrada de topics
    if isinstance(topics_json, dict):
        requested_topics = topics_json.get('topics', [])
    elif isinstance(topics_json, list):
        requested_topics = topics_json
    else:
        requested_topics = []
    
    # Validar configuración MQTT
    if not isinstance(mqtt_config, dict):
        raise ValueError("mqtt_config debe ser un diccionario")
    
    host = mqtt_config.get('host')
    port = mqtt_config.get('port', 1883)
    client_id = mqtt_config.get('client_id', device_mac)
    user = mqtt_config.get('user')
    password = mqtt_config.get('password')
    
    if not host:
        raise ValueError("El host MQTT es requerido en mqtt_config")
    
    # Crear cliente MQTT
    try:
        if user and password:
            client = MQTTClient(client_id, host, port, user=user, password=password)
        else:
            client = MQTTClient(client_id, host, port)
        
        client.connect()
        print(f"[INFO] Conectado al servidor MQTT {host}:{port}")
    except Exception as e:
        print(f"[ERROR] No se pudo conectar al servidor MQTT: {e}")
        return {
            'mac': device_mac,
            'subscribed_topics': [],
            'messages': {},
            'error': str(e)
        }
    
    # Preparar topics con el MAC del ESP32
    topics_to_subscribe = []
    
    if requested_topics:
        # Si hay topics solicitados, usarlos en el orden proporcionado
        for topic in requested_topics:
            full_topic = f"{device_mac}/{topic}"
            topics_to_subscribe.append(full_topic)
    else:
        # Si no hay topics, obtener todos los topics asociados al MAC
        # En este caso, nos subscribimos a un wildcard del MAC
        full_topic = f"{device_mac}/#"
        topics_to_subscribe.append(full_topic)
        print(f"[INFO] Sin topics específicos. Suscribiendo a todos los topics del MAC: {full_topic}")
    
    # Suscribirse a los topics
    messages = {}
    subscribed_topics = []
    
    try:
        for topic in topics_to_subscribe:
            client.subscribe(topic)
            subscribed_topics.append(topic)
            print(f"[INFO] Suscrito a: {topic}")
    except Exception as e:
        print(f"[ERROR] Error al suscribirse a topics: {e}")
        client.disconnect()
        return {
            'mac': device_mac,
            'subscribed_topics': subscribed_topics,
            'messages': {},
            'error': str(e)
        }
    
    # Esperar y recibir mensajes (con timeout de 5 segundos por topic)
    timeout_per_topic = 5
    start_time = time.time()
    
    try:
        while (time.time() - start_time) < (len(topics_to_subscribe) * timeout_per_topic):
            # Procesar mensajes MQTT
            client.check_msg()
            
            # Intentar recibir mensaje si está disponible
            try:
                # Usar wait_msg con timeout pequeño
                client.wait_msg()
            except OSError:
                # Timeout esperado
                pass
            
            time.sleep(0.1)
    except Exception as e:
        print(f"[ERROR] Error al recibir mensajes: {e}")
    
    # Desconectar
    try:
        client.disconnect()
        print("[INFO] Desconectado del servidor MQTT")
    except:
        pass
    
    return {
        'mac': device_mac,
        'subscribed_topics': subscribed_topics,
        'messages': messages,
        'timestamp': time.time()
    }


def subscribe_with_callback(mqtt_config, topics_json, callback=None):
    """
    Función alternativa de subscribe con callback personalizado.
    
    Parámetros:
    -----------
    mqtt_config : dict
        Configuración MQTT
    
    topics_json : dict o list
        JSON con los topics a los que subscribirse
    
    callback : function
        Función callback que se ejecuta cuando llega un mensaje.
        Firma: callback(topic, message)
    
    Retorna:
    --------
    MQTTClient : Cliente MQTT activo para control manual
    """
    
    device_mac = get_device_mac()
    
    # Normalizar entrada de topics
    if isinstance(topics_json, dict):
        requested_topics = topics_json.get('topics', [])
    elif isinstance(topics_json, list):
        requested_topics = topics_json
    else:
        requested_topics = []
    
    host = mqtt_config.get('host')
    port = mqtt_config.get('port', 1883)
    client_id = mqtt_config.get('client_id', device_mac)
    user = mqtt_config.get('user')
    password = mqtt_config.get('password')
    
    # Crear cliente MQTT
    if user and password:
        client = MQTTClient(client_id, host, port, user=user, password=password)
    else:
        client = MQTTClient(client_id, host, port)
    
    # Establecer callback personalizado
    if callback:
        client.set_callback(callback)
    
    # Conectar
    client.connect()
    print(f"[INFO] Conectado al servidor MQTT {host}:{port}")
    
    # Preparar topics
    if requested_topics:
        for topic in requested_topics:
            full_topic = f"{device_mac}/{topic}"
            client.subscribe(full_topic)
            print(f"[INFO] Suscrito a: {full_topic}")
    else:
        full_topic = f"{device_mac}/#"
        client.subscribe(full_topic)
        print(f"[INFO] Suscrito a todos los topics del MAC: {full_topic}")
    
    print("[INFO] Cliente MQTT listo para recibir mensajes")
    return client