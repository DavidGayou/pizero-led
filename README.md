# pizero-led

First install the library as stated in https://github.com/jgarff/rpi_ws281x


## Pull on startup and launch the controller

Copy the systemd service 
```
sudo cp src/systemd/pizero-led.service /lib/systemd/system/
```

Then enable it
```
sudo systemctl enable pizero-led.service
```

it will launch the src/sh/boot.sh at startup
