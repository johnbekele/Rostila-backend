import requests
import os
from dotenv import load_dotenv
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import sys

load_dotenv()

url = os.getenv("BACKEND_URL")


class AuthTest(FileSystemEventHandler):
    def __init__(self, script):
        self.url = url
        self.headers = {"Content-Type": "application/json"}
        self.script = script
        self.process = None
        self.run_script()

    def run_script(self):
        if self.process:
            self.process.kill()
        self.process = subprocess.Popen([sys.executable, self.script])

    def on_modified(self, event):
        if event.src_path.endswith(self.script):
            print(f"Script {self.script} has been modified, restarting...")
            self.run_script()

    def test_resend_verification_email(self):
        email = input("Enter your email to resend verification email: ")
        payload = {"email": email}
        try:
            response = requests.post(
                f"{self.url}/api/auth/resend-verification-email",
                json=payload,
                headers=self.headers,
            )
            print(response.json())
        except Exception as e:
            print(e)

    def test_verify_email(self):
        token = input("Enter your verification token: ")
        try:
            response = requests.post(
                f"{self.url}/api/auth/verify-email?token={token}",
                headers=self.headers,
            )
            print(response.json())
        except Exception as e:
            print(e)

    def display_menu(self):
        print("================================================")
        print("============ Auth Test Routes ==================")
        print("================================================")
        print("1. Resend verification email")
        print("2. Verify email")
        print("3. Exit")


def main():
    script_file = "auth_test_script.py"  # replace with your script file to auto-reload
    auth_test = AuthTest(script_file)
    observer = Observer()
    observer.schedule(auth_test, path=script_file, recursive=False)
    observer.start()
    try:
        while True:
            print("Starting Auth Test on URL: " + url)
            auth_test.display_menu()
            user_input = input("Enter your choice: ")
            match user_input:
                case "1":
                    auth_test.test_resend_verification_email()
                case "2":
                    auth_test.test_verify_email()
                case "3":
                    observer.stop()
                    auth_test.process.kill()
                    break
                case _:
                    print("Invalid input")
    finally:
        observer.join()


if __name__ == "__main__":
    main()
