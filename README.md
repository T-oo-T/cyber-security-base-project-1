# Simple application demonstrating 5 OWASP top-10 vulnerabilities

## Vulnerabilities
1. [Identification_and_Authentication_Failures](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/): weak passwords can be used
2. [Insecure design](https://owasp.org/Top10/A04_2021-Insecure_Design/): passwords are stored as plain text
3. [Broken_Access_Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/): another users profile is accessible by changing url parameter
4. [Injection](https://owasp.org/Top10/A03_2021-Injection/): XSS vulnerability in user description
5. [Security_Logging_and_Monitoring_Failures](https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/): user logins are not logged

## How to run application
1. Setup database: ```python manage.py migrate```
2. Run application: ```python manage.py runserver````
3. Open http://127.0.0.1:8000/