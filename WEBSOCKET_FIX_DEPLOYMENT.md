# 🔧 WebSocket Connection Fix - Railway Deployment

## ❌ Problem Identified

WebSocket connections were immediately disconnecting with error:
```
WS ERROR: Connection to remote host was lost.
🔴 WS Disconnected
❌ Status banner: Offline
```

## 🔍 Root Cause

**Double `ws.accept()` call** causing crash:

1. In `backend/routers/chat_v3.py` line 56:
   ```python
   await ws.accept()  # First accept
   ```

2. In `backend/realtime/chat_socket_manager.py` line 45:
   ```python
   await ws.accept()  # Second accept - CRASH!
   ```

When a WebSocket is accepted twice, it immediately closes the connection.

## ✅ Fix Applied

Removed duplicate `await ws.accept()` from `chat_socket_manager.py`:

```python
async def connect(self, user_id: int, building_id: int, ws: WebSocket, db: Session):
    """Accept new WebSocket connection and set user online"""
    # NOTE: ws.accept() is already called in the router, don't call it again here
    
    self.active_connections[user_id] = ws
    # ... rest of the code
```

## 🚀 Deployment Status

✅ **Fix committed**: `29287f12` - "Fix WebSocket double accept crash"  
✅ **Pushed to GitHub**: Railway auto-deploy triggered  
⏳ **Railway deployment**: In progress (2-3 minutes)

## 📋 Files Changed

- `LIFEASY_V27/backend/realtime/chat_socket_manager.py`

## 🧪 Test Results

**Before Fix:**
```
🔌 Testing WebSocket: wss://lifeasy-backend-production.up.railway.app/api/chat/v3/ws/1/1
✅ WebSocket CONNECTED!
❌ Connection closed: no close frame received
```

**After Fix (Expected):**
```
🔌 Testing WebSocket: wss://lifeasy-backend-production.up.railway.app/api/chat/v3/ws/1/1
✅ WebSocket CONNECTED!
📤 Sent: ping
📥 Received: {"action": "pong"}
✅ WebSocket is working!
```

## ⏱️ What Happens Next

1. **Railway detects GitHub push** (immediate)
2. **Railway builds new deployment** (1-2 minutes)
3. **Railway starts new server** (30 seconds)
4. **Health check passes** (`/health` endpoint)
5. **Old deployment replaced** (seamless)
6. **WebSocket connections work** ✅

## 🔄 How to Verify

### Option 1: Wait 3 minutes, then restart desktop app
```bash
# Desktop app will automatically reconnect
python main.py
```

Expected output:
```
🟢 WS Connected
✅ Status banner: Online
📞 CALL WS CONNECTED
```

### Option 2: Test WebSocket directly
```bash
python test_railway_websocket.py
```

Expected: `✅ WebSocket is working!`

### Option 3: Check Railway Dashboard
1. Go to: https://railway.app/
2. Select your project: `lifeasy-backend-production`
3. Check deployment status
4. View logs for any errors

## 📊 Current Architecture

```
Desktop App (PyQt5)
    │
    ├── WebSocket: wss://lifeasy-backend-production.up.railway.app/api/chat/v3/ws/1/1
    │
    └── WebSocket: wss://lifeasy-backend-production.up.railway.app/api/call/v2/ws/1
                      │
                      ▼
              Railway Backend (Port 8080)
                      │
                      ├── chat_v3.py router
                      ├── call_router_v2.py
                      ├── chat_socket_manager.py ← FIXED
                      └── call_socket_manager.py
```

## 🎯 Expected Result

After deployment completes:

✅ **Desktop App**: Green "Online" status stays stable  
✅ **Chat**: Real-time messaging works  
✅ **Calls**: Voice/video signaling works  
✅ **No more reconnection loops**

## 🚨 If Still Not Working

1. **Check Railway logs** for errors
2. **Verify database connection** (PostgreSQL on Render)
3. **Check if user_id=1 and building_id=1 exist** in database
4. **Test with mobile app** to isolate issue

## 📝 Note for Future

**NEVER call `ws.accept()` twice!**

Correct pattern:
```python
# In router file:
@router.websocket("/ws/{user_id}")
async def websocket_endpoint(ws: WebSocket, user_id: int):
    await ws.accept()  # ← Call here ONCE
    await manager.connect(user_id, ws)  # ← Manager does NOT accept again

# In manager file:
async def connect(self, user_id: int, ws: WebSocket):
    # NO ws.accept() here!
    self.connections[user_id] = ws
```

---

**Status**: 🟡 Deployment in progress - wait 2-3 minutes, then test!
