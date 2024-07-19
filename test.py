from selenium import webdriver
from selenium.webdriver.safari.service import Service as SafariService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
import requests
import ssl
import socket
import time
import csv
from datetime import datetime

def check_domain_validity(url):
    start_time = time.time()
    try:
        response = requests.get(url)
        is_valid = response.status_code == 200
    except requests.RequestException:
        is_valid = False
    duration = time.time() - start_time
    return is_valid, duration

def check_https_ssl(url):
    start_time = time.time()
    try:
        hostname = url.split("//")[-1].split("/")[0]
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as secure_sock:
                ssl_version = secure_sock.version()
    except:
        ssl_version = None
    duration = time.time() - start_time
    return ssl_version, duration

def wait_for_element(driver, by, value, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return element
    except TimeoutException:
        print(f"Timeout waiting for element: {value}")
        return None

def test_login(driver, username, password, url):
    start_time = time.time()
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        username_field = wait_for_element(driver, By.NAME, "username")
        if username_field:
            username_field.clear()
            username_field.send_keys(username)
            print("Username entered successfully")
        else:
            print("Username field not found")
            return False, time.time() - start_time

        password_field = wait_for_element(driver, By.NAME, "password")
        if password_field:
            password_field.clear()
            password_field.send_keys(password)
            print("Password entered successfully")
        else:
            print("Password field not found")
            return False, time.time() - start_time

        login_button = wait_for_element(driver, By.ID, "login")
        if login_button:
            print("Login button found, attempting to click")
            try:
                login_button.click()
                print("Login button clicked successfully")
            except Exception as e:
                print(f"Error clicking login button: {str(e)}")
                print("Attempting to use JavaScript to click the button")
                driver.execute_script("arguments[0].click();", login_button)
        else:
            print("Login button not found, trying to submit form")
            password_field.send_keys(Keys.RETURN)

        try:
            WebDriverWait(driver, 10).until(EC.url_changes(url))
            print(f"URL changed after login. New URL: {driver.current_url}")
            return True, time.time() - start_time
        except TimeoutException:
            print("No URL change detected after login attempt")
            error_message = driver.find_elements(By.CLASS_NAME, "alert-danger")
            if error_message:
                print(f"Login failed. Error message: {error_message[0].text}")
            else:
                print("Login failed. No error message found.")
            return False, time.time() - start_time

    except Exception as e:
        print(f"Error during login test: {str(e)}")
        print(f"Current URL: {driver.current_url}")
        print(f"Page source: {driver.page_source[:1000]}")
        return False, time.time() - start_time

def test_payment_generation(driver):
    start_time = time.time()
    try:
        print("Navigating to unpaid bills page...")
        driver.get("https://iglobal.pintro.id/ng_stu_unpaid_new")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        print("Navigated to unpaid bills page")

        print("Looking for billing checkbox...")
        billing_checkbox = wait_for_element(driver, By.CSS_SELECTOR, "input[name='select_row[]'][class*='check_debt check_child_debt']")
        if billing_checkbox:
            driver.execute_script("arguments[0].click();", billing_checkbox)
            print(f"Billing checkbox clicked. Value: {billing_checkbox.get_attribute('value')}")
        else:
            print("Billing checkbox not found")
            return False, time.time() - start_time

        print("Looking for 'Proses Tagihan' button...")
        process_button = wait_for_element(driver, By.ID, "process")
        if process_button:
            driver.execute_script("arguments[0].click();", process_button)
            print("'Proses Tagihan' button clicked")
        else:
            print("'Proses Tagihan' button not found")
            return False, time.time() - start_time

        print("Waiting for redirect to detail transaction page...")
        WebDriverWait(driver, 30).until(EC.url_contains("https://iglobal.pintro.id/ng_stu_unpaid_new/getDetailTransaction"))
        print(f"Redirected to detail transaction page. Current URL: {driver.current_url}")

        print("Looking for 'Pilih Pembayaran' div...")
        payment_channel = wait_for_element(driver, By.CSS_SELECTOR, "div[data-bs-toggle='modal'][data-bs-target='#paymentChannel']")
        if payment_channel:
            driver.execute_script("arguments[0].click();", payment_channel)
            print("'Pilih Pembayaran' clicked")
        else:
            print("'Pilih Pembayaran' div not found")
            return False, time.time() - start_time

        print("Waiting for payment modal to appear...")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "paymentChannel")))
        print("Payment modal appeared")
        
        print("Looking for 'VA Bank Mega Syariah' radio button...")
        bank_option = wait_for_element(driver, By.CSS_SELECTOR, "input[type='radio'][name='channel'][data-text='VA Bank Mega Syariah']")
        if bank_option:
            driver.execute_script("arguments[0].click();", bank_option)
            print("'VA Bank Mega Syariah' selected")
        else:
            print("'VA Bank Mega Syariah' option not found")
            return False, time.time() - start_time

        print("Looking for 'Pilih Pembayaran' button in modal...")
        change_channel_button = wait_for_element(driver, By.CSS_SELECTOR, "button#changeChannel[data-bs-dismiss='modal']")
        if change_channel_button:
            print("'Pilih Pembayaran' button found, waiting for it to be clickable...")
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button#changeChannel[data-bs-dismiss='modal']")))
            driver.execute_script("arguments[0].click();", change_channel_button)
            print("'Pilih Pembayaran' button clicked")
        else:
            print("'Pilih Pembayaran' button not found")
            return False, time.time() - start_time

        print("Looking for 'Bayar Tagihan' button...")
        pay_now_button = wait_for_element(driver, By.ID, "pay_now")
        if pay_now_button:
            print("'Bayar Tagihan' button found, waiting for it to be clickable...")
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "pay_now")))
            driver.execute_script("arguments[0].click();", pay_now_button)
            print("'Bayar Tagihan' button clicked")
        else:
            print("'Bayar Tagihan' button not found")
            return False, time.time() - start_time

        print("Waiting for redirect after clicking 'Bayar Tagihan'...")
        WebDriverWait(driver, 30).until(EC.url_changes(driver.current_url))
        print(f"Redirected to new page. Current URL: {driver.current_url}")

        success = True
        print("Payment generation process completed successfully")
        return success, time.time() - start_time
    except Exception as e:
        print(f"Error during payment generation test: {str(e)}")
        print(f"Current URL: {driver.current_url}")
        print(f"Page source: {driver.page_source[:1000]}")
        return False, time.time() - start_time

def run_tests(url, username, password):
    print(f"Testing URL: {url}")
    results = []
    
    is_valid, domain_duration = check_domain_validity(url)
    print(f"Domain is valid: {is_valid}")
    results.append(("Domain Validity", is_valid, domain_duration))
    
    ssl_version, ssl_duration = check_https_ssl(url)
    if ssl_version:
        print(f"HTTPS/SSL is ready. SSL version: {ssl_version}")
    else:
        print("HTTPS/SSL is not ready or encountered an error")
    results.append(("HTTPS/SSL Check", ssl_version is not None, ssl_duration))
    
    safari_service = SafariService()
    driver = webdriver.Safari(service=safari_service)
    
    try:
        start_time = time.time()
        driver.get(url)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        page_load_duration = time.time() - start_time
        results.append(("Page Load", True, page_load_duration))
        
        login_success, login_duration = test_login(driver, username, password, url)
        results.append(("Login Test", login_success, login_duration))
        
        if login_success:
            payment_success, payment_duration = test_payment_generation(driver)
            results.append(("Payment Generation Test", payment_success, payment_duration))
        
    except Exception as e:
        print(f"Error during test: {str(e)}")
        print(f"Exception type: {type(e).__name__}")
        print(f"Exception details: {e.args}")
        results.append(("Test Error", False, 0))
    finally:
        driver.quit()
    
    return results

def write_to_csv(url, results):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"test_results_{timestamp}.csv"
    
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["URL", "Test", "Result", "Duration (seconds)"])
        for test, result, duration in results:
            writer.writerow([url, test, result, f"{duration:.4f}"])
    
    print(f"Results written to {filename}")

if __name__ == "__main__":
    url = "https://iglobal.pintro.id/login"
    username = "SD12204014"  # Replace with actual test username
    password = "01012017"  # Replace with actual test password
    results = run_tests(url, username, password)
    write_to_csv(url, results)