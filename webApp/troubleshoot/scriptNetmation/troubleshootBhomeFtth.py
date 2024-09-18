from common.utils import RouterOsGetApi
import json

secret = RouterOsGetApi('103.73.72.182', 'jul', 'Juliandi123!@#', '8728', '/ppp/secret')

print(json.dumps(secret, indent=4))