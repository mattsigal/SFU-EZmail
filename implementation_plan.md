# Implementation Plan: SFU Grade Distribution Applet

Due to the Canvas outage at SFU, we need a robust, user-friendly tool for instructors to distribute grades securely via email. This applet will be a self-contained Python application with a modern GUI.

## User Review Required

> [!IMPORTANT]
> **Authentication Method**: The SFU SMTP settings specify **OAuth2**, which is standard for Microsoft 365 but requires a complex "App Registration" process for custom software. For a "small, self-contained" applet, the most reliable approach is to have instructors use an **App Password** (a unique password generated in their SFU Microsoft 365 account settings).
>
> **I will proceed with the "Username + App Password" approach as it fits your "Step 0" (saving credentials) and avoids making every instructor register an Azure application.**

## Proposed Changes

### Core Technology Stack
- **GUI Framework**: `CustomTkinter` (Modern, premium look with dark/light mode support).
- **Data Handling**: `pandas` and `openpyxl` (To support both `.csv` and `.xlsx`).
- **Email**: `smtplib` with `STARTTLS`.
- **Packaging**: `PyInstaller` (To create the standalone `.exe` for Windows and `.app` for Mac).

---

### [NEW] `grade_applet.py`
The main application file containing the logic and UI.

#### Features:
1.  **Secure Setup**: A configuration dialog to save SMTP credentials locally (encrypted or hidden in user config).
2.  **Modern Dashboard**:
    -   **Email Subject**: Text entry.
    -   **Template Body**: Scrollable text area with support for `$GRADE$` placeholder.
    -   **File Picker**: Button to select the grades spreadsheet.
3.  **Live Preview**: A split-screen view where selecting a student from the imported list shows a real-time preview of their specific email.
4.  **Batch Processing**:
    -   Validation of email formats.
    -   A "Send All" button with a progress bar and status log.
    -   Error handling (e.g., failed login, invalid email).

### [NEW] `config_manager.py`
Handles saving and loading the faculty member's credentials and preferences locally.

---

### UI Design Mockup
- **Left Panel**: Configuration and Inputs.
- **Right Panel**: Large "Email Preview" card with a sleek, card-based design.
- **Bottom**: Status bar and "Send" controls.

## Verification Plan

### Automated Tests
- Unit tests for template replacement logic.
- Mock SMTP server tests to verify connection and message formatting.

### Manual Verification
1.  **Import Test**: Import a sample `.xlsx` and `.csv` to ensure columns are mapped correctly (Email, Grade).
2.  **Preview Test**: Verify that `$GRADE$` is correctly replaced in the preview pane.
3.  **Connectivity Test**: Perform a "Test Connection" in the setup screen.
4.  **Visual Polish**: Verify the UI looks premium on both Windows and Mac (simulated via high-res UI components).

## Next Steps
1. Create the `config_manager.py` to handle data persistence.
2. Build the `grade_applet.py` GUI layout.
3. Implement the email sending and preview logic.
