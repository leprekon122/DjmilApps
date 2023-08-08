import asyncio
import os

import psycopg2
import websockets
import json
from .models import SkySafeData
from asgiref.sync import sync_to_async


async def make_api_call():
    async with websockets.connect(f"{os.getenv('SkySafeUrl')}", extra_headers={
        "Authorization": f"bearer {os.getenv('SkySafeApiKey')}"}) as wb:

        conn = psycopg2.connect(
            f"dbname=vidma, user=djmil_admin, password={os.getenv('djmil67dev')}, host=localhost,"
            f"port=5432")
        curs = conn.cursor()

        while True:
            res = json.loads(await wb.recv())
            if res['type'] == 'target-report':
                curs = curs.execute("INSERT INTO skysafedata (sensor_id, station_id, persistent_id,"
                                   "tgt_model, rc_id, dl_freq, dl_rssi, ul_rssi, home_position"
                                   "app_position, tgt_position, tgt_alt_msl, tgt_alt_hae, tgt_alt_prs) VALUES "
                                   "(res['msg']['sensor_id']), res['msg']['station_id'], res['msg']['persistent_id'],"
                                   "res['msg']['tgt_model'], res['msg']['rc_id'], res['msg']['dl_freq'],"
                                   "res['msg']['dl_rssi'], res['msg']['ul_rssi'], res['msg']['home_position'],"
                                   "res['msg']['home_position'], res['msg']['tgt_position'], res['msg']['tgt_alt_msl'],"
                                   "res['msg']['tgt_alt_hae'], res['msg']['tgt_alt_prs']")
                curs.curs.fetchall()



                #return {'sensor_id': res['msg']['sensor_id'], 'station_id': res['msg']['station_id'],
                #        'persistent_id': res['msg']['persistent_id'], 'tgt_model': res['msg']['tgt_model'],
                #        'rc_id': res['msg']['rc_id'], 'dl_freq': res['msg']['dl_freq'],
                #        'dl_rssi': res['msg']['dl_rssi'], 'ul_rssi': res['msg']['ul_rssi'],
                #        'home_position': res['msg']['home_position'], 'app_position': res['msg']['home_position'],
                #        'tgt_position': res['msg']['tgt_position'], 'tgt_alt_msl': res['msg']['tgt_alt_msl'],
                #        'tgt_alt_hae': res['msg']['tgt_alt_hae'], 'tgt_alt_prs': res['msg']['tgt_alt_prs']
                #        }

            print(res)
            await asyncio.sleep(10)
            print('connection continue')
