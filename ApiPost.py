from typing import List, Set
from digi.xbee.devices import XBeeDevice

# Endereco para enviar os dados
host = "https://sistemas.acidinformatica.com.br:8443/acid/wsrw3/sensor/api/"
# Endereco para retorno de dados
get_host = "https://sistemas.acidinformatica.com.br:8443/acid/wsrw3/dados/"
# Porta usb usada para comunicacao!!!
PORT = "/dev/ttyUSB0"
# Velocidade da porta
BAUD_RATE = 9600
# Tags rfid dos containers.
tags = (
    "00000000000000202078B517",
    "00000000000000202078B50E",
    "00000000000000202078B51B",
    "000000000000002020788D6D",
    "000000000000002020794CD3",
    "00000000000000202078D85A",
    "00000000000000202078AFB8",
    "00000000000000202078D856",
    "00000000000000202078B524")
# Id dos nodos sensores.
nodes = (
    "6eba",
    "6ebc",
    "6ebd",
    "6ebe",
    "6ebf",
    "6eca",
    "6ecb",
    "6ecd",
    "6ece")


def main():
    device = XBeeDevice(PORT, BAUD_RATE)
    device.open()
    while 1:
        def data_receive_callback(xbee_message):
            #  Separa os dados em uma lista
            data: List[str] = str.split(xbee_message.data.decode(), ",", len(xbee_message.data))
            # Verifica se existem dados
            if data != 0:
                index = nodes.index(data[0])
                # Formata os dados a serem enviados em uma array list
                data_arr = [{"tag": tags[index], "id": str(data[0]), "tipo": "01",
                             "temperatura": str(data[12])},
                            {"tag": tags[index], 'id': data[0], 'tipo': '02', "umidade": data[11]},
                            {"tag": tags[index], 'id': data[0], 'tipo': '03', "x1": data[1], "x2": data[2],
                             "x3": data[3]},
                            {"tag": tags[index], 'id': data[0], 'tipo': '04', "x1": data[4], "x2": data[5],
                             "x3": data[6]},
                            {"tag": tags[index], 'id': data[0], 'tipo': '05', "x1": data[7], "x2": data[8],
                             "x3": data[9]},
                            {"tag": tags[index], 'id': data[0], 'tipo': '06', "bar": data[10], "alt": data[21]},
                            {"tag": tags[index], 'id': data[0], 'tipo': '07', "latitude": data[16],
                             "longitude": data[17], "ns": data[19], "lo": data[20], "hr_utc": data[15],
                             "data": data[23],
                             "altitude": data[22], "velocidade": data[18]},
                            {"tag": tags[index], 'id': data[0], 'tipo': '08', "gas": data[13]},
                            {"tag": tags[index], 'id': data[0], 'tipo': '09', "vibracao": data[14]}]

            # Percorre a lista para que possamos enviar os dados
            for obj in data_arr:
                print(obj)  # Uso para debug
                # Faz o post dos dados da lista, no host destino. Usando o formato json.s
                # print(requests.post(host, json=obj))
            print("Mensagem Recebida")

        # Callback para recebimento de dados via porta serial.
        device.add_data_received_callback(data_receive_callback)
        print("Waiting for data...\n")
        input()


if __name__ == '__main__':
    main()
