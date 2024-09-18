from routeros_api import RouterOsApiPool
import json

def get_traffic_data():
    # Connect ke RouterOS
    connection = RouterOsApiPool(
        '103.73.72.162',
        username='jul',
        password='Juliandi123!@#',
        port=8728,
        plaintext_login=True
        )
    
    api = connection.get_api()
    
    # Ambil data traffic
    interface = api.get_resource('/interface')
    traffic = interface.call('monitor-traffic', { 'interface': 'vlan109', 'duration': '1s' })

    # Misalnya, data yang diambil hanya rx dan tx bytes dari interface ether1
    for data in traffic:
        rx_bytes = int(data['rx-bits-per-second'])/ 1000000
        tx_bytes = int(data['tx-bits-per-second'])/ 1000000

    # Kembalikan dalam format JSON
    connection.disconnect()

    result = ({
        'rx_bytes': int(rx_bytes),
        'tx_bytes': int(tx_bytes),
    })

    return result

print(json.dumps(get_traffic_data(), indent=4))