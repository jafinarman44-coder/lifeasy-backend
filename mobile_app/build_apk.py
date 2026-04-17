import subprocess
import os

mobile_app = r"e:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\mobile_app"
flutter = r"E:\Flutter\flutter\bin\flutter.bat"

os.chdir(mobile_app)
print(f"Working in: {os.getcwd()}\n")

print("[1/3] Cleaning...")
result = subprocess.run([flutter, "clean"])
if result.returncode != 0:
    print("Clean failed, but continuing...\n")

print("\n[2/3] Getting dependencies...")
result = subprocess.run([flutter, "pub", "get"])
if result.returncode != 0:
    print("Pub get failed, but continuing...\n")

print("\n[3/3] Building APK (3-5 minutes)...")
result = subprocess.run([flutter, "build", "apk", "--release"])

if result.returncode == 0:
    print("\n" + "="*50)
    print("BUILD SUCCESS!")
    print("="*50)
    print(f"\nAPK: {mobile_app}\\build\\app\\outputs\\flutter-apk\\app-release.apk")
else:
    print("\n" + "="*50)
    print("BUILD FAILED")
    print("="*50)

input("\nPress Enter to exit...")
