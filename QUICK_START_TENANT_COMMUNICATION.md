# 🚀 QUICK START: Tenant-to-Tenant Communication

## ⚡ 5-Minute Setup Guide

### Step 1: Configure Server IP (Required)

Search and replace `YOUR_SERVER_IP` in these files:

**Flutter Files:**
- `mobile_app/lib/screens/tenant_list_screen.dart` (line ~38)
- `mobile_app/lib/services/chat_socket_manager.dart` (when connecting)
- `mobile_app/lib/services/call_socket_manager.dart` (when connecting)
- `mobile_app/lib/services/block_service.dart` (line ~13)

**Example:**
```dart
// Change this:
final url = Uri.parse('http://YOUR_SERVER_IP:8000/api/tenants/all');

// To this:
final url = Uri.parse('http://192.168.1.100:8000/api/tenants/all');
```

---

### Step 2: Start Backend Server

```bash
cd e:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\backend
python main_prod.py
```

Server will start at: `http://0.0.0.0:8000`

**Test the tenant endpoint:**
```bash
curl http://localhost:8000/api/tenants/all
```

---

### Step 3: Run Flutter App

```bash
cd e:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\mobile_app
flutter run
```

---

### Step 4: Test Features

#### 📱 From Dashboard:
1. Tap **"Messages"** → Opens WhatsApp-style inbox
2. Tap **"Tenants"** → Browse all tenants
3. Tap **"Chat with Manager"** → Legacy owner chat

#### 💬 Tenant List:
1. Search tenants by name/email
2. Tap any tenant → Opens chat
3. See online status (🟢/🟡/⚫)

#### 📨 Chat Screen:
1. Type and send messages
2. Tap 📎 for attachments
3. Tap 📞 for voice call
4. Tap 📹 for video call
5. Tap ⋮ → Block User

#### 📞 Incoming Calls:
- Beautiful popup appears automatically
- Tap **Accept** → Opens call screen
- Tap **Decline** → Rejects call

---

## 🎯 Key Features at a Glance

| Feature | Location | Status |
|---------|----------|--------|
| Browse Tenants | Dashboard → Tenants | ✅ Working |
| WhatsApp Inbox | Dashboard → Messages | ✅ Working |
| Tenant Chat | Tap tenant from list | ✅ Working |
| Voice Call | Chat → 📞 icon | ✅ Working |
| Video Call | Chat → 📹 icon | ✅ Working |
| Block User | Chat → ⋮ → Block | ✅ Working |
| Incoming Call | Automatic popup | ✅ Working |

---

## 🔧 Code Examples

### Start Chat with Specific Tenant:

```dart
Navigator.push(
  context,
  MaterialPageRoute(
    builder: (_) => ChatScreen(
      tenantId: '1',           // Current user
      receiverId: '2',         // Target tenant
      receiverName: 'John Doe',
    ),
  ),
);
```

### Connect to Chat WebSocket:

```dart
ChatSocketManager().connect(
  '1',                          // Current tenant ID
  receiverId: '2',              // Who to chat with
  serverIp: '192.168.1.100',   // Your server IP
);

// Listen for messages
ChatSocketManager().onMessageReceived = (messageData) {
  print('New message: $messageData');
  // Update UI
};
```

### Make Voice Call:

```dart
Navigator.push(
  context,
  MaterialPageRoute(
    builder: (_) => VoiceCallScreen(
      tenantId: '1',
      receiverId: '2',
      receiverName: 'John Doe',
    ),
  ),
);
```

### Show Incoming Call:

```dart
showIncomingCallDialog(
  context,
  callerId: '2',
  callerName: 'John Doe',
  callType: 'video',
  onAccept: (callerId) {
    // Open video call
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) => RealVideoCallScreen(
          tenantId: '1',
          receiverId: callerId,
          receiverName: 'John Doe',
        ),
      ),
    );
  },
  onDecline: (callerId) {
    CallSocketManager().endCall(
      receiverId: callerId,
      reason: 'declined',
    );
  },
);
```

---

## 🐛 Troubleshooting

### "Failed to load tenants"
- Check server is running on port 8000
- Verify server IP in `tenant_list_screen.dart`
- Check firewall allows port 8000

### WebSocket not connecting
- Ensure backend WebSocket endpoint is accessible
- Check server IP in socket managers
- Look for errors in Flutter console

### Video call shows "Waiting..."
- Both users must be online
- Check Agora App ID is valid
- Verify internet connection

### Messages not sending
- Check WebSocket connection is active
- Verify receiver ID is valid
- Check rate limiting (15 msg/10sec)

---

## 📚 Full Documentation

See complete guide: `PHASE6_STEP10_TENANT_COMMUNICATION.md`

---

## ✅ All Features Implemented

✅ Backend: GET /api/tenants/all  
✅ Tenant list screen  
✅ Dynamic chat routing  
✅ Voice/video calls  
✅ Block/unblock  
✅ Incoming call popup  
✅ WhatsApp-style inbox  
✅ Socket managers updated  
✅ Agora ready  
✅ Full documentation  

**You're all set! 🎉**
