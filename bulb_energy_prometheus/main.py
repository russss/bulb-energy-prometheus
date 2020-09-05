from prometheus_client import start_http_server, Gauge, Summary
import os
import sys
import asyncio
import aiohttp
import pysmartthings

# Newly-initialised gauges are set to 0, which is bad. Only create the gauge once we have a valid reading.
gauge_electricity = None
gauge_gas = None
refresh_time = Summary(
    "smartthings_refresh_time_seconds", "Time taken to fetch data from SmartThings"
)


async def get_device(api):
    for device in await api.devices():
        if device.name == "smartthings-energy-control-bulb":
            return device
    return None


def valid_reading(reading, previous_reading):
    """ Check if a reading is valid.

        The SmartThings API may return zero or the reading may go backwards, which confuses things.
        Ensure that we have a valid, increasing reading here.
    """
    return (
        reading is not None
        and reading > 0
        and (previous_reading is None or reading >= previous_reading)
    )


async def main(api_token):
    global gauge_electricity, gauge_gas

    async with aiohttp.ClientSession() as session:
        api = pysmartthings.SmartThings(session, api_token)
        device = await get_device(api)
        if device is None:
            print("Can't find energy monitor device")
            return

        gas_reading = None
        electricity_reading = None

        print("Connected, running...")
        while True:
            with refresh_time.time():
                await device.status.refresh()

            new_electricity = device.status.values.get("energy")
            if valid_reading(new_electricity, electricity_reading):
                electricity_reading = new_electricity
            else:
                print(
                    f"Invalid electricity reading: {new_electricity} (previous:"
                    f" {electricity_reading})"
                )

            new_gas = device.status.values.get("gasMeter")
            if valid_reading(new_gas, gas_reading):
                gas_reading = new_gas
            else:
                print(f"Invalid gas reading: {new_gas} (previous: {gas_reading})")

            if electricity_reading:
                if gauge_electricity is None:
                    gauge_electricity = Gauge("bulb_electricity_used_kwh", "Electricity meter reading")
                gauge_electricity.set(electricity_reading)

            if gas_reading:
                if gauge_gas is None:
                    gauge_gas = Gauge("bulb_gas_used_units", "Gas meter reading")
                gauge_gas.set(gas_reading)

            await asyncio.sleep(10)


def run():
    print("Starting...")

    if not os.environ.get("SMARTTHINGS_API_TOKEN"):
        print(
            "SmartThings API Token should be provided in the SMARTTHINGS_API_TOKEN"
            " environment variable."
        )
        sys.exit(1)

    start_http_server(8023)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main(os.environ["SMARTTHINGS_API_TOKEN"]))
