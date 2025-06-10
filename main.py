import time
import requests
from smartcard.System import readers
from smartcard.util import toHexString
from smartcard.Exceptions import NoCardException

# API_URL = "https://example.com/api/rfid"  # Ganti dengan endpoint REST API kamu
API_URL = "https://dummyjson.com/products/add"  # Ganti dengan endpoint REST API kamu
GET_UID = [0xFF, 0xCA, 0x00, 0x00, 0x00]

def get_reader():
    contactless_readers = [r for r in readers() if '-CL' in str(r)]
    if not contactless_readers:
        raise Exception("❌   Reader contactless tidak ditemukan.")
    return contactless_readers[0]

def send_uid(uid, device_name):
    payload = {"uid": uid, "device": device_name}
    try:
        res = requests.post(API_URL, json=payload, timeout=5)
        print("✅   UID terkirim:", uid) if res.ok else print("⚠️\tGagal kirim:", res.status_code)
        print()
    except Exception as e:
        print("❌   Error API:", e)

def main():
    reader = get_reader()
    device_name = str(reader)
    conn = reader.createConnection()

    print(f"🔍   Reader aktif: {device_name}\nTempelkan kartu RFID...")

    last_uid = None
    while True:
        try:
            conn.connect()
            data, sw1, sw2 = conn.transmit(GET_UID)
            if (sw1, sw2) == (0x90, 0x00):
                uid = toHexString(data)
                if uid != last_uid:
                    last_uid = uid
                    print(f"🎯\tUID terbaca: {uid}")
                    send_uid(uid, device_name)
            time.sleep(1)
        except NoCardException:
            last_uid = None
            time.sleep(0.5)
        except Exception as e:
            print("❌   ", e)
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Dihentikan pengguna.")
