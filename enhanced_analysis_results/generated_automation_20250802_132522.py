#!/usr/bin/env python3
"""
Auto-generated form automation code
Generated on: 2025-08-02 13:26:45
Source form: https://forms.office.com/Pages/ResponsePage.aspx?id=WGeXB8aT70uz3FOGA9yRbsbr_tTOC29AvupnhyEvx8FUNlFMQlVGMFNQUjJNUFZOTUJTMlk0SElTWSQlQCN0PWcu&origin=QRCode
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class GeneratedFormAutomation:
    def __init__(self):
        # Initialize your driver here
        pass
    
    def automate_form(self, form_data):
        """Generated automation based on form analysis"""
        try:

            # Page 1: Nexus (North Tower) Visitor Registration
            self.logger.info("Processing page 1")

            # Fill 
            try:
                element = self.driver.find_element(By.XPATH, "//*[@data-automation-id='textInput']")
                element.clear()
                element.send_keys(form_data.get('text_input_1', ''))
            except Exception as e:
                self.logger.warning(f"Could not fill text_input_1: {e}")

            # Fill 
            try:
                element = self.driver.find_element(By.XPATH, "//*[@data-automation-id='textInput']")
                element.clear()
                element.send_keys(form_data.get('text_input_2', ''))
            except Exception as e:
                self.logger.warning(f"Could not fill text_input_2: {e}")

            # Handle dropdown: English (United States)
            try:
                dropdown = self.driver.find_element(By.XPATH, "/html/body/div/div/div[1]/div/div/div/div/div[3]/div/div/div[1]/div[1]/div[1]/div[1]/div[1]/div")
                dropdown.click()
                time.sleep(1)
                # Select option based on form_data
                # Options available: ['English (United States)', '中文（简体）']
            except Exception as e:
                self.logger.warning(f"Could not handle dropdown: {e}")

            # Handle dropdown: Select your answer
            try:
                dropdown = self.driver.find_element(By.XPATH, "/html/body/div/div/div[1]/div/div/div/div/div[3]/div/div/div[2]/div[2]/div[3]/div[2]/div/div/div")
                dropdown.click()
                time.sleep(1)
                # Select option based on form_data
                # Options available: ['1', '2', '3', '4', '5', '6']
            except Exception as e:
                self.logger.warning(f"Could not handle dropdown: {e}")

            # Handle dropdown: Select your answer
            try:
                dropdown = self.driver.find_element(By.XPATH, "/html/body/div/div/div[1]/div/div/div/div/div[3]/div/div/div[2]/div[2]/div[4]/div[2]/div/div/div")
                dropdown.click()
                time.sleep(1)
                # Select option based on form_data
                # Options available: ['Contractor', 'Delivery', 'Meeting', 'Visit', 'Training', 'Staff']
            except Exception as e:
                self.logger.warning(f"Could not handle dropdown: {e}")

            # Click Next button
            try:
                next_button = self.driver.find_element(By.XPATH, "/html/body/div/div/div[1]/div/div/div/div/div[3]/div/div/div[2]/div[3]/div/button")
                next_button.click()
                time.sleep(3)
            except Exception as e:
                self.logger.warning(f"Could not click Next button: {e}")

            # Page 2: Nexus (North Tower) Visitor Registration
            self.logger.info("Processing page 2")

            # Fill 
            try:
                element = self.driver.find_element(By.XPATH, "//*[@data-automation-id='textInput']")
                element.clear()
                element.send_keys(form_data.get('text_input_1', ''))
            except Exception as e:
                self.logger.warning(f"Could not fill text_input_1: {e}")

            # Fill 
            try:
                element = self.driver.find_element(By.XPATH, "//*[@data-automation-id='textInput']")
                element.clear()
                element.send_keys(form_data.get('text_input_2', ''))
            except Exception as e:
                self.logger.warning(f"Could not fill text_input_2: {e}")

            # Handle dropdown: English (United States)
            try:
                dropdown = self.driver.find_element(By.XPATH, "/html/body/div/div/div[1]/div/div/div/div/div[3]/div/div/div[1]/div[1]/div[1]/div[1]/div[1]/div")
                dropdown.click()
                time.sleep(1)
                # Select option based on form_data
                # Options available: ['English (United States)', '中文（简体）']
            except Exception as e:
                self.logger.warning(f"Could not handle dropdown: {e}")

            # Handle dropdown: Select your answer
            try:
                dropdown = self.driver.find_element(By.XPATH, "/html/body/div/div/div[1]/div/div/div/div/div[3]/div/div/div[2]/div[2]/div[3]/div[2]/div/div/div")
                dropdown.click()
                time.sleep(1)
                # Select option based on form_data
                # Options available: ['1', '2', '3', '4', '5', '6']
            except Exception as e:
                self.logger.warning(f"Could not handle dropdown: {e}")

            # Handle dropdown: Select your answer
            try:
                dropdown = self.driver.find_element(By.XPATH, "/html/body/div/div/div[1]/div/div/div/div/div[3]/div/div/div[2]/div[2]/div[4]/div[2]/div/div/div")
                dropdown.click()
                time.sleep(1)
                # Select option based on form_data
                # Options available: ['Contractor', 'Delivery', 'Meeting', 'Visit', 'Training', 'Staff']
            except Exception as e:
                self.logger.warning(f"Could not handle dropdown: {e}")

            # Click Next button
            try:
                next_button = self.driver.find_element(By.XPATH, "/html/body/div/div/div[1]/div/div/div/div/div[3]/div/div/div[2]/div[3]/div/button")
                next_button.click()
                time.sleep(3)
            except Exception as e:
                self.logger.warning(f"Could not click Next button: {e}")

        except Exception as e:
            self.logger.error(f"Form automation failed: {e}")
    
# Example usage:
# automator = GeneratedFormAutomation()
# form_data = {
#     'text_input_1': 'Your Name',
#     'text_input_2': 'Your Company',
#     # Add more fields as needed
# }
# automator.automate_form(form_data)
