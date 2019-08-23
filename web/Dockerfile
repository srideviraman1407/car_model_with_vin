#pull python 3 image
FROM python:latest
#create a work dir
WORKDIR /usr/src/vin_decode.py
#copy requirements.txt into workdir created above
COPY requirements.txt ./
#Install all requirements
RUN python3 -m pip install --user --no-cache-dir -r requirements.txt
# Copy entire project into workdir
COPY . .
# Run our app
CMD ["python", "vin_decode.py"]
