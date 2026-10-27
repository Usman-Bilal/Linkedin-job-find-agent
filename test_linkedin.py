from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import os
from dotenv import load_dotenv

load_dotenv()

email = os.getenv('LINKEDIN_EMAIL', '')
password = os.getenv('LINKEDIN_PASSWORD', '')

print(f"Email: {email[:5]}..." if email else "Email not set")
print(f"Password: {'*' * len(password)}" if password else "Password not set")

options = Options()
# NO headless mode - browser stays visible
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option("excludeSwitches", ["enable-automation"])

driver = webdriver.Chrome(options=options)

try:
    print("Opening LinkedIn login page...")
    driver.get('https://www.linkedin.com/login')
    time.sleep(3)
    
    print("Page title:", driver.title)
    print("Current URL:", driver.current_url)
    
    print("Entering credentials...")
    username_field = driver.find_element(By.ID, 'username')
    password_field = driver.find_element(By.ID, 'password')
    
    username_field.send_keys(email)
    time.sleep(1)
    password_field.send_keys(password)
    time.sleep(1)
    
    print("Clicking submit...")
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    time.sleep(8)
    
    print("After login URL:", driver.current_url)
    
    if 'checkpoint' in driver.current_url:
        print("\n⚠️ SECURITY CHECKPOINT DETECTED")
        print("LinkedIn requires manual verification")
        print("Browser will stay open for 60 seconds - complete verification manually")
        time.sleep(60)
    elif 'feed' in driver.current_url:
        print("\n✓ Login successful!")
        
        print("\nNavigating to jobs...")
        driver.get('https://www.linkedin.com/jobs/search/?keywords=procurement')
        time.sleep(5)
        
        print("Scrolling...")
        for i in range(3):
            driver.execute_script('window.scrollBy(0,800)')
            time.sleep(1)
        
        job_cards = driver.find_elements(By.CSS_SELECTOR, 'div.base-card, li.jobs-search-results__list-item')
        print(f"\nFound {len(job_cards)} job cards")
        
        for i, card in enumerate(job_cards[:5], 1):
            try:
                title = card.find_element(By.CSS_SELECTOR, 'h3, span.sr-only').text
                print(f"{i}. {title}")
            except:
                print(f"{i}. (Could not extract title)")
        
        print("\nBrowser will stay open for 60 seconds...")
        time.sleep(60)
    else:
        print("\n❌ Login may have failed")
        print("Browser will stay open for 60 seconds...")
        time.sleep(60)
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    print("\nBrowser will stay open for 60 seconds...")
    time.sleep(60)
finally:
    driver.quit()
    print("Test complete")
