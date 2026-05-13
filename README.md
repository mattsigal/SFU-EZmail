# SFU-EZmail

A lightweight, secure desktop applet for SFU instructors to distribute grades via email. 

## Key Features
- **VPN Powered**: Uses SFU's internal SMTP relay (requires sender have the SFU VPN enabled).
- **Zero-Auth**: No passwords or 2FA required when connected to the VPN relay.
- **Personalization**: Use `$NAME$` and `$GRADE$` tags to automatically personalize every email.
- **Privacy Focused**: Student data and templates are never saved or cached between launches.

## How to Use
1. **Connect to SFU VPN**: This applet requires the VPN to access the internal mail relay.
2. **Launch SFU-EZmail**: Open the `.exe` (Windows) or `.app` (Mac).
3. **Import Data**: Load a CSV or Excel file with `Name`, `Email`, and `Grade` columns. You can also have the app generate a "template" file with these variables to fill in.
4. **Send**: Click "SEND VIA SFU RELAY".

## Installation
You can download the latest versions from the **Releases** tab:
- **Windows**: `SFU-EZmail.exe`
- **macOS**: `SFU-EZmail.app` (Zip)
