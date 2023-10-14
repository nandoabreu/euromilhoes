#!/usr/bin/env python3
from os import makedirs
from time import sleep

import requests
import ssl
import urllib3

source_url: str = 'https://www.jogossantacasa.pt/web/SCCartazResult/euroMilhoes'
oldest_draw, newest_draw = 373.0, 12994.0  # 373.0 is the first registered draw number; there are 1600 draws by Oct/2023
target_raw_directory: str = 'data/raw'
regular_pause_seconds: float = 3
pause_every_n_requests: int = 15

makedirs(target_raw_directory, exist_ok=True)


class TLSAdapter(requests.adapters.HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        urllib3.disable_warnings()
        ctx = ssl.create_default_context()
        ctx.set_ciphers('DEFAULT@SECLEVEL=1')
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_OPTIONAL
        kwargs['ssl_context'] = ctx
        return super(TLSAdapter, self).init_poolmanager(*args, **kwargs)


responses_size = 0
print(f'Start data extraction from {source_url}', flush=True)
print(f'Raw data files will be stored in {target_raw_directory}\n')

for current_draw in range(int(oldest_draw), int(newest_draw) + 1):
    current_draw = f'{current_draw:.1f}'
    raw_storage_file = f'{target_raw_directory}/draw-{float(current_draw):07.1f}.html'
    print(f'Scrap draw ref. {current_draw} and store in {raw_storage_file}')

    if not float(current_draw) % pause_every_n_requests:
        sleep(regular_pause_seconds)  # Prevent possible request flood

    session = requests.session()
    session.mount('https://', TLSAdapter())
    post_data = dict(selectContest=current_draw, Consultar='Consultar')
    response = session.post(source_url, verify=False, data=post_data)
    responses_size += len(response.content)

    if response.status_code != 200:
        print(f'Scrap request responded HTTP status {response.status_code}')
        continue

    if 'Últimos Resultados' not in response.text:
        print("Expected title not found in response")
        continue

    if 'class="dataInfo"' not in response.text:
        print("Expected date container not found in response")
        continue

    if 'Data do Sorteio' not in response.text:
        print("Expected draw date label not found in response")
        continue

    with open(raw_storage_file, 'wb') as f:
        f.write(response.content)

    print('Raw data extracted and stored')

print(f'Fetched data: {responses_size} bytes')
