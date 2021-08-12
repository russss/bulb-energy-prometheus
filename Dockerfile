FROM python:3-slim

WORKDIR /app

COPY . .
RUN pip3 install -e .

CMD ["/usr/local/bin/bulb-energy-prometheus"]
