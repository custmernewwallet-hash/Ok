#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
أتمتة شراء بطاقات Umniah PUBG - نسخة كاملة مع اختبار الأرقام
Umniah PUBG Card Purchase Automation - Complete Version with Number Testing
"""

import subprocess
import sys
import time
import requests
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

def install_requirements():
    packages = ['selenium', 'webdriver-manager', 'requests']
    for package in packages:
        try:
            __import__(package)
        except ImportError:
            print(f"📦 تثبيت {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package, "-q"])

install_requirements()

# ============================================================================
# البيانات
# ============================================================================
PRODUCT_URL = "https://eshop.umniah.com/ar/بطاقة-هدية-ببجي-600-يو-سي.html"
CHECKOUT_URL = "https://eshop.umniah.com/ar/checkout/index/"

PHONE = "797230107"
EMAIL = "ggssgg@gmail.com"
FULL_NAME = "testtesttest"
QUANTITY = 2

TELEGRAM_TOKEN = "7327256170:AAEiQ_F_BI1V9iUHzgPPui7JRwqGnj6Jys4"
TELEGRAM_CHAT_ID = "6873334348"

WAIT_TIME = 15
PAGE_LOAD_TIME = 2

# ============================================================================
# إعداد المتصفح
# ============================================================================

def setup_driver():
    """إعداد المتصفح"""
    print("🔧 إعداد المتصفح...")
    opts = Options()
    opts.add_argument("--start-maximized")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=opts)
    print("✅ تم إعداد المتصفح\n")
    return driver

# ============================================================================
# الدوال المساعدة
# ============================================================================

def click_element(driver, xpath):
    """انقر على عنصر"""
    try:
        element = WebDriverWait(driver, WAIT_TIME).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
        time.sleep(0.2)
        element.click()
        return True
    except:
        return False

def fill_input(driver, xpath, text):
    """ملء حقل نصي"""
    try:
        element = WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
        element.click()
        time.sleep(0.1)
        element.clear()
        time.sleep(0.1)
        element.send_keys(text)
        driver.execute_script(
            "arguments[0].dispatchEvent(new Event('input',{bubbles:true}));"
            "arguments[0].dispatchEvent(new Event('change',{bubbles:true}));",
            element
        )
        time.sleep(0.2)
        return True
    except:
        return False

def send_telegram(message, wallet_number="", status="success"):
    """إرسال رسالة للتليجرام"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        status_emoji = "✅" if status == "success" else "❌"
        text = f"{status_emoji} النتيجة:\n━━━━━━━━━━\n📱 الرقم: {wallet_number}\n💬 {message}\n⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        response = requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": text}, timeout=10)
        if response.status_code == 200:
            print("✅ تم إرسال الرسالة للتليجرام\n")
            return True
    except Exception as e:
        print(f"⚠️ خطأ في التليجرام: {e}")
    return False

def read_wallet_numbers(filename="lu.txt"):
    """قراءة أرقام المحافظ من ملف"""
    try:
        if not os.path.exists(filename):
            print(f"❌ الملف {filename} غير موجود")
            return []
        
        with open(filename, 'r', encoding='utf-8') as f:
            numbers = [line.strip() for line in f if line.strip()]
        
        print(f"✅ تم قراءة {len(numbers)} رقم من الملف\n")
        return numbers
    except Exception as e:
        print(f"❌ خطأ في قراءة الملف: {e}")
        return []

def get_success_message(driver):
    """الحصول على رسالة النجاح الخضراء فقط"""
    try:
        print("   🔍 البحث عن رسالة خضراء...")
        
        # البحث عن رسائل خضراء
        message_xpaths = [
            "//div[contains(@class, 'alert') and contains(@class, 'success')]",
            "//div[contains(@class, 'alert-success')]",
            "//span[contains(@class, 'success') and contains(@class, 'green')]"
        ]
        
        for xpath in message_xpaths:
            try:
                elements = driver.find_elements(By.XPATH, xpath)
                for el in elements:
                    try:
                        if el.is_displayed():
                            text = el.text or ""
                            if text.strip() and ('نجح' in text or 'تم' in text or 'success' in text.lower()):
                                print(f"   ✅ وجدت رسالة خضراء: {text[:100]}")
                                return text, True
                    except:
                        pass
            except:
                pass
        
        # محاولة JavaScript للبحث عن اللون الأخضر
        result = driver.execute_script("""
            var allDivs = document.querySelectorAll('div, span, p');
            for (var div of allDivs) {
                if (div.offsetParent !== null) {
                    var text = div.innerText;
                    if (!text) continue;
                    
                    var style = window.getComputedStyle(div);
                    var bgColor = style.backgroundColor;
                    
                    // تحقق من اللون الأخضر
                    if (bgColor && (bgColor.includes('0, 128, 0') || bgColor.includes('rgb(0, 128, 0)') || 
                        bgColor.includes('green') || bgColor.includes('008000'))) {
                        
                        if (text.includes('نجح') || text.includes('تم') || text.includes('إرسال')) {
                            return {
                                text: text,
                                color: bgColor
                            };
                        }
                    }
                }
            }
            return null;
        """)
        
        if result and result['text']:
            print(f"   ✅ وجدت رسالة خضراء (JS): {result['text'][:100]}")
            return result['text'], True
        
        print("   ❌ لم توجد رسالة خضراء")
        return "لم يتم العثور على رسالة خضراء", False
        
    except Exception as e:
        print(f"   ❌ خطأ: {e}")
        return "خطأ", False

# ============================================================================
# الخطوات الأساسية
# ============================================================================

def step1_add_to_cart(driver):
    """الخطوة 1: إضافة للسلة"""
    print("📍 الخطوة 1: إضافة للسلة")
    driver.get(PRODUCT_URL)
    time.sleep(PAGE_LOAD_TIME)
    
    if not fill_input(driver, "//input[@name='qty']", str(QUANTITY)):
        print("❌ فشل إدخال الكمية")
        return False
    
    if not click_element(driver, "//button[@id='product-addtocart-button']"):
        print("❌ فشل الإضافة للسلة")
        return False
    
    time.sleep(2)
    print("✅ تمت الخطوة 1\n")
    return True

def step2_checkout(driver):
    """الخطوة 2: الانتقال للدفع"""
    print("📍 الخطوة 2: الانتقال لصفحة الدفع")
    driver.get(CHECKOUT_URL)
    time.sleep(PAGE_LOAD_TIME)
    print("✅ تمت الخطوة 2\n")
    return True

def step3_fill_info(driver):
    """الخطوة 3: ملء البيانات"""
    print("📍 الخطوة 3: ملء بيانات العميل")
    
    # البريد
    fill_input(driver, "//input[@id='customer-email']", EMAIL)
    time.sleep(0.3)
    
    # رقم الهاتف
    try:
        phone_element = WebDriverWait(driver, 8).until(
            EC.presence_of_element_located((By.ID, "phoneNumber"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", phone_element)
        time.sleep(0.3)
        phone_element.click()
        time.sleep(0.1)
        phone_element.clear()
        time.sleep(0.1)
        phone_element.send_keys(PHONE)
        driver.execute_script("""
            var el = arguments[0];
            el.dispatchEvent(new Event('input', {bubbles: true}));
            el.dispatchEvent(new Event('change', {bubbles: true}));
        """, phone_element)
        time.sleep(0.3)
        print("✅ تم إدخال الهاتف")
    except:
        print("⚠️ خطأ في الهاتف")
    
    time.sleep(0.3)
    
    # الاسم
    try:
        name_element = WebDriverWait(driver, 8).until(
            EC.presence_of_element_located((By.XPATH, "//input[@class='input-text form-input']"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", name_element)
        time.sleep(0.3)
        name_element.click()
        time.sleep(0.1)
        name_element.clear()
        time.sleep(0.1)
        name_element.send_keys(FULL_NAME)
        driver.execute_script("""
            var el = arguments[0];
            el.dispatchEvent(new Event('input', {bubbles: true}));
            el.dispatchEvent(new Event('change', {bubbles: true}));
        """, name_element)
        time.sleep(0.3)
        print("✅ تم إدخال الاسم")
    except:
        print("⚠️ خطأ في الاسم")
    
    print("✅ تمت الخطوة 3\n")
    return True

def step4_payment_method(driver):
    """الخطوة 4: اختيار UWallet"""
    print("📍 الخطوة 4: اختيار طريقة الدفع UWallet")
    
    try:
        time.sleep(0.5)
        driver.execute_script("window.scrollBy(0, 300);")
        time.sleep(0.3)
        
        radios = driver.find_elements(By.XPATH, "//input[@type='radio']")
        
        for i, radio in enumerate(radios):
            try:
                radio_value = radio.get_attribute("value") or ""
                radio_id = radio.get_attribute("id") or ""
                
                label_text = ""
                try:
                    if radio_id:
                        label = driver.find_element(By.XPATH, f"//label[@for='{radio_id}']")
                        label_text = label.text
                except:
                    pass
                
                if 'uwallet' in label_text.lower() or 'uwallet' in radio_value.lower():
                    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", radio)
                    time.sleep(0.2)
                    driver.execute_script("arguments[0].click();", radio)
                    time.sleep(0.5)
                    print("✅ تم اختيار UWallet")
                    return True
            except:
                pass
        
        print("⚠️ لم يتم العثور على UWallet")
        return True
        
    except Exception as e:
        print(f"⚠️ خطأ: {e}")
        return True

def step5_agree_terms(driver):
    """الخطوة 5: الموافقة على الشروط"""
    print("📍 الخطوة 5: الموافقة على الشروط")
    
    try:
        checkbox = WebDriverWait(driver, 8).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='checkbox' and @class='checkbox required-entry']"))
        )
        
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", checkbox)
        time.sleep(0.3)
        
        if not checkbox.is_selected():
            driver.execute_script("arguments[0].click();", checkbox)
            time.sleep(0.3)
        
        print("✅ تم الموافقة على الشروط")
        time.sleep(0.5)
        return True
        
    except Exception as e:
        print(f"⚠️ خطأ: {e}")
        return True

def step6_place_order(driver):
    """الخطوة 6: إجراء الطلب"""
    print("📍 الخطوة 6: إجراء الطلب")
    
    order_xpaths = [
        "//button[contains(@class, 'place-order')]",
        "//button[contains(text(), 'إجراء الطلب')]"
    ]
    
    for xp in order_xpaths:
        if click_element(driver, xp):
            print("✅ تم إجراء الطلب")
            time.sleep(4)
            print("✅ تمت الخطوة 6\n")
            return True
    
    return False

def process_wallet_number(driver, wallet_number):
    """معالجة رقم محفظة واحد"""
    print(f"\n{'='*70}")
    print(f"🔄 معالجة الرقم: {wallet_number}")
    print(f"{'='*70}\n")
    
    try:
        # البحث عن حقل المحفظة
        print("1️⃣ البحث عن حقل رقم المحفظة...")
        wallet_input = WebDriverWait(driver, 8).until(
            EC.visibility_of_element_located((By.ID, "phone_number"))
        )
        
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", wallet_input)
        time.sleep(0.2)
        
        # تنظيف وملء الحقل
        print("2️⃣ إدخال رقم المحفظة...")
        wallet_input.click()
        time.sleep(0.1)
        wallet_input.clear()
        time.sleep(0.1)
        wallet_input.send_keys(wallet_number)
        
        # تفعيل الأحداث
        driver.execute_script("""
            const el = arguments[0];
            el.value = arguments[1];
            el.dispatchEvent(new Event('input', {bubbles: true}));
            el.dispatchEvent(new Event('change', {bubbles: true}));
        """, wallet_input, wallet_number)
        
        time.sleep(0.3)
        
        final_value = wallet_input.get_attribute("value") or ""
        if wallet_number not in final_value:
            print(f"❌ فشل إدخال المحفظة")
            send_telegram("فشل إدخال رقم المحفظة", wallet_number, "error")
            return False
        
        print(f"✅ تم إدخال رقم المحفظة")
        time.sleep(0.3)
        
        # البحث عن زر الإرسال
        print("3️⃣ البحث عن زر الإرسال...")
        
        send_button = None
        send_button_xpaths = [
            "//button[contains(@class, 'btn-primary')]",
            "//button[contains(text(), 'إرسال')]"
        ]
        
        for xpath in send_button_xpaths:
            try:
                buttons = driver.find_elements(By.XPATH, xpath)
                if buttons:
                    send_button = buttons[0]
                    break
            except:
                pass
        
        if send_button is None:
            print("❌ فشل العثور على الزر")
            send_telegram("فشل العثور على زر الإرسال", wallet_number, "error")
            return False
        
        # تفعيل الزر
        print("4️⃣ تفعيل الزر والضغط...")
        driver.execute_script("""
            const btn = arguments[0];
            btn.disabled = false;
            btn.removeAttribute('disabled');
            btn.click();
        """, send_button)
        
        print("✅ تم الضغط على الزر")
        
        # الانتظار 10 ثواني
        print("5️⃣ الانتظار للنتيجة...")
        for i in range(10):
            remaining = 10 - i
            print(f"   ⏳ {remaining}s...", end="\r")
            time.sleep(1)
        
        print("\n6️⃣ التحقق من النتيجة الخضراء...")
        message, is_success = get_success_message(driver)
        
        if is_success:
            print(f"✅ نجاح!")
            send_telegram(message[:200], wallet_number, "success")
            return True
        else:
            print(f"❌ فشل: {message[:100]}")
            send_telegram(f"رسالة: {message[:100]}", wallet_number, "error")
            return False
        
    except TimeoutException:
        print("❌ انتهت مهلة الانتظار")
        send_telegram("انتهت مهلة الانتظار", wallet_number, "error")
        return False
    except Exception as e:
        print(f"❌ خطأ: {e}")
        send_telegram(f"خطأ: {str(e)}", wallet_number, "error")
        return False

# ============================================================================
# البرنامج الرئيسي
# ============================================================================

def main():
    print("=" * 70)
    print("🚀 بدء أتمتة شراء Umniah PUBG مع اختبار الأرقام")
    print("=" * 70)
    print()
    
    driver = None
    
    try:
        driver = setup_driver()
        
        # الخطوات الأساسية
        steps = [
            ("إضافة للسلة", step1_add_to_cart),
            ("الانتقال للدفع", step2_checkout),
            ("ملء البيانات", step3_fill_info),
            ("اختيار الدفع", step4_payment_method),
            ("الموافقة على الشروط", step5_agree_terms),
            ("إجراء الطلب", step6_place_order),
        ]
        
        for step_name, step_func in steps:
            if not step_func(driver):
                print(f"❌ فشلت خطوة: {step_name}")
                send_telegram(f"❌ فشلت خطوة: {step_name}", "", "error")
                return
        
        # قراءة الأرقام من الملف
        wallet_numbers = read_wallet_numbers("lu.txt")
        if not wallet_numbers:
            print("❌ لا توجد أرقام في الملف")
            return
        
        # معالجة كل رقم
        results = []
        for i, wallet_number in enumerate(wallet_numbers, 1):
            print(f"\n📊 معالجة رقم {i} من {len(wallet_numbers)}")
            success = process_wallet_number(driver, wallet_number)
            results.append((wallet_number, success))
            
            # انتظر قليلاً بين الأرقام
            if i < len(wallet_numbers):
                time.sleep(2)
        
        # الملخص
        print("\n" + "=" * 70)
        print("📊 ملخص النتائج:")
        print("=" * 70)
        successful = sum(1 for _, s in results if s)
        print(f"✅ نجح: {successful}/{len(wallet_numbers)}")
        print(f"❌ فشل: {len(wallet_numbers) - successful}/{len(wallet_numbers)}")
        
        for wallet, success in results:
            status = "✅ نجح" if success else "❌ فشل"
            print(f"  {status} - {wallet}")
        
        print("=" * 70)
        
    except Exception as e:
        print(f"❌ خطأ: {e}\n")
        send_telegram(f"❌ خطأ: {str(e)}", "", "error")
    
    finally:
        if driver:
            try:
                driver.quit()
                print("\n🔒 تم إغلاق المتصفح")
            except:
                pass

if __name__ == "__main__":
    main()
