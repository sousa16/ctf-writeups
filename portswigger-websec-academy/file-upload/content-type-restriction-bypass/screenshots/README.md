# Lab: Web shell upload via Content-Type restriction bypass

## Challenge Information

* **Link:** https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-content-type-restriction-bypass
* **Challenge Description:**  This lab contains a vulnerable image upload function. It attempts to prevent users from uploading unexpected file types, but relies on checking user-controllable input to verify this.
To solve the lab, upload a basic PHP web shell and use it to exfiltrate the contents of the file /home/carlos/secret. Submit this secret using the button provided in the lab banner.
You can log in to your own account using the following credentials: **wiener:peter** 

## Background

This lab extends on the concept of file upload vulnerabilities by demonstrating how to bypass Content-Type restrictions. Unrestricted file upload leading to Remote Code Execution (RCE) occurs when a web application allows users to upload files without properly validating their type, content, or extension, enabling an attacker to upload a malicious script known as a "web shell".

A web shell is a server-side script (commonly written in PHP, ASP, JSP, or Python) that provides a remote interface for an attacker to execute arbitrary commands on the web server's operating system. Once uploaded and accessed, the web shell acts as a backdoor, allowing the attacker to navigate the file system, read sensitive files, execute commands, and potentially escalate privileges.

Content-Type Restriction Bypass:
Many web applications attempt to validate uploaded files by checking the Content-Type HTTP header, which indicates the MIME type of the file (e.g., image/jpeg, image/png, text/plain). This client-provided header is often a weak form of validation, as it can be easily intercepted and modified by an attacker using a proxy tool like Caido. By changing the Content-Type to an allowed image type (e.g., image/png), while still sending a malicious file (like a PHP web shell), an attacker can deceive the server's validation mechanisms and achieve a successful upload. This vulnerability highlights the critical need for robust server-side validation that inspects the actual file content, not just user-supplied headers.

## Solution Steps

Upon accessing the lab, I observed a simple file upload form. The goal was to upload a web shell that could execute commands on the server to retrieve the secret file.

1.  **Logging In:**
    My first step was to log in into the user account provided. After this, it was displayed a profile section with the possibility to upload a profile image.

    ![Profile Page](screenshots/profile.png)

2. **Creating the Web Shell Payload:**
   I crafted a basic PHP web shell - [rcewebshell.php](scripts/rcewebshell.php)
    This payload uses the `system()` function to execute the `cat /home/carlos/secret` command, aiming to read the content of the `secret` file located in Carlos's home directory, as specified by the lab.

3.  **Uploading the Web Shell:**
    I used the provided file upload form to upload my `rcewebshell.php` file. Since this lab specifically focuses on *unrestricted* upload, the application did not perform any client-side or server-side checks on the file's extension or content. The upload was successful.

    ![Successful File Upload](screenshots/upload.png)


4.  **Identifying the Uploaded File's Location:**
    After the successful upload, I used **Caido's HTTP History** to observe the subsequent requests and responses (specifically, the response to "Back to My Account"). This loads the profile with the new profile image, using a GET request to `files/avatars/rcewebshell.php`.

    ![GET Request](screenshots/get-request.png)

5.  **Executing the Web Shell and Retrieving the Secret:**
    To execute the web shell, I simply navigated to the identified URL (`/files/avatars/rcewebshell.php`) in my web browser.
    The web server processed the `.php` file, executing the embedded command. The output of this command, which was the secret key, was then returned in the HTTP response and displayed in my browser, solving the lab.

    ![Flag](screenshots/flag.png)

## Lessons Learned

* **Fundamental File Upload Vulnerability:** This lab clearly demonstrates the most basic form of file upload vulnerability where no validation prevents the upload of malicious executable files.
* **Web Shell Basics:** Understanding how a simple PHP web shell can be used to achieve remote code execution by leveraging server-side scripting capabilities.
* **Impact of RCE:** Unrestricted file upload leading to RCE is a critical vulnerability that can grant an attacker full control over the affected web server.
* **Importance of Validation:** Reinforces the absolute necessity for robust server-side validation on all uploaded files (checking extension, content type/magic bytes, and potentially sanitizing filenames) to prevent such attacks.