import sys
import threading # برای اجرای پینگ در پس زمینه
import time # برای ایجاد مکث در حلقه پینگ
import json # برای تبدیل دیکشنری به رشته JSON
import base64
import os # برای تولید nonce
from datetime import datetime # برای timestamp در payload


from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.exceptions import InvalidTag # در سمت سرور برای رمزگشایی استفاده می شود

import paho.mqtt.client as mqtt
from kivy.uix.textinput import TextInput
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

from kivy.clock import mainthread # برای به روز رسانی UI از ترد پس زمینه
from ping3 import ping # اطمینان حاصل کنید که ping3 نصب شده است: pip install ping3



try:#در بلاک try_except تلاش ما برای انی هست که بتوانیم با استفاده از ماشین محازی جاوا در کدمون یک کلاسی که مربوط به جاوا میباشد پیاده سازی کنیم تا بتوپان از اندروید یک apiبگیریم که با پایتون امکان پذیر نبودش
    from jnius import autoclass
    Build = autoclass('android.os.Build')#ما در این جا یک متغیری مسیازیم که به کلاسی در اندروید که برای جاوا هست اشاره دارد و میتوانیم ازش موارد که میخواهیم را استخارج کنیم
    def get_device_info():
        manufacturer = Build.MANUFACTURER#نام شرکت
        model = Build.MODEL#مدلی که از اون شکرت ساخته شده است
        return {"manufacturer": manufacturer, "model": model}
except Exception as e:
    # jniusدرون دکستاپ ارور میدهد و با این حالت میتوانیم ارور که بر روی دسکتاپ است را کندرل کنیم
    print(f"Warning: Android Build class not available. Device info will be generic. Error: {e}")
    def get_device_info():
        return {"manufacturer": "Unknown", "model": "Desktop"}

# این تابع به ما کمک میکند تا بتوانیم مواردی که قرار است ارسال شود را در حالت دیکشنری و بعد جیسون ارسال کنیم به بروکر و از اونجا به مشترکی که منتظر دریافت استش
def build_payload(ping_value, device_info):
    data = {
        "device_info": device_info,
        "ping": ping_value
    }
    return data

# --- تنظیمات رمزنگاری ---
# توجه: این کلید باید در سمت سرور و کلاینت یکسان باشد!
# این کلید باید 32 بایت (256 بیت) باشد. می توانید با os.urandom(32) تولید کنید.
# سپس آن را به base64 تبدیل کنید تا قابل ذخیره و استفاده باشد.
# مثال: base64.urlsafe_b64encode(os.urandom(32)).decode('utf-8')
SECRET_KEY_STR = "_yJo28KsmzN1sjIjoLOlQqPZyWRDhlV2jviiGFw6j4c="
try:
    SECRET_KEY = base64.urlsafe_b64decode(SECRET_KEY_STR)
    print(f"---------------------{SECRET_KEY}")
    if len(SECRET_KEY) != 32:
        raise ValueError("SECRET_KEY must be 32 bytes after base64 decoding.")#ما با  raiseایجاد استثنا میکنیم
except (ValueError, TypeError) as e:
    print(f"Error decoding SECRET_KEY: {e}. Please ensure it's a valid 32-byte base64 encoded string.")
    # در محیط تولید، اینجا باید برنامه را متوقف کنید یا از یک کلید پیش فرض امن استفاده کنید.
    # برای مثال، اگر خطایی در کلید وجود داشت، از یک کلید ثابت برای ادامه برنامه استفاده می کنیم.
    sys.exit(1)# کلید جایگزین برای جلوگیری از کرش، اما امن نیست!

def encrypt_message(message: str) -> bytes:#این یعنی ما تابعی داریم که ورودی strمیگیرد و خروجی بایت بیرون میدهد
    """پیام متنی را با AES-GCM رمزنگاری می کند و nonce + ciphertext + tag را برمی گرداند."""
    nonce = os.urandom(12) #این کد همان ساخت نانسی تصادفی است و معنیش این مشود که برای هر بلاک ما که قرار است در ctr با شمارنده بلک ترکیب شود و aesاونو رمز نگاری کنه تولید شود و این نانسی یک دیتایی است به ازای هر بار اجرا شدن یک ۱۲ بایتی متفاوت میدهد تا جلوب خطای نانسی  تکراری گرفته شود و این خیلی درون فرایند کد گذاری مهم است  (بلوک شمارنده میشود نانسی و عدد شمارنده بلوکی که قرار است در آخر با کدگذارش شده این فرایند در غالب aesه شکل xor کد گذاری شوند)
    cipher = Cipher(algorithms.AES(SECRET_KEY), modes.GCM(nonce), backend=default_backend())#این خط  هسته عملیات رمز نگاری ما میباشد که درونش ما تعریف میکنیم algorithmمیشودaes که یعنی فرایند کد گذاری ما aes است که یک گد گذاری مدرن میباشد و نحوه کدگذاری یان حالت بلوکی دارد و مدل کد گذاریش هم spn میباشد و اگر کد گذاری با حالت عملیاتی تغیر نکند باید با پدینگ حتما نادازه بایت ها را اندازه کرد و وردی که میگیرد میشود کیلید ما و آرگومان بعدی که میگرد میشود  مدل حالت عملیاتی ما که غالب های مختلفی دارد و انیکه الان ما استفاده میکنیم gcm است(gcl یک حالت کد گذاری جریانی است که این مشود مدل کد گذای ما و دیگر به پدینگ نیازی نداریم که gcm چندین مزیت عالی دارد مثل اینکه قابلیت محرمانگی زیادی داری و مهم تر اینکه قابیلت تایید اصالت دارد یعنی اینکه با استفاده از مدل و فرایند هایی که دارد قطعا کد ارسالی در میانه راه تقیری نکرده است چرا چون بخش محرمانیگی با ctr یعنی اینکه نانسی بعلاوه شمارنه هر بلوک میشود همان چیزی که با aes کد گزاری میشود و ادامه  که این فریاند مربوط به ctr است و بخش دوم gcm میشود این بخش با استفاده از عمیلیات ضرب در میدان محدود که باعث میشود کوچچک تریناثری بهمت تولید کند و نتیجه ای غیر قابل پیش بینی داشته باشد و gmac از یک کیلید هشینگ استفاده میکند که از secret_key به دست آمده است این با بلوک های رمز شده و داده های احراز هویت شده به صورت متوالی در میدان gf(2 128) ضرب و جمع میشود که حتی یک بیت تغییر هم نتیجه چیزی غیر از اونیکه باید باشد در گیرنده میکند و این فراین هم باعث میشود که این ها به شکل یک پارچه و مرتبط به هم انتقال پیدا کنند و وردی که نانسی است به مدلس در بخش ctr میشود کیلید ایجاد تفاوت و مغر رمز نگاری و در gmac میشود بخش تولید تگ احراز هویت
    encryptor = cipher.encryptor()#در این خط ما روی شیی که تازه با nonce,gcm,aesپیکر بنده شده است را اماده رمز نگاری میکند به این روش که با ااستفاده از متود encrypt(این شایی اماده اپدیت و فاینالیز کردن دیتا میشود که نتیجش رمز نگاری دیتا ما میشود
    # Pkcs7 padding برای اطمینان از اینکه طول داده ها مضربی از اندازه بلاک AES است
    # padder = padding.PKCS7(algorithms.AES.block_size).padder()#اینجا ما یک شکل پدر داریم برای اسنتاندارد (پی کی سی اس ۷) که میشود یک نوع پروتکل رای تضمین امنیت بلوک هاو این خط با استفاده از پدینگ تایید میکنه که حتما اندازه بلوک ها ۱۶ بایت باشد
    # padded_data = padder.update(message.encode('utf-8')) + padder.finalize()#این تکمیل کننده عملیات پدینگ است جوری که به انتهای بلوک ها بایت اضافه میکند تا نتیجه مضربی از ۱۶ شود تا به میزان دلخواه aesبرسد
    #ولی چونکه ما ازgmac اریم استفاده میکنیم خودش جریان بایتی کار میکند و خیلی هم قوی است با نبود این فرایند به مشکل نخواهیم خوردش

    ciphertext = encryptor.update(message.encode('utf-8')) + encryptor.finalize()#اینجا وروید به شکلی از بایت های رمز نگاره شده با  utf-8شروع به رمز نگرای میکنیم و فاینالایز مسول ساخت تک احراز هویت میشباشد
    print(f"-----------////////------------{ciphertext}")
    return nonce + ciphertext + encryptor.tag # ترکیب nonce, ciphertext و tag


# --- پایان تنظیمات رمزنگاری ---


class ping_modem(App):
    ping_st = False # پرچم برای کنترل وضعیت پینگ (شروع/توقف)
    ping_thred = None # برای نگهداری ارجاع به ترد پینگ
    mqtt_client = None # برای نگهداری شیء کلاینت MQTT

    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.label = Label(text='Ping :N/A', font_size='20sp')
        layout.add_widget(self.label)

        start_button = Button(text='Start', font_size='17sp')
        layout.add_widget(start_button)
        start_button.bind(on_press=self.ping_start)

        stop_button = Button(text='Stop', font_size='17sp') # اصلاح: نامگذاری صحیح دکمه ها
        layout.add_widget(stop_button)
        stop_button.bind(on_press=self.ping_stop)
        return layout

    def on_start(self): # این متد وقتی برنامه Kivy شروع به کار می کند فراخوانی می شود
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self._on_mqtt_connect
        self.mqtt_client.on_disconnect = self._on_mqtt_disconnect
        try:
        #     "localhost" را با آدرس IP سروری که Mosquitto روی آن اجرا می شود جایگزین کنید
            self.mqtt_client.connect("192.168.1.147", 1883, 60)
            self.mqtt_client.loop_start() # شروع حلقه MQTT در پس زمینه برای مدیریت پیام ها
            print("Attempting to connect to MQTT broker from Kivy app...")
        except Exception as e:
            print(f"Failed to connect to MQTT broker from Kivy app: {e}")
            self.label.text = "MQTT Connect Error" # بهتر است در ترد اصلی UI به روز شود

    def on_stop(self): # این متد وقتی برنامه Kivy بسته می شود فراخوانی می شود
        if self.mqtt_client:
            self.mqtt_client.loop_stop() # توقف حلقه MQTT
            self.mqtt_client.disconnect() # قطع اتصال از بروکر
            print("Kivy app disconnected from MQTT broker.")

    def _on_mqtt_connect(self,  rc):
        if rc == 0:
            print("Kivy app connected to MQTT Broker!")
            @mainthread
            def update_label():
                self.label.text = "MQTT Connected"
            update_label()
        else:
            print(f"Kivy app failed to connect to MQTT Broker with code {rc}")
            @mainthread
            def update_label():
                self.label.text = f"MQTT Connect Error: {rc}"
            update_label()

    def _on_mqtt_disconnect(self,  rc):
        print(f"Kivy app disconnected from MQTT Broker with code {rc}")
        @mainthread
        def update_label():
            self.label.text = "MQTT Disconnected"
        update_label()


    def ping_start(self, button):
        try:
            if not self.ping_st:
                self.ping_st = True
                self.label.text = 'Ping: Running...'

                if not self.ping_thred or not self.ping_thred.is_alive():
                    self.ping_thred = threading.Thread(target=self.ping_bg)
                    self.ping_thred.daemon = True
                    self.ping_thred.start()
                else:
                    print("Ping thread is already running.")
            else:
                print("Ping is already running.")
        except Exception as e:
            print(f"Error starting ping: {e}")

    def ping_stop(self, button):
        if self.ping_st:
            self.ping_st = False
            self.label.text = 'Ping: Stopping...'
            print("Signaling ping thread to stop.")
        else:
            print('Ping is not running.')

    def ping_bg(self):
        adres = "8.8.8.8"
        print("Background ping thread started.")
        while self.ping_st:
            try:
                delay = ping(adres, timeout=2)
                delay=delay*1000
                device_info = get_device_info()
                payload_data = build_payload(delay, device_info)

                # تبدیل دیکشنری به رشته JSON
                json_payload_str = json.dumps(payload_data)

                # --- رمزنگاری پیام JSON ---
                encrypted_payload_bytes = encrypt_message(json_payload_str)
                # --- پایان رمزنگاری ---

                # ارسال پیام رمزنگاری شده به بروکر MQTT
                if self.mqtt_client and self.mqtt_client.is_connected():
                    # 'mobile/ping/updates' تاپیکی است که سرور Flask شما به آن گوش می دهد
                    # پیام رمزنگاری شده (بایت) را ارسال می کنیم
                    self.mqtt_client.publish('mobile/ping/updates', encrypted_payload_bytes, qos=1)
                    print(f"Published encrypted message to MQTT. Length: {len(encrypted_payload_bytes)} bytes")
                else:
                    print("MQTT client not connected, cannot publish.")

                @mainthread
                def update_label_text(ping_result):
                    if ping_result is None:
                        self.label.text = "ping: Timeout"
                    else:
                        self.label.text = f"ping: {round(ping_result)} ms"
                update_label_text(delay)

            except Exception as e:
                print(f"An error occurred during ping or MQTT publish: {e}")
                @mainthread
                def update_label_error():
                    self.label.text = f'Ping Error'
                update_label_error()

            time.sleep(2)

        print("Background ping thread actually stopped.")
        @mainthread
        def update_label_stopped():
            if self.label.text == 'Ping: Stopping...':
                self.label.text = 'Ping: Stopped.'
            elif self.label.text == 'Ping: Running...':
                self.label.text = 'Ping: Runn.'
        update_label_stopped()


if __name__ == '__main__':
    ping_modem().run()