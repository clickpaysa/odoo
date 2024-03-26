<h1 align="center">ClickPay - Odoo</h1>
<p align="center"><i>The Official Odoo plugin for ClickPay</i></p>
<div align="center">
   <h2 align="center">Plugin features</h2>
<h4>Embeded Forms</h4>
<h4>Direct Apple Pay</h4>
<h4>Automatic Invoice</h4>
</div>

- - -

## Installation

### Install using FTP method

*Note: Delete any previous ClickPay plugin.*

1. Download the latest release of the plugin
2. Upload the contents of the folder in ODOO addons folder. (You can find the path for addon folders
   in odoo.conf)
3. Login to your odoo as admin and navigate to settings.
4. Scroll down to bottom of the page and click “Activate the Developer Mode (with Assets)”
5. Wait for the page to load and Navigate to Apps. Click Update Apps List in the navigation menu. You
   can disable the developer mode now by following same steps in previous point. Wait for the operation to complete. Now click “Accounting” from the left menu.
6. Here, find the module named “CLICKPAY Payment Module”.
7. Click on “Install” button. Wait for the module to be installed. Navigate to “Invoicing” module. From
   the navigation menu, goto “Configuration” -> “Payment Acquirers”.
   
   <img width="822" alt="Screenshot 2024-03-26 at 1 59 19 PM" src="https://github.com/clickpaysa/odoo/assets/135695828/891f6f43-38ec-465d-9f46-274e21946559">
   
9. Find “Clickpay Payment Gateway” and click Activate.
10. Fill in the form entering the corresponding details in each tab.
    
    * Change State to Enable
    * Fill in credentials
       - **Profile ID**: Enter the Profile ID of your ClickPay account
       - **Server Key**: `Merchant’s Dashboard >> Developers >> Key management >> Server Key`
       - **Client Key**: `Merchant’s Dashboard >> Developers >> Key management >> Server Key`
    * Enable hosted or iframe method or managed form.
    * In configuration tab, Enter the display name in website
    * Configure other according to your requirments.
    * Select Payment journal under Configuration tab. The Payment journal must have incoming
      payment set to clickpay. You can set this by clicking the arrow icon in front on Payment Journal
      field and then go to Incoming Payments tab and click Add a line.
      
      <img width="974" alt="Screenshot 2024-03-26 at 2 10 49 PM" src="https://github.com/clickpaysa/odoo/assets/135695828/bbe10908-fde2-48e2-a516-1e4753c640a3">
- - -

## Configure the Plugin for Direct Apple Pay on your website

1. Navigate to `"Invoicing" >> Configuration >> payment providers`
2. Open `ClickPay - ApplePay`
3. Please find the setup section below for the apple pay certificate creation
5. Once certificates created upload the certificates in admin panel
6. Add the Merchnat identifier name
   
   <img width="876" alt="Screenshot 2024-03-26 at 2 12 34 PM" src="https://github.com/clickpaysa/odoo/assets/135695828/d876163b-6b5c-4d04-a6ff-30d462766be8">
7. Enter the primary credentials:
   - **Profile ID**: Enter the Profile ID of your ClickPay account
   - **Server Key**: `Merchant’s Dashboard >> Developers >> Key management >> Server Key`
   - **Client Key**: `Merchant’s Dashboard >> Developers >> Key management >> Server Key`
8. Click `Save Config`


## Setup

1. You must have a Apple Developer Account To use this Feature
2. The Domain URL which you want to display the ApplePay Button. It should be verfied under same Apple Developer Account and under same merchant ID which you will create Certificates

![image](https://github.com/clickpaysa/Direct_ApplePay_on_Web/assets/135695828/2b6c16ba-58b3-44ed-a690-dfeb7762b9cb)
 
3. Create two certificates (Apple Pay Payment Processing Certificate & Apple Pay Merchant Identity Certificate)
4. Create Apple Pay Payment Processing Certificate using below Link

       https://support.clickpay.com.sa/en/support/solutions/articles/73000593115-how-to-configure-apple-pay-certificate-in-my-clickpay-dashboard-
5. Create Apple Pay Merchant Identity Certificate using below Steps

       openssl req -sha256 -nodes -newkey rsa:2048 -keyout merchant-cert.key -out merchant-cert.csr   (Create the CSR and Key File)
   
       Upload the CSR in Apple Developer portal to create merchant identifier
       Once Created Download the Certificate and Convert the downloaded cer to crt using below command
   
       openssl x509 -inform der -in merchant_id.cer -out merchant-cert.crt


## Log Access

### ClickPay custome log

1. Access `debug_Clickpay.log` file found at: `/var/log/debug_Clickpay.log`

- - -

Done
