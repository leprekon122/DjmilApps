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

            print(res)
            if res['type'] == 'target-report':
                await SkySafeData.objects.acreate(sensor_id=res['msg']['sensor_id'],
                                                  station_id=res['msg']['station_id'],
                                                  persistent_id=res['msg']['persistent_id'],
                                                  tgt_model=res['msg']['tgt_model'], rc_id=res['msg']['rc_id'],
                                                  dl_freq=res['msg']['dl_freq'], dl_rssi=res['msg']['dl_rssi'],
                                                  ul_rssi=res['msg']['ul_rssi'],
                                                  home_position=res['msg']['home_position'],
                                                  app_position=res['msg']['home_position'],
                                                  tgt_position=res['msg']['tgt_position'],
                                                  tgt_alt_msl=res['msg']['tgt_alt_msl'],
                                                  tgt_alt_hae=res['msg']['tgt_alt_hae'],
                                                  tgt_alt_prs=res['msg']['tgt_alt_prs'],
                                                  write_time=datetime.today()
                                                  )
            await asyncio.sleep(2)
