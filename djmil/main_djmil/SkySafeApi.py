import asyncio
import os
import websockets
import json
from .models import SkySafeData
from datetime import datetime


async def make_api_call():
    async with websockets.connect(f"{os.getenv('SkySafeUrl')}",
                                  extra_headers={"Authorization": f"bearer {os.getenv('SkySafeApiKey')}"}) as wb:
        while True:
            res = json.loads(await wb.recv())

            if res['type'] == 'target-report':
                print(res)

                if res['msg']['home_position'] is not None:
                    home_position_lan = res['msg']['home_position'][1]
                    home_position_lon = res['msg']['home_position'][0]
                else:
                    home_position_lan = 0.00000000
                    home_position_lon = 0.00000000

                if res['msg']['app_position'] is not None:
                    app_position_lan = res['msg']['app_position'][1]
                    app_position_lon = res['msg']['app_position'][0]
                else:
                    app_position_lan = 0.00000000
                    app_position_lon = 0.00000000

                if res['msg']['tgt_position'] is not None:
                    tgt_position_lan = res['msg']['tgt_position'][1]
                    tgt_position_lon = res['msg']['tgt_position'][0]
                else:
                    tgt_position_lan = 0.0000000
                    tgt_position_lon = 0.0000000
                await SkySafeData.objects.acreate(sensor_id=res['msg']['sensor_id'],
                                                  station_id=res['msg']['station_id'],
                                                  persistent_id=res['msg']['persistent_id'],
                                                  tgt_model=res['msg']['tgt_model'], rc_id=res['msg']['rc_id'],
                                                  dl_freq=res['msg']['dl_freq'], dl_rssi=res['msg']['dl_rssi'],
                                                  ul_rssi=res['msg']['ul_rssi'],
                                                  home_position_lan=home_position_lan,
                                                  home_position_lon=home_position_lon,
                                                  app_position_lan=app_position_lan,
                                                  app_position_lon=app_position_lon,
                                                  tgt_position_lan=tgt_position_lan,
                                                  tgt_position_lon=tgt_position_lon,
                                                  tgt_alt_msl=res['msg']['tgt_alt_msl'],
                                                  tgt_alt_hae=res['msg']['tgt_alt_hae'],
                                                  tgt_alt_prs=res['msg']['tgt_alt_prs'],
                                                  write_time=datetime.today()
                                                  )
                await asyncio.sleep(2)
