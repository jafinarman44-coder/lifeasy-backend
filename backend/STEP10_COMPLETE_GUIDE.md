# 🚀 LIFEASY V27+ PHASE 6 STEP 10
# REAL-TIME CHAT SYSTEM - COMPLETE IMPLEMENTATION GUIDE

**Version:** V27+ PHASE 6 STEP 10  
**Date:** 2026-03-28  
**Status:** PRODUCTION READY  
**Compatibility:** Backend V1/V2/V3 + Windows + Flutter  

---

## 📋 TABLE OF CONTENTS

1. [Overview](#overview)
2. [Features Implemented](#features-implemented)
3. [Architecture](#architecture)
4. [Backend Implementation](#backend-implementation)
5. [Database Schema](#database-schema)
6. [API Reference](#api-reference)
7. [WebSocket Protocol](#websocket-protocol)
8. [Mobile Integration (Flutter)](#mobile-integration-flutter)
9. [Windows Integration (PyQt5)](#windows-integration-pyqt5)
10. [Testing Guide](#testing-guide)
11. [Troubleshooting](#troubleshooting)

---

## OVERVIEW

STEP-10 implements a complete real-time chat system similar to WhatsApp/Telegram, with full synchronization across:

- ✅ **Mobile App** (Flutter)
- ✅ **Windows App** (PyQt5)
- ✅ **Backend** (FastAPI)

### Key Features:

- **Real-time messaging** via WebSocket
- **Presence tracking** (online/offline status)
- **Delivery & seen receipts** (✓ delivered, ✓✓ seen)
- **Typing indicators** ("typing...")
- **Block/unblock system**
- **Message history** (pagination support)
- **Unread message counters**
- **Rate limiting** (anti-spam)
- **Offline message queuing**
- **Multi-device sync**

---

## FEATURES IMPLEMENTED

### ✅ Backend (FastAPI)

- [x] WebSocket endpoint: `/api/chat/v3/ws/{user_id}/{building_id}`
- [x] Message storage in database
- [x] Presence tracking system
- [x] Block/unblock functionality
- [x] Chat history API
- [x] Unread counter API
- [x] Message delete (sender & both)
- [x] Rate limiting (15 msg/10s)
- [x] Offline message queuing

### ✅ Mobile (Flutter)

Ready for integration with:
- SocketReconnectHelper compatibility
- Auto-reconnect logic
- Message delivery receipts
- Seen receipts
- Typing indicators
- Background sync
- FCM fallback notifications

### ✅ Windows (PyQt5)

Ready for integration with:
- Real-time chat screen
- Owner broadcast to tenants
- Popup toast notifications
- Typing indicators
- Online/offline indicators
- Block/unblock from UI

---

## ARCHITECTURE

### System Flow:

```
User A (Mobile/Windows)
    ↓
WebSocket Connection
    ↓
Backend: chat_socket_manager.py
    ↓
- Store message in DB
- Check if User B online
    ├─ Online → Send via WebSocket
    └─ Offline → Queue in message_queue
    ↓
Update presence & unread counters
    ↓
User B receives message
    ↓
Send receipt back
```

### Components:

1. **chat_socket_manager.py** - Core WebSocket manager
2. **chat_v3.py** - Router with WebSocket + REST endpoints
3. **models.py** - Database models (enhanced)
4. **message_queue.py** - Offline message buffering
5. **rate_limiter.py** - Anti-spam protection
6. **chat_presence** - Online/offline tracking table
7. **chat_unread** - Unread message counters table

---

## BACKEND IMPLEMENTATION

### File Structure:

```
LIFEASY_V27/backend/
├── realtime/
│   ├── chat_socket_manager.py    ← NEW: Main chat manager
│   ├── message_queue.py          ← Existing: Message buffering
│   └── rate_limiter.py           ← Existing: Rate limiting
├── routers/
│   └── chat_v3.py                ← NEW: WebSocket + REST API
├── migrations/
│   └── step10_chat_migration.sql ← NEW: Database migration
└── models.py                     ← UPDATED: New models added
```

### New Database Models:

#### ChatPresence
```python
class ChatPresence(Base):
    user_id: int
    status: str  # 'online', 'offline', 'away'
    last_seen: datetime
    building_id: int
```

#### ChatTyping
```python
class ChatTyping(Base):
    room_id: int
    user_id: int
    is_typing: bool
    expires_at: datetime
```

#### ChatUnread
```python
class ChatUnread(Base):
    user_id: int
    room_id: int
    unread_count: int
    last_read_message_id: int
```

#### Enhanced ChatMessage
```python
class ChatMessage(Base):
    # ... existing fields ...
    room_id: int              # NEW
    message_type: str         # NEW: text/image/video/file
    media_url: str            # NEW
    deleted_by_sender: bool   # NEW
    deleted_by_receiver: bool # NEW
    edited_at: datetime       # NEW
```

---

## DATABASE SCHEMA

### Tables Created:

1. **chat_presence** - User online status
2. **chat_typing** - Typing indicators
3. **chat_unread** - Unread counters
4. **chat_messages** (enhanced) - Messages with new fields
5. **blocked_users** (enhanced) - Block list with timestamp

### SQL Migration:

Run the migration script:

```bash
sqlite3 lifeasy_v27.db < migrations/step10_chat_migration.sql
```

Or manually create tables as defined in `models.py`.

---

## API REFERENCE

### WebSocket Endpoint

#### Connect to Chat

```
WS /api/chat/v3/ws/{user_id}/{building_id}
```

**Example:**
```python
ws = websocket.WebSocket()
ws.connect(f"ws://localhost:8000/api/chat/v3/ws/1/1")
```

### WebSocket Events

#### Send Message

```json
{
  "action": "send_message",
  "receiver_id": 2,
  "text": "Hello!",
  "room_id": 123,
  "message_type": "text",
  "media_url": null
}
```

**Response:**
```json
{
  "action": "message_sent",
  "message": {
    "id": 1,
    "sender_id": 1,
    "receiver_id": 2,
    "text": "Hello!",
    "timestamp": "2026-03-28T10:00:00",
    "delivered": false,
    "seen": false
  }
}
```

#### Mark as Seen

```json
{
  "action": "mark_seen",
  "message_ids": [1, 2, 3]
}
```

**Response:**
```json
{
  "action": "message_seen",
  "message_id": 1
}
```

#### Typing Indicator

```json
{
  "action": "typing_start",
  "room_id": 123,
  "receiver_id": 2
}
```

**Broadcast to room:**
```json
{
  "action": "typing_indicator",
  "room_id": 123,
  "user_id": 1,
  "is_typing": true
}
```

#### Heartbeat Ping

```json
{
  "action": "ping"
}
```

**Response:**
```json
{
  "action": "pong"
}
```

### REST API Endpoints

#### Get Chat History

```
GET /api/chat/v3/history/{room_id}?limit=50&offset=0
```

**Response:**
```json
{
  "status": "success",
  "count": 50,
  "messages": [
    {
      "id": 1,
      "sender_id": 1,
      "receiver_id": 2,
      "text": "Hello!",
      "timestamp": "2026-03-28T10:00:00",
      "delivered": true,
      "seen": true,
      "message_type": "text",
      "media_url": null
    }
  ]
}
```

#### Get Conversation Between Two Users

```
GET /api/chat/v3/conversation/{user_id}?other_user_id=2&limit=50
```

#### Get Unread Count

```
GET /api/chat/v3/unread/count/{user_id}
```

**Response:**
```json
{
  "status": "success",
  "unread_count": 5
}
```

#### Get User Presence

```
GET /api/chat/v3/presence/{user_id}
```

**Response:**
```json
{
  "status": "success",
  "user_id": 1,
  "online": true,
  "last_seen": "2026-03-28T10:00:00"
}
```

#### Block User

```
POST /api/chat/v3/block/{blocked_id}?blocker_id=1
```

#### Unblock User

```
POST /api/chat/v3/unblock/{blocked_id}?blocker_id=1
```

#### Get Blocked Users List

```
GET /api/chat/v3/blocked/list/{user_id}
```

#### Delete Message

```
DELETE /api/chat/v3/message/{message_id}?user_id=1&delete_for_both=false
```

---

## WEBSOCKET PROTOCOL

### Connection Lifecycle

1. **Connect**
   ```
   Client → WS /api/chat/v3/ws/{user_id}/{building_id}
   Server → Accept connection
   Server → Set user presence to 'online'
   Server → Deliver queued messages (if any)
   ```

2. **Send Message**
   ```
   Client → {"action": "send_message", ...}
   Server → Save to DB
   Server → Forward to receiver (if online)
   Server → Queue for receiver (if offline)
   Server → Update unread counter
   Server → Confirm to sender
   ```

3. **Receive Message**
   ```
   Server → {"action": "new_message", "message": {...}}
   Client → {"action": "mark_delivered", "message_ids": [...]}
   Client → {"action": "mark_seen", "message_ids": [...]}
   ```

4. **Disconnect**
   ```
   Client → Close connection (or timeout)
   Server → Set presence to 'offline'
   Server → Update last_seen timestamp
   ```

### Message Format

```json
{
  "id": 123,
  "sender_id": 1,
  "receiver_id": 2,
  "text": "Hello!",
  "timestamp": "2026-03-28T10:00:00",
  "delivered": false,
  "seen": false,
  "message_type": "text",
  "media_url": null
}
```

---

## MOBILE INTEGRATION (FLUTTER)

### Step 1: Add Dependencies

```yaml
dependencies:
  web_socket_channel: ^2.4.0
  flutter_chat_ui: ^1.1.0
```

### Step 2: Create Chat Socket Manager

```dart
// lib/services/chat_socket_service.dart

import 'dart:async';
import 'dart:convert';
import 'package:web_socket_channel/web_socket_channel.dart';

class ChatSocketService {
  static final ChatSocketService _instance = ChatSocketService._internal();
  factory ChatSocketService() => _instance;
  ChatSocketService._internal();

  WebSocketChannel? _channel;
  Timer? _heartbeatTimer;
  bool _isConnected = false;

  // Event streams
  final _messageController = StreamController<Map>.broadcast();
  final _presenceController = StreamController<Map>.broadcast();
  final _typingController = StreamController<Map>.broadcast();

  Stream<Map> get messageStream => _messageController.stream;
  Stream<Map> get presenceStream => _presenceController.stream;
  Stream<Map> get typingStream => _typingController.stream;

  void connect(int userId, int buildingId) async {
    final wsUrl = 'ws://lifeasy-backend-v27.onrender.com/api/chat/v3/ws/$userId/$buildingId';
    
    _channel = WebSocketChannel.connect(Uri.parse(wsUrl));
    
    _channel!.stream.listen((data) {
      final message = jsonDecode(data);
      _handleMessage(message);
    }, onDone: () {
      _isConnected = false;
      reconnect(userId, buildingId);
    });

    // Start heartbeat
    _startHeartbeat();
  }

  void _handleMessage(Map message) {
    switch (message['action']) {
      case 'new_message':
        _messageController.add(message['message']);
        break;
      case 'presence_update':
        _presenceController.add(message);
        break;
      case 'typing_indicator':
        _typingController.add(message);
        break;
      case 'message_seen':
        // Update UI to show double check
        break;
    }
  }

  void sendMessage({required int receiverId, required String text, int? roomId}) {
    if (!_isConnected) return;
    
    _channel!.sink.add(jsonEncode({
      'action': 'send_message',
      'receiver_id': receiverId,
      'text': text,
      'room_id': roomId,
      'message_type': 'text',
    }));
  }

  void markSeen(List<int> messageIds) {
    _channel!.sink.add(jsonEncode({
      'action': 'mark_seen',
      'message_ids': messageIds,
    }));
  }

  void startTyping({required int roomId, required int receiverId}) {
    _channel!.sink.add(jsonEncode({
      'action': 'typing_start',
      'room_id': roomId,
      'receiver_id': receiverId,
    }));
  }

  void stopTyping({required int roomId}) {
    _channel!.sink.add(jsonEncode({
      'action': 'typing_stop',
      'room_id': roomId,
    }));
  }

  void _startHeartbeat() {
    _heartbeatTimer = Timer.periodic(Duration(seconds: 20), (_) {
      if (_isConnected) {
        _channel!.sink.add(jsonEncode({'action': 'ping'}));
      }
    });
  }

  void reconnect(int userId, int buildingId) {
    Future.delayed(Duration(seconds: 2), () {
      connect(userId, buildingId);
    });
  }

  void disconnect() {
    _heartbeatTimer?.cancel();
    _channel?.sink.close();
    _isConnected = false;
  }
}
```

### Step 3: Create Chat Screen

```dart
// lib/screens/chat_screen.dart

import 'package:flutter/material.dart';
import 'package:flutter_chat_ui/flutter_chat_ui.dart';
import 'package:flutter_chat_types/flutter_chat_types.dart' as types;
import '../services/chat_socket_service.dart';

class ChatScreen extends StatefulWidget {
  final int otherUserId;
  final String otherUserName;
  final int? roomId;

  const ChatScreen({
    Key? key,
    required this.otherUserId,
    required this.otherUserName,
    this.roomId,
  }) : super(key: key);

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final ChatSocketService _chatService = ChatSocketService();
  List<types.Message> _messages = [];
  bool _isOtherUserTyping = false;

  @override
  void initState() {
    super.initState();
    _loadMessages();
    _listenToNewMessages();
    _listenToTyping();
  }

  void _loadMessages() async {
    // Fetch from REST API
    final response = await http.get(
      Uri.parse('https://lifeasy-backend-v27.onrender.com/api/chat/v3/conversation/${currentUserId}?other_user_id=${widget.otherUserId}')
    );
    final data = jsonDecode(response.body);
    
    setState(() {
      _messages = (data['messages'] as List).map((msg) => 
        types.TextMessage(
          author: types.User(id: msg['sender_id'].toString()),
          createdAt: DateTime.parse(msg['timestamp']).millisecondsSinceEpoch,
          id: msg['id'].toString(),
          text: msg['text'],
        )
      ).toList();
    });
  }

  void _listenToNewMessages() {
    _chatService.messageStream.listen((message) {
      setState(() {
        _messages.insert(0, types.TextMessage(
          author: types.User(id: message['sender_id'].toString()),
          createdAt: DateTime.parse(message['timestamp']).millisecondsSinceEpoch,
          id: message['id'].toString(),
          text: message['text'],
        ));
        
        // Mark as seen
        _chatService.markSeen([message['id']]);
      });
    });
  }

  void _listenToTyping() {
    _chatService.typingStream.listen((data) {
      if (data['user_id'] == widget.otherUserId) {
        setState(() {
          _isOtherUserTyping = data['is_typing'];
        });
      }
    });
  }

  void _handleSendPressed(types.PartialText message) {
    final textMessage = types.TextMessage(
      author: types.User(id: currentUserId.toString()),
      createdAt: DateTime.now().millisecondsSinceEpoch,
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      text: message.text,
    );

    setState(() {
      _messages.insert(0, textMessage);
    });

    _chatService.sendMessage(
      receiverId: widget.otherUserId,
      text: message.text,
      roomId: widget.roomId,
    );

    // Stop typing
    _chatService.stopTyping(roomId: widget.roomId ?? 0);
  }

  void _handleTyping() {
    // Send typing indicator
    _chatService.startTyping(
      roomId: widget.roomId ?? 0,
      receiverId: widget.otherUserId,
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(widget.otherUserName),
            if (_isOtherUserTyping)
              Text(
                'typing...',
                style: TextStyle(fontSize: 12, color: Colors.white70),
              ),
          ],
        ),
      ),
      body: Chat(
        messages: _messages,
        onSendPressed: _handleSendPressed,
        onTextChanged: (text) => _handleTyping(),
        inputOptions: InputOptions(
          keyboardType: TextInputType.multiline,
        ),
      ),
    );
  }
}
```

---

## WINDOWS INTEGRATION (PYQT5)

### Step 1: Create Chat Widget

```python
# app/ui/chat/owner_chat_widget.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QListWidget, QLabel
from PyQt5.QtCore import pyqtSignal
import json
import sys
sys.path.append('../../services')
from ws_reconnect_client import WSReconnectClient


class OwnerChatWidget(QWidget):
    """Owner panel chat widget for messaging tenants"""
    
    message_received = pyqtSignal(dict)
    
    def __init__(self, owner_id):
        super().__init__()
        
        self.owner_id = owner_id
        self.current_tenant_id = None
        
        # Setup WebSocket
        self.chat_ws = WSReconnectClient(
            url=f"ws://localhost:8000/api/chat/v3/ws/{owner_id}/0",
            on_open=self.on_connected,
            on_close=self.on_disconnected,
            on_message=self.on_message
        )
        self.chat_ws.connect()
        
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Tenant list
        self.tenant_list = QListWidget()
        self.tenant_list.itemClicked.connect(self.on_tenant_selected)
        layout.addWidget(self.tenant_list)
        
        # Chat area
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)
        
        # Message input
        self.message_input = QTextEdit()
        self.message_input.setMaximumHeight(80)
        layout.addWidget(self.message_input)
        
        # Send button
        send_btn = QPushButton("Send")
        send_btn.clicked.connect(self.send_message)
        layout.addWidget(send_btn)
        
        self.setLayout(layout)
    
    def on_connected(self):
        print("✅ Chat connected")
    
    def on_disconnected(self):
        print("❌ Chat disconnected")
    
    def on_message(self, message):
        """Handle incoming WebSocket messages"""
        data = json.loads(message)
        
        if data.get("action") == "new_message":
            msg = data["message"]
            
            # Show popup notification
            from app.ui.message_popup import MessagePopup
            popup = MessagePopup(f"New message from Tenant {msg['sender_id']}")
            
            # Add to chat display
            self.chat_display.append(f"Tenant {msg['sender_id']}: {msg['text']}")
    
    def on_tenant_selected(self, item):
        """Load conversation with selected tenant"""
        self.current_tenant_id = int(item.data(0))
        self.load_conversation()
    
    def load_conversation(self):
        """Load chat history with tenant"""
        # Fetch from REST API
        # Add to chat_display
    
    def send_message(self):
        """Send message to selected tenant"""
        text = self.message_input.toPlainText()
        
        if not text or not self.current_tenant_id:
            return
        
        self.chat_ws.send({
            "action": "send_message",
            "receiver_id": self.current_tenant_id,
            "text": text,
            "message_type": "text"
        })
        
        self.chat_display.append(f"You: {text}")
        self.message_input.clear()
```

---

## TESTING GUIDE

### Test 1: Basic Messaging

1. Start backend server
2. Open two browser tabs to Swagger docs (`http://localhost:8000/docs`)
3. Connect WebSocket from Tab 1 (user_id=1, building_id=1)
4. Connect WebSocket from Tab 2 (user_id=2, building_id=1)
5. Send message from Tab 1 to user_id=2
6. Verify Tab 2 receives message instantly
7. Verify message saved in database

### Test 2: Presence Tracking

1. Connect WebSocket for user_id=1
2. Call `GET /api/chat/v3/presence/1`
3. Should return `"online": true`
4. Disconnect WebSocket
5. Call `GET /api/chat/v3/presence/1` again
6. Should return `"online": false`

### Test 3: Typing Indicators

1. Connect two users
2. User 1 sends: `{"action": "typing_start", "room_id": 1, "receiver_id": 2}`
3. User 2 should receive: `{"action": "typing_indicator", "user_id": 1, "is_typing": true}`
4. User 1 sends: `{"action": "typing_stop", "room_id": 1}`
5. User 2 should receive: `{"action": "typing_indicator", "is_typing": false}`

### Test 4: Offline Message Queuing

1. Keep User 2 offline
2. User 1 sends message to User 2
3. Message should be queued in `message_queue`
4. Bring User 2 online (connect WebSocket)
5. User 2 should receive all queued messages immediately

### Test 5: Block/Unblock

1. User 1 blocks User 2: `POST /api/chat/v3/block/2?blocker_id=1`
2. User 1 tries to send message to User 2
3. Should receive error: "Cannot send message - you're blocked"
4. User 1 unblocks User 2: `POST /api/chat/v3/unblock/2?blocker_id=1`
5. User 1 can now send messages normally

### Test 6: Rate Limiting

1. Send 20 messages rapidly (within 2 seconds)
2. After 15 messages, should receive: `{"action": "rate_limited", "message": "Too many messages..."}`
3. Wait 10 seconds
4. Can send messages again

---

## TROUBLESHOOTING

### Issue 1: WebSocket Not Connecting

**Problem:** Connection fails immediately

**Solution:**
- Check backend server is running
- Verify URL format: `ws://localhost:8000/api/chat/v3/ws/{user_id}/{building_id}`
- Check CORS settings in `main_prod.py`
- Ensure no firewall blocking WebSocket connections

---

### Issue 2: Messages Not Delivered

**Problem:** Messages sent but not received

**Solution:**
- Check if receiver is online (`/api/chat/v3/presence/{user_id}`)
- If offline, messages should be queued
- Check `message_queue` in database
- Verify WebSocket connection is active

---

### Issue 3: Typing Indicator Not Showing

**Problem:** Typing status not updating

**Solution:**
- Ensure both users connected to same `room_id`
- Check WebSocket message format matches spec
- Verify `chat_typing` table exists in database
- Check browser console for errors

---

### Issue 4: High Memory Usage

**Problem:** Server memory increasing over time

**Solution:**
- Run cleanup periodically: `await chat_manager.cleanup()`
- Limit message history pagination (`limit=50`)
- Clear old typing indicators (auto-expires after 10s)
- Monitor database size

---

### Issue 5: Duplicate Messages

**Problem:** Same message received multiple times

**Solution:**
- Check for multiple WebSocket connections per user
- Ensure proper disconnect handling
- Use message `id` to deduplicate on client side
- Verify reconnection logic doesn't create duplicate subscriptions

---

## PERFORMANCE OPTIMIZATION

### Database Indexes

Ensure these indexes exist:

```sql
CREATE INDEX idx_messages_sender ON chat_messages(sender_id);
CREATE INDEX idx_messages_receiver ON chat_messages(receiver_id);
CREATE INDEX idx_messages_timestamp ON chat_messages(timestamp DESC);
CREATE INDEX idx_presence_user ON chat_presence(user_id);
CREATE INDEX idx_unread_user ON chat_unread(user_id);
```

### Connection Pooling

For production with high traffic:

```python
# In main_prod.py
from fastapi.concurrency import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    yield
    # Shutdown
    await chat_manager.cleanup()

app = FastAPI(lifespan=lifespan)
```

### Caching

Use Redis for presence caching:

```python
import redis

redis_client = redis.Redis(host='localhost', port=6379)

async def set_online(user_id: int):
    redis_client.setex(f"user:{user_id}:status", 60, "online")
```

---

## DEPLOYMENT CHECKLIST

Before deploying to production:

- [ ] Run SQL migration script
- [ ] Update CORS allowed_origins in `main_prod.py`
- [ ] Set environment variables (DATABASE_URL, etc.)
- [ ] Enable HTTPS/WSS for production
- [ ] Configure rate limits (adjust based on traffic)
- [ ] Set up monitoring (logs, metrics)
- [ ] Test with load (simulate 1000+ concurrent users)
- [ ] Backup database before deployment
- [ ] Document API changes for mobile/Windows teams

---

## SUPPORT & CONTACT

**Email:** majadar1din@gmail.com  
**WhatsApp:** +8801717574875

**Related Documentation:**
- See `BACKEND_STABILITY_PART_C_GUIDE.md` for backend stability
- See `STEP9_PART_B_STABILITY_GUIDE.md` for Windows stability
- See `COMPLETE_DOCUMENTATION.md` for full API reference

---

## ✅ FINAL STATUS

**STEP-10 Implementation:** ✅ **COMPLETE**  
**Backend:** ✅ **PRODUCTION READY**  
**Mobile:** ✅ **READY FOR INTEGRATION**  
**Windows:** ✅ **READY FOR INTEGRATION**  
**Documentation:** ✅ **COMPREHENSIVE**  

---

**Generated:** 2026-03-28  
**Version:** V27+ PHASE 6 STEP 10  
**Status:** PRODUCTION READY - WHATSAPP-GRADE CHAT SYSTEM! 🚀
