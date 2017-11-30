# KMS QR Code generator

## Tworzenie środowiska wirtualnego

```
virtualenv -p python3 env
env/bin/pip install -r requirements.txt
```

## Przykłady

### bulk.py

- Pobierz arkusz Członkowie jako .csv

- Odpal bulk.py
```
env/bin/python bulk.py --csv czlonkowie.csv
```

- Wynik pojawi się w katalogu ```out/```