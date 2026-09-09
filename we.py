#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
أتمتة شراء بطاقات Umniah PUBG - نسخة مصححة v3
Umniah PUBG Card Purchase Automation - Fixed Version v3
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

# البيانات
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

def fill_input_advanced(driver, xpath, text, field_name=""):
    """ملء حقل نصي مع محاولات متعددة"""
    try:
        element = WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
        time.sleep(0.5)
        
        # محاولة النقر وتفريغ الحقل
        try:
            element.click()
            time.sleep(0.3)
            element.clear()
        except:
            pass
        
        # المحاولة الأولى: send_keys
        element.send_keys(text)
        time.sleep(0.3)
        
        # تفعيل الأحداث JavaScript
        driver.execute_script("""
            var el = arguments[0];
            el.dispatchEvent(new Event('input', {bubbles: true}));
            el.dispatchEvent(new Event('change', {bubbles: true}));
            el.dispatchEvent(new Event('blur', {bubbles: true}));
        """, element)
        
        time.sleep(0.5)
        
        # تحقق من القيمة
        current_value = element.get_attribute("value") or ""
        if current_value == text:
            print(f"✅ تم إدخال {field_name}: {text}")
            return True
        
        # المحاولة الثانية: JavaScript مباشر
        element.clear()
        driver.execute_script("""
            var input = arguments[0];
            var value = arguments[1];
            
            input.value = value;
            input.textContent = value;
            
            var inputEvent = new Event('input', { bubbles: true });
            var changeEvent = new Event('change', { bubbles: true });
            var blurEvent = new Event('blur', { bubbles: true });
            
            input.dispatchEvent(inputEvent);
            input.dispatchEvent(changeEvent);
            input.dispatchEvent(blurEvent);
            
            if (input.parentElement) {
                input.parentElement.dispatchEvent(new Event('change', {bubbles: true}));
            }
        """, element, text)
        
        time.sleep(0.5)
        
        # التحقق النهائي
        final_value = element.get_attribute("value") or ""
        if final_value == text:
            print(f"✅ تم إدخال {field_name}: {text}")
            return True
        
        print(f"⚠️ قد يكون هناك مشكلة في إدخال {field_name}")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في {field_name}: {e}")
        return False

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
# الخطوات المحسنة
# ============================================================================

def step1_add_to_cart(driver):
    """الخطوة 1: إضافة للسلة"""
    print("📍 الخطوة 1: إضافة للسلة")
    driver.get(PRODUCT_URL)
    time.sleep(PAGE_LOAD_TIME)
    
    if not fill_input_advanced(driver, "//input[@name='qty']", str(QUANTITY), "الكمية"):
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
    """الخطوة 3: ملء البيانات"""
    print("📍 الخطوة 3: ملء بيانات العميل")
    
    # البريد
    fill_input_advanced(driver, "//input[@id='customer-email']", EMAIL, "البريد الإلكتروني")
    time.sleep(0.7)
    
    # الاسم الكامل
    firstname_xpaths = [
        "//input[@name='firstname']",
        "//input[contains(@name, 'firstname')]",
        "//input[contains(@id, 'firstname')]",
    ]
    
    for xpath in firstname_xpaths:
        try:
            if driver.find_elements(By.XPATH, xpath):
                fill_input_advanced(driver, xpath, FULL_NAME, "الاسم الكامل")
                break
        except:
            pass
    
    time.sleep(0.7)
    
    # رقم الهاتف - البحث الدقيق
    phone_xpaths = [
        "//input[contains(@class, 'inputPhoneNumber')]",
        "//input[@id='telephone']",
        "//input[@name='telephone']",
        "//input[@placeholder='رقم الهاتف']",
        "//input[@type='tel']",
        "//input[contains(@class, 'phone')]"
    ]
    
    phone_found = False
    for xpath in phone_xpaths:
        try:
            elements = driver.find_elements(By.XPATH, xpath)
            if elements:
                element = elements[0]
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
                time.sleep(0.5)
                
                element.click()
                time.sleep(0.3)
                element.clear()
                time.sleep(0.3)
                
                element.send_keys(PHONE)
                time.sleep(0.4)
                
                driver.execute_script("""
                    var el = arguments[0];
                    el.value = arguments[1];
                    el.dispatchEvent(new Event('input', {bubbles: true}));
                    el.dispatchEvent(new Event('change', {bubbles: true}));
                    el.dispatchEvent(new Event('blur', {bubbles: true}));
                """, element, PHONE)
                
                time.sleep(0.5)
                
                current_value = element.get_attribute("value") or ""
                if current_value == PHONE:
                    print(f"✅ تم إدخال رقم الهاتف: {PHONE}")
                    phone_found = True
                    break
        except:
            pass
    
    if not phone_found:
        print(f"⚠️ لم يتم إدخال رقم الهاتف بنجاح")
    
    print("✅ تمت الخطوة 3\n")
    return True

def step4_payment_method(driver):
    """الخطوة 4: اختيار طريقة الدفع UWallet - محسنة جداً"""
    print("📍 الخطوة 4: اختيار طريقة الدفع UWallet")
    
    try:
        time.sleep(1)
        driver.execute_script("window.scrollBy(0, 300);")
        time.sleep(0.5)
        
        # 🔴 جلب جميع radio buttons
        print("🔍 البحث عن جميع خيارات الدفع...")
        radios = driver.find_elements(By.XPATH, "//input[@type='radio']")
        print(f"📊 تم العثور على {len(radios)} خيار دفع\n")
        
        uwallet_index = -1
        
        for i, radio in enumerate(radios):
            try:
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", radio)
                time.sleep(0.3)
                
                # احصل على معلومات الـ radio
                radio_id = radio.get_attribute("id") or ""
                radio_value = radio.get_attribute("value") or ""
                radio_name = radio.get_attribute("name") or ""
                
                # ابحث عن النص المرتبط
                label_text = ""
                try:
                    if radio_id:
                        label = driver.find_element(By.XPATH, f"//label[@for='{radio_id}']")
                        label_text = label.text
                except:
                    pass
                
                if not label_text:
                    try:
                        parent = radio.find_element(By.XPATH, "ancestor::div[contains(@class, 'payment')]")
                        label_text = parent.text[:80]
                    except:
                        pass
                
                # اطبع معلومات الخيار
                print(f"   [{i}] Value: '{radio_value}' | ID: '{radio_id}' | Text: '{label_text[:50]}'")
                
                # تحقق إذا كان هذا هو UWallet
                if 'uwallet' in label_text.lower() or 'uwallet' in radio_value.lower():
                    uwallet_index = i
                    print(f"   ✅ وجدت UWallet في الخيار {i}!\n")
                    break
            
            except Exception as e:
                print(f"   ⚠️ خطأ في الخيار {i}: {str(e)[:50]}")
        
        print()
        
        # إذا وجدنا UWallet، اضغط عليه
        if uwallet_index != -1:
            radio_to_click = radios[uwallet_index]
            print(f"🔴 محاولة تحديد خيار UWallet (رقم {uwallet_index})...")
            
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", radio_to_click)
            time.sleep(0.5)
            
            try:
                radio_to_click.click()
                time.sleep(0.5)
            except:
                driver.execute_script("arguments[0].click();", radio_to_click)
                time.sleep(0.5)
            
            # تحقق من التحديد
            if radio_to_click.is_selected():
                print("✅ تم تحديد UWallet بنجاح!\n")
                time.sleep(1)
                print("✅ تمت الخطوة 4\n")
                return True
            else:
                # جرب JavaScript للتحديد
                driver.execute_script("""
                    arguments[0].checked = true;
                    arguments[0].dispatchEvent(new Event('change', {bubbles: true}));
                    arguments[0].dispatchEvent(new Event('click', {bubbles: true}));
                """, radio_to_click)
                time.sleep(0.5)
                
                if radio_to_click.is_selected():
                    print("✅ تم تحديد UWallet بنجاح (via JavaScript)!\n")
                    time.sleep(1)
                    print("✅ تمت الخطوة 4\n")
                    return True
        
        print("⚠️ لم يتم العثور على UWallet")
        print("✅ تمت الخطوة 4\n")
        return True
        
    except Exception as e:
        print(f"⚠️ خطأ عام في اختيار UWallet: {e}")
        print("✅ تمت الخطوة 4\n")
        return True

def step5_agree_terms(driver):
    """الخطوة 5: الموافقة على الشروط"""
    print("📍 الخطوة 5: الموافقة على الشروط والأحكام")
    
    try:
        agreement_xpaths = [
            "//div[contains(@class, 'checkout-agreement')]//input[@type='checkbox']",
            "//input[@name='agreement']",
            "//input[contains(@class, 'agreement')]"
        ]
        
        for xpath in agreement_xpaths:
            try:
                agreement_field = driver.find_element(By.XPATH, xpath)
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", agreement_field)
                time.sleep(0.3)
                
                if not agreement_field.is_selected():
                    agreement_field.click()
                    time.sleep(0.5)
                    
                    if not agreement_field.is_selected():
                        driver.execute_script("""
                            arguments[0].checked = true;
                            arguments[0].dispatchEvent(new Event('change', {bubbles: true}));
                            arguments[0].dispatchEvent(new Event('click', {bubbles: true}));
                        """, agreement_field)
                
                print("✅ تم الموافقة على الشروط")
                time.sleep(1)
                print("✅ تمت الخطوة 5\n")
                return True
            except:
                pass
        
        print("⚠️ لم يتم العثور على حقل الموافقة")
        print("✅ تمت الخطوة 5\n")
        return True
        
    except Exception as e:
        print(f"⚠️ خطأ في الشروط: {e}")
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
