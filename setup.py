from setuptools import setup

setup(
    name="bulb-energy-prometheus",
    version="1.0",
    description="Prometheus exporter for Bulb Energy smart meters",
    license="mit",
    author="Russ Garrett",
    author_email="russ@garrett.co.uk",
    url="https://github.com/russss/bulb-energy-prometheus",
    classifiers=[
        "development status :: 4 - beta",
        "license :: osi approved :: mit license",
        "programming language :: python :: 3",
    ],
    keywords="prometheus energy smets2 smartthings bulb",
    python_requires=">=3.4",
    packages=["bulb_energy_prometheus"],
    install_requires=[
        "pysmartthings",
        "prometheus_client",
    ],
    entry_points={"console_scripts": {"bulb-energy-prometheus=bulb_energy_prometheus.main:run"}},
)
