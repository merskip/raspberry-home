# raspberry-home
![raspberry_home](https://github.com/merskip/raspberry-home/workflows/raspberry_home/badge.svg?branch=master)

Manage your home with raspberry Pi

# Install on Raspberry Pi
```shell
$ sudo apt install python3
$ sudo pip3 install schedule
$ sudo pip3 install w1thermsensor
```

## Example of config.ini
```
[database]
url=mysql+mysqldb://root:root@localhost:3306/raspberry_home

[scheduler]
every_minutes=5
```

## Launch
```shell
$ sudo python3 __main__.py
```

