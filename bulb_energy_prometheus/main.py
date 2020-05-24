from prometheus_client import start_http_server, Gauge, Summary
import os
import sys
import asyncio
import aiohttp
import pysmartthings

gauge_electricity = Gauge("bulb_electricity_used_kwh", "Electricity meter reading")
gauge_gas = Gauge("bulb_gas_used_units", "Gas meter reading")
refresh_time = Summary("smartthings_refresh_time_seconds", "Time taken to fetch data from SmartThings")


async def get_device(api):
    for device in await api.devices():
        if device.name == "smartthings-energy-control-bulb":
            return device
    return None


async def main(api_token):
    async with aiohttp.ClientSession() as session:
        api = pysmartthings.SmartThings(session, api_token)
        device = await get_device(api)
        if device is None:
            print("Can't find energy monitor device")
            return

        print("Connected, running...")
        while True:
            with refresh_time.time():
                await device.status.refresh()
            gauge_electricity.set(device.status.values.get("energy"))
            gauge_gas.set(device.status.values.get("gasMeter"))
            await asyncio.sleep(10)


def run():
    print("Starting...")

    if not os.environ.get("SMARTTHINGS_API_TOKEN"):
        print(
            "SmartThings API Token should be provided in the SMARTTHINGS_API_TOKEN environment variable."
        )
        sys.exit(1)

    start_http_server(8023)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main(os.environ["SMARTTHINGS_API_TOKEN"]))
