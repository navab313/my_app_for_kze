import sys  # برای دست رسی به بپارامتر های سیستم و انجام توابع با پیشوند sys
# import subprocess  # اجرا کردن دستورات اکستر نال برای ما
# import time  # ایجاد وقفه و هر زمان یک ه با تایم داریم ما
# import queue  # ایجاد صف و شاخه ای منظم برای محاسبات ما و دیتا بیسی که بشود درونش کنکاش کرد
import threading  # مکمل بالایی
import zipfile  # استفاده از زیپ فایل برای اکسترکت کردن و کار هایی که مربوط به فایل هایی زیپ میشود
import os  # پردازش سیستم عامل مثل پیدا کردن مسیر فایل ها و ...
# import shutil  # انجام کار هایی با فایل ها که نیاز به سطح دست رسی بالا دارد مثل پاک کردن و...
import json  # ساخت فایلی که به شکل کی ولیو کار میکند و برای زخیره سازی اطلاعات کاربرد دارد و همچنین ادیت و بروززسانی اطلاعات خیلی سبک
# from fileinput import filename
# from typing import Union
from pathlib import Path
import time
from threading import Thread

# import socket
# from pathlib import Path

# import platform
# import re
# import subprocess


import socketio
# try:
import selenium  # اسجاد فرایندی اتوملت برای کار با وب
import ttkbootstrap as ttk  # برای کار کردن با ویجت های تکینتر
# from ttkbootstrap.constants import *  # برای کار کردن با انواع کانتنت های ttk
import requests  # ایجاد ارتباط با وپ با پروتکل http
import pyperclip  # کپی متن انتخاب شده درون کیلیپبورد
import tkinter as tk  # ایجاد یک فرایند گرافیک
from cryptography.fernet import Fernet  # بریا رمز نگاره فایل جیسون و خوادن رمز نگاره شده اون و اما زدنش
from tkinter import messagebox, Button  # ایجاد مسیج هایی به حالت پاپ آپ

# except ImportError:
#     print("وابستگی های مورد نیاز درحال نصب هستن...")
#     subprocess.run([sys.executable, "-m", "pip", "install", "--break-system-packages", "--no-cache-dir", "selenium", "ttkbootstrap", "requests", "pyperclip", "cryptography"])
#     subprocess.run(["sudo", "-n", "apt", "install", "-y", "python-tk"])
    # print("وابستکی ها نصب شدن و نیار است دوباره برنامه اجرا شوذ")
    # sys.exit()

# برای این است که در کد برای استفاده ار این ها نیاز نباشد از selenium
from selenium import webdriver  # استقاده از وب درایور برای ارتباز با سایت
from selenium.webdriver.chrome.service import Service  # برای استفاده از وب درایور درون سلنیوم نسخه ۴ به بالا سروایس لازم است
from selenium.webdriver.common.keys import Keys  # برای استفاده از دکمه هایی که غیر حرقی هستن مثل اینتر
from selenium.webdriver.common.by import By  # برای جست وحو برای برای المنت ها و موارد این چنین
from selenium.webdriver.support.ui import WebDriverWait  #
from selenium.webdriver.support import expected_conditions as EC  # این و بالایی برای ایجاد وفقه برای محاسبات و یالا اومدت سایت هست

print("ماژول ها با موفقیت نصب شده است")

Fernet.generate_key()


def secret_key(filname: str = "key.key") -> None:
    if not os.path.exists(filname):
        try:
            with open(filname, "wb") as f:
                f.write(Fernet.generate_key())
        except FileNotFoundError as e:
            print(f"{e}نشد که رمز را بار گذاری کنیم")
    pass

def secret_key_load(filname: str = "key.key") -> bytes:
    try:
        with open(filname, "rb") as f:
            return f.read()
    except FileNotFoundError as e:
        print(f"{e}")


secret_key(filname="key.key")
key = secret_key_load("key.key")
f1 = Fernet(key)

# این وریبل ها برای زخیره شدن مواردی است که در کد ها مون استفاده میکنیم
settings = None
master_values = None
dn = None
driver_choice = None
user_provided_driver_path = None
url_web_driver_acres = None
zip_file_name = None
zip_file_storage_path = None
user_name_modem_login = None
pas_modem_login = None
flag_point=None
num1=None
num2=None
# تابعی برای ساخت موراد پایه ای وب درایور
def star01():
    global settings
    settings = {"path_driver": user_provided_driver_path, "username": user_name_modem_login, "pasword": pas_modem_login,"adres": dn,"ping1": num1,"ping2": num2}
    print(f"{settings}--------")
    settings_s00 = json.dumps(settings)
    settings_s01 = settings_s00.encode()
    settings_s02 = f1.encrypt(settings_s01)
    print(f"###############3{settings_s02}\n{f1.decrypt(settings_s02)}")

    def save_settings(filename: str = "settings.json") -> str:  # ما در این بخش میایم و تمام مواردی که این تابع نیاز دارد بگیرد را طبق موارد اصلاحی پایتون جدید تنظیم میکنیم یعنی آرگومان اول باید متغیری در تایبپ دیکت بگیرد و میتوان تایپ کی و ویلیو های داخل خود اون هم مشخص کرد و بعد میگوییم متغیر دومی دیتایی با تایپ استرینگ باشد و مقدار دیفالت اون اگر مخاطب نداد میگذاریم و بعد با علامت <-میگوییم که خروجی تابع  ما چی خواهد بود که هر نوع دیتایی باشد میتوانیم بدهیم مثل اینت و ..
        try:
            with open(filename,"w") as f:  # یعنی با متودپ داخیلی مدیریت فایب ویث برای این فایل در خال نوشتن درونش باز کن و قابلیت دست رسی بهش بده با شی به نام f
                f.write(settings_s02.decode())  # یعنی اف که میشود اشاره به فایل ما درونش بنویس
        except FileNotFoundError as e:
            print(f"problem1{e}")
        try:
            with open(filename, "r") as f:
                return f.read()
        except FileNotFoundError as e:
            print(f"{e}")

    def load_settings( filename: str = "settings.json") -> dict:  # تابعی میسازیم برای خواندن تنظیمات و جایگذاری و اپیدت در صورت لزوم با ورودی استرینگ که فایل نیم ما دیفالت میشود مقداری که میبینید
        settings_d = save_settings("settings.json")

        if not os.path.exists(
                filename):  # میره در مسیر فایل نیم و اگر چیزی نبودش غلت بر میگرداند که نات میخورد و ایف اجچرا میشود
            with open(filename, "wb") as f:  # فایلی که جیسون هست باز میکند با قابلیت نشتن درونش یا نبود میسازتش
                json.dump({},
                          f)  # و اگر ساخت یک دیکشنری خالی میسازارد تا که مخاطب با مواردی که مارد میکند ناخ.د آگاه آن را پر کندش
                # درست را بر میگرداند
        try:

            val = settings_d  # و در این مرحله که فایل باز شده است سعی میکند آن فایل را بخواند و در اینده بهش میگیم که موارد یک همیخماهیم را ازشون در بیاورد تا درون جایگاخ مناسب قرار دهیم
            val2 = f1.decrypt(val)
            return json.loads(val2)
        except json.decoder.JSONDecodeError as e:
            print(
                f"is fille or streachters bad{e}")  # میگوید اگر اروری بودش یا نوع فایل بد بودش همچنین اروری بده و غلت را بر میرگداند

    load_settings()


try:
    with open("settings.json", "r") as f:
        a = f.read()
        a = a.encode()
        try:
            master_values = json.loads(f1.decrypt(a))
            print(master_values)
        except json.decoder.JSONDecodeError as e:
            print(f"{e}")
            master_values = {}
        except Exception as e:
            print(f"{e}")
            master_values = {}
except FileNotFoundError as e:
    with open("settings.json", "w") as f:
        master_values = {}


def run_webdriver_setup():
    global user_provided_driver_path

#    برای اینک هدر این بخش میفهمیم ایا مسیر درست وارد شده است یا خیر


    print("\n فرایندی که برای سنجش این است که ما درایور داریم یا خیر🌕")

    if driver_choice == "yes":

        if user_provided_driver_path and os.path.isfile(user_provided_driver_path):
            try:
                master_values.update({"path_driver": user_provided_driver_path})
                print("فرایند کپی مسیر اتقاف افتاده است")
                return True
            except Exception as  e:
                messagebox.showerror("ERror", f"{e}شما yes کیلیک کردید ولی به دستی ادرس قایل کیپ تشده است")
                return False
                # این ارور وقتی نمایش داده میش.د که مخاطب آدرس درست نداده باشد
        else:
            messagebox.showerror( "error","The path is wrong.")
    elif driver_choice == "no":  # یعنی اینکه اگر انتخاب کلاینت noبودش برای ما این فرایند پایین انجام بده
        if not all([url_web_driver_acres, zip_file_name, zip_file_storage_path]):
            print(f"{url_web_driver_acres}\n{zip_file_name}\n{zip_file_storage_path}")
            messagebox.showerror("error ", "بعضی وریبل ها مشکل دارند برسی کنید")
            return False
        print(f"شروع میکند به دانلود مواردی که مربوط به وب درایور میشود از {url_web_driver_acres}")
        try:
            zip_file_full_path = os.path.join(zip_file_storage_path, zip_file_name)
            print(
                f"فایل ها دانلود میشوند درون{zip_file_full_path}")  # به مخاطب نشان میدهیم که فایل دانلود شدهخ درون چه فولدری ریخته میسود
            response = requests.get(url_web_driver_acres,
                                    stream=True)  # در این بخ شمیگوویک از کدام urlدانلود کن و به چه حالتی دانلود انجام بده اینجا میگوییم که غیر یکباره و به حالت جریانی به مقدار چانک ها داده وارد کنش
            # raisesبرای این است جلوی خطا ها بگیرد و مدیریت کند
            response.raise_for_status()
            # در این بخش میگوییم که که فایل های ما در چه ابعاد و اندازه ای ریخته شوند و با چه غالبی در اینجا به شکل باینری است نوشته شوند
            if response.status_code == 200:
                os.makedirs(zip_file_storage_path, exist_ok=True)
                with open(zip_file_full_path, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            file.write(
                                chunk)  # در اینجا میگوششم هرکدام از اون for هارا داتخل فایل بریز که حجم هرکدامشون هم ۸کیلو بایت است
            print("دانلود کامل شده است")

            print(f"بخش دوم اکسترکت کردن فایل ها {zip_file_full_path} into {zip_file_storage_path}")
            # در اینجا یدونه فایل برای عملیات اکسترک کردن میازد  و یا پیدا میکند اگه مخاطب درست وارد کرده باشد
            with zipfile.ZipFile(zip_file_full_path, 'r') as zip_ref:
                zip_ref.extractall(zip_file_storage_path)
            print("اکسترکت موفقیت امیز بودش")

            # در بخش ما دنبلا درایور میگردیم
            driver_filename = "chromedriver.exe" if sys.platform == "win32" else "chromedriver"
            print(f"در حال جست و جوی{driver_filename}")
            found_driver_path = None
            for root, dirs, files in os.walk(zip_file_storage_path):
                for file in files:
                    # حروف فایل بدون در نظر گرفتن بزرگی و کوچکی مقایسه کنید
                    if file.lower() == driver_filename.lower():
                        found_driver_path = os.path.join(root, file)  # اینجا ما اسم کامل مسیر در دست داریم
                        print(f"fuond{driver_filename} at {found_driver_path}")
                        break
                if found_driver_path:
                    break  # پیدا شده نیازی به گردش در موارد دایین تر درخت نیست
            if not found_driver_path:
                print(f" not founfd in the extracted content")
                raise FileNotFoundError(f"{driver_filename} پیدا نشد درون فایل اکسترکت شده")
            target_dir = "driver_files"  # تعریف نام فهرست زخیره سازی نهایی
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
                print(f"created {target_dir}")

            target_path = os.path.join(target_dir, driver_filename)
            print(f"fuond{driver_filename} at {target_path}")

            if not sys.platform == "win32":
                try:
                    os.chmod(found_driver_path, 0o777)
                    print(f"ایجاد سطح دست رسی")
                except OSError as e:
                    print(f"<<<نتوانستیم که سطح دست رسی اجرایی به کد بدهیم")


            print(f"{target_dir}------------{driver_filename}--------{os.getcwd()}------------{target_path}-----{found_driver_path}")
            user_provided_driver_path=os.path.join(os.getcwd(),found_driver_path)
            print(master_values)
            print(user_provided_driver_path)
            try:
                pyperclip.copy(user_provided_driver_path)
                print(f"مسیر{user_provided_driver_path}درون کلیپبورد کپی شدش")
            except Exception as e:
                print(f"optinal:خطا برای کپی شدت مسیر درون کلیپبورد{e}")
            # در این مرحله ما فایل هارا از هرز زیپ ها پاک میکنیم
            # try:#تلاش پرای پاک کردن هرز زیپ ها
            # print(chromedriver_zip_path)
            # os.remove(chromedriver_zip_path)
            # print(f"زیپ فایل{zip_file_name}پاکشده است")
            # except OSError as e :
            #     print(f"ارور داده شده سات {e}و نیاز به پاک کردن است")
            # try:
            #     shutil.rmtree(chromedriver_zip_path)
            #     print(f"فایل زیپ {chromedriver_zip_path}پاک شده است")
            # except OSError as e: #فرق oserrorبرای خطاهای مربوط به سیستم عامل مثل پیدا نکردن دیسک یا فایل یا قطعی شبکه است و اکسکپشن برای همه خطاها
            #     print(f"    نتوانستیم پاک سازی را درست انجام دهیم: {e}")

            print("   پاکسازی پایان یافت")
            print("فرایند وب دریاور و نصب اون به درست انجام گرفت")
            return True  # Indicate success.
        # شکار خطاهای خاصی که در طول فرایند راه اندازی شناسایی نشدن

        except requests.exceptions.RequestException as e:  # برای مدیریت ارور های با محوریت ریکوست
            messagebox.showerror("Download Error", f"این ارور مربوط به بخش دانلود فایل میشود: {e}")
            return False
        except zipfile.BadZipFile:  # یعنی فایل زیپ دجار اشکال شده است و خراب است
            messagebox.showerror("Zip Error",
                                 f"فایل دانلود شده برای ما قابلیت شناسایی ندارد و ممکن استنا معتبر بوده باشد{zip_file_name}")
            return False
        except FileNotFoundError as e:  # فایلی که در جست وجوی اون بودیم نیستش
            messagebox.showerror("File Not Found", f"ارور: {e}")
            return False
        except OSError as e:  # این جا یعنی اینکه به ما ارور مربوط به osداده است که در قبل کش نشده است
            messagebox.showerror("OS Error", f"Error during file/folder operations: {e}")
            return False
        except Exception as e:  # هر اروری
            messagebox.showerror("شناسایی نشده", f"اروری که برای ما قابلیت شناسایی نداشته است: {e}")
            return False

    else:
        # این بخش رسیدگی میگند به جایی که درایور انتخاب شده اصلاتهی باشد
        messagebox.showerror("Error", "شما هیچ حالتی برای وب درایور انتخاب نکرده اید")
        return False



# بخش دوم ساخت صفه لاگین در مودم و تنظیمات صفه مودم
# creat_tread = queue.Queue()
# THREAD_SENTNEL = object()  # از این درون ترد و مواردی که به یک نشانه برای پایان کار نیاز داریم استفاده میشود و ابجکت یعنی هر بار باری من یم شی خالی بساز که یکتا است و هیچ شبیهی ندارد


def create_and_show_key_ring(root_salam):#$
    # در اینجا ما یک نسخه از پنجره اصلی که لوپ روی اون هست به ونجره ای میدهیم که  داریم میسازیم و قبل از شروع پنجره جدید قبلی را پنهان مکینیم
    root_salam.withdraw()
    # پمجره بعدی مسازیم که بچه بنبجره قلی است
    key_ring = ttk.Toplevel(root_salam)
    key_ring.title("Modem Login Setup")
    key_ring.geometry("700x600")  # سایز صفه جدید تنطیم میکنیم

    # تم هم خود به خود به حالت صفه مادر در می اید خود به خود
    # نمیتوانیم که حالتی غیر از صفه مادر دهیم
    # اسخت  تابع داخلی مخصوص کی رینگ و ویجت هایی که دارد
    def click_modem_pass():
        global pas_modem_login  # ما باید این متغیر به حالت جهانی زخیره کنیم
        # این پنجره مخصوص دریافترمز از ویجت است
        pas_input = import01_kr.get().strip()
        if len(pas_input) == 0:
            # اگر خالی بود درون لیبل مینویسه  که مقدار وارد شده خالی است
            label01_kr.configure(text="خالیه", bootstyle="danger")
        else:
            pas_modem_login = pas_input  # رمز به حالت جهانی زخیره میکند
            label01_kr.configure(text="ست کردن پسوورد", bootstyle="success")  # پیام تایید
            # settings.update({"pasword":pas_modem_login})

    def click_modem_user():
        global user_name_modem_login  # نساز است که اسم بهع حالت جهانی زخیره شود
        # اینجا میگیریم اسم ورود و نام کاربری مخاطب با کیلیک روی ویجت
        user_input = import02_kr.get().strip()
        if len(user_input) == 0:
            label02_kr.configure(text="فیلد یوسر نیم خالیهیا رنج دامنه", bootstyle="danger")
        else:
            user_name_modem_login = user_input
            label02_kr.configure(text="یوسر نیم زخیره شد", bootstyle="success")
            # settings.update({"username":user_name_modem_login})
    def click_modem_adres():
        global dn
        # اینجا میگیریم اسم ورود و نام کاربری مخاطب با کیلیک روی ویجت
        dn = import03_kr.get().strip()
        if len(dn) == 0:
            label03_kr.configure(text="فیلد آدرس مودم خالی است", bootstyle="danger")
        else:
            label03_kr.configure(text="آدرس زخیره شد", bootstyle="success")

    def creat_range():
        global num1
        num1 = import04_kr.get().strip()
        if len(num1) == 0:
            label04_kr.configure(text="فیلد میزان رنج مورد نظر برا پینگ خالی است", bootstyle="danger")
        else:
            label04_kr.configure(text="میزان مورد نظر زخیره شدش", bootstyle="success")
        try: 
            num1=int(num1)
        except ValueError:
            label04_kr.configure(text="باید عدد وارد کنید", bootstyle="danger")

    def creat_range2():
        global num2
        num2 = import05_kr.get().strip()
        if len(num2) == 0:
            label05_kr.configure(text="فیلد میزان رنج مورد نظر برا پینگ خالی است", bootstyle="danger")
        else:
            label05_kr.configure(text="میزان مورد نظر زخیره شدش", bootstyle="success")
        try: 
            num2=int(num2)
        except ValueError:
            label03_kr.configure(text="باید عدد وارد کنید", bootstyle="danger")


        # اینجا برای گذاشتن نخ های ما است هدف proccess_input شروع کنه کار را ترد در نظر داشته باشید جایی برای سنجش مقدرا نگهبان تا به مشکل نخوریم و صدا کند ترد جوین on_key_ring_cluoe و statrt_selenium

    print("Note: Background input processing thread/widgets from original code are omitted here for clarity.")

    # ویجت های ما برای key_ringو پسوند هم دادیم تا با صفه اصلی ترکیب نشوند
    label00_kr = ttk.Label(key_ring, text="Enter Modem Credentials:", bootstyle="info")
    label00_kr.pack(pady=10, padx=10)

    # اینجاما دکمه هارابه شکل لیبل وارد میکنیم و اون ها به تابع مورد نظر ربط میدهیم
    label01_kr = ttk.Button(key_ring, text="Modem Password:", bootstyle="info", width=20, command=click_modem_pass)
    # به ما پسوورد به حالت *
    import01_kr = ttk.Entry(key_ring, width=40, show="@")
    try:
        if master_values["pasword"]:
            import01_kr.insert(0, f"{master_values["pasword"]}")
    except:
        pass
    label01_kr.pack(pady=10)
    import01_kr.pack(pady=5)

    label02_kr = ttk.Button(key_ring, text="Modem Username:", bootstyle="info", width=20, command=click_modem_user)
    import02_kr = ttk.Entry(key_ring, width=40)
    try:
        if master_values["username"]:
            import02_kr.insert(0, f"{master_values['username']}")
    except:
        pass
    label02_kr.pack(pady=10)
    import02_kr.pack(pady=5)

    label03_kr = ttk.Button(key_ring, text="Modem adres:(192.168.1.1)", bootstyle="info", width=25, command=click_modem_adres)
    import03_kr = ttk.Entry(key_ring, width=40)
    try:
        if master_values["adres"]:
            import03_kr.insert(0, f"{master_values["adres"]}")
    except:
        pass
    label03_kr.pack(pady=10)
    import03_kr.pack(pady=5)
    
    
    label04_kr = ttk.Button(key_ring, text=f"ping A(A>ping low power)", bootstyle="info", width=20, command=creat_range)
    import04_kr = ttk.Entry(key_ring, width=40)
    try:
        if master_values["ping1"]:
            import04_kr.insert(0, f"{master_values["ping1"]}")
    except:
        pass
    label04_kr.pack(pady=10)
    import04_kr.pack(pady=5)

    label05_kr = ttk.Button(key_ring, text="ping Q(Q< ping <A stable) ", bootstyle="info", width=20, command=creat_range2)
    import05_kr = ttk.Entry(key_ring, width=40)
    try:
        if master_values["ping2"]:
            import05_kr.insert(0, f"{master_values["ping2"]}")
    except:
        pass
    label05_kr.pack(pady=10)
    import05_kr.pack(pady=5)



    def star_selenium_action():
        # تعیین پسوورد و اسم که مخاطب میدهد
        if not user_name_modem_login or not pas_modem_login or not dn:
            messagebox.showwarning("بخوان پیام", "دوباره باید مقادیر وارد کنید")
            return  # کد نگه میدارد تا مخاطب بتواند که دوبارهع مقدار وارد کند

        print("صفه تنظیمات مودخم بسته میشود و فرایند سلنیوم آغاز میشود")
        # اینجا ما تصمیم میگریم که صفه تنظیم رمز نابود شود تا فرایند مخاسبات ما شروع شود
        key_ring.destroy()

        run_selenium_logic(root_salam)

    ttk.Button(key_ring, text="متصل شو به تنظیمات مودم", command=star_selenium_action, bootstyle="success").pack(
        pady=23)

    # فرایند بستن پتجره تاپ لول از طریق زدن روی دکمه x
    def on_key_ring_cluse():
        key_ring.destroy()
        if root_salam and root_salam.winfo_exists():
            root_salam.destroy()

    key_ring.protocol("WM_DELETE_WINDOW", on_key_ring_cluse)  # برای مدریت رفتار های سیستم عامل است که با اون کلمه خاص با کیلیک روی ضربدر بسته میشود



# مسیر اسکریپت در حال اجرا
APP_NAME = "my-app-package" # نام بسته که در control و دسکتاپ استفاده می‌شود

# --- مسیرهای استاندارد برای داده‌های کاربر در پوشه خانگی ---
# این پوشه‌ها همیشه برای کاربر عادی قابل نوشتن هستند.
USER_DATA_DIR = Path.home() / ".local" / "share" / APP_NAME # برای فایل‌های داده برنامه (مثل دیتابیس)
USER_CONFIG_DIR = Path.home() / ".config" / APP_NAME # برای فایل‌های پیکربندی (مثل کلید رمزنگاری)

# --- اطمینان از وجود پوشه‌های پایه ---
# این خطوط پوشه‌های بالا را در صورت عدم وجود ایجاد می‌کنند.
# این‌ها نیازی به دسترسی روت ندارند چون در پوشه خانگی کاربر هستند.
USER_DATA_DIR.mkdir(parents=True, exist_ok=True)
USER_CONFIG_DIR.mkdir(parents=True, exist_ok=True)

# --- تعریف مسیر فایل دیتابیس ---
DATABASE_FILE_NAME = "device_data.json"
JSON_DB_FILE = USER_DATA_DIR / DATABASE_FILE_NAME #



#JSON_DB_FILE = salam_dir.mkdir(parents=True, exist_ok=True)
  #os.path.join( os.path.join(os.path.expanduser('~'), '.local', 'share', 'modem-m') , 'device_data.json')

def ping_ai():
    global JSON_DB_FILE
    print(f"JSON_DB_FILE-------------//////////////////-------------> {JSON_DB_FILE}")
    db_lock = threading.Lock()  # برای جلوگیری از تداخل در زمان دسترسی به فایل
    def load_data():
        """
        داده‌ها را از فایل JSON می‌خواند.
        اگر فایل وجود ندارد یا خالی/خراب است، یک دیکشنری خالی برمی‌گرداند
        و خطا نمی‌دهد، بلکه لاگ می‌کند.
        """
        with db_lock:
            # اگر فایل وجود ندارد یا خالی است
            if not os.path.exists(JSON_DB_FILE) or os.path.getsize(JSON_DB_FILE) == 0:
                print(
                    f"اطلاعات: فایل دیتابیس JSON در '{JSON_DB_FILE}' یافت نشد یا خالی است. یک فایل جدید ایجاد خواهد شد.")
                return {}  # یک دیکشنری خالی برای شروع برگردان
            try:
                with open(JSON_DB_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                # اگر فایل JSON خراب است
                print(f"هشدار: فایل دیتابیس JSON در '{JSON_DB_FILE}' خراب است. یک فایل جدید جایگزین آن خواهد شد.")
                return {}
            except Exception as e:
                # هر خطای دیگری در زمان خواندن فایل
                print(f"هشدار: خطایی در خواندن فایل دیتابیس JSON رخ داد: {e}. یک فایل جدید جایگزین آن خواهد شد.")
                return {}

    def save_data(data_to_save):
        """ داده‌ها را در فایل JSON ذخیره می‌کند. """
        with db_lock:
            try:
                with open(JSON_DB_FILE, 'w', encoding='utf-8') as f:
                    json.dump(data_to_save, f, indent=2, ensure_ascii=False)
                # print(f"اطلاعات: دیتابیس JSON در '{JSON_DB_FILE}' با موفقیت ذخیره شد.")
            except Exception as e:
                print(f"خطا: در زمان ذخیره دیتابیس JSON خطایی رخ داد: {e}")

    def safe():
        time.sleep(12)
        with db_lock:
            try:
                with open(JSON_DB_FILE, 'w', encoding='utf-8') as f:
                    json.dump({}, f, indent=2)
            except Exception as e:
                print(f"error:{e}")

    def update_device_data(device_id: str, ping: float, model: str = None, manufacturer: str = None):
        global flag_point
        """
        اطلاعات یک دستگاه را در دیتابیس JSON به‌روزرسانی یا اضافه می‌کند.
        """
        current_db_data = load_data()  # داده‌های فعلی را بارگذاری کن

        if device_id in current_db_data:
            # دستگاه از قبل وجود دارد، فقط اطلاعات را به‌روزرسانی کن
            print(f"دستگاه '{device_id}' در دیتابیس موجود است. به‌روزرسانی اطلاعات...")
            print(f"---------------//////////------------/////////---------{flag_point}")
            # ping_ai2()
            current_db_data[device_id]['ping'] = ping
            # مدل و سازنده را فقط اگر مقادیر جدیدی داده شده‌اند، آپدیت کن
            if model is not None:
                current_db_data[device_id]['model'] = model
            if manufacturer is not None:
                current_db_data[device_id]['manufacturer'] = manufacturer
        else:
            # دستگاه جدید است، یک ورودی جدید ایجاد کن
            print(f"دستگاه جدید '{device_id}' شناسایی شد. اضافه کردن به دیتابیس...")
            current_db_data[device_id] = {
                'ping': ping,
                'model': model,
                'manufacturer': manufacturer
            }

        save_data(current_db_data)  # داده‌های به‌روز شده را ذخیره کن
        # print(f"اطلاعات '{device_id}' با موفقیت در دیتابیس ذخیره شد.") # این خط تکراری بود، از تابع save_data حذف شد
    # --- کلاینت Socket.IO (بدون تغییر در منطق) ---
    sio = socketio.Client()

    # def get_own_ip():
    #     hostname = socket.gethostname()
    #     return socket.gethostbyname(hostname)

    @sio.on('ping_update')
    def on_ping_update(data) :
        print(f"-----/-/-/-/---{data}")
        """
        این تابع وقتی پیام 'ping_update' از سرور دریافت می‌شود، اجرا می‌شود.
        داده‌های دریافتی را برای به‌روزرسانی دیتابیس JSON استفاده می‌کند.
        """
        thred=threading.Thread(target=safe, daemon=True)
        thred.start()
        if not data:
            print("هیچ داده‌ای برای به‌روزرسانی دریافت نشد.")
            return

        try:
            device_id = next(iter(data))
            # print(f"///[[[[--{device_id}")
            device_info_dict = data[device_id]
            # print(f"///-///{device_info_dict}")
            ping_value = device_info_dict.get("ping")
            # print(f"///-///---/=/{ping_value}")
            model_value = device_info_dict.get('model')
            manufacturer_value = device_info_dict.get('manufacturer')

            if ping_value is not None:
                print(f"پینگ جدید دریافت شده برای دستگاه {device_id}: {ping_value}")
                # حالا اطلاعات را در دیتابیس JSON ذخیره یا به‌روزرسانی می‌کنیم
                update_device_data(device_id, ping_value, model_value, manufacturer_value)
            else:
                print(f"مقدار پینگ برای دستگاه '{device_id}' در داده دریافتی موجود نیست.")

        except StopIteration:
            print("خطا: داده دریافتی ساختار نامعتبری دارد (دیکشنری خالی).")
        except KeyError as e:
            print(f"خطا: داده دریافتی ساختار نامعتبری دارد. کلید {e} پیدا نشد.")
        except Exception as e:
            print(f"خطایی در پردازش داده دریافت شده: {e}")

    @sio.on('connect')
    def on_connect():
        print("connected sucsefully")

        # می‌توانید بلافاصله پس از اتصال وضعیت فعلی دیتابیس را چاپ کنید
        # current_devices = load_data()
        # print("دستگاه‌های موجود در دیتابیس JSON:", json.dumps(current_devices, indent=2, ensure_ascii=False))

    @sio.on('disconnect')
    def on_disconnect():
        print("disconnected sucsefully")

    @sio.on('connect_error')
    def on_connect_error(data):
        print("error connect")

    # def print_device_info(device_id: str, model: str = None, manufacturer: str = None):
    #     info_str = f"دستگاه: {device_id}"
    #     if model:
    #         info_str += f", مدل: {model}"
    #     if manufacturer:
    #         info_str += f", سازنده: {manufacturer}"
    #     print(info_str)



    # def safe(js):

    # def monitor_clients(standard, min_ping, max_ping):
    #     clients_in_db = load_data()  # کلاینت‌ها را از دیتابیس JSON بارگذاری می‌کنیم
    #
    #     print(f"تعداد دستگاه‌های موجود در دیتابیس: {len(clients_in_db)}")
    #     if clients_in_db:
    #         print("اطلاعات دستگاه‌ها:")
    #         for client_id, device_data in clients_in_db.items():
    #             print_device_info(client_id, device_data.get('model'), device_data.get('manufacturer'))
    #             print(f"  آخرین پینگ: {device_data.get('ping', 'نامعلوم')}")
    #     else:
    #         print("دیتابیس دستگاه‌ها خالی است.")
    #
    def connect_to_server():
        try:
            sio.connect('http://0.0.0.0:5000')  # اطمینان از صحت ادرس مودم
            print(f"اتصال به سرور برقرار شد.")
        except Exception as e:
            print(f"خطا در اتصال به سرور: {e}")

    # --- شروع برنامه ---
    # این تابع در زمان اجرا، دیتابیس را لود می‌کند و اگر وجود نداشته باشد/خراب باشد، لاگ می‌کند.
    # در اولین ذخیره‌سازی، فایل جدید ساخته خواهد شد.

    connect_to_server()
    # sio.wait()
    # standard_ping = 3  # تعین پیشینه و کمینه مورد نظر برای کار کردن
    # min_ping = 2
    # max_ping = 4
    # monitor_clients(standard_ping, min_ping, max_ping)




def run_selenium_logic(root_window_to_distory):
    global flag_point
    driver = webdriver.Chrome(service=Service(executable_path=user_provided_driver_path))
    print(f"___________________________?_?_?_{bool(driver)}")
    print("شروع منطق سلنیوم")
    star01()
    settings.update({"path_driver": user_provided_driver_path, "username": user_name_modem_login, "pasword": pas_modem_login, "adres": dn,"ping1": num1,"ping2": num2})
    print(settings)
    print("جایگزینی اتفاق افتاد")

    while bool(driver):
        if not user_provided_driver_path:
            messagebox.showerror("Error", "ChromeDriver path is not set. Cannot run Selenium.")
            # پنجره ریشه نابود میسکند تا بتوانیم درست از ان خارج شویم
            if root_window_to_distory and root_window_to_distory.winfo_exists(): root_window_to_distory.destroy()
            return

        if not user_name_modem_login or not pas_modem_login:
            messagebox.showerror("تنظیم نشده", "شما درست رمز عبور یا یوزر نیم وارد نکرده اید و ما نمیتوانیم که سلنیوم را باز کنیم")
            if root_window_to_distory and root_window_to_distory.winfo_exists(): root_window_to_distory.destroy()
            return
        def e_9 ():
            root_window_to_distory.destroy()
            driver.quit()
        try:
            driver.get(f"http:/{dn}")  #
        except Exception as e:
            messagebox.showerror("erroR", e)
            salam.protocol("ERR_INTERNET_DISCONNECTED",e_9())
        try:  #
            # ورود به صفحه
            username_input = WebDriverWait(driver, 10).until(  #
                EC.presence_of_element_located((By.ID, "user_name"))  #
            )
            username_input.send_keys(user_name_modem_login)

            password_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "user_passwd"))
            )
            password_input.send_keys(pas_modem_login)
            password_input.send_keys(Keys.RETURN)

            WebDriverWait(driver, 10).until(
                EC.url_changes(driver.current_url)
            )

            time.sleep(3)

            # اجرای اسکریپت جاوااسکریپت برای تغییر صفحه
            driver.execute_script("ajax_change_page('advance');")

            time.sleep(3)

            # پیدا کردن و نمایش تمام المان‌های hidden
            hidden_elements = driver.find_elements(By.CSS_SELECTOR, '[type="hidden"]')
            for elem in hidden_elements:
                driver.execute_script("arguments[0].style.display = 'block'; arguments[0].style.visibility = 'visible';",
                                      elem)

            # پیدا کردن و نمایش فرم‌های مخفی
            hidden_forms = driver.find_elements(By.CSS_SELECTOR, 'form[style*="display: none"], form[hidden]')
            for form in hidden_forms:
                driver.execute_script("arguments[0].style.display = 'block';", form)

            # پیدا کردن و نمایش جداول مخفی
            hidden_tables = driver.find_elements(By.CSS_SELECTOR, 'table[style*="display: none"], table[hidden]')
            for table in hidden_tables:
                driver.execute_script("arguments[0].style.display = 'table';", table)

            print("✅ تمام عناصر مخفی نمایش داده شدند.")

            # پیدا کردن iframe ها
            frames = driver.find_elements(By.TAG_NAME, "iframe")
            print(f"🔍 تعداد iframe‌ها در صفحه: {len(frames)}")

            if len(frames) > 0:
                driver.switch_to.frame(frames[0])  # سوئیچ به iframe 0
                print("✅ داخل iframe شماره 0 رفتیم.")

                try:
                    # پیدا کردن فیلد confirm_code و نمایش آن
                    hidden_confirm_code = driver.find_element(By.CSS_SELECTOR, 'input[type="hidden"][name="confirm_code"]')
                    driver.execute_script(
                        "arguments[0].style.display = 'block'; arguments[0].style.visibility = 'visible';",
                        hidden_confirm_code)

                    print("عنصر confirm_code در iframe 0 قابل مشاهده شد.")

                    # استخراج و نمایش کل خط HTML
                    confirm_code_html = hidden_confirm_code.get_attribute("outerHTML")
                    print(f"🔹 کل خط HTML مربوط به confirm_code: {confirm_code_html}")

                except Exception as e:
                    print(" نتوانستیم مقدار confirm_code را استخراج کنیم:", e)

                # پیدا کردن فیلد FirewallEnable و نمایش آن
                try:
                    hidden_firewall_enable = driver.find_element(By.CSS_SELECTOR,'input[type="hidden"][name="FirewallEnable"]')
                    driver.execute_script(
                        "arguments[0].style.display = 'block'; arguments[0].style.visibility = 'visible';",
                        hidden_firewall_enable)


                    print("✅ عنصر FirewallEnable قابل مشاهده شد.")

                    # استخراج و نمایش کل خط HTML
                    firewall_enable_html = hidden_firewall_enable.get_attribute("outerHTML")
                    print(f"🔹 کل خط HTML مربوط به FirewallEnable: {firewall_enable_html}")

                except Exception as e:
                    print("⛔ نتوانستیم مقدار FirewallEnable را استخراج کنیم:", e)

                # پیدا کردن و کلیک روی checkbox ui_FirewallEnable

                def ping_ai2():
                    global JSON_DB_FILE
                    global num1
                    global num2
                    try:
                        with open(JSON_DB_FILE, 'r', encoding='utf-8') as f:
                            global flag_point
                            data0 = json.load(f)
                            all_pings = []
                            for device_id, device_info in data0.items():
                                ping_value = device_info.get("ping")
                                all_pings.append(ping_value)
                                print(all_pings)
                            print(f"{num1}: {type(num1)}, {num2}: {type(num2)}")
                            if all(num1 >= p for p in all_pings):#وقتی همه پینگ ها از کمترین میزان پینگ مورد نظر ما کمتر باشند قدرت مودم    کم میشود
                                flag_point = 1
                            elif all( num1 >= p >= num2 for p in all_pings) or any(num1 >= p for p in all_pings ) : #وقتی همه پینگ ها در رنج مورد نظر ما باشند و یا فقط تعدادی وضعیت مناسب داشته باشند     ثابت می ماند
                                flag_point = 2
                            else:
                                flag_point = 3#وقتی چیزی غیر از این است یعنی تمام پینگ ها عالی نیستن و تمام پینگ ها بین مقادری مورد نظر ما نیست و یا حد اقل چند پینگ در وضعیت عالی نیستن پس قدرت زیاد میشود
                    except Exception as e:
                        time.sleep(7)
                        print(f'error reading JSON file: {e}')

                print(f"////////-=-=-=-=/////////{flag_point}")

                try:
                    firewall_enable_checkbox = driver.find_element(By.CSS_SELECTOR,'input[type="checkbox"][name="ui_FirewallEnable"]')
                    wan_enable_checkbox = driver.find_element(By.CSS_SELECTOR,'input[type="checkbox"][name="ui2_wan_ping"]')
                    wan_enable_https_checkbox = driver.find_element(By.CSS_SELECTOR,"input[type='checkbox'][name='ui_WebLoginEnable']")
                    firewall_enable_checkbox.click()  # کلیک بر روی checkbox
                    print(" روی فیلد ui_FirewallEnable کلیک شد.")
                    threading.Thread(target=ping_ai, args=(),daemon=True).start()
                    print(f"////////-=-=-=-=/////////{flag_point}")
                    # cread_theتred = queue.Queue()
                    while True:

                        ping_ai2()
                        if flag_point == 1:
                            firewall_enable_checkbox.click()
                            time.sleep(2)
                        elif flag_point == 2:
                            wan_enable_checkbox.click()
                            time.sleep(2)
                        elif flag_point == 3:
                            # pass
                            wan_enable_https_checkbox.click()
                            time.sleep(2)
                except Exception as e:
                    try:
                        print(driver.window_handles)
                        print(" نتوانستیم روی فیلد ui_FirewallEnable کلیک کنیم:", e)
                        driver.quit()
                        # run_selenium_logic(root_window_to_distory)
                    except Exception as e:
                        root_window_to_distory.destroy()
                        driver.quit()
                        break
                driver.switch_to.default_content()  # برگشت به صفحه اصلی

            else:
                print("⛔ هیچ iframe‌ای در صفحه پیدا نشد!")
        except selenium.common.exceptions.TimeoutException:  # زمان از حد مجاز خودس برای یافتن موارد خوایته سده گذسته و دیگر مشکل دارد
            messagebox.showerror("Timeout Error",
                                 "A timeout occurred waiting for an element or page load. Check credentials, network speed, or element locators.")
            print("❌ Timeout error during Selenium interaction.")
        # به دیگر ارور هایی که ممکن است از تور برسی هارد بشن رسیدگی میکند
        except Exception as e:
            messagebox.showerror("Selenium Error", f"An unexpected error occurred during Selenium interaction: {e}")
            print(f"❌ Unexpected error during Selenium interaction: {e}") # ساختار finallyبرای ما ایجاد کننده این قابلیت است که در هر شرایطی هم باشد کد زیر مجمموعه اون اجرا میشود حتی اگر شرطی مثل بریک تجرت شود باز هم finallyاجرا میشود
        finally:
            # این فرایند بیشتر برای این است که پاکسازی مند و بعد از اتمام کار حتما موارد درخواستی راببند یا حذف کند یا...
            if driver:
                print("   Closing browser...")
                # driver.quit() # اگر درایور درست ران شده باشد و حاوی truباشد اینجا بعد از بسته شدن کار کامل بسته میشود
                print("   Browser closed.")
            # برای این این کد را نوشتیم که از کیل شدن تمام فرایند های این مطمن شویم تا در اجرا های بعدی مشکللی ایجاد نکند
            if root_window_to_distory and root_window_to_distory.winfo_exists():
                print("Closing main application window.")
                root_window_to_distory.destroy()
                driver.quit()
    root_window_to_distory.destroy()
    driver.quit()
# در این بهش است که ما کد اصلی برنامه را اجرا میکنیم و به حرکت در می آد برنامه
# به ای شکل که ما اینجا یک متغیر ویزّ داریم که در بر دارنده یک فرایند یا مقدار خاصی است مثال __name__یعنی اینکه این کد در چه حالتی ران شده مستقیم یا با ایمپورت که ارگ ایمپورت بوده مقدار__name__مساوی با خود اون کد ی بوده که ایمپورت کرده ولی اگر مستقیم ران شود متقیر ما برابر با __main__میشود
if __name__ == "__main__":
    # 1.مرحله اول و اساسی یعنی یاخت پنجره اصلی برنامه است
    salam = ttk.Window(themename="vapor")
    salam.title("WebDriver Setup")
    salam.geometry("900x750")

    # برای تعریف ویجت ها و ساختار بندی کردن مواردی مثل فیلد ها و این چنین درون صفحات مورد نیاز
    driver_option_var = tk.StringVar(value="")
    question_frame = ttk.Frame(salam);
    question_frame.pack(pady=10)
    ttk.Label(question_frame, text="Do you already have the ChromeDriver executable file on your system?",
              bootstyle="info").pack(side=tk.TOP, pady=5)
    ttk.Radiobutton(question_frame, text="Yes, I will provide the path", variable=driver_option_var, value="yes",
                    command=lambda: toggle_fields("yes"), bootstyle="success-toolbutton").pack(side=tk.LEFT, padx=10)
    ttk.Radiobutton(question_frame, text="No, I need to download it", variable=driver_option_var, value="no",
                    command=lambda: toggle_fields("no"), bootstyle="warning-toolbutton").pack(side=tk.LEFT, padx=10)

    path_frame = ttk.Frame(salam)
    label_path = ttk.Label(path_frame, text="Enter the full path to your chromedriver file:", bootstyle="info")
    import_path = ttk.Entry(path_frame, width=60)
    try:
        if master_values["path_driver"]:
            import_path.insert(tk.END, f"{master_values["path_driver"]}")
    except Exception as e:
        pass
    button_path = ttk.Button(path_frame, text="Confirm Driver Path", command=lambda: click_path(), bootstyle="primary")
    label_path_status = ttk.Label(path_frame, text="", bootstyle="primary")

    download_frame = ttk.Frame(salam)
    label00_dl = ttk.Label(download_frame, text="Please enter the following information to download ChromeDriver:",
                           bootstyle="info");
    label00_dl.pack(pady=5)
    label01_dl = ttk.Label(download_frame, text="ChromeDriver Zip File Download URL:", bootstyle="info")
    import01_dl = ttk.Entry(download_frame, width=60)
    button01_dl = ttk.Button(download_frame, text="Confirm URL", command=lambda: click_dl(1),
                             bootstyle="success")  # لامبدا برای این است که تابع ما در زکان کیلیک و با آرگومان مدنظر احضار شود چون لاکبدا تابعی بی نام اجرا میکند که با کیلیک اجرای تبع بینام باعث اجرای تابع اصلی ما یمشود
    label01_dl_status = ttk.Label(download_frame, text="", bootstyle="primary")
    label02_dl = ttk.Label(download_frame, text="Desired name to save the zip file (e.g., chromedriver.zip):",
                           bootstyle="info")
    import02_dl = ttk.Entry(download_frame, width=60)
    button02_dl = ttk.Button(download_frame, text="Confirm Zip File Name", command=lambda: click_dl(2),
                             bootstyle="success")
    label02_dl_status = ttk.Label(download_frame, text="", bootstyle="primary")
    label03_dl = ttk.Label(download_frame, text="Folder name for extracting files (e.g., driver_extracted):",
                           bootstyle="info")
    import03_dl = ttk.Entry(download_frame, width=60)
    button03_dl = ttk.Button(download_frame, text="Confirm Extraction Folder Name", command=lambda: click_dl(3),
                             bootstyle="success")
    label03_dl_status = ttk.Label(download_frame, text="", bootstyle="primary")
    label03_dl_download = ttk.Entry(download_frame, width=35,text = "downloading...").pack_forget()


    # این توابعرای ویجت های پنجره سلام هست و باید قبل از استفاده از اونها این ها قابل فذاخوانی باشند
    def toggle_fields(choice):
        global driver_choice
        driver_choice = choice
        if choice == "yes":
            download_frame.pack_forget()
            label_path.pack(pady=5)
            import_path.pack(pady=5, padx=20, fill=tk.X)
            button_path.pack(pady=10)
            label_path_status.pack(pady=5)
            path_frame.pack(pady=20, fill=tk.X, padx=20)
        elif choice == "no":
            path_frame.pack_forget()
            label01_dl.pack(pady=(10, 0));
            import01_dl.pack(pady=5, padx=20, fill=tk.X);
            button01_dl.pack(pady=5);
            label01_dl_status.pack(pady=2)
            label02_dl.pack(pady=(10, 0));
            import02_dl.pack(pady=5, padx=20, fill=tk.X);
            button02_dl.pack(pady=5);
            label02_dl_status.pack(pady=2)
            label03_dl.pack(pady=(10, 0));
            import03_dl.pack(pady=5, padx=20, fill=tk.X);
            button03_dl.pack(pady=5);
            label03_dl_status.pack(pady=2)
            download_frame.pack(pady=20, fill=tk.X, padx=20)
        else:
            path_frame.pack_forget();
            download_frame.pack_forget()


    def click_path():
        global user_provided_driver_path
        path_input = import_path.get().strip()
        # تعین مسکند اغسم مورد ناتظار برای فایل را طبق os
        driver_filename = "chromedriver.exe" if sys.platform == "win32" else "chromedriver"
        # چک میکند ایا فایلی با این اسم وجود دارد بدون در نظر گرفتن بزرگ یا ک.چک بودن حروف
        if os.path.isfile(path_input) and os.path.basename(path_input).lower() == driver_filename.lower():
            user_provided_driver_path = path_input
            label_path_status.configure(text=f"Path seems valid.", bootstyle="success")  # مسیج جواب را به ما میدهد
        elif len(path_input) == 0:
            label_path_status.configure(text="Please enter the path.", bootstyle="warning")
        else:
            user_provided_driver_path = None
            # اگر ارور بدهد اسم فیابل تعین شده را نشان میدهد
            label_path_status.configure(text=f"Invalid path. Must be the '{driver_filename}' file.", bootstyle="danger")


    def click_dl(field_index):
        # برای اینکه بتونیم یک فرایند بهتر و یک ساختار بهتری داشته باشیم به متغیر هایمان حالت گلوبال میدهیم تا در تمام کد استفاده کنیم ان هارا
        global url_web_driver_acres, zip_file_name, zip_file_storage_path
        if field_index == 1:
            url_input = import01_dl.get().strip()
            print(url_input)
            # یک برسی ساده که ببینم ایا با موارد مورد نیار همخوانی دارد یا خیر
            if len(url_input) == 0:
                label01_dl_status.configure(text="URL cannot be empty.",bootstyle="warning"); url_web_driver_adres = None
            elif not (url_input.startswith("http://") or url_input.startswith("https://")):
                label01_dl_status.configure(text="URL seems invalid.",bootstyle="warning"); url_web_driver_adres = None  # میسنجیم که آیا با موارد مورد نیاز ما شروع شده است یا خیر که ایا url است یا چرت و پرت وارد کرده است
            else:
                url_web_driver_acres = url_input; label01_dl_status.configure(text=f"URL confirmed.",bootstyle="success")
        elif field_index == 2:
            zip_input = import02_dl.get().strip()
            print(zip_input)
            if len(zip_input) == 0:
                label02_dl_status.configure(text="Zip file name ccannot be empty.",bootstyle="warning"); zip_file_name = None
            # میسنجیم که ایا اسم وارد شده توسط مخاطب با پسوند زیپ پایان یافته است یا اصلا همچین چیزی وجود دندارد
            elif not zip_input.lower().endswith(".zip"):
                label02_dl_status.configure(text="Recommended name ends with .zip.",bootstyle="info"); zip_file_name = zip_input
            else:
                zip_file_name = zip_input; label02_dl_status.configure(text=f"Zip file name confirmed.",bootstyle="success")
        elif field_index == 3:
            storage_input = import03_dl.get().strip()
            print(storage_input)
            if len(storage_input) == 0:
                label03_dl_status.configure(text="Extraction folder name cannot be empty.",bootstyle="warning"); zip_fille_storage = None
            else:
                zip_file_storage_path = storage_input; label03_dl_status.configure(text=f"Extraction folder name confirmed.", bootstyle="success")

    # تعریف فرایند های قابل انتظار برای دکمه ادامه
    def proceed_button_action():
        # 1.اگر موارد ابتدایی ما به اجرا در امده بود که یعنی تابع اون که اینجا امده به اجرا در انده بودش
        if run_webdriver_setup():
            # 2. اگر تایید شد و درست بود صفه دوم مارو بساز
            create_and_show_key_ring(salam)
        else:
            # فرایند مقدماتی و اولیه به درستی ران نشده که شما متن پایین میخوانید
            print("WebDriver setup failed. Cannot proceed.")
    

    # میسازیم دکمه ادامه و بهش اون تابع مورد نیاز الحاق میکنیم
    ttk.Button(salam, text="Continue", command=proceed_button_action, bootstyle="danger").pack(pady=20)

    # 2. شروع فرایند محاسبات گرافیکی
    # این حلقه است که باعث میشود تا فرایند های گرافیکی ما پایدار بماند چه والد باشد چه وارث
    # با بودن این اسکریپت ما اجرا است تا اینکه از بین برود.
    salam.mainloop()
    # salam.protocol("WM_DELETE_WINDOW", cpde_9)

    # پایان
    print("Application finished.")