# Group3-Automation

This project provides a set of automated test cases for testing the Mental Health support app, [Wysa ](https://www.wysa.com/).

## Prerequisites

1. Install and start Appium:  
   Follow the [Appium Quickstart Guide](https://appium.io/docs/en/latest/quickstart/install/) to install Appium and start the server.

2. Set up an Android Virtual Device or use a physical Android phone:
   - **Virtual Device:**  
     Set up and start a virtual Android device using the Android Virtual Device (AVD) Manager. Refer to the [Managing AVDs guide](https://developer.android.com/studio/run/managing-avds) to get started.
   - **Physical Device:**  
     Plug in your physical device via USB and set up `adb` (Android Debug Bridge).

3. Clone and innstall Python dependencies:
   - Ensure Python is installed, then install the required packages by running the following command:
     ```bash
     git clone https://github.com/dh0169/Group3-Automation
     cd ./Group3-Automation
     pip install -r requirements.txt
     ```

## Running the Automation

After completing the setup steps:

1. Ensure the virtual device or physical phone is running and Appium is active.
2. Run the automation script by executing:
   ```bash
   python3 automation.py
   ```