# Bulb Energy Prometheus exporter

This is a [Prometheus](https://prometheus.io/) exporter for [Bulb Energy](https://bulb.co.uk/) customers with SMETS2 smart meters. It allows you to fetch electricity and gas meter readings and exposes them as a Prometheus endpoint.

This relies on Bulb's SmartThings integration to exfiltrate the meter readings. It will not work with other energy suppliers.

Ideally we would be able to integrate directly with the SMETS2 home area network, but this (still!) doesn't appear to be possible.

Electricity meter readings are sent to SmartThings every minute or so, but gas meter readings are only updated a few times per day (due to battery life). This exporter polls the SmartThings API every 10 seconds for an updated reading - it's technically possible to subscribe to event notifications but this requires opening a port for webhooks and life is too short.

## Configuration

* First, you'll need to set up the [SmartThings integration](https://help.bulb.co.uk/hc/en-us/articles/360034651651-Setting-up-SmartThings-Energy-Control-STEC-) on your Chameleon IHD.
* Next, you'll need to [generate a personal access token on the SmartThings website](https://account.smartthings.com/tokens). The token needs the "List all devices" and "See all devices" permissions.

### Install using pip

Install this exporter using `pip3 install git+https://github.com/russss/bulb-energy-prometheus#egg=bulb-energy-prometheus`. Now you can run the exporter as `SMARTTHINGS_API_TOKEN=<token> bulb-energy-prometheus`, where `<token>` is the token you generated in the previous step. The Prometheus endpoint should be visible at `http://localhost:8023`.

You'll want to run the exporter under a process supervisor, as it will crash if it can't access the SmartThings API.

### Docker

Alternatively, you can use [the Docker image](https://hub.docker.com/repository/docker/russss/bulb-energy-prometheus). Set the `SMARTTHINGS_API_TOKEN` environment variable as above.

## Example output
An example of the exported metrics:
```
# HELP bulb_electricity_used_kwh Electricity meter reading
# TYPE bulb_electricity_used_kwh gauge
bulb_electricity_used_kwh 787.517
# HELP bulb_gas_used_units Gas meter reading
# TYPE bulb_gas_used_units gauge
bulb_gas_used_units 1871.826
# HELP smartthings_refresh_time_seconds Time taken to fetch data from SmartThings
# TYPE smartthings_refresh_time_seconds summary
smartthings_refresh_time_seconds_count 3.0
smartthings_refresh_time_seconds_sum 0.13676668800000036
# TYPE smartthings_refresh_time_seconds_created gauge
smartthings_refresh_time_seconds_created 1.590315433754121e+09
```
