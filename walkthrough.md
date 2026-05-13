# Walkthrough: SFU Grade Distribution Applet (Outlook Mode)

This applet has been updated to use **Outlook Automation**, which is the most reliable way to send mass emails at SFU. It bypasses all authentication, MFA, and IT block issues by using the Outlook app already on your computer.

## How it Works
Instead of connecting to a server, the applet sends commands directly to your **Outlook Desktop App**.
- **No Login Required**: If your Outlook is open, the applet is ready to go.
- **Sent Items**: Every email sent will appear in your "Sent Items" folder just like a normal email.
- **MFA Friendly**: Since Outlook is already logged in, you never have to deal with authenticator codes.

## How to Use
1.  **Open Outlook**: Ensure your Outlook desktop app is open and signed in.
2.  **Launch the Applet**: Double-click [grade_applet.exe](file:///C:/Users/matth/OneDrive%20-%20Simon%20Fraser%20University%20%281sfu%29/attn/DeveloperMode/antigravity/2026-05-11_Grade-Distribution-Applet/dist/grade_applet.exe).
3.  **Check Status**: Look at **Step 3** in the applet. It should say "Outlook is open and ready."
4.  **Import & Send**:
    -   Write your template (use `$GRADE$`).
    -   Import your CSV or Excel file (or use the "Get Template CSV" button to create one).
    -   Click **SEND VIA OUTLOOK**.

## Troubleshooting
- **Outlook must be open**: If the app says "Outlook not found", simply open your Outlook desktop app and click "Refresh Status" in the applet.
- **Mac Users**: The applet also supports Outlook for Mac via AppleScript automation.

## Distribution
You can copy [grade_applet.exe](file:///C:/Users/matth/OneDrive%20-%20Simon%20Fraser%20University%20%281sfu%29/attn/DeveloperMode/antigravity/2026-05-11_Grade-Distribution-Applet/dist/grade_applet.exe) to any Windows computer. No other files are needed.
