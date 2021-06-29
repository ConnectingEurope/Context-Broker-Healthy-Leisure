FROM python:3.7-stretch

WORKDIR /app

# copy the dependencies file to the working directory
COPY requirements.txt .

RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

COPY process_data ./process_data
COPY modbus_providers.py .

CMD ["python3", "-u", "/app/modbus_providers.py"]