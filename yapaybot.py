import discord
import requests
import time

# Discord bot token'ınızı buraya ekleyin
TOKEN = 'MTI2MzIxMDA5OTE0MTUxMzM4Nw.Gw5ERH.G_gmw_7PW90z8oJ_XW7w10Y2QWgyakzsQPr0Lo'

# API URL'sini buraya ekleyin
API_URL = 'https://msii.xyz/api/yapay-zeka?soru='

# Intents ayarları
intents = discord.Intents.default()
intents.messages = True  # Mesajları dinle
intents.message_content = True  # Mesaj içeriğini dinle

# Discord istemcisi oluştur
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Bot {client.user} olarak giriş yaptı.')

@client.event
async def on_message(message):
    # Bot kendi mesajlarına cevap vermemeli
    if message.author == client.user:
        return

    retry_attempts = 3
    for attempt in range(retry_attempts):
        try:
            # Mesaj içeriğini API'ye gönder
            response = requests.get(API_URL + message.content)
            
            # Yanıt detaylarını yazdır
            print(f"API Yanıt Durum Kodu: {response.status_code}")
            print(f"API Yanıtı: {response.text}")
            
            # API'den yanıt al
            if response.status_code == 200:
                data = response.json()
                if 'reply' in data:
                    answer = data['reply']
                else:
                    answer = 'API yanıtında beklenmeyen bir format var.'
                break
            else:
                if response.status_code == 500:
                    answer = 'API sunucu hatası meydana geldi. Lütfen daha sonra tekrar deneyin.'
                else:
                    answer = f'API isteğinde bir hata oluştu. Durum kodu: {response.status_code}'
                if attempt < retry_attempts - 1:
                    print(f"Retrying... ({attempt + 1}/{retry_attempts})")
                    time.sleep(10)  # Retry için bekleme süresi artırıldı
                else:
                    break

        except Exception as e:
            error_message = f'Hata oluştu: {str(e)}'
            print(error_message)
            answer = 'Bir hata oluştu. Lütfen daha sonra tekrar deneyin.'
            break

    # Yanıtın uzunluğunu kontrol et
    print(f"Yanıt Uzunluğu: {len(answer)}")
    
    # Discord'da mesajı gönder
    try:
        await message.channel.send(answer)
    except discord.DiscordException as e:
        print(f"Discord mesaj gönderim hatası: {str(e)}")

# Botu çalıştır
client.run(TOKEN)
