#!/usr/bin/env python3
"""
Microsoft Forms Comprehensive Analyzer

This script analyzes a Microsoft Forms page and logs detailed information
about all form elements to help develop automation scripts.
"""

import os
import time
import json
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

class FormAnalyzer:
    def __init__(self, headless=False):
        """Initialize the form analyzer"""
        self.driver = None
        self.wait = None
        self.analysis_results = {
            'timestamp': datetime.now().strftime('%Y%m%d_%H%M%S'),
            'url': '',
            'page_title': '',
            'form_elements': [],
            'interactive_elements': [],
            'all_elements_summary': {},
            'recommendations': []
        }
        
        # Create output directory
        os.makedirs("analysis_results", exist_ok=True)
        
        # Setup logging
        log_filename = f"analysis_results/form_analysis_{self.analysis_results['timestamp']}.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_filename),
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
            self.wait = WebDriverWait(self.driver, 20)
            self.logger.info("✅ Form analyzer initialized successfully")
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize browser: {e}")
            raise

    def analyze_form(self, url):
        """Analyze the Microsoft Forms page"""
        try:
            self.logger.info(f"🌐 Opening form URL: {url}")
            self.analysis_results['url'] = url
            
            # Load the page
            self.driver.get(url)
            time.sleep(5)  # Wait for page to fully load
            
            # Get page title
            self.analysis_results['page_title'] = self.driver.title
            self.logger.info(f"📄 Page title: {self.driver.title}")
            
            # Take initial screenshot
            screenshot_path = f"analysis_results/initial_page_{self.analysis_results['timestamp']}.png"
            self.driver.save_screenshot(screenshot_path)
            self.logger.info(f"📸 Initial screenshot saved: {screenshot_path}")
            
            # Wait for form to load
            self.logger.info("⏳ Waiting for form elements to load...")
            time.sleep(3)
            
            # Analyze different types of elements
            self._analyze_input_fields()
            self._analyze_buttons()
            self._analyze_dropdowns()
            self._analyze_radio_buttons()
            self._analyze_checkboxes()
            self._analyze_interactive_elements()
            self._analyze_custom_microsoft_elements()
            
            # Generate summary and recommendations
            self._generate_summary()
            self._generate_recommendations()
            
            # Save detailed results
            self._save_results()
            
            self.logger.info("✅ Form analysis completed successfully!")
            
        except Exception as e:
            self.logger.error(f"❌ Error analyzing form: {e}")
            raise

    def _analyze_input_fields(self):
        """Analyze all input fields"""
        self.logger.info("🔍 Analyzing input fields...")
        
        input_selectors = [
            "input",
            "input[type='text']",
            "input[type='email']",
            "input[type='number']",
            "input[type='tel']",
            "textarea",
            "[role='textbox']"
        ]
        
        inputs_found = []
        for selector in input_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if element.is_displayed():
                        input_info = self._extract_element_info(element, "INPUT")
                        inputs_found.append(input_info)
                        self.logger.info(f"  📝 Input found: {input_info['attributes'].get('placeholder', 'No placeholder')} | Type: {input_info['attributes'].get('type', 'text')}")
            except Exception as e:
                self.logger.warning(f"⚠️ Error finding inputs with selector {selector}: {e}")
        
        self.analysis_results['form_elements'].extend(inputs_found)
        self.analysis_results['all_elements_summary']['input_fields'] = len(inputs_found)

    def _analyze_buttons(self):
        """Analyze all buttons"""
        self.logger.info("🔍 Analyzing buttons...")
        
        button_selectors = [
            "button",
            "input[type='button']",
            "input[type='submit']",
            "[role='button']",
            ".office-form-button"
        ]
        
        buttons_found = []
        for selector in button_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if element.is_displayed():
                        button_info = self._extract_element_info(element, "BUTTON")
                        buttons_found.append(button_info)
                        self.logger.info(f"  🔘 Button found: '{element.text}' | Type: {button_info['attributes'].get('type', 'N/A')}")
            except Exception as e:
                self.logger.warning(f"⚠️ Error finding buttons with selector {selector}: {e}")
        
        self.analysis_results['form_elements'].extend(buttons_found)
        self.analysis_results['all_elements_summary']['buttons'] = len(buttons_found)

    def _analyze_dropdowns(self):
        """Analyze dropdowns and select elements"""
        self.logger.info("🔍 Analyzing dropdowns...")
        
        dropdown_selectors = [
            "select",
            "[role='combobox']",
            "[role='listbox']",
            ".office-form-dropdown",
            "[data-automation-id*='dropdown']",
            "[aria-expanded]"
        ]
        
        dropdowns_found = []
        for selector in dropdown_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if element.is_displayed():
                        dropdown_info = self._extract_element_info(element, "DROPDOWN")
                        
                        # Try to get dropdown options
                        try:
                            options = element.find_elements(By.TAG_NAME, "option")
                            dropdown_info['options'] = [opt.text for opt in options if opt.text.strip()]
                        except:
                            dropdown_info['options'] = []
                        
                        dropdowns_found.append(dropdown_info)
                        self.logger.info(f"  📋 Dropdown found: {element.tag_name} | Role: {dropdown_info['attributes'].get('role', 'N/A')}")
            except Exception as e:
                self.logger.warning(f"⚠️ Error finding dropdowns with selector {selector}: {e}")
        
        self.analysis_results['form_elements'].extend(dropdowns_found)
        self.analysis_results['all_elements_summary']['dropdowns'] = len(dropdowns_found)

    def _analyze_radio_buttons(self):
        """Analyze radio buttons"""
        self.logger.info("🔍 Analyzing radio buttons...")
        
        radio_selectors = [
            "input[type='radio']",
            "[role='radio']"
        ]
        
        radios_found = []
        for selector in radio_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if element.is_displayed():
                        radio_info = self._extract_element_info(element, "RADIO")
                        radios_found.append(radio_info)
                        self.logger.info(f"  🔘 Radio found: Value='{radio_info['attributes'].get('value', '')}' | Name='{radio_info['attributes'].get('name', '')}'")
            except Exception as e:
                self.logger.warning(f"⚠️ Error finding radio buttons with selector {selector}: {e}")
        
        self.analysis_results['form_elements'].extend(radios_found)
        self.analysis_results['all_elements_summary']['radio_buttons'] = len(radios_found)

    def _analyze_checkboxes(self):
        """Analyze checkboxes"""
        self.logger.info("🔍 Analyzing checkboxes...")
        
        checkbox_selectors = [
            "input[type='checkbox']",
            "[role='checkbox']"
        ]
        
        checkboxes_found = []
        for selector in checkbox_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if element.is_displayed():
                        checkbox_info = self._extract_element_info(element, "CHECKBOX")
                        checkboxes_found.append(checkbox_info)
                        self.logger.info(f"  ☑️ Checkbox found: Value='{checkbox_info['attributes'].get('value', '')}' | Name='{checkbox_info['attributes'].get('name', '')}'")
            except Exception as e:
                self.logger.warning(f"⚠️ Error finding checkboxes with selector {selector}: {e}")
        
        self.analysis_results['form_elements'].extend(checkboxes_found)
        self.analysis_results['all_elements_summary']['checkboxes'] = len(checkboxes_found)

    def _analyze_interactive_elements(self):
        """Find all clickable/interactive elements"""
        self.logger.info("🔍 Analyzing interactive elements...")
        
        interactive_selectors = [
            "[onclick]",
            "[data-automation-id]",
            "[aria-label]",
            ".ms-Button",
            "[tabindex]",
            "[role='option']"
        ]
        
        interactive_found = []
        for selector in interactive_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if element.is_displayed():
                        interactive_info = self._extract_element_info(element, "INTERACTIVE")
                        interactive_found.append(interactive_info)
            except Exception as e:
                self.logger.warning(f"⚠️ Error finding interactive elements with selector {selector}: {e}")
        
        self.analysis_results['interactive_elements'] = interactive_found
        self.logger.info(f"  🎯 Found {len(interactive_found)} interactive elements")

    def _analyze_custom_microsoft_elements(self):
        """Analyze Microsoft Forms specific elements"""
        self.logger.info("🔍 Analyzing Microsoft Forms custom elements...")
        
        ms_selectors = [
            "[class*='office-form']",
            "[class*='ms-']",
            "[data-automation-id*='question']",
            "[data-automation-id*='choice']",
            "#question-list",
            "[role='group']"
        ]
        
        ms_elements = []
        for selector in ms_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if element.is_displayed():
                        ms_info = self._extract_element_info(element, "MS_CUSTOM")
                        ms_elements.append(ms_info)
            except Exception as e:
                self.logger.warning(f"⚠️ Error finding MS elements with selector {selector}: {e}")
        
        self.analysis_results['interactive_elements'].extend(ms_elements)
        self.logger.info(f"  🏢 Found {len(ms_elements)} Microsoft-specific elements")

    def _extract_element_info(self, element, element_type):
        """Extract comprehensive information about an element"""
        try:
            # Get all attributes
            attributes = {}
            for attr in ['id', 'name', 'class', 'type', 'value', 'placeholder', 'aria-label', 
                        'data-automation-id', 'role', 'tabindex', 'onclick', 'aria-expanded']:
                try:
                    attr_value = element.get_attribute(attr)
                    if attr_value:
                        attributes[attr] = attr_value
                except:
                    pass
            
            # Get location and size
            location = element.location
            size = element.size
            
            # Generate selectors
            xpath = self._generate_xpath(element)
            css_selector = self._generate_css_selector(element)
            
            return {
                'element_type': element_type,
                'tag_name': element.tag_name,
                'text': element.text.strip()[:200] if element.text else '',
                'attributes': attributes,
                'location': location,
                'size': size,
                'xpath': xpath,
                'css_selector': css_selector,
                'is_displayed': element.is_displayed(),
                'is_enabled': element.is_enabled()
            }
        except Exception as e:
            self.logger.warning(f"⚠️ Error extracting element info: {e}")
            return {}

    def _generate_xpath(self, element):
        """Generate XPath for element"""
        try:
            return self.driver.execute_script("""
                function getXPath(element) {
                    if (element.id !== '') {
                        return '//*[@id="' + element.id + '"]';
                    }
                    if (element === document.body) {
                        return '/html/body';
                    }
                    var ix = 0;
                    var siblings = element.parentNode.childNodes;
                    for (var i = 0; i < siblings.length; i++) {
                        var sibling = siblings[i];
                        if (sibling === element) {
                            return getXPath(element.parentNode) + '/' + element.tagName.toLowerCase() + '[' + (ix + 1) + ']';
                        }
                        if (sibling.nodeType === 1 && sibling.tagName === element.tagName) {
                            ix++;
                        }
                    }
                }
                return getXPath(arguments[0]);
            """, element)
        except:
            return "Could not generate XPath"

    def _generate_css_selector(self, element):
        """Generate CSS selector for element"""
        try:
            if element.get_attribute('id'):
                return f"#{element.get_attribute('id')}"
            elif element.get_attribute('class'):
                classes = element.get_attribute('class').replace(' ', '.')
                return f"{element.tag_name}.{classes}"
            else:
                return element.tag_name
        except:
            return "Could not generate CSS selector"

    def _generate_summary(self):
        """Generate analysis summary"""
        total_elements = len(self.analysis_results['form_elements'])
        total_interactive = len(self.analysis_results['interactive_elements'])
        
        summary = f"""
============================================================
FORM ANALYSIS SUMMARY
============================================================
URL: {self.analysis_results['url']}
Page Title: {self.analysis_results['page_title']}
Analysis Time: {self.analysis_results['timestamp']}

FORM ELEMENTS FOUND:
- Input Fields: {self.analysis_results['all_elements_summary'].get('input_fields', 0)}
- Buttons: {self.analysis_results['all_elements_summary'].get('buttons', 0)}
- Dropdowns: {self.analysis_results['all_elements_summary'].get('dropdowns', 0)}
- Radio Buttons: {self.analysis_results['all_elements_summary'].get('radio_buttons', 0)}
- Checkboxes: {self.analysis_results['all_elements_summary'].get('checkboxes', 0)}
- Interactive Elements: {total_interactive}
- Total Form Elements: {total_elements}

KEY FINDINGS:
"""
        
        # Add key findings for each element type
        for element in self.analysis_results['form_elements'][:10]:  # First 10 elements
            element_desc = f"- {element['element_type']}: {element.get('text', 'No text')}"
            if element.get('attributes', {}).get('placeholder'):
                element_desc += f" | Placeholder: {element['attributes']['placeholder']}"
            if element.get('attributes', {}).get('type'):
                element_desc += f" | Type: {element['attributes']['type']}"
            summary += element_desc + "\n"
        
        summary += "============================================================\n"
        
        self.logger.info(summary)
        return summary

    def _generate_recommendations(self):
        """Generate automation recommendations"""
        recommendations = []
        
        # Analyze form complexity
        input_count = self.analysis_results['all_elements_summary'].get('input_fields', 0)
        dropdown_count = self.analysis_results['all_elements_summary'].get('dropdowns', 0)
        
        if input_count > 0:
            recommendations.append(f"Found {input_count} input fields - use placeholder or label text for identification")
        
        if dropdown_count > 0:
            recommendations.append(f"Found {dropdown_count} dropdowns - may need custom handling for Microsoft Forms dropdowns")
        
        # Check for Microsoft-specific patterns
        ms_elements = [e for e in self.analysis_results['interactive_elements'] if 'ms-' in str(e.get('attributes', {}).get('class', ''))]
        if ms_elements:
            recommendations.append(f"Detected {len(ms_elements)} Microsoft-specific elements - use data-automation-id attributes")
        
        self.analysis_results['recommendations'] = recommendations
        
        for rec in recommendations:
            self.logger.info(f"💡 Recommendation: {rec}")

    def _save_results(self):
        """Save analysis results to files"""
        timestamp = self.analysis_results['timestamp']
        
        # Save JSON results
        json_file = f"analysis_results/detailed_analysis_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.analysis_results, f, indent=2, ensure_ascii=False)
        
        # Save text summary
        text_file = f"analysis_results/analysis_summary_{timestamp}.txt"
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write(self._generate_summary())
            f.write("\n\nDETAILED ELEMENT INFORMATION:\n")
            f.write("=" * 60 + "\n")
            
            for i, element in enumerate(self.analysis_results['form_elements'], 1):
                f.write(f"\n{i}. {element['element_type']} - {element['tag_name']}\n")
                f.write(f"   Text: {element.get('text', 'No text')}\n")
                f.write(f"   XPath: {element.get('xpath', 'N/A')}\n")
                f.write(f"   CSS Selector: {element.get('css_selector', 'N/A')}\n")
                f.write(f"   Attributes: {element.get('attributes', {})}\n")
                f.write("-" * 40 + "\n")
            
            f.write("\n\nRECOMMENDATIONS:\n")
            f.write("=" * 60 + "\n")
            for rec in self.analysis_results['recommendations']:
                f.write(f"• {rec}\n")
        
        self.logger.info(f"📄 Results saved to: {json_file}")
        self.logger.info(f"📄 Summary saved to: {text_file}")

    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            self.logger.info("🔒 Browser closed")

def main():
    """Main function to run the analysis"""
    # The Microsoft Forms URL to analyze
    form_url = "https://forms.office.com/Pages/ResponsePage.aspx?id=WGeXB8aT70uz3FOGA9yRbsbr_tTOC29AvupnhyEvx8FUNlFMQlVGMFNQUjJNUFZOTUJTMlk0SElTWSQlQCN0PWcu&origin=QRCode"
    
    analyzer = None
    try:
        print("🚀 Starting Microsoft Forms Analysis...")
        print(f"📋 Target URL: {form_url}")
        print("=" * 80)
        
        # Initialize analyzer (set headless=True for background operation)
        analyzer = FormAnalyzer(headless=True)
        
        # Run analysis
        analyzer.analyze_form(form_url)
        
        print("=" * 80)
        print("✅ Analysis completed! Check the analysis_results/ directory for detailed reports.")
        print("📄 Files generated:")
        print("  - detailed_analysis_[timestamp].json - Full JSON results")
        print("  - analysis_summary_[timestamp].txt - Human-readable summary")
        print("  - form_analysis_[timestamp].log - Detailed log file")
        print("  - initial_page_[timestamp].png - Screenshot of the form")
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
    finally:
        if analyzer:
            analyzer.close()

if __name__ == "__main__":
    main()