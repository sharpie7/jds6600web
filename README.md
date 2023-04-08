# JDS6600 Web

Hacky web-server to control the JDS6600 signal generator over a serial connection.

Only supports the normal signal-generator mode on Channel 1.

## Running

Requires pyserial to be installed.

Communications provided using [JDS6600 Python](https://github.com/on1arf/jds6600_python/).

Use
```
python3 main.py <Server Name> <Port Number> <Serial Port>
```

eg
```
python3 main.py localhost 8888 COM3
```
