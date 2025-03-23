#!/usr/bin/env python3
import time
import os
import sys
import smtplib
import argparse
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Email configuration
EMAIL_ADDRESS = 'krdo13scanner@gmail.com'
EMAIL_PASSWORD = 'gpfv zxkq ngud eqya'
TO_EMAIL_ADDRESS = 'sam.page@krdo.com'
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

# URL to monitor
URL = "https://member.everbridge.net/1772417038942752/notif"

# Path to store the last alert
LAST_ALERT_FILE = "last_alert.txt"

def log_message(message):
    """Log a message with timestamp to console"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def get_last_alert():
    """Read the last alert from file"""
    if os.path.exists(LAST_ALERT_FILE):
        with open(LAST_ALERT_FILE, 'r') as f:
            return f.read().strip()
    return ""

def save_last_alert(title):
    """Save the current alert title to file"""
    with open(LAST_ALERT_FILE, 'w') as f:
        f.write(title)

def send_email(title, timestamp, description, alert_id=None, map_data=None, detailed_description=None):
    """Send an email notification"""
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = TO_EMAIL_ADDRESS
    msg['Subject'] = f"🚨 New Everbridge Alert: {title}"
    
    # Link to the specific Everbridge alert if ID is available
    if alert_id:
        alert_link = f"https://member.everbridge.net/1772417038942752/notif/{alert_id}"
    else:
        alert_link = "https://member.everbridge.net/1772417038942752/notif"
        
    # Map image HTML - only included if map data is available
    map_html = ""
    if map_data:
        map_html = f"""
        <div class="map-container" style="margin: 20px 0; border: 1px solid #ddd; border-radius: 4px; overflow: hidden;">
            <a href="{alert_link}" style="display: block;">
                <img src="data:image/png;base64,{map_data}" style="width: 100%; max-width: 100%;" alt="Location Map">
            </a>
        </div>
        """
    
    # Use the detailed description if available, otherwise use the brief description
    display_description = description
    if detailed_description:
        display_description = detailed_description

    body = f"""
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            max-width: 600px;
            margin: 0 auto;
            padding: 0;
            color: #333333;
            background-color: #f7f7f7;
        }}
        .email-wrapper {{
            border-radius: 6px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            margin: 20px 0;
            background-color: white;
        }}
        .email-header {{
            background-color: #d9534f;
            padding: 20px;
            text-align: center;
        }}
        .email-header-text {{
            color: white;
            margin: 0;
            font-size: 24px;
            font-weight: 600;
        }}
        .email-body {{
            padding: 25px;
        }}
        .alert-title {{
            font-size: 22px;
            font-weight: 600;
            color: #222222;
            margin-top: 0;
            margin-bottom: 20px;
            padding-bottom: 12px;
            border-bottom: 1px solid #eaeaea;
        }}
        .alert-meta {{
            background-color: #f9f9f9;
            padding: 15px;
            border-radius: 4px;
            margin-bottom: 20px;
            border-left: 4px solid #5bc0de;
        }}
        .alert-meta-label {{
            font-weight: 600;
            display: inline-block;
            min-width: 60px;
        }}
        .alert-description {{
            line-height: 1.6;
            margin-bottom: 25px;
        }}
        .alert-button-container {{
            text-align: center;
            margin: 30px 0 10px;
        }}
        .alert-button {{
            display: inline-block;
            background-color: #337ab7;
            color: white;
            padding: 12px 25px;
            text-decoration: none;
            border-radius: 4px;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 14px;
            letter-spacing: 0.5px;
            transition: background-color 0.2s;
        }}
        .alert-button:hover {{
            background-color: #23527c;
        }}
        .email-footer {{
            background-color: #f2f2f2;
            padding: 15px;
            text-align: center;
            font-size: 13px;
            color: #777777;
            border-top: 1px solid #e5e5e5;
        }}
        .footer-logo {{
            margin-top: 10px;
            font-weight: 600;
            color: #555555;
        }}
        .priority-indicator {{
            background-color: #ffdc00;
            color: #000;
            padding: 5px 10px;
            border-radius: 3px;
            font-size: 12px;
            font-weight: 600;
            display: inline-block;
            margin-bottom: 15px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .map-container {{
            margin: 20px 0;
            border: 1px solid #ddd;
            border-radius: 4px;
            overflow: hidden;
        }}
        @media only screen and (max-width: 480px) {{
            .email-body {{
                padding: 15px;
            }}
            .alert-title {{
                font-size: 18px;
            }}
            .alert-button {{
                padding: 10px 15px;
                font-size: 12px;
            }}
        }}
    </style>
</head>
<body>
    <div class="email-wrapper">
        <div class="email-header">
            <h1 class="email-header-text">🚨 EMERGENCY ALERT</h1>
        </div>
        <div class="email-body">
            <div class="priority-indicator">High Priority</div>
            <h2 class="alert-title">{title}</h2>
            
            <div class="alert-meta">
                <p><span class="alert-meta-label">Time:</span> {timestamp}</p>
                <p><span class="alert-meta-label">Source:</span> Peak Alerts - El Paso & Teller Counties</p>
            </div>
            
            <div class="alert-description">
                {display_description}
            </div>
            
            {map_html}
            
            <div class="alert-button-container">
                <a href="{alert_link}" class="alert-button">View Complete Alert</a>
            </div>
        </div>
        <div class="email-footer">
            <p>This is an automated emergency notification.<br>Please do not reply to this email.</p>
            <p class="footer-logo">AlertLine ⚡ </p>
        </div>
    </div>
</body>
</html>
"""
    msg.attach(MIMEText(body, 'html'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.ehlo()
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        log_message(f"Email notification sent: {title}")
        return True
    except Exception as e:
        log_message(f"Failed to send email: {str(e)}")
        return False

def send_test_alert():
    """Send a test alert email using the latest actual alert content"""
    log_message("Preparing to send test alert with latest real alert content...")
    
    # Set up Chrome options for headless browsing
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    try:
        # Initialize the driver
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(URL)
        log_message(f"Loaded URL: {URL} to fetch latest alert for test")
        
        # Wait for the alert box to load
        wait = WebDriverWait(driver, 30)
        alert_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".box-list")))
        
        # Extract alert information
        try:
            title_element = alert_box.find_element(By.CSS_SELECTOR, "h2 a")
            title = title_element.text.strip()
            
            # Extract the notification ID from the href attribute
            alert_id = None
            href = title_element.get_attribute("href")
            if href:
                # Extract the ID from the href (format: /1772417038942752/notif/SxzzE7Nm4)
                parts = href.split('/')
                if len(parts) > 2:
                    alert_id = parts[-1]
            
            timestamp_element = alert_box.find_element(By.CSS_SELECTOR, "time[aria-label]")
            timestamp = timestamp_element.get_attribute("aria-label").strip()
            
            description_element = alert_box.find_element(By.CSS_SELECTOR, "article .description-content span")
            description = description_element.text.strip()
            
            # Map data variable - will be populated if we can extract it
            map_data = None
            # Detailed description variable - will be populated if we can extract it
            detailed_description = None
            
            # If we have an alert ID, navigate to the specific alert page to get the map and detailed description
            if alert_id:
                try:
                    # Navigate to the specific alert page
                    specific_alert_url = f"https://member.everbridge.net/1772417038942752/notif/{alert_id}"
                    log_message(f"Navigating to specific alert page: {specific_alert_url}")
                    driver.get(specific_alert_url)
                    
                    # Wait for page to load
                    time.sleep(3)  # Allow time for JavaScript to render content
                    
                    # Look for the detailed description
                    try:
                        # Wait for the detailed description element to be present
                        detailed_desc_element = wait.until(EC.presence_of_element_located(
                            (By.CSS_SELECTOR, "div[eb-test='ee_notificationDetail_text_body']")
                        ))
                        
                        if detailed_desc_element:
                            # Get the HTML content directly - we'll use it as is since it's already formatted
                            detailed_description = detailed_desc_element.get_attribute('innerHTML').strip()
                            log_message("Successfully captured detailed description")
                    except Exception as desc_err:
                        log_message(f"Error finding detailed description: {str(desc_err)}")
                    
                    # Look for the map element
                    try:
                        # Try to find the map container or elements that indicate a map
                        map_elements = driver.find_elements(By.CSS_SELECTOR, "div[style*='position: absolute'][style*='width: 100%'][style*='height: 100%']")
                        
                        # If map elements found, get a screenshot of the map area
                        if map_elements and len(map_elements) > 0:
                            log_message("Map element found on alert page")
                            
                            # Take screenshot of the map area if possible
                            try:
                                # Find the main map container
                                map_container = driver.find_element(By.CSS_SELECTOR, ".notification-content .map-container")
                                
                                # Get a screenshot
                                map_data = map_container.screenshot_as_base64
                                log_message("Successfully captured map screenshot")
                            except Exception as map_ss_err:
                                log_message(f"Could not capture map screenshot: {str(map_ss_err)}")
                    except Exception as map_err:
                        log_message(f"Error finding map element: {str(map_err)}")
                        
                except Exception as nav_err:
                    log_message(f"Error navigating to specific alert page: {str(nav_err)}")
            
            log_message(f"Found latest alert for test: {title}, ID: {alert_id}")
            
            # Modify title to indicate it's a test
            test_title = f"TEST - {title}"
            
            # Send the test email with real alert data
            success = send_email(test_title, timestamp, description, alert_id, map_data, detailed_description)
            
            if success:
                log_message("Test alert email sent successfully with latest real alert content!")
            else:
                log_message("Failed to send test alert email. Check email configuration.")
            
            return success
            
        except Exception as e:
            log_message(f"Error extracting alert data for test: {str(e)}")
            # Fall back to generic test content if we can't extract the real alert
            return send_generic_test_alert()
            
    except Exception as e:
        log_message(f"Error accessing Everbridge for test alert: {str(e)}")
        # Fall back to generic test content if we can't access the site
        return send_generic_test_alert()
        
    finally:
        # Clean up
        try:
            driver.quit()
        except:
            pass

def send_generic_test_alert():
    """Send a generic test alert email as fallback"""
    log_message("Sending generic test alert email...")
    
    test_title = "TEST ALERT - Emergency Notification System"
    test_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    test_description = ("This is a TEST of the emergency notification system. "
                       "Unable to fetch the latest real alert, so using generic test content. "
                       "This message confirms that your alert monitoring system "
                       "is functioning correctly. No action is required.")
    
    # Send the test email
    success = send_email(test_title, test_timestamp, test_description, "test-alert-id")
    
    if success:
        log_message("Generic test alert email sent successfully!")
    else:
        log_message("Failed to send generic test alert email. Check email configuration.")
        
    return success

def monitor_alerts():
    """Main function to monitor for alerts"""
    log_message("Starting Everbridge alert monitor")
    
    # Set up Chrome options for headless browsing
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    while True:
        try:
            # Initialize the driver
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(URL)
            log_message(f"Loaded URL: {URL}")
            
            # Wait for the alert box to load
            wait = WebDriverWait(driver, 30)
            alert_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".box-list")))
            
            # Extract alert information
            try:
                title_element = alert_box.find_element(By.CSS_SELECTOR, "h2 a")
                title = title_element.text.strip()
                
                # Extract the notification ID from the href attribute
                alert_id = None
                href = title_element.get_attribute("href")
                if href:
                    # Extract the ID from the href (format: /1772417038942752/notif/SxzzE7Nm4)
                    parts = href.split('/')
                    if len(parts) > 2:
                        alert_id = parts[-1]
                
                timestamp_element = alert_box.find_element(By.CSS_SELECTOR, "time[aria-label]")
                timestamp = timestamp_element.get_attribute("aria-label").strip()
                
                description_element = alert_box.find_element(By.CSS_SELECTOR, "article .description-content span")
                description = description_element.text.strip()
                
                # Map data variable - will be populated if we can extract it
                map_data = None
                # Detailed description variable - will be populated if we can extract it
                detailed_description = None
                
                # If we have an alert ID, navigate to the specific alert page to get the map and detailed description
                if alert_id:
                    try:
                        # Navigate to the specific alert page
                        specific_alert_url = f"https://member.everbridge.net/1772417038942752/notif/{alert_id}"
                        log_message(f"Navigating to specific alert page: {specific_alert_url}")
                        driver.get(specific_alert_url)
                        
                        # Wait for page to load
                        time.sleep(3)  # Allow time for JavaScript to render content
                        
                        # Look for the detailed description
                        try:
                            # Wait for the detailed description element to be present
                            detailed_desc_element = wait.until(EC.presence_of_element_located(
                                (By.CSS_SELECTOR, "div[eb-test='ee_notificationDetail_text_body']")
                            ))
                            
                            if detailed_desc_element:
                                # Get the HTML content directly - we'll use it as is since it's already formatted
                                detailed_description = detailed_desc_element.get_attribute('innerHTML').strip()
                                log_message("Successfully captured detailed description")
                        except Exception as desc_err:
                            log_message(f"Error finding detailed description: {str(desc_err)}")
                        
                        # Look for the map element
                        try:
                            # Try to find the map container or elements that indicate a map
                            map_elements = driver.find_elements(By.CSS_SELECTOR, "div[style*='position: absolute'][style*='width: 100%'][style*='height: 100%']")
                            
                            # If map elements found, get a screenshot of the map area
                            if map_elements and len(map_elements) > 0:
                                log_message("Map element found on alert page")
                                
                                # Take screenshot of the map area if possible
                                try:
                                    # Try different selector strategies for the map container
                                    map_container = None
                                    
                                    # Try method 1: Look for specific map container class
                                    try:
                                        map_container = driver.find_element(By.CSS_SELECTOR, ".map-container")
                                    except:
                                        log_message("Could not find map with .map-container selector")
                                    
                                    # Try method 2: Look for broader notification content area
                                    if not map_container:
                                        try:
                                            map_container = driver.find_element(By.CSS_SELECTOR, ".notification-content")
                                        except:
                                            log_message("Could not find map with .notification-content selector")
                                    
                                    # Try method 3: Look for any div containing the map elements
                                    if not map_container:
                                        try:
                                            # Find the parent of the map element
                                            map_parent = map_elements[0].find_element(By.XPATH, "..")
                                            map_container = map_parent.find_element(By.XPATH, "..")
                                        except:
                                            log_message("Could not find map parent container")
                                    
                                    # If we found a container, take a screenshot
                                    if map_container:
                                        # Set window size to ensure full map is visible
                                        original_size = driver.get_window_size()
                                        driver.set_window_size(1200, 1000)
                                        
                                        # Wait a moment for the map to adjust to new window size
                                        time.sleep(1)
                                        
                                        # Take screenshot
                                        map_data = map_container.screenshot_as_base64
                                        log_message("Successfully captured map screenshot")
                                        
                                        # Restore original window size
                                        driver.set_window_size(original_size['width'], original_size['height'])
                                    else:
                                        # Last resort: Try to take a screenshot of the first map element directly
                                        try:
                                            # Set window size to ensure full map is visible
                                            original_size = driver.get_window_size()
                                            driver.set_window_size(1200, 1000)
                                            
                                            # Wait a moment for the map to adjust to new window size
                                            time.sleep(1)
                                            
                                            map_data = map_elements[0].screenshot_as_base64
                                            log_message("Captured screenshot of map element directly")
                                            
                                            # Restore original window size
                                            driver.set_window_size(original_size['width'], original_size['height'])
                                        except Exception as direct_err:
                                            log_message(f"Could not take direct map screenshot: {str(direct_err)}")
                                            
                                except Exception as map_ss_err:
                                    log_message(f"Could not capture map screenshot: {str(map_ss_err)}")
                        except Exception as map_err:
                            log_message(f"Error finding map element: {str(map_err)}")
                            
                    except Exception as nav_err:
                        log_message(f"Error navigating to specific alert page: {str(nav_err)}")
                
                log_message(f"Found alert: {title}, ID: {alert_id}")
                
                # Check if this is a new alert
                last_alert = get_last_alert()
                if title != last_alert:
                    log_message(f"New alert detected! Previous: '{last_alert}', Current: '{title}'")
                    
                    # Send email notification
                    if send_email(title, timestamp, description, alert_id, map_data, detailed_description):
                        # Save the new alert
                        save_last_alert(title)
                else:
                    log_message("No new alerts detected")
                    
            except Exception as e:
                log_message(f"Error extracting alert data: {str(e)}")
                
        except Exception as e:
            log_message(f"Error monitoring alerts: {str(e)}")
            
        finally:
            # Clean up
            try:
                driver.quit()
            except:
                pass
                
            # Wait before next check
            log_message(f"Waiting 60 seconds before next check...")
            time.sleep(60)

if __name__ == "__main__":
    # Set up command line arguments
    parser = argparse.ArgumentParser(description='Everbridge Alert Monitor')
    parser.add_argument('--test', action='store_true', help='Send a test alert email and exit')
    args = parser.parse_args()
    
    # If test flag is used, send test alert and exit
    if args.test:
        send_test_alert()
        sys.exit(0)
    
    try:
        monitor_alerts()
    except KeyboardInterrupt:
        log_message("Monitor stopped by user")
    except Exception as e:
        log_message(f"Unexpected error: {str(e)}")
