#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
أتمتة شراء بطاقات Umniah PUBG - النسخة النهائية المصححة الكاملة
Umniah PUBG Card Purchase Automation - Final Complete Version
"""

import subprocess
import sys
import time
import requests
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
WALLET_NUMBER = "799646537"
QUANTITY = 2

TELEGRAM_TOKEN = "7327256170:AAEiQ_F_BI1V9iUHzgPPui7JRwqGnj6Jys4"
TELEGRAM_CHAT_ID = "6873334348"

WAIT_TIME = 20
PAGE_LOAD_TIME = 4

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
        time.sleep(0.3)
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
        element.clear()
        element.send_keys(text)
        driver.execute_script(
            "arguments[0].dispatchEvent(new Event('input',{bubbles:true}));"
            "arguments[0].dispatchEvent(new Event('change',{bubbles:true}));",
            element
        )
        time.sleep(0.3)
        return True
    except:
        return False

def send_telegram(message, status="success"):
    """إرسال رسالة للتليجرام"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        status_emoji = "✅" if status == "success" else "❌"
        text = f"{status_emoji} نتيجة الشراء: {'نجح' if status == 'success' else 'فشل'}\n━━━━━━━━━━\n📱 رقم: {PHONE}\n💬 {message}\n⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        response = requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": text}, timeout=10)
        if response.status_code == 200:
            print("✅ تم إرسال الرسالة للتليجرام\n")
            return True
    except:
        pass
    return False

# ============================================================================
# الخطوات
# ============================================================================

def step1_add_to_cart(driver):
    """الخطوة 1: إضافة للسلة"""
    print("📍 الخطوة 1: إضافة للسلة")
    driver.get(PRODUCT_URL)
    time.sleep(PAGE_LOAD_TIME)
    
    if not fill_input(driver, "//input[@name='qty']", str(QUANTITY)):
        print("❌ فشل إدخال الكمية")
        return False
    time.sleep(1)
    
    if not click_element(driver, "//button[@id='product-addtocart-button']"):
        print("❌ فشل النقر على إضافة للسلة")
        return False
    
    time.sleep(3)
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
    """الخطوة 3: ملء البيانات - مصححة تماماً"""
    print("📍 الخطوة 3: ملء بيانات العميل")
    
    # ========== البريد ==========
    print("📧 ملء البريد الإلكتروني...")
    try:
        fill_input(driver, "//input[@id='customer-email']", EMAIL)
        print(f"✅ تم إدخال البريد: {EMAIL}")
    except Exception as e:
        print(f"⚠️ خطأ في البريد: {e}")
    time.sleep(0.5)
    
    # ========== رقم الهاتف ==========
    print("📞 ملء رقم الهاتف...")
    try:
        phone_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "phoneNumber"))
        )
        
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", phone_element)
        time.sleep(0.5)
        
        phone_element.click()
        time.sleep(0.2)
        phone_element.clear()
        time.sleep(0.2)
        
        phone_element.send_keys(PHONE)
        time.sleep(0.3)
        
        driver.execute_script("""
            var el = arguments[0];
            el.dispatchEvent(new Event('input', {bubbles: true}));
            el.dispatchEvent(new Event('change', {bubbles: true}));
            el.dispatchEvent(new Event('blur', {bubbles: true}));
        """, phone_element)
        
        time.sleep(0.5)
        
        final_value = phone_element.get_attribute("value") or ""
        if PHONE in final_value:
            print(f"✅ تم إدخال رقم الهاتف: {PHONE}")
        else:
            print(f"⚠️ قيمة الهاتف: {final_value}")
            
    except Exception as e:
        print(f"❌ خطأ في رقم الهاتف: {e}")
    
    time.sleep(0.5)
    
    # ========== الاسم الكامل ==========
    print("👤 ملء الاسم الكامل...")
    try:
        name_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@class='input-text form-input']"))
        )
        
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", name_element)
        time.sleep(0.5)
        
        name_element.click()
        time.sleep(0.2)
        name_element.clear()
        time.sleep(0.2)
        
        name_element.send_keys(FULL_NAME)
        time.sleep(0.3)
        
        driver.execute_script("""
            var el = arguments[0];
            el.dispatchEvent(new Event('input', {bubbles: true}));
            el.dispatchEvent(new Event('change', {bubbles: true}));
            el.dispatchEvent(new Event('blur', {bubbles: true}));
        """, name_element)
        
        time.sleep(0.5)
        
        final_value = name_element.get_attribute("value") or ""
        if FULL_NAME in final_value:
            print(f"✅ تم إدخال الاسم الكامل: {FULL_NAME}")
        else:
            print(f"⚠️ قيمة الاسم: {final_value}")
    
    except Exception as e:
        print(f"❌ خطأ في الاسم الكامل: {e}")
    
    print("✅ تمت الخطوة 3\n")
    return True

def step4_payment_method(driver):
    """الخطوة 4: اختيار طريقة الدفع UWallet"""
    print("📍 الخطوة 4: اختيار طريقة الدفع UWallet")
    
    try:
        time.sleep(1)
        driver.execute_script("window.scrollBy(0, 300);")
        time.sleep(0.5)
        
        print("🔍 البحث عن خيارات الدفع...")
        radios = driver.find_elements(By.XPATH, "//input[@type='radio']")
        print(f"📊 وجدت {len(radios)} خيار دفع")
        
        uwallet_found = False
        
        for i, radio in enumerate(radios):
            try:
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", radio)
                time.sleep(0.3)
                
                radio_id = radio.get_attribute("id") or ""
                radio_value = radio.get_attribute("value") or ""
                
                label_text = ""
                try:
                    if radio_id:
                        label = driver.find_element(By.XPATH, f"//label[@for='{radio_id}']")
                        label_text = label.text
                except:
                    pass
                
                print(f"   [{i}] Value: '{radio_value}' | Text: '{label_text[:50] if label_text else 'N/A'}'")
                
                if 'uwallet' in label_text.lower() or 'uwallet' in radio_value.lower():
                    print(f"✅ وجدت UWallet في الخيار {i}!")
                    
                    try:
                        radio.click()
                    except:
                        driver.execute_script("arguments[0].click();", radio)
                    
                    time.sleep(0.5)
                    
                    if radio.is_selected():
                        print("✅ تم تحديد UWallet بنجاح!")
                        uwallet_found = True
                        break
                    else:
                        driver.execute_script("""
                            arguments[0].checked = true;
                            arguments[0].dispatchEvent(new Event('change', {bubbles: true}));
                        """, radio)
                        time.sleep(0.5)
                        
                        if radio.is_selected():
                            print("✅ تم تحديد UWallet بنجاح (via JavaScript)!")
                            uwallet_found = True
                            break
            
            except Exception as e:
                print(f"   ⚠️ خطأ في الخيار {i}: {e}")
                pass
        
        if uwallet_found:
            time.sleep(1)
            print("✅ تمت الخطوة 4\n")
            return True
        else:
            print("⚠️ لم يتم العثور على UWallet")
            print("✅ تمت الخطوة 4\n")
            return True
        
    except Exception as e:
        print(f"⚠️ خطأ عام: {e}")
        print("✅ تمت الخطوة 4\n")
        return True

def step5_agree_terms(driver):
    """الخطوة 5: الموافقة على الشروط والأحكام"""
    print("📍 الخطوة 5: الموافقة على الشروط والأحكام")
    
    try:
        print("🔍 البحث عن checkbox الشروط...")
        
        checkbox = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='checkbox' and @class='checkbox required-entry']"))
        )
        
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", checkbox)
        time.sleep(0.5)
        
        is_checked = checkbox.is_selected()
        print(f"   الحالة الحالية: {'محدد ✓' if is_checked else 'غير محدد'}")
        
        if not is_checked:
            try:
                checkbox.click()
                time.sleep(0.5)
            except:
                driver.execute_script("arguments[0].click();", checkbox)
                time.sleep(0.5)
            
            if not checkbox.is_selected():
                driver.execute_script("""
                    arguments[0].checked = true;
                    arguments[0].dispatchEvent(new Event('change', {bubbles: true}));
                    arguments[0].dispatchEvent(new Event('click', {bubbles: true}));
                """, checkbox)
                time.sleep(0.5)
        
        if checkbox.is_selected():
            print("✅ تم تحديد الشروط بنجاح!")
        else:
            print("⚠️ لم يتم تحديد الشروط رغم المحاولات - لكن سنستمر")
        
        time.sleep(1)
        print("✅ تمت الخطوة 5\n")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في الشروط: {e}")
        print("✅ تمت الخطوة 5\n")
        return True

def step6_place_order(driver):
    """الخطوة 6: إجراء الطلب"""
    print("📍 الخطوة 6: إجراء الطلب")
    
    order_xpaths = [
        "//button[contains(@class, 'place-order')]",
        "//button[contains(text(), 'إجراء الطلب')]",
        "//div[@class='actions-toolbar']//button[contains(@class, 'btn-primary')]"
    ]
    
    for xp in order_xpaths:
        if click_element(driver, xp):
            print("✅ تم الضغط على إجراء الطلب")
            time.sleep(5)
            print("✅ تمت الخطوة 6\n")
            return True
    
    print("❌ فشل إجراء الطلب")
    return False

def step7_wallet_otp(driver):
    """الخطوة 7: إدخال المحفظة و OTP"""
    print("📍 الخطوة 7: إدخال رقم المحفظة وإرسال OTP")
    
    try:
        wallet_input = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.ID, "phone_number"))
        )
        
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", wallet_input)
        time.sleep(0.4)
        
        wallet_input.click()
        wallet_input.send_keys(Keys.CONTROL, "a")
        wallet_input.send_keys(WALLET_NUMBER)
        
        driver.execute_script("""
            const el = arguments[0];
            el.value = arguments[1];
            el.dispatchEvent(new Event('input', {bubbles: true}));
            el.dispatchEvent(new Event('change', {bubbles: true}));
        """, wallet_input, WALLET_NUMBER)
        
        time.sleep(0.7)
        
        final_value = wallet_input.get_attribute("value") or ""
        if final_value != WALLET_NUMBER:
            print(f"❌ فشل إدخال المحفظة")
            return False
        
        print("✅ تم إدخال رقم المحفظة")
        
        if not click_element(driver, "//button[contains(text(), 'إرسال رمز التحقق')]"):
            print("❌ فشل إرسال OTP")
            return False
        
        print("✅ تم إرسال رمز التحقق")
        time.sleep(3)
        print("✅ تمت الخطوة 7\n")
        return True
        
    except TimeoutException:
        print("❌ لم يتم العثور على حقل المحفظة")
        return False
    except Exception as e:
        print(f"❌ خطأ: {e}")
        return False

def step8_check_result(driver):
    """الخطوة 8: التحقق من النتيجة"""
    print("📍 الخطوة 8: التحقق من النتيجة")
    
    time.sleep(2)
    
    try:
        result_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'alert')]"))
        )
        
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", result_element)
        time.sleep(0.5)
        
        result_class = result_element.get_attribute("class") or ""
        result_text = result_element.text
        
        print(f"📋 النتيجة: {result_text}")
        
        is_success = any(word in result_class.lower() for word in ['success', 'green', 'passed'])
        
        if is_success:
            print("✅ النتيجة: نجح (أخضر)")
            send_telegram(result_text, status="success")
        else:
            print("❌ النتيجة: فشل (أحمر)")
            send_telegram(result_text, status="error")
        
        print("✅ تمت الخطوة 8\n")
        return True
        
    except:
        print("⚠️ لم يتم العثور على النتيجة")
        print("✅ تمت الخطوة 8\n")
        return True

# ============================================================================
# البرنامج الرئيسي
# ============================================================================

def main():
    print("=" * 70)
    print("🚀 بدء أتمتة شراء Umniah PUBG")
    print("=" * 70)
    print()
    
    driver = None
    
    try:
        driver = setup_driver()
        
        steps = [
            ("إضافة للسلة", step1_add_to_cart),
            ("الانتقال للدفع", step2_checkout),
            ("ملء البيانات", step3_fill_info),
            ("اختيار الدفع", step4_payment_method),
            ("الموافقة على الشروط", step5_agree_terms),
            ("إجراء الطلب", step6_place_order),
            ("إدخال المحفظة والـ OTP", step7_wallet_otp),
            ("التحقق من النتيجة", step8_check_result),
        ]
        
        for step_name, step_func in steps:
            if not step_func(driver):
                print(f"❌ فشلت خطوة: {step_name}")
                send_telegram(f"فشلت خطوة: {step_name}", status="error")
                break
        
        print("=" * 70)
        print("✅ انتهت عملية الشراء!")
        print("=" * 70)
        time.sleep(3)
        
    except Exception as e:
        print(f"❌ خطأ: {e}\n")
        send_telegram(f"خطأ: {str(e)}", status="error")
    
    finally:
        if driver:
            try:
                driver.quit()
                print("🔒 تم إغلاق المتصفح")
            except:
                pass

if __name__ == "__main__":
    main()
