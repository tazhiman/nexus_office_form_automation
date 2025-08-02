#!/usr/bin/env python3
"""
Nexus (North Tower) Visitor Registration Form Automation - Lightweight Version

Containerized version for daily automated execution without debug features.
Optimized for headless operation and minimal resource usage.
"""

import os
import time
import logging
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class VisitorRegistrationBot:
    def __init__(self, wait_time=15):
        """
        Initialize the lightweight bot for containerized operation
        
        Args:
            wait_time (int): Maximum wait time for elements
        """
        self.wait_time = wait_time
        self.driver = None
        self.wait = None
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.execution_log = {
            'timestamp': self.timestamp,
            'start_time': datetime.now().isoformat(),
            'steps': [],
            'success': False,
            'error': None
        }
        
        # Create logs directory
        os.makedirs("/app/logs", exist_ok=True)
        
        # Setup logging for container environment
        log_filename = f"/app/logs/form_automation_{self.timestamp}.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_filename, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Chrome options optimized for containers
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-images")
        chrome_options.add_argument("--disable-javascript")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--remote-debugging-port=9222")
        
        try:
            # Use system ChromeDriver in container
            service = Service('/usr/bin/chromedriver')
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.wait = WebDriverWait(self.driver, self.wait_time)
            self.logger.info("✅ Browser initialized successfully")
            self.log_step("browser_init", "success", "Browser initialized")
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize browser: {e}")
            self.log_step("browser_init", "error", str(e))
            raise

    def log_step(self, step_name, status, message):
        """Log execution steps for monitoring"""
        self.execution_log['steps'].append({
            'step': step_name,
            'status': status,
            'message': message,
            'timestamp': datetime.now().isoformat()
        })

    def wait_for_page_load(self):
        """Wait for page to fully load"""
        try:
            self.wait.until(EC.presence_of_element_located((By.ID, "form-main-content1")))
            time.sleep(2)
            self.logger.info("✅ Page loaded successfully")
            self.log_step("page_load", "success", "Page loaded")
            return True
        except TimeoutException:
            self.logger.warning("⚠️ Page load timeout")
            self.log_step("page_load", "error", "Page load timeout")
            return False

    def fill_text_input(self, xpath, value, description):
        """Fill a text input field"""
        try:
            self.logger.info(f"📝 Filling {description}: {value}")
            
            element = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.5)
            
            element.clear()
            element.send_keys(value)
            
            self.logger.info(f"✅ Successfully filled {description}")
            self.log_step(f"fill_{description.lower().replace(' ', '_')}", "success", f"Filled {description}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to fill {description}: {e}")
            self.log_step(f"fill_{description.lower().replace(' ', '_')}", "error", str(e))
            return False

    def handle_microsoft_dropdown(self, xpath, option_text, description):
        """Handle Microsoft Forms custom dropdown"""
        try:
            self.logger.info(f"🔽 Handling dropdown {description}: {option_text}")
            
            dropdown = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", dropdown)
            time.sleep(0.5)
            
            dropdown.click()
            self.logger.info(f"🔽 Clicked dropdown {description}")
            time.sleep(1)
            
            option_found = False
            
            # Strategy 1: Look for exact text match
            try:
                option_elements = self.driver.find_elements(By.XPATH, f"//*[contains(text(), '{option_text}')]")
                for option in option_elements:
                    if option.is_displayed() and option.text.strip() == option_text:
                        option.click()
                        option_found = True
                        self.logger.info(f"✅ Selected option: {option_text}")
                        break
            except:
                pass
            
            # Strategy 2: Look for options in dropdown menu
            if not option_found:
                try:
                    option_selectors = [
                        f"//div[@role='option' and contains(text(), '{option_text}')]",
                        f"//li[contains(text(), '{option_text}')]",
                        f"//*[@data-automation-id='choice' and contains(text(), '{option_text}')]"
                    ]
                    
                    for selector in option_selectors:
                        try:
                            option = self.driver.find_element(By.XPATH, selector)
                            if option.is_displayed():
                                option.click()
                                option_found = True
                                self.logger.info(f"✅ Selected option with selector: {option_text}")
                                break
                        except:
                            continue
                except:
                    pass
            
            # Strategy 3: Use keyboard input
            if not option_found:
                try:
                    actions = ActionChains(self.driver)
                    actions.send_keys(option_text).perform()
                    time.sleep(0.5)
                    actions.send_keys(Keys.ENTER).perform()
                    option_found = True
                    self.logger.info(f"✅ Selected option using keyboard: {option_text}")
                except:
                    pass
            
            if not option_found:
                self.logger.warning(f"⚠️ Could not find option '{option_text}' in dropdown {description}")
                self.log_step(f"dropdown_{description.lower().replace(' ', '_')}", "error", f"Option {option_text} not found")
                return False
            
            time.sleep(0.5)
            self.log_step(f"dropdown_{description.lower().replace(' ', '_')}", "success", f"Selected {option_text}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to handle dropdown {description}: {e}")
            self.log_step(f"dropdown_{description.lower().replace(' ', '_')}", "error", str(e))
            return False

    def click_next_button(self):
        """Click the Next button to proceed"""
        try:
            self.logger.info("➡️ Clicking Next button")
            
            next_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[@data-automation-id='nextButton']"))
            )
            
            self.driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
            time.sleep(0.5)
            
            next_button.click()
            self.logger.info("✅ Next button clicked successfully")
            
            time.sleep(2)
            self.log_step("click_next", "success", "Next button clicked")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to click Next button: {e}")
            self.log_step("click_next", "error", str(e))
            return False

    def handle_radio_button(self, value_text, description):
        """Handle radio button selection"""
        try:
            self.logger.info(f"🔘 Selecting radio button {description}: {value_text}")
            
            radio_selectors = [
                f"//input[@type='radio' and contains(@value, '{value_text}')]",
                f"//label[contains(text(), '{value_text}')]",
                f"//*[contains(text(), '{value_text}')]/preceding-sibling::input[@type='radio']",
                f"//*[contains(text(), '{value_text}')]/following-sibling::input[@type='radio']",
                f"//*[contains(text(), '{value_text}')]/../input[@type='radio']"
            ]
            
            radio_found = False
            for selector in radio_selectors:
                try:
                    radio_element = self.driver.find_element(By.XPATH, selector)
                    if radio_element.is_displayed():
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", radio_element)
                        time.sleep(0.5)
                        
                        radio_element.click()
                        radio_found = True
                        self.logger.info(f"✅ Selected radio button: {value_text}")
                        break
                except:
                    continue
            
            # Alternative approach
            if not radio_found:
                try:
                    label_element = self.driver.find_element(By.XPATH, f"//*[contains(text(), '{value_text}')]")
                    if label_element.is_displayed():
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", label_element)
                        time.sleep(0.5)
                        label_element.click()
                        radio_found = True
                        self.logger.info(f"✅ Selected radio button via label: {value_text}")
                except:
                    pass
            
            if not radio_found:
                self.logger.warning(f"⚠️ Could not find radio button for: {value_text}")
                self.log_step("radio_button", "error", f"Radio button {value_text} not found")
                return False
            
            time.sleep(0.5)
            self.log_step("radio_button", "success", f"Selected {value_text}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to handle radio button {description}: {e}")
            self.log_step("radio_button", "error", str(e))
            return False

    def handle_mobile_number_page(self, form_data):
        """Handle the mobile number page"""
        try:
            self.logger.info("📱 Handling mobile number page")
            
            time.sleep(1)
            mobile_field_found = False
            mobile_number = form_data.get('mobile', '87686853')
            
            strategies = [
                {
                    'name': 'mobile_context_search',
                    'selector': "//input[@type='text' or @data-automation-id='textInput']",
                    'validate': lambda: 'mobile' in self.driver.page_source.lower()
                },
                {
                    'name': 'empty_field_search',
                    'selector': "//input[@type='text' or @data-automation-id='textInput']",
                    'validate': lambda: True
                },
                {
                    'name': 'tel_input_search', 
                    'selector': "//input[@type='tel']",
                    'validate': lambda: True
                }
            ]
            
            for strategy in strategies:
                if mobile_field_found:
                    break
                    
                try:
                    if not strategy['validate']():
                        continue
                        
                    self.logger.info(f"🔍 Trying strategy: {strategy['name']}")
                    
                    elements = self.driver.find_elements(By.XPATH, strategy['selector'])
                    
                    for i, element in enumerate(elements):
                        try:
                            if element.is_displayed() and element.is_enabled():
                                if strategy['name'] == 'empty_field_search':
                                    current_value = element.get_attribute('value') or ''
                                    if current_value.strip():
                                        continue
                                
                                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                                time.sleep(0.5)
                                
                                element.clear()
                                element.send_keys(mobile_number)
                                
                                filled_value = element.get_attribute('value')
                                if mobile_number in filled_value:
                                    mobile_field_found = True
                                    self.logger.info(f"✅ Successfully filled mobile number: {mobile_number}")
                                    self.log_step("mobile_number", "success", f"Filled mobile: {mobile_number}")
                                    break
                                     
                        except Exception as e:
                            continue
                            
                except Exception as e:
                    continue
            
            if not mobile_field_found:
                self.logger.warning("⚠️ Could not find mobile number field")
                self.log_step("mobile_number", "error", "Mobile field not found")
            
            # Submit form
            time.sleep(1)
            submit_success = self.click_submit_button()
            
            if submit_success:
                self.logger.info("✅ Form submitted successfully!")
                self.log_step("form_submit", "success", "Form submitted")
            
        except Exception as e:
            self.logger.error(f"❌ Error handling mobile number page: {e}")
            self.log_step("mobile_number", "error", str(e))

    def click_submit_button(self):
        """Click the Submit button"""
        try:
            self.logger.info("📤 Looking for Submit button")
            
            submit_selectors = [
                "//button[contains(text(), 'Submit')]",
                "//button[@type='submit' and contains(text(), 'Submit')]",
                "//input[@type='submit']",
                "//button[@data-automation-id='submitButton']"
            ]
            
            for selector in submit_selectors:
                try:
                    submit_button = self.driver.find_element(By.XPATH, selector)
                    if submit_button.is_displayed() and submit_button.is_enabled():
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
                        time.sleep(0.5)
                        
                        submit_button.click()
                        self.logger.info("✅ Submit button clicked successfully")
                        time.sleep(2)
                        return True
                except:
                    continue
            
            self.logger.warning("⚠️ Could not find Submit button")
            return False
                 
        except Exception as e:
            self.logger.error(f"❌ Failed to click Submit button: {e}")
            return False

    def automate_form(self, form_data):
        """Main automation method"""
        try:
            self.logger.info("🚀 Starting form automation")
            self.logger.info(f"📋 Target URL: {form_data['url']}")
            
            # Open the form
            self.driver.get(form_data['url'])
            
            # Wait for page to load
            if not self.wait_for_page_load():
                raise Exception("Page failed to load")
            
            # Fill form fields
            success = self.fill_text_input(
                "//*[@id='question-list']/div[2]/div[2]/div[1]/span[1]/input[1]",
                form_data['name'],
                "Visitor Name"
            )
            
            success = self.handle_microsoft_dropdown(
                "//*[@id='question-list']/div[3]/div[2]/div[1]/div[1]/div[1]",
                form_data['access_level'],
                "Access Level"
            )
            
            success = self.handle_microsoft_dropdown(
                "//*[@id='question-list']/div[4]/div[2]/div[1]/div[1]/div[1]",
                form_data['purpose'],
                "Purpose"
            )
            
            success = self.fill_text_input(
                "//*[@id='question-list']/div[5]/div[2]/div[1]/span[1]/textarea[1]",
                form_data['additional_info'],
                "Additional Information"
            )
            
            # Handle radio buttons and subsequent pages
            radio_buttons = self.driver.find_elements(By.XPATH, "//input[@type='radio']")
            if radio_buttons:
                self.logger.info("🔘 Found radio buttons")
                
                success = self.handle_radio_button("Yes", "Locally Registered Number")
                if not success:
                    success = self.handle_radio_button("是", "Locally Registered Number (Chinese)")
                
                if success:
                    if self.click_next_button():
                        time.sleep(1)
                        self.handle_mobile_number_page(form_data)
            
            self.execution_log['success'] = True
            self.logger.info("✅ Form automation completed successfully!")
            
        except Exception as e:
            self.execution_log['error'] = str(e)
            self.logger.error(f"❌ Form automation failed: {e}")
            raise

    def save_execution_log(self):
        """Save execution log as JSON"""
        try:
            self.execution_log['end_time'] = datetime.now().isoformat()
            log_file = f"/app/logs/execution_log_{self.timestamp}.json"
            with open(log_file, 'w') as f:
                json.dump(self.execution_log, f, indent=2)
            self.logger.info(f"📄 Execution log saved: {log_file}")
        except Exception as e:
            self.logger.error(f"❌ Failed to save execution log: {e}")

    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            self.logger.info("🔒 Browser closed")

def get_form_data():
    """Get form data from environment variables"""
    return {
        'url': os.getenv('FORM_URL', 'https://forms.office.com/Pages/ResponsePage.aspx?id=WGeXB8aT70uz3FOGA9yRbsbr_tTOC29AvupnhyEvx8FUNlFMQlVGMFNQUjJNUFZOTUJTMlk0SElTWSQlQCN0PWcu&origin=QRCode'),
        'name': os.getenv('VISITOR_NAME', 'Rizwan Ahamed'),
        'access_level': os.getenv('ACCESS_LEVEL', '5'),
        'purpose': os.getenv('PURPOSE', 'Meeting'),
        'company': os.getenv('COMPANY', 'Cognizant'),
        'mobile': os.getenv('MOBILE', '87686853'),
        'additional_info': os.getenv('ADDITIONAL_INFO', 'Daily automated visitor registration')
    }

def main():
    """Main function for containerized execution"""
    bot = None
    try:
        print("🚀 Starting Automated Nexus Visitor Registration")
        print(f"⏰ Execution time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Get configuration from environment
        form_data = get_form_data()
        
        print(f"👤 Visitor: {form_data['name']}")
        print(f"🏢 Company: {form_data['company']}")
        print(f"🎯 Purpose: {form_data['purpose']}")
        print(f"📱 Mobile: {form_data['mobile']}")
        print("=" * 60)
        
        # Initialize lightweight bot
        bot = VisitorRegistrationBot(wait_time=15)
        
        # Run automation
        bot.automate_form(form_data)
        
        # Save execution log
        bot.save_execution_log()
        
        print("=" * 60)
        print("✅ Automation completed successfully!")
        print("📄 Check /app/logs/ for detailed logs")
        
        return 0  # Success exit code
        
    except Exception as e:
        print(f"❌ Automation failed: {e}")
        if bot:
            bot.execution_log['error'] = str(e)
            bot.save_execution_log()
        return 1  # Error exit code
    finally:
        if bot:
            bot.close()

if __name__ == "__main__":
    exit(main())