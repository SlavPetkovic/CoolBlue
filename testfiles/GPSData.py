import serial
import traceback

SERIAL_PORT = "/dev/serial0"
running = True


def ddmm2deg(sval):
    vals = sval.split(".")
    deg = vals[0][:-2]
    minit = vals[0][-2:] + "." + vals[1]
    return int(deg) + float(minit) / 60


def gpsProcess(data):
    print(data, "\t", end="")
    message = data[0:6]
    if (message == b'$GNRMC'):
        parts = data.decode().split(",")
        if parts[2] == 'V':
            # V = Warning, most likely, there are no satellites in view...
            print("GPS receiver warning")
        else:
            # OK
            lat = ddmm2deg(parts[3])
            lon = ddmm2deg(parts[5])
            ns = parts[4]
            ew = parts[6]
            sfmt = "{:.6f}"
            print("GPS Position:", sfmt.format(lat) + ns, ",", sfmt.format(lon) + ew)
            # Convert to +- type
            nlat = lat
            nlon = lon
            zoomlevel = 18
            if ns == "S":   nlat = 0 - lat
            if ew == "W":   nlon = 0 - lon
            url = "https://maps.google.com/maps?q=" + sfmt.format(nlat) + "," + sfmt.format(nlon) + "&z=" + str(
                zoomlevel)
            print(url)
    else:
        print(message, " ignore")


def getPositionData(gps):
    data = gps.readline()
    print(data)
    gpsProcess(data)


# if True:
if False:
    # Test
    testdata = b'$GNRMC,082116.000,A,3404.8820,N,08353.7835,W,0.69,71.62,091222,,,A*5C\r\n'
    gpsProcess(testdata)

if __name__ == '__main__':
    print("Application started!")
    gps = serial.Serial(SERIAL_PORT, baudrate=9600, timeout=0.5)

    while running:
        try:
            getPositionData(gps)
        except KeyboardInterrupt:
            running = False
            gps.close()
            print("KeyboardInterrupt. Application closed!")
        except Exception as err:
            # You should do some error handling here...
            print("Something went wrong! {}".format(err))
            traceback.print_exc()
            print("Application error!")

