# import binascii #بریا تبیدیل باینری به متن استفاده میشود
import logging#برای لاگ نگاری استفاده میشود که کاراییی خیلی زیادی در حوزه امنیت پیدا میکند اگه که ما به مشکل بخوری و برای ما پیدا میکند مشکلات را
# import subprocess#بریا اجرای دیتورات تحت شل و سیستمی است از درون کد و برنامه پایتونی ما
import sys
# import tkinter as tk
# import ttkbootstrap as ttk
# from threading import Thread
import json
#import time
import base64  # برای دیکد کردن کلید Base64
#import os  # برای os.urandom در رمزنگاری/رمزگشایی
from flask import Flask, request
from flask_socketio import SocketIO, emit
from flask_mqtt import Mqtt
# --- وارد کردن ماژول‌های رمزنگاری ---
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
#from cryptography.hazmat.primitives import padding  # اگرچه برای GCM نیاز نیست، اما برای سازگاری در تعریف تابع decrypt_message نگهداری می‌شود
from cryptography.exceptions import InvalidTag  # برای مدیریت خطای تگ نامعتبر در رمزگشایی

# --- پایان وارد کردن ماژول‌های رمزنگاری ---

# --- بررسی و نصب پکیج‌ها ---
# try:

# except ImportError:
#     print("پکیج ها درحال دانلود شدن هستن...")
#     --break-system-packages برای سیستم‌های جدیدتر پایتون
#     --no-cache-dir برای اطمینان از دانلود جدیدترین نسخه‌ها
    # subprocess.run(
    #     [sys.executable, "-m", "pip", "install", "--break-system-packages", "--no-cache-dir", "flask", "flask_socketio",
    #      "flask_mqtt", "cryptography"])
    # print("وابستگی ها نصب شدند.")
    # sys.exit()
print("heloo")
SECRET_KEY_STR = "_yJo28KsmzN1sjIjoLOlQqPZyWRDhlV2jviiGFw6j4c="
try:
    secret_key = base64.urlsafe_b64decode(SECRET_KEY_STR)
    if len(secret_key) != 32:
        raise ValueError("secret key must be 32 bytes lon")
    logging.getLogger('werkzeug').info(f"secret_key :-){len(secret_key)}")#این یک سیستم لاگ نویسی درون پایتون است که برمینای آرگومانی که میگیرد اینجاwerkzeug که یک فضایی است که فلاسک از اون ساخته شده است با عث میشود خطایی که میدهد مربوط به وب باشد و این و در صورت موفقیت امیز بودن فرایند کد شکنی ما اینو مشاهده خواهیم کردش
except (ValueError, TypeError) as e:
    logging.getLogger('werkzeug').info(f"secret_key :-({e}")
    sys.exit()#اینجا ما تایید مکینم که اگر برای ما اروری پیش امد در این بخش قطعا از رنامه خارج میشود چون این ارور قابل اغماز نیستش
def decrypt_data(data:bytes) -> str:
    """پیام رمزنگاری شده AES-GCM را رمزگشایی می‌کند و متن اصلی را برمی‌گرداند."""

    if len(data) < 12 + 16:  # Nonce (12 bytes) + Tag (16 bytes)
        raise ValueError("Encrypted data is too short to contain nonce and tag.")

    nonce = data[:12]
    ciphertext = data[12:-16]
    tag = data[-16:]

    try:
        # **این تنها الگویی است که با تمام خطاهای قبلی و فعلی شما سازگار است:**
        # تگ احراز هویت را مستقیماً به constructor حالت GCM می‌دهیم.
        # این به این معنی است که decryptor بلافاصله تگ را برای تأیید اعتبار نهایی دریافت می‌کند.
        cipher = Cipher(algorithms.AES(secret_key), modes.GCM(nonce, tag), backend=default_backend())
        decryptor = cipher.decryptor()

        # ciphertext را رمزگشایی می‌کنیم.
        decrypted_main_data = decryptor.update(ciphertext)

        # finalize() صرفاً عملیات را نهایی کرده و صحت تگ را بر اساس آنچه قبلاً داده شده بود، بررسی می‌کند.
        decrypted_final_part = decryptor.finalize()

        return (decrypted_main_data + decrypted_final_part).decode("utf-8")
    except InvalidTag as e:
        raise InvalidTag(f"Invalid tag. Data might be tampered or key/nonce/tag is incorrect: {e}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred during decryption: {e}")
#پایان توابع رمزگشا
# class Redirector:
#     def __init__(self, widget): # این متود سازنده کلاس است و برای هر شی  که تولید شود از این کلاس این فرایند به خاطر بودن __init__ دوباره تکرار میشود که ذات init همین کار است تا به اشیا مجودیت دهد و با آرگومان هایی مثل self که میشود خاصیت پایه ای کلاس ما و موارد دیگر که بهش اضافه میکنیم شی ما حالت های منحصر بفرد در غالب ی که کلاس تایین میکند ساخته میشود
#         self.widget = widget# در  اینجا ما ویجت که میشود تکست اریا یعنی در این بخش ما ویجتی که خودمات تعین کردیم را برابر با خاصیت ویجت در ذات کلاس نهادینه شده است قرار میدهیم
#
#     def write(self, message):#  ما درون سیستم خروجی و وروید پایتونت مثل خیلی از زبان های دیگری یک مسیر ورودی و خروجی به شکل استریم داریم که میشود فرایندی که باآن میشود برای پایتون از ورودی ها دیتا دریافت کرد و از پایتون به خروجی ها دیتا دادش با پروتکل هایی که با عث قابل فهم شدن این فرایند ها میشوند و سه مفهوم داریم stdin,stderr,stdoutکه میشوند ورودی اتاندارد خروجی استاندارد و ارور استاندارد پایتون این قدرت به ما میدهد که بتوانیم این سه فرایند را با چیز هایی که میخواهیم جایگزین کنیم تا این موارد  هدایت مجدد شوند به اونجایی که ما میخواهیمو بریا اسم گذاری تابع این خیلی مهم است که حتما باید با همین اسم نوشته شود تا از قاعده Duck typing پیروی کند این قادعه یعنی اگر چیزی شبیه اردک راه برود و شبیه لردک صدا دربیارد پس اردک است و درکد ما یعنی اگر شی متود writeداشته باشد و قابلیت دریافت متن یا بایت داشته باشد پس پایتون اونو به شکل یک فایل قابل نوشتنمی پذیرد و این نتیجه اش میود اینکه پایتون این تابع را به جای  sys.stderr,stdoutمیپذیرد خلاصه که این تابع برای انتقال داده ها از cmd به اون پنجره ای که  ما میخواهیم است و چون پیاتون از قاعده نوشتن اردکی استفاده میکند باید متود write با قابلیت نوشتن حتما باشد باشد
#         self.widget.insert("end", message)#ما با این خط میگوییم که وقتی ورودی ها را در غالب آرگومان مسیج گرفته ایم و با api پایتون ارتباط برقرار کردیم و حد انتظارش بر اورده کردیم به ما خروجی در غالب مسیج بده و اونو در آخری text مورد نظر چاپ میکند
#         self.widget.see("end")#بریا این است
#
#     def flush(self):#تابع برای جلوگیری از خطایی  است که حاصل از عملیات نوشتن است چرا که پایتون توقع بودن تخلیه بافر را دارد ولی کتاب خونه ای که مه استفاده میکنیم خودش خود به خود این قابلیت را دارد و این تابع برای جلو گیری از خطا ساخته شده است و کاری نمیکند
#         pass
#
def run_server():
    socketio.run(app, host='0.0.0.0', port=5000, debug=False,use_reloader=False,allow_unsafe_werkzeug=True)#این متود برای راه ندازی سرور استفاده میشود سروری که اماده دریافت در خواست های http و websocket میباشد اولین آرگومان نمونه اپلیکشن ما است و میشود نمونه واقعی از موارید که نیاز است فلاسک با مانور دادن روشون و با محوریت قرار دادن اون ها در کار هایی که میخواهد انجام دهد عمل  و فرایند خودش به نتیجه قابل پیش بینی و مورد نیاز برسناد مثل مسیر ها و موارد از این قبیل و هاست ما میگوید که سرور ما به تمام در خواست های ipها چه داخلی یا خارجی گوش دهد و اون هارا مورد پردازش خودش قرار دهد و پورت هم میشود پورتی که شبکه روش گوش میدهد وا فالس بودن دیباگ برای این است که وقتی تراک بک دا میخواهد در زمان وقوع خطا نشان دهد چون محصول در حالت اراعه به مشتری است این کار را نکند تا ورژن ها مسیر ها و الگوریتم ها و .. فاش نشود و ریلودر که قابلیتش این است که بریا ما هر کاری که انجام میشود را سرور را دوباره راه اندازی کند تا این کار از دوش مابرداشته شود و این کار الان که ما در حال کار درون یک ترد دیگه هستیم و فلاسک ما کوچک هست نیازی نیست
#

# class loghandler(logging.Handler):#با استفاده از دریافت کننده لاگ است که ما میتوانیم تمام لاگ هارا درون cmd را در محیط مورد نظر خودمان داشته باشیم و موردی که به عنوان آرگومان است کلاسی است که برای دریافت تمام لاگ هارا دریافت کند و با logging.Handlerاست که میتوانیم تمام لاگ درون ایناکلاس مدیریت کنیم
#     def __init__(self,widget):#ما برای هر شی ساخته شده ازا ین کلاس با اینیت میاییم و مواردی گه لازم است را در نظر میگیرم و بهش میدهیم که این باعث ایجاد وراثت میشود و در این جا ما بعلاوه self ویجت هم دارمی که مربوط به نمایش لاگ ها میشود
#         super().__init__()#اینجا ما بیان میکنیم که شی که قرار است از این فرایند متولد شود حتما باید در بیر دارنده تمام خصوصیات و قابلیت های شی پدر باشد که این پروسه با اومندن متود super().__INIT__()شکال گرفته است و این باعث آن میشود که بتوانیم به تمام این خصوصیات های لازم درون شی پدر دست رسی داشته باشیم و اگر پروسه ای است که نیاز دارد شی خصوصیت والد کلاسی که ازش  به دنیا اومده را داشته باشد اینجا دارد و حامل است که این خیلی فرایند و نکته طلایی است
#         self.widget = widget
#
#     def emit(self, record):#یک متود اجباری است گه باید در فرزند هایی که ازlogging.Handler ارث بری میکن اجرایی شود یعنی وقتی لاگی تولید میشود و سطح اون جوری است که لاگر به این نتیجه میسر که اونو به هندلر ها واگذار کند و در این مرحله لاگر  emit(record)هارا روی هر کدوم از هندلر ها احضار میکند و آرگومانی که میگیرد یک شی  logrecorderاست که حامل متن اصلی زمان و خیلی جزعیات دیگر میباشد
#         msg = self.format(record)#اینجا ما که نظیمات فرمت را با فرمتر انجام داده ایم مشخص میکنیم که چه چیزی قرار است برای ما در لاگ ها نشان داده شود از اونهمه جزعیات دقیق
#         self.widget.insert("end", msg+"\n")#به انتهای لاگ متنی اضافه میکند بعلاوه یم خط اضفا
#         self.widget.see("end")#تنضمین میکند که حتما همیشه آخرین لاگ هم قابل دیدن باشد و صفه به صورت دستی به پایین اسکرول شود و نیازی به اسکرول دستی نباشد
#ما خیلی از تنظیمات لازم را درون فرایند اجرا از cmd جایگذاری کردیم تا لاگ هنلر سفارشی ما به لاگر werkzeug اتصال پیدا کنتد و تمام لاگ های اون هم قابل مشاهده باشد درون محیط متنی انتخاب شده
app = Flask(__name__)#ساخت یک کلاس که سرور ما میباشد برای انجام کار های سوکت پروگرمینگ از کتابخونه فلاسک و این سرور مارو فقط میشه بهش از طریق اینترنت خپود اون مودم وصل شدن بهش که درخواست ها هم فقط از کلاینت ها تحت پوشش همون مودم خواهند بودش
app.config['SECRET_KEY'] = 'sesuusdfiubsfuskjbfijeoiwriuh34i5y4DAWDAFWDAWaDu0[gbkfd0oseasfjhehfcretASD!'#این سکرت کی درون سشن(ارتباطی که سرور و کلاینت زنده و ریل تایم دارن)ازطریق کوکی به هر کلاینت  و به هر ازتباط  درون کوکی  که حاوی اطالاعات سشن هست گذاشته میشود و هش میشود و امکان جعل را کاهش میدهد تا اطلاعات سشن همونی بمونند که سرور به کلاینت داده است
socketio = SocketIO(app, cors_allowed_origins="*")#این خط یعنی ما سرور کهappهست را مجهز به وب سوکت میکنیم و آرگومان دومش یعنی اجازه اتصال هر سیستمس از هر مبدأ به این داده میشود و شیsoketioمدیریت  وب سوکت را بر عهده دارد

clients_data = {}#این مخزن برای زیخره سازی داده هایی یاست که ما میخواهیم از موبایل دریافت کنیمی

#این بخش ها برای انی هستن که سرور ما بالا بیاید و به بروکر مورد نیاز متصل شود
app.config['MQTT_BROKER_URL']= 'localhost'#ای پی بروکر یا ادرس سرور mqtt
app.config['MQTT_BROKER_PORT'] = 1883#پورت بیشفرض برای اتصال
app.config['MQTT_BROKER_USERNAME']= ''#اگر بروکر یوسرنیم و پسوورد دارد
app.config['MQTT_BROKER_PASSWORD']= ''
app.config['MQTT_BROKER_TLS']= False#اگر از tlsاستفاده نمیکنیم فالس باشد
app.config['MQTT_KEEPALIVE']= 60# مدت زمان کپ لایو یعنی حداکثر وقتی که کلاینت در سکوت به بروکر میتواند بماند و برای تشخیص قطعی اتصال بکار میرود

mqtt = Mqtt(app)#مقدار دهی اولیه شی که از مواردبال پیروی میکند

@app.route('/receive_ping',methods=['POST'])#@یک دکوراتور هست که یعنی آدرس آورده شده از سرور که receive_pingهست به این تابع پایین وصل میشود و پردازش داده میشود که فقط درخواست های POSTرا قبول دارد
def receive_pinng():#تحت تاثیر دکوراتور بالا فقط در آدرسی که دکوراتور گفته و متود پست را برای پردازش قبول میکند یعنی هر زمان درخواست پست به آدرسی که دکوراتور گفته ارسال شود این تابع فعال میشود
    data = request.json#این کاری میکند که باعث شود دیتای ما جیسون خوانده شود و این خاصیت  شی است یعنی پروپرتی و میتوان از متود جیسون هم استفاده کرد که قابلیت های بیشتری برای کنترل به ما میدهد
    device_id = data.get("device_id")#ای دی دستگاه استخراج کرده و زخیره میکند
    ping_value = data.get("ping")#مقدار پینگ را استخراج میکند

    if device_id and ping_value is not None:
        clients_data[device_id] = {#اینجا ما وارد دیکشنری میشویم که بالاتر طراحی کردیم و درون کیلید device_idبرای ما یک مقدار جدید ثبت کنش
            'ping': ping_value
        }

        socketio.emit('ping_update',{device_id:clients_data[device_id]})#روی خط ping_updata برای همه اون ها میاد ای دی واز دیکشنری مقدار ای دی که میشود پینگ ارسال  میکند و کلاینت میتواند حالا با داشتن پینگ جدی د کاری انجام دهد
        logging.getLogger('werkzeug').info(f"received {ping_value} and {device_id}")
        return {"message":"ping received and broadcasted!-)"}#پیامی بر میگرداند که یا درست بود همه چی یا اشیتباه که پایین پیام اشتباه را میبینم
    else:
        logging.getLogger('werkzeug').error(f"received {data}")
        return {"error":"missing device_id or ping value"}

@mqtt.on_connect()#یک دکوراتور است که مثل بقیه دکوراتور ها روی تابعی که زیر خودش قرار دارد تاثیر میگذارد و این وقتی اجرا میشود که که کلانیت mqttیرور با موفقیت به بروکر متصل شود
def on_connect(client, userdata, flags, rc):
    if rc == 0:#  که یعنی کد برگشتی به ما نشان میدهد از کدی که بر میگردد وضعیت چطور است ۰ یعنی موفقیت ۱ مشکل در پروتکل ۲ کلاینت با ای دی نا معتبر و ۳ یعنی سرور دردست رس نیست ۴ یعنی یوزر و پیوورد اشتباه
        logging.getLogger('werkzeug').info("Connected :-}")# لاگ نگاری با استفاده از بیس فلاسک که در اولین آرگومان اورده شده است
        mqtt.subscribe('mobile/ping/updates')#بعد از اینکه اتصال موفق بود سرور در این تاپیک شروع به دریافت میکند و این تاپیک باید درون  فرستنده همین باشد دقیقا
        logging.getLogger('werkzeug').info("Subscribed to 'mobile/ping/updates'")
    else:
        logging.getLogger('werkzeug').error(f"❌ Failed----code {rc}")

@mqtt.on_message()#این دکوراتور هر وقتی تابع را فراخوانی میکند که پیام جدید از طرف تاپیک مورد نظر دریافت شود
def handle_mqtt_msg(client, userdata, msg):
    #msgای شی شامل جزعیات پیام دریافتی است
    topic = msg.topic# نام تاپیکی که پیام روی آن ارسال شده است
    payload = msg.payload #این همون پیام اصلی است که توسط کلاینت رمز نگاری شده است  و برنامه کیوی اینو رمز نگاری کرده است
    qos=msg.qos#نشان دهنده میزان ارسال پیام که نشان دههنده نوع پیام ما است
    # logging.getLogger('werkzeug').info(f"Received  payload={payload} topic={topic} qos={qos}")

    try:
        decrypted_data = decrypt_data(payload)#این مهم ترین بشخ ما است که پیام اصلی که بر مبنای aes و حالت عملی gcm و با فرایند ctrرمز نگاری شده و محرمانگی اون تاییید شده وبا فرایند gmacیک پارچگی این تاییید و تضمین شده است قرار است دیکد شود
        json_data = json.loads(decrypted_data)#رشته جیسون رمز گشایی شده به یک دیکشنری پایتونمبدل میگردد

        device_info = json_data.get("device_info",{})#این میشود تمام دریافتی های من که مربوط به مشخصات دستگاه اندرویدی میباشد که مدلش نام شکرتش که ما این دوتا خواستیم فقط
        device_id = device_info.get("model")#اینجا ما بریا شناسایی دیتگاه ها برای ای دی از مدل اون استفاده میکنیم که ضعیفه ولی برای ما همین کافی هست
        ping_val=json_data.get("ping")#دری این خط هم ما از دیتای رمز گشایی شده مقدار پینگ که برای ما ارسال شده بود را دریافت میکنیم

        if device_id and ping_val is not None:#اگر موراد خواسته شده را داده بودش این بلوک را اجرا کن
            clients_data[device_id] = {# این خط وظیفه ذخیره سازی و بروز رسانی وضعیت دیتا ها را دارد دیکشنری سراسری است که با کیلید های که همان دیوایس ای دی هستن وضعیت نگهداری میکند |  برای دیوایس id در دیکشنری کلاینت دیتا یک ورودی جدید ایجاد کن یا بروزرسانی کن
                "ping": ping_val,
                "model": json_data.get("model"),
                "manufacturer": json_data.get("manufacturer")
            }
            socketio.emit('ping_update',{device_id:clients_data[device_id]})# ارسال بلادرنگ به کلاینت هایی که به این رویداد گوش میدهند به این دیتا خواهند رسید که میشود سیستم پردازش  برنامه اصلی ب کیلید دیوایس ای دی تمام مقادیر بروز شده دستکاه ارسال میشود
            logging.getLogger('werkzeug').info(f"received {ping_val} and {device_id}")#لاگیکه برای ما فعالیت را ضبط و در کنسول مربوط به لاگ ها نشان میدهد
        else:
            logging.getLogger('werkzeug').warning("error",decrypted_data)
    except InvalidTag:
        logging.getLogger('werkzeug').error("Authentication tag invalid. Message might be tampered or incorrect key.")#عدم اعتبار در تگ احراز هویت
    except json.JSONDecodeError as e:
        logging.getLogger('werkzeug').error(
        f"Error decoding JSON from decrypted MQTT payload: {e}. Payload: {payload.hex()}")#نتوانستیم فایل را رمز گشایی کنیم
    except Exception as e:
        print(f"Error processing MQTT message: {e}. Payload: {payload.hex()}")

    # اجرای سرور در ترد جدا برای جلوگیری از کرش کردن حلثه محاسباتی صفه گرافیکی ما به دلیل ایجاد تداخلات
if __name__ == '__main__':
    run_server()
    print("server started :)")
    # الزامات صفه گرافیکی که طبق این بریا ما یک صفه ای باز تاپ صفه cmd میسازد
    # salam_rot = ttk.Window(themename="superhero")
    # salam_rot.title("server")
    # salam_rot.geometry("580x420")
    #
    # text_area = tk.Text(salam_rot, height=20, wrap='word', bg='black', fg='lime')#این یک ابزارک متنی است که از کتاب خانه کینتر  ایجاد میشود و خروجی های لاگ و تمام موارد داخل این نشان داده شودند والین آرگومان پنجره والد است که به ما نشان میدهد و ابزارک درونم این پنجره قرار خواهد گرفت و مشخص میکنیم که متن ها در آخر کلمه شکسته نشوند و مدل های دیگری مثل noneنیاز به اسکرول وcharشکستن کلمات هم دارد و ترکیب رنگی کنسول های قدیمی استفاده میکنیم
    # text_area.pack()#یک تنظیم گر هندسی است و تظمین میکند که حتما متن روی صفه مورد نظر به نمایش در بیاید
    # flask_log = logging.getLogger('werkzeug')#یک ارتباط مستقیم به لاگری که فلاسک از زیر ساخت های اون برای ایجاد ارتباط استفاده میکند و این مبدا اون کد های لاگ گیری بالا است که لاگ هارا درون cmd نمایش میدادش
    # flask_log.setLevel(logging.DEBUG)  # با تنظیم دستی این و خارج کردنش از حالت دیفالت و که اینفو یا وارنینگ بود باعث میشود که ریز ترین جزعیات هم برای ما قابل شناسایی باشد و به هندلر های مورد نیاز متصل گردد
    #
    # text_handler = loghandler(text_area)#با فراخوانی هندلری که قبلا ساخته ایم به مقصدش  الان تمام لاگ ها به جای یکه باید نمایش پیدا کند میروند
    # text_handler.setFormatter(logging.Formatter('%(message)s'))  #اینجا ما میتوانیم که فرمت و با استفاده از فرمتر تنظیم کنیم تا که برای ما مشخص کند چه چیبزی نمایش در آید و اینجا ما تصمیم گرفته ای که فقط خود پیام نمایش داده شود
    #
    # flask_log.addHandler(text_handler)#ارسال لاگ ها به تکست هندلر برای فرایندی که قبلا شرحش داده شده است
    #
    # sys.stdout = Redirector(text_area)#این ها مربوط به تنظیمات هدایت پیام های cmd در وایتون هستن که با رعایت استاندارد های پایتون ما ارور ها و خروجی هارا در چیزی که میخواهیم نمایبش میدهیم و خطا هم نمیدهد
    # sys.stderr = Redirector(text_area)
    #
    # print("✅ سرور در حال اجراست!","\n",text_area)
    # salam_rot.mainloop()#:-)