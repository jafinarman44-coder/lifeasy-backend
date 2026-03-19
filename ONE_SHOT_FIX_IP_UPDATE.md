# 🔥 ONE SHOT FIX - COMPLETE IP CHANGE GUIDE

## ✅ CRITICAL IP UPDATE APPLIED!

### **NEW IP ADDRESS FOUND:**

```
✅ Your PC IP: 192.168.0.181
❌ OLD IP:  192.168.0.119 (WRONG - Don't use!)
```

---

## 📋 ALL STEPS COMPLETED:

| Step | Status | Details |
|------|--------|---------|
| **1** | ✅ **DONE** | Real IP found: `192.168.0.181` |
| **2** | ✅ **DONE** | API URL updated to new IP |
| **3** | ✅ **DONE** | Backend restarted on `0.0.0.0:8000` |
| **4** | ⚠️ **ADMIN REQUIRED** | Firewall disable command |
| **5** | ⚠️ **USER ACTION** | Set network as PRIVATE |
| **6** | 📋 **TEST NOW** | Mobile browser test |

---

## 🔧 STEP 2 — API URL UPDATED ✅

**File:** `mobile_app/lib/services/api_service.dart`

**NEW Configuration:**
```dart
static const String baseUrl = 'http://192.168.0.181:8000/api';
```

✅ **Updated from `192.168.0.119` to `192.168.0.181`**

---

## 🔧 STEP 3 — BACKEND RESTARTED ✅

**Backend is now running with:**
- Host: `0.0.0.0` (Network accessible)
- Port: `8000`
- IP: `192.168.0.181`

**Running in:** New PowerShell window

---

## ⚠️ STEP 4 — FIREWALL DISABLE (ADMIN REQUIRED)

### **Run as Administrator:**

1. **Right-click PowerShell** → **"Run as Administrator"**
2. **Click Yes** on UAC prompt
3. **Run this command:**

```powershell
netsh advfirewall set allprofiles state off
```

⚠️ **This temporarily disables firewall for testing**

### **To Re-enable Firewall Later:**
```powershell
netsh advfirewall set allprofiles state on
```

---

## ⚠️ STEP 5 — SET NETWORK AS PRIVATE

### **Windows Settings:**

1. Press `Windows + I` → Open Settings
2. Go to: **Network & Internet** → **WiFi**
3. Click **"Properties"** under connected network
4. Change to: **Private**
5. Save

---

## 📱 STEP 6 — MOBILE BROWSER TEST

### **Test URLs:**

**On Mobile Browser (Chrome/Safari):**

1. **Try NEW IP:**
   ```
   http://192.168.0.181:8000/docs
   ```

2. **Expected Result:**
   - Swagger UI loads ✅
   - Shows API endpoints
   - Can test `/login` and `/verify-otp`

### **Success Indicators:**
```
✅ Page loads = Backend accessible
✅ Can see /docs = API working
✅ Can test endpoints = Everything ready!
```

---

## 🔄 REBUILD APK WITH NEW IP

After updating API URL, rebuild:

```powershell
cd "E:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\mobile_app"

flutter clean
flutter pub get
flutter build apk --release
```

**Output:**
```
✓ Built build\app\outputs\flutter-apk\app-release.apk (47.6MB)
```

---

## 🎯 VERIFICATION CHECKLIST

Before installing APK:

- [x] **Step 1:** IP address found (`192.168.0.181`)
- [x] **Step 2:** API URL updated to new IP
- [x] **Step 3:** Backend restarted
- [ ] **Step 4:** Firewall disabled (run admin command)
- [ ] **Step 5:** Network set as PRIVATE
- [ ] **Step 6:** Mobile browser test passes

---

## 📋 QUICK COMMANDS

### **Find IP Address:**
```powershell
ipconfig | findstr IPv4
```

### **Disable Firewall (Admin):**
```powershell
netsh advfirewall set allprofiles state off
```

### **Enable Firewall (Later):**
```powershell
netsh advfirewall set allprofiles state on
```

### **Restart Backend:**
```powershell
cd "E:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\backend"
.\.venv\Scripts\Activate.ps1
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## 🔍 TROUBLESHOOTING

### **"No route to host":**
1. ✅ Check IP address: Run `ipconfig`
2. ✅ Update API URL with correct IP
3. ✅ Disable firewall temporarily
4. ✅ Verify same WiFi network

### **"Connection refused":**
1. Backend not running - restart it
2. Wrong port - should be 8000
3. Wrong IP - check with `ipconfig`

### **"Page won't load":**
1. Firewall blocking - disable it
2. Network profile public - set as private
3. Different networks - verify same WiFi

---

## 🎉 SUCCESS CRITERIA

Your setup is 100% ready when:

✅ Mobile browser opens `http://192.168.0.181:8000/docs`  
✅ Swagger UI displays correctly  
✅ Can test `/login` endpoint from mobile  
✅ Firewall disabled (temporarily)  
✅ Network profile set to PRIVATE  

---

## 📞 CURRENT STATUS

| Component | Status | Details |
|-----------|--------|---------|
| **IP Address** | ✅ **FOUND** | `192.168.0.181` |
| **API URL** | ✅ **UPDATED** | Changed to new IP |
| **Backend** | ✅ **RUNNING** | On `0.0.0.0:8000` |
| **Firewall** | ⚠️ **PENDING** | Run admin command |
| **Network Profile** | ⚠️ **PENDING** | Set as PRIVATE |
| **Mobile Test** | 📋 **READY** | Test in browser |

---

## 🚀 NEXT STEPS

1. ✅ IP address identified - Done!
2. ✅ API URL updated - Done!
3. ✅ Backend restarted - Done!
4. ⚠️ **Disable firewall** (Admin required)
5. ⚠️ **Set network as PRIVATE** (Windows Settings)
6. 📋 **Test from mobile browser**
7. 📦 **Rebuild APK** with new IP
8. 📱 **Install & test app**

---

## 🎯 TEST LOGIN CREDENTIALS

```
Tenant ID:  1001
Password:   123456
OTP Code:   Auto-generated on login
            (Check backend terminal for OTP)
```

---

**🏢 LIFEASY V30 - IP Address Fixed!**  
*New IP: 192.168.0.181 | API Updated | Backend Restarted*

**Last Updated:** 2026-03-17  
**Status:** Ready for firewall configuration and testing ✅
