import time
import requests
from smartcard.System import readers
from smartcard.util import toHexString
from smartcard.Exceptions import NoCardException
import json

API_URL = "http://146.190.93.211:8099/api/read-rfid"  # Ganti dengan endpoint REST API
GET_UID = [0xFF, 0xCA, 0x00, 0x00, 0x00]

def get_reader():
    # Mencari pembaca contactless
    contactless_readers = [r for r in readers() if '-CL' in str(r)]
    if not contactless_readers:
        raise Exception("❌\tReader contactless tidak ditemukan.")
    return contactless_readers[0]

def send_uid(uid, device_name):
    payload = {"uid": uid, "device": device_name, "rfid": uid}
    try:
        res = requests.post(API_URL, json=payload, timeout=5)
        print("✅\tUID terkirim:", uid) if res.ok else print("⚠️\tGagal kirim:", res.status_code)
        res = json.loads(res.content.decode())
        print(f"Response : {res}")
        print()
    except Exception as e:
        print("❌   Error API:", e)

def main():
    reader = None
    conn = None
    device_name = None

    # Menunggu pembaca tersedia pertama kali
    while not reader:
        try:
            reader = get_reader()
            device_name = str(reader)
            conn = reader.createConnection()
            print(f"\n🔍\tReader aktif: {device_name}\nTempelkan kartu RFID...\n")
        except Exception as e:
            print("❌\tTidak ada reader yang ditemukan. Menunggu reader untuk dihubungkan...")
            time.sleep(3)

    last_uid = None
    while True:
        try:
            # Cek koneksi dan sambungkan jika sudah tersedia
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
            # Jika pembaca dicabut, coba untuk mencari pembaca lagi
            print("❌\tTerjadi kesalahan:", e)
            print("🔄\tMencoba untuk mendeteksi pembaca baru...")
            time.sleep(3)

            # Coba untuk me-reconnect pembaca
            reader = None
            while not reader:
                try:
                    reader = get_reader()
                    device_name = str(reader)
                    conn = reader.createConnection()
                    print(f"\n🔍   Reader aktif: {device_name}\nTempelkan kartu RFID...\n")
                except Exception as e:
                    print("❌\tTidak ada reader yang ditemukan. Menunggu reader untuk dihubungkan...")
                    time.sleep(3)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("👋 Dihentikan pengguna.")
