#!/usr/bin/env python3
"""
Nexus (North Tower) Visitor Registration Form Automation

This script automates the filling and submission of the visitor registration form
based on the analysis results from form_analyzer.py
"""

import os
import time
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager

class VisitorRegistrationBot:
    def __init__(self, headless=False, wait_time=15, debug=True):
        """
        Initialize the bot with Chrome WebDriver
        
        Args:
            headless (bool): Run browser in headless mode
            wait_time (int): Maximum wait time for elements
            debug (bool): Enable debug mode with screenshots
        """
        self.wait_time = wait_time
        self.driver = None
        self.wait = None
        self.debug = debug
        self.step_counter = 0
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Create directories
        if self.debug:
            os.makedirs("debug_screenshots", exist_ok=True)
        os.makedirs("automation_logs", exist_ok=True)
        
        # Setup logging
        log_filename = f"automation_logs/form_automation_{self.timestamp}.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_filename, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Chrome options
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        try:
            # Install and setup ChromeDriver automatically
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.wait = WebDriverWait(self.driver, self.wait_time)
            self.logger.info("✅ Browser initialized successfully")
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize browser: {e}")
            raise
    
    def take_screenshot(self, description):
        """Take a debug screenshot"""
        if self.debug:
            self.step_counter += 1
            filename = f"debug_screenshots/step_{self.step_counter:02d}_{description}_{self.timestamp}.png"
            self.driver.save_screenshot(filename)
            self.logger.info(f"📸 Screenshot saved: {filename}")

    def wait_for_page_load(self):
        """Wait for page to fully load"""
        try:
            # Wait for the main form content to be present
            self.wait.until(EC.presence_of_element_located((By.ID, "form-main-content1")))
            time.sleep(2)  # Additional wait for dynamic content
            self.logger.info("✅ Page loaded successfully")
            return True
        except TimeoutException:
            self.logger.warning("⚠️ Page load timeout")
            return False

    def fill_text_input(self, xpath, value, description):
        """Fill a text input field"""
        try:
            self.logger.info(f"📝 Filling {description}: {value}")
            
            # Wait for element to be present and visible
            element = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            
            # Scroll to element
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(1)
            
            # Clear and fill
            element.clear()
            element.send_keys(value)
            
            self.logger.info(f"✅ Successfully filled {description}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to fill {description}: {e}")
            return False

    def handle_microsoft_dropdown(self, xpath, option_text, description):
        """Handle Microsoft Forms custom dropdown"""
        try:
            self.logger.info(f"🔽 Handling dropdown {description}: {option_text}")
            
            # Find and click the dropdown trigger
            dropdown = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            
            # Scroll to dropdown
            self.driver.execute_script("arguments[0].scrollIntoView(true);", dropdown)
            time.sleep(1)
            
            # Click to open dropdown
            dropdown.click()
            self.logger.info(f"🔽 Clicked dropdown {description}")
            time.sleep(1)  # Wait for dropdown options to appear
            
            # Take screenshot after clicking dropdown
            # self.take_screenshot(f"dropdown_{description.replace(' ', '_')}_opened")
            
            # Try different strategies to find the option
            option_found = False
            
            # Strategy 1: Look for exact text match in visible elements
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
            
            # Strategy 2: Look for options in a dropdown menu container
            if not option_found:
                try:
                    # Look for common dropdown option selectors
                    option_selectors = [
                        f"//div[@role='option' and contains(text(), '{option_text}')]",
                        f"//li[contains(text(), '{option_text}')]",
                        f"//div[contains(@class, 'option') and contains(text(), '{option_text}')]",
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
            
            # Strategy 3: Use ActionChains to send keys
            if not option_found:
                try:
                    actions = ActionChains(self.driver)
                    actions.send_keys(option_text).perform()
                    time.sleep(1)
                    actions.send_keys(Keys.ENTER).perform()
                    option_found = True
                    self.logger.info(f"✅ Selected option using keyboard: {option_text}")
                except:
                    pass
            
            if not option_found:
                self.logger.warning(f"⚠️ Could not find option '{option_text}' in dropdown {description}")
                # Take screenshot for debugging
                # self.take_screenshot(f"dropdown_{description.replace(' ', '_')}_options_not_found")
                return False
            
            time.sleep(1)  # Wait for selection to register
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to handle dropdown {description}: {e}")
            # self.take_screenshot(f"dropdown_{description.replace(' ', '_')}_error")
            return False

    def click_next_button(self):
        """Click the Next button to proceed"""
        try:
            self.logger.info("➡️ Clicking Next button")
            
            # Find the Next button using the data-automation-id
            next_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[@data-automation-id='nextButton']"))
            )
            
            # Scroll to button
            self.driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
            time.sleep(1)
            
            # Click the button
            next_button.click()
            self.logger.info("✅ Next button clicked successfully")
            
            # Wait for page transition
            time.sleep(2)
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to click Next button: {e}")
            return False

    def automate_form(self, form_data):
        """Main automation method"""
        try:
            self.logger.info("🚀 Starting form automation")
            self.logger.info(f"📋 Target URL: {form_data['url']}")
            
            # Open the form
            self.driver.get(form_data['url'])
            # self.take_screenshot("page_loaded")
            
            # Wait for page to load
            if not self.wait_for_page_load():
                raise Exception("Page failed to load")
            
            # self.take_screenshot("form_loaded")
            
            # Page 1: Fill the visible fields based on analysis
            
            # Fill first text input (likely visitor name)
            success = self.fill_text_input(
                "//*[@id='question-list']/div[2]/div[2]/div[1]/span[1]/input[1]",
                form_data['name'],
                "Visitor Name"
            )
            # if success:
                # self.take_screenshot("name_filled")
            
            # Handle first dropdown (likely Access Level)
            success = self.handle_microsoft_dropdown(
                "//*[@id='question-list']/div[3]/div[2]/div[1]/div[1]/div[1]",
                form_data['access_level'],
                "Access Level"
            )
            # if success:
            #     self.take_screenshot("access_level_selected")
            
            # Handle second dropdown (likely Purpose)
            success = self.handle_microsoft_dropdown(
                "//*[@id='question-list']/div[4]/div[2]/div[1]/div[1]/div[1]",
                form_data['purpose'],
                "Purpose"
            )
            # if success:
            #     self.take_screenshot("purpose_selected")
            
            # Fill textarea (likely additional information)
            success = self.fill_text_input(
                "//*[@id='question-list']/div[5]/div[2]/div[1]/span[1]/textarea[1]",
                form_data['additional_info'],
                "Additional Information"
            )
            # if success:
            #     self.take_screenshot("additional_info_filled")
    
                
            # Try to fill any additional fields on subsequent pages
            self.handle_additional_pages(form_data)
            
            self.logger.info("✅ Form automation completed successfully!")
            
        except Exception as e:
            self.logger.error(f"❌ Form automation failed: {e}")
            # self.take_screenshot("automation_error")
            raise

    def handle_radio_button(self, value_text, description):
        """Handle radio button selection"""
        try:
            self.logger.info(f"🔘 Selecting radio button {description}: {value_text}")
            
            # Look for radio buttons with the specified value
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
                        # Scroll to element
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", radio_element)
                        time.sleep(1)
                        
                        # Click the radio button
                        radio_element.click()
                        radio_found = True
                        self.logger.info(f"✅ Selected radio button: {value_text}")
                        break
                except:
                    continue
            
            # Alternative approach: click on the label or parent element
            if not radio_found:
                try:
                    label_element = self.driver.find_element(By.XPATH, f"//*[contains(text(), '{value_text}')]")
                    if label_element.is_displayed():
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", label_element)
                        time.sleep(1)
                        label_element.click()
                        radio_found = True
                        self.logger.info(f"✅ Selected radio button via label: {value_text}")
                except:
                    pass
            
            if not radio_found:
                self.logger.warning(f"⚠️ Could not find radio button for: {value_text}")
                return False
            
            time.sleep(1)
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to handle radio button {description}: {e}")
            return False

    def handle_additional_pages(self, form_data):
        """Handle additional form pages"""
        try:
            self.logger.info("📄 Checking for additional form pages")
            
            # Check if there are more input fields or dropdowns
            time.sleep(1)
            
            # Check for radio buttons (locally registered number question)
            radio_buttons = self.driver.find_elements(By.XPATH, "//input[@type='radio']")
            if radio_buttons:
                self.logger.info("🔘 Found radio buttons, handling locally registered number question")
                
                # Click "Yes" for locally registered number
                success = self.handle_radio_button("Yes", "Locally Registered Number")
                if not success:
                    # Try alternative text
                    success = self.handle_radio_button("是", "Locally Registered Number (Chinese)")
                
                if success:
                    # self.take_screenshot("radio_button_selected")
                    
                    # Click Next to proceed to mobile number page
                    if self.click_next_button():
                        # self.take_screenshot("mobile_number_page_loaded")
                        time.sleep(1)
                        
                        # Handle mobile number field
                        self.handle_mobile_number_page(form_data)
            
            # Look for company name field only if we're not on mobile page
            # Check if we're still on a page that needs company info
            page_text = self.driver.page_source.lower()
            if 'company' in page_text and 'mobile' not in page_text:
                input_fields = self.driver.find_elements(By.CSS_SELECTOR, "input[data-automation-id='textInput']")
                textareas = self.driver.find_elements(By.CSS_SELECTOR, "textarea[data-automation-id='textInput']")
                
                # Fill any additional input fields with appropriate data
                for i, field in enumerate(input_fields):
                    if field.is_displayed():
                        field_name = f"company_field_{i+1}"
                        field_value = form_data.get('company', 'Additional Information')
                        
                        try:
                            field.clear()
                            field.send_keys(field_value)
                            self.logger.info(f"✅ Filled {field_name}: {field_value}")
                            # self.take_screenshot(f"{field_name}_filled")
                        except Exception as e:
                            self.logger.warning(f"⚠️ Could not fill {field_name}: {e}")
                
        except Exception as e:
            self.logger.warning(f"⚠️ Error handling additional pages: {e}")

    def handle_mobile_number_page(self, form_data):
        """Handle the mobile number page"""
        try:
            self.logger.info("📱 Handling mobile number page")
            
            # Take screenshot to see what we're working with
            # self.take_screenshot("mobile_page_analysis")
            
            # Wait a moment for page to fully load
            time.sleep(1)
            
            mobile_field_found = False
            mobile_number = form_data.get('mobile', '87686853')
            
            # Look for mobile number input field with multiple strategies
            strategies = [
                # Strategy 1: Look for text inputs on pages containing "Mobile" or "手机"
                {
                    'name': 'mobile_context_search',
                    'selector': "//input[@type='text' or @data-automation-id='textInput']",
                    'validate': lambda: 'mobile' in self.driver.page_source.lower() or '手机' in self.driver.page_source
                },
                # Strategy 2: Look for empty text inputs (mobile field is usually empty)
                {
                    'name': 'empty_field_search',
                    'selector': "//input[@type='text' or @data-automation-id='textInput']",
                    'validate': lambda: True
                },
                # Strategy 3: Look for tel type inputs
                {
                    'name': 'tel_input_search', 
                    'selector': "//input[@type='tel']",
                    'validate': lambda: True
                },
                # Strategy 4: Look for inputs with mobile-related attributes
                {
                    'name': 'mobile_attribute_search',
                    'selector': "//input[contains(@placeholder, 'Mobile') or contains(@placeholder, 'mobile') or contains(@aria-label, 'Mobile') or contains(@aria-label, 'mobile')]",
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
                    self.logger.info(f"Found {len(elements)} potential fields with {strategy['name']}")
                    
                    for i, element in enumerate(elements):
                        try:
                            if element.is_displayed() and element.is_enabled():
                                # For empty field strategy, only fill if field is actually empty
                                if strategy['name'] == 'empty_field_search':
                                    current_value = element.get_attribute('value') or ''
                                    if current_value.strip():
                                        self.logger.info(f"Skipping field {i+1} - already contains: '{current_value}'")
                                        continue
                                
                                # Scroll to element
                                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                                time.sleep(1)
                                
                                # Clear and fill with mobile number
                                element.clear()
                                time.sleep(0.5)
                                element.send_keys(mobile_number)
                                
                                # Verify the value was set correctly
                                filled_value = element.get_attribute('value')
                                if mobile_number in filled_value:
                                    mobile_field_found = True
                                    self.logger.info(f"✅ Successfully filled mobile number using {strategy['name']}: {mobile_number}")
                                    # self.take_screenshot(f"mobile_filled_{strategy['name']}")
                                    break
                                else:
                                    self.logger.warning(f"⚠️ Field filled but value doesn't match. Expected: {mobile_number}, Got: {filled_value}")
                                    
                        except Exception as e:
                            self.logger.warning(f"⚠️ Error trying element {i+1} with {strategy['name']}: {e}")
                            continue
                            
                except Exception as e:
                    self.logger.warning(f"⚠️ Strategy {strategy['name']} failed: {e}")
                    continue
            
            if not mobile_field_found:
                self.logger.error("❌ Could not find or fill mobile number field with any strategy")
                # self.take_screenshot("mobile_field_not_found_final")
                
                # Last resort: try to find ANY input field and fill it
                try:
                    all_inputs = self.driver.find_elements(By.TAG_NAME, "input")
                    for inp in all_inputs:
                        if inp.is_displayed() and inp.get_attribute('type') in ['text', 'tel', None]:
                            inp.clear()
                            inp.send_keys(mobile_number)
                            self.logger.info(f"✅ Last resort: filled input with mobile number: {mobile_number}")
                            mobile_field_found = True
                            break
                except:
                    pass
            
            # Look for Submit button
            time.sleep(1)
            submit_success = self.click_submit_button()
            
            if submit_success:
                # self.take_screenshot("form_submitted_with_mobile")
                self.logger.info("✅ Form submitted successfully!")
            
        except Exception as e:
            self.logger.error(f"❌ Error handling mobile number page: {e}")
            # self.take_screenshot("mobile_page_error")

    def click_submit_button(self):
        """Click the Submit button"""
        try:
            self.logger.info("📤 Looking for Submit button")
            
            # Look for Submit button
            submit_selectors = [
                "//button[contains(text(), 'Submit')]",
                "//button[@type='submit' and contains(text(), 'Submit')]",
                "//input[@type='submit']",
                "//button[@data-automation-id='submitButton']",
                "//button[contains(@aria-label, 'Submit')]"
            ]
            
            for selector in submit_selectors:
                try:
                    submit_button = self.driver.find_element(By.XPATH, selector)
                    if submit_button.is_displayed() and submit_button.is_enabled():
                        # Scroll to button
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
                        time.sleep(1)
                        
                        # Click Submit
                        submit_button.click()
                        self.logger.info("✅ Submit button clicked successfully")
                        time.sleep(2)  # Wait for submission
                        return True
                except:
                    continue
            
            self.logger.warning("⚠️ Could not find Submit button")
            return False
                
        except Exception as e:
            self.logger.error(f"❌ Failed to click Submit button: {e}")
            return False

    def close(self):
        """Close the browser"""
        if self.driver:
            # Keep browser open for a bit so user can see results
            self.logger.info("⏳ Keeping browser open for 10 seconds for review...")
            time.sleep(5)
            
            self.driver.quit()
            self.logger.info("🔒 Browser closed")

def main():
    """Main function to run the automation"""
    
    # Sample form data - modify as needed
    form_data = {
        'url': 'https://forms.office.com/Pages/ResponsePage.aspx?id=WGeXB8aT70uz3FOGA9yRbsbr_tTOC29AvupnhyEvx8FUNlFMQlVGMFNQUjJNUFZOTUJTMlk0SElTWSQlQCN0PWcu&origin=QRCode',
        'name': 'Rizwan Ahamed',
        'access_level': '5',  # Access level 1-5
        'purpose': 'Meeting',  # Common purposes: Meeting, Delivery, Training, etc.
        'company': 'Cognizant',
        'mobile': '87686853',  # Mobile number for locally registered users
        'additional_info': 'Cognizant'
    }
    
    bot = None
    try:
        print("🚀 Starting Nexus Visitor Registration Automation")
        print(f"📋 Target URL: {form_data['url']}")
        print(f"👤 Visitor: {form_data['name']}")
        print(f"🏢 Company: {form_data['company']}")
        print(f"🎯 Purpose: {form_data['purpose']}")
        print(f"📱 Mobile: {form_data['mobile']}")
        print("=" * 80)
        
        # Initialize bot with visible browser
        bot = VisitorRegistrationBot(headless=False, wait_time=20, debug=True)
        
        # Run automation
        bot.automate_form(form_data)
        
        print("=" * 80)
        print("✅ Automation completed! Check the debug_screenshots/ and automation_logs/ directories.")
        print("🔍 The browser will stay open for 10 seconds so you can see the results.")
        
    except Exception as e:
        print(f"❌ Automation failed: {e}")

    finally:
        if bot:
            bot.close()

if __name__ == "__main__":
    main()