import socket
import time
from datetime import datetime, timedelta
import random

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

# Create socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Sample data for 6 reports
reports_data = [
    {"team": "ALPHA", "pool": "ZIELONY", "ph": 7.24, "conductivity": 465, "temp": 18.5},
    {"team": "BETA", "pool": "NIEBIESKI", "ph": 7.18, "conductivity": 472, "temp": 19.2},
    {"team": "GAMMA", "pool": "CZERWONY", "ph": 7.31, "conductivity": 458, "temp": 17.8},
    {"team": "DELTA", "pool": "ZÓLTY", "ph": 7.22, "conductivity": 461, "temp": 18.9},
    {"team": "EPSILON", "pool": "FIOLETOWY", "ph": 7.26, "conductivity": 467, "temp": 19.1},
    {"team": "ZETA", "pool": "POMARAŃCZOWY", "ph": 7.20, "conductivity": 464, "temp": 18.6},
]

report_counter = 0

try:
    while report_counter < len(reports_data):
        current_time = datetime.now()

        data = reports_data[report_counter]
        
        # Generate report
        report = (
            f"---- HYDROLAB RAPORT ----\n"
            f"Zespół: [{data['team']}] | Czas: {current_time.strftime('%H:%M:%S')}\n"
            f"Basen: {data['pool']} (500ml) | Próbka: 500ml ✓\n"
            f"pH: {data['ph']} | Przewodność: {data['conductivity']} µS/cm | Temp: {data['temp']}°C\n"
            f"Status: PRÓBKA_DOSTARCZONA | Zsuw: OK ✓"
        )
        
        print(f"Sending report {report_counter + 1}/{len(reports_data)}:")
        print(report)
        print()
        
        # Send via UDP
        sock.sendto(bytes(report, "utf-8"), (UDP_IP, UDP_PORT))
        
        report_counter += 1
        
        if report_counter < len(reports_data):
            time.sleep(1)

    print("All 6 reports sent.")

except KeyboardInterrupt:
    print("\nSender stopped early.")
finally:
    sock.close()