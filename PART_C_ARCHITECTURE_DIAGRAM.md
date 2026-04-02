# 🏗️ LIFEASY V30 PRO - PART C ARCHITECTURE DIAGRAM

## Complete WebSocket Enhancement System (C1-C6)

---

## 📊 SYSTEM OVERVIEW

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CLIENT APPLICATIONS                         │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│   │   Web App    │  │  Mobile App  │  │ Desktop App  │             │
│   │   (React)    │  │ (React Native)│  │   (PyQt6)    │             │
│   └──────┬───────┘  └──────┬───────┘  └──────┬───────┘             │
│          │                  │                  │                     │
│          └──────────────────┴──────────────────┘                     │
│                             │                                        │
│                      WebSocket Messages                              │
│                  (JSON over port 8000)                               │
└─────────────────────────────┼────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    FASTAPI SERVER (Port 8000)                       │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                   MIDDLEWARE LAYER                            │ │
│  │                                                               │ │
│  │  ┌─────────────────┐                                         │ │
│  │  │  Rate Limiter   │  ← C5: 15 req / 10s window              │ │
│  │  │  (rate_limit.py)│     Per-user tracking, anti-spam        │ │
│  │  └────────┬────────┘                                         │ │
│  │           │                                                   │ │
│  │           ▼                                                   │ │
│  │  ┌─────────────────┐                                         │ │
│  │  │  Heartbeat Mgr  │  ← C1: Monitor connection health         │ │
│  │  │(heartbeat_mgr.py)│    20s timeout, cleanup every 5s       │ │
│  │  └────────┬────────┘                                         │ │
│  │           │                                                   │ │
│  └───────────┼───────────────────────────────────────────────────┘ │
│              │                                                     │
│              ▼                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                   ROUTING LAYER                               │ │
│  │                                                               │ │
│  │  ┌────────────────────┐    ┌────────────────────┐            │ │
│  │  │  call_router_v2.py │    │ chat_router_v2.py  │            │ │
│  │  │  + Heartbeat (C2)  │    │ + Buffer Delivery  │            │ │
│  │  │  + Buffering (C4)  │    │   (on reconnect)   │            │ │
│  │  │  + Rate Limit (C5) │    │                    │            │ │
│  │  └─────────┬──────────┘    └─────────┬──────────┘            │ │
│  │            │                         │                        │ │
│  └────────────┼─────────────────────────┼────────────────────────┘ │
│               │                         │                          │
│               ▼                         ▼                          │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                  SERVICE LAYER                                │ │
│  │                                                               │ │
│  │  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐   │ │
│  │  │ Call Manager │    │ Chat Manager │    │ Message Queue│   │ │
│  │  │(call_socket) │    │(chat_socket) │    │ (message_q)  │   │ │
│  │  │              │    │              │    │              │   │ │
│  │  │ - Connect    │    │ - Connect    │    │ - push()     │   │ │
│  │  │ - Disconnect │    │ - Disconnect │    │ - pop_all()  │   │ │
│  │  │ - Send Signal│    │ - Broadcast  │    │ - Buffer msg │   │ │
│  │  │ - Status     │    │ - Personal   │    │ - Max 100    │   │ │
│  │  └──────────────┘    └──────────────┘    └──────────────┘   │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                  BACKGROUND TASKS                             │ │
│  │                                                               │ │
│  │  ┌─────────────────────────────────────────────────────────┐ │ │
│  │  │  Heartbeat Cleanup Task (runs every 5 seconds)          │ │ │
│  │  │  - Scan all connections                                 │ │ │
│  │  │  - Find stale (> 20s since last heartbeat)              │ │ │
│  │  │  - Remove from call_manager                             │ │ │
│  │  │  - Free resources                                       │ │ │
│  │  └─────────────────────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                  AUTHENTICATION LAYER                         │ │
│  │                                                               │ │
│  │  ┌─────────────────────────────────────────────────────────┐ │ │
│  │  │  auth_v2.py                                             │ │ │
│  │  │                                                         │ │ │
│  │  │  + Token Refresh Endpoint (C6)                          │ │ │
│  │  │    GET /api/auth/v2/refresh-token?user_id={id}         │ │ │
│  │  │                                                         │ │ │
│  │  │  - Verify user active                                   │ │ │
│  │  │  - Generate new JWT (24h validity)                      │ │ │
│  │  │  - Return without re-login                              │ │ │
│  │  └─────────────────────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────────────┘ │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      DATABASE LAYER                                 │
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │  Tenant      │  │  CallLog     │  │  ChatMessage │             │
│  │  - id        │  │  - id        │  │  - id        │             │
│  │  - name      │  │  - caller_id │  │  - room_id   │             │
│  │  - email     │  │  - receiver  │  │  - sender_id │             │
│  │  - password  │  │  - status    │  │  - message   │             │
│  │  - building  │  │  - duration  │  │  - created_at│             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 MESSAGE FLOW DIAGRAM

### Scenario: User A calls User B (with buffering)

```
┌─────────┐                ┌─────────┐                ┌─────────┐
│  User A │                │  Server │                │  User B │
│ (Caller)│                │         │                │(Receiver)│
└────┬────┘                └────┬────┘                └────┬────┘
     │                          │                          │
     │ 1. Connect WS            │                          │
     │─────────────────────────>│                          │
     │                          │                          │
     │ 2. Send heartbeat        │                          │
     │    every 10s             │                          │
     │─────────────────────────>│                          │
     │    {action: heartbeat}   │                          │
     │                          │                          │
     │ 3. Send call_offer       │                          │
     │─────────────────────────>│                          │
     │    {action: call_offer,  │                          │
     │     receiver: B}         │                          │
     │                          │                          │
     │                          │ 4. Check if B online     │
     │                          │    is_user_available(B)? │
     │                          │                          │
     │                          │    NO → BUFFER           │
     │                          │──────────────────────────┐
     │                          │    message_queue.push(B, │
     │                          │      {call_offer})       │
     │                          │                          │
     │                          │                          │
     │                          │                   User B offline
     │                          │                          │
     │                          │                          │
     │                          │                          │
     │                          │                   User B reconnects
     │                          │                          │
     │                          │<─────────────────────────│
     │                          │     5. Connect WS        │
     │                          │                          │
     │                          │ 6. Pop buffered messages │
     │                          │─────────────────────────>│
     │                          │    {action: call_offer,  │
     │                          │     caller: A}           │
     │                          │                          │
     │                          │ 7. Accept call           │
     │                          │<─────────────────────────│
     │                          │    {action: call_answer} │
     │                          │                          │
     │ 8. Forward answer        │                          │
     │<─────────────────────────│                          │
     │                          │                          │
     │ 9. Begin WebRTC          │                          │
     │══════════════════════════▶                          │
     │    (peer-to-peer media)  │                          │
     │                          │                          │
     │                          │   Monitor heartbeats     │
     │<─────────────────────────│─────────────────────────>│
     │         heartbeat        │                          │
     │                          │                          │
     │ 10. End call             │                          │
     │══════════════════════════▶                          │
     │                          │                          │
     │    {action: call_end,    │                          │
     │     duration: 120}       │                          │
     │                          │                          │
     │                          │ 11. Log to database      │
     │                          │     CallLog.create()     │
     │                          │                          │
     │                          │ 12. Forward end signal   │
     │                          │─────────────────────────>│
     │                          │                          │
```

---

## ⏱️ TIMELINE DIAGRAM

### Heartbeat & Cleanup Process

```
Time →
0s    ┌────────────────────────────────────────────┐
      │ Client connects, last_seen[user] = 0      │
      └────────────────────────────────────────────┘
      
10s   ┌────────────────────────────────────────────┐
      │ Client sends heartbeat                    │
      │ last_seen[user] = 10                      │
      └────────────────────────────────────────────┘
      
20s   ┌────────────────────────────────────────────┐
      │ Client sends heartbeat                    │
      │ last_seen[user] = 20                      │
      └────────────────────────────────────────────┘
      
25s   ┌────────────────────────────────────────────┐
      │ Cleanup task runs                         │
      │ now - last_seen = 5s < 20s ✓              │
      │ Connection stays alive                    │
      └────────────────────────────────────────────┘
      
30s   ┌────────────────────────────────────────────┐
      │ Client should send heartbeat (MISSING!)   │
      │ last_seen[user] = 20 (stale)              │
      └────────────────────────────────────────────┘
      
35s   ┌────────────────────────────────────────────┐
      │ Cleanup task runs                         │
      │ now - last_seen = 15s < 20s ✓             │
      │ Still alive (grace period)                │
      └────────────────────────────────────────────┘
      
40s   ┌────────────────────────────────────────────┐
      │ Cleanup task runs                         │
      │ now - last_seen = 20s >= 20s ✗            │
      │ MARKED AS STALE                           │
      └────────────────────────────────────────────┘
      
41s   ┌────────────────────────────────────────────┐
      │ Cleanup removes connection                │
      │ call_manager.disconnect(user)             │
      │ last_seen.remove(user)                    │
      └────────────────────────────────────────────┘
```

---

## 🛡️ RATE LIMITING VISUALIZATION

```
User sends requests over time (window = 10 seconds):

Time(s)  Request #  Window Count  Status
──────────────────────────────────────────
0.0      Req 1      1             ✓ ALLOWED
0.5      Req 2      2             ✓ ALLOWED
1.0      Req 3      3             ✓ ALLOWED
1.5      Req 4      4             ✓ ALLOWED
2.0      Req 5      5             ✓ ALLOWED
2.5      Req 6      6             ✓ ALLOWED
3.0      Req 7      7             ✓ ALLOWED
3.5      Req 8      8             ✓ ALLOWED
4.0      Req 9      9             ✓ ALLOWED
4.5      Req 10     10            ✓ ALLOWED
5.0      Req 11     11            ✓ ALLOWED
5.5      Req 12     12            ✓ ALLOWED
6.0      Req 13     13            ✓ ALLOWED
6.5      Req 14     14            ✓ ALLOWED
7.0      Req 15     15            ✓ ALLOWED (MAX!)
7.5      Req 16     16            ✗ BLOCKED (Rate Limit)
8.0      Req 17     16            ✗ BLOCKED
9.0      Req 18     16            ✗ BLOCKED
10.0     Req 19     15            ✓ ALLOWED (Req 1 expired)
10.5     Req 20     15            ✓ ALLOWED


Window slides forward, oldest requests expire:

[0s-----1s-----2s-----3s-----4s-----5s-----6s-----7s-----8s-----9s-----10s]
 |       |       |       |       |       |       |       |       |       |
Req1   Req2    Req3    Req4    Req5    Req6    Req7    Req8    Req9   Req10
(expires at 10s)                                   
                                               
At t=10.5s: Only Req6-Req20 are in window (15 requests)
```

---

## 💾 MESSAGE QUEUE OPERATION

```
User goes offline → Messages buffer → User reconnects → Deliver all

Timeline:
─────────────────────────────────────────────────────────────────

t=0: User A connected
     buffer[A] = []

t=10: User A disconnects (network issue)
      buffer[A] = []

t=15: Message sent to User A (while offline)
      buffer[A].push({type: 'call_offer', caller: 'B'})
      buffer[A] = [{call_offer from B}]

t=20: Another message to User A
      buffer[A].push({type: 'chat', from: 'C'})
      buffer[A] = [{call_offer from B}, {chat from C}]

t=25: User A reconnects
      WebSocket connection established
      
      On connect trigger:
        msgs = buffer.pop_all(A)
        buffer[A] = []
        
        for msg in msgs:
          ws.send(msg)
      
      User A receives:
        1. {call_offer from B}
        2. {chat from C}
        
t=30: New message to User A (now online)
      Direct delivery via WebSocket
      No buffering needed
```

---

## 🎯 COMPONENT INTERACTIONS

```
┌──────────────────────────────────────────────────────────────┐
│                        USER ACTIONS                          │
└──────────────────┬───────────────────────────────────────────┘
                   │
     ┌─────────────┼─────────────┐
     │             │             │
     ▼             ▼             ▼
┌─────────┐  ┌──────────┐  ┌──────────┐
│ Connect │  │  Send   │  │ Receive  │
│    WS   │  │ Message │  │  Signal  │
└────┬────┘  └────┬─────┘  └────┬─────┘
     │            │             │
     │            │             │
     ▼            ▼             ▼
┌──────────────────────────────────────┐
│         CONNECTION MANAGER           │
│  - Tracks online/offline status     │
│  - Manages WebSocket connections    │
└──────────────────────────────────────┘
     │            │             │
     │            │             │
     ▼            ▼             ▼
┌─────────┐  ┌──────────┐  ┌──────────┐
│Register │  │Check Rate│  │  Check   │
│  User   │  │  Limit   │  │ Available│
└────┬────┘  └────┬─────┘  └────┬─────┘
     │            │             │
     │            │             │
     ▼            ▼             ▼
┌──────────────────────────────────────┐
│      HEARTBEAT MANAGER (C1)         │
│  - Update last_seen timestamp       │
│  - Background cleanup task          │
└──────────────────────────────────────┘
     │            │             │
     │            │             │
     ▼            ▼             ▼
┌─────────┐  ┌──────────┐  ┌──────────┐
│ Start   │  │  Pass   │  │  Send    │
│Tracking │  │ Through │  │  Signal  │
└─────────┘  └────┬─────┘  └────┬─────┘
                  │             │
                  │             │
                  ▼             ▼
           ┌──────────┐  ┌──────────┐
           │  Block   │  │  Buffer  │
           │   (C5)   │  │   (C4)   │
           └──────────┘  └──────────┘
```

---

## 📊 DATA STRUCTURES

### HeartbeatManager
```python
{
    "last_seen": {
        1: 1711234567.890,  # user_id → timestamp
        2: 1711234568.123,
        3: 1711234569.456,
    },
    "TIMEOUT": 20,
    "CHECK_INTERVAL": 5
}
```

### MessageQueue
```python
{
    "buffer": {
        1: deque([msg1, msg2, msg3], maxlen=100),
        2: deque([msg4], maxlen=100),
        # user_id → deque of messages
    }
}
```

### RateLimiter
```python
{
    "timestamps": {
        1: [1711234560.0, 1711234561.0, 1711234562.0],
        2: [1711234563.0, 1711234564.0],
        # user_id → list of request timestamps
    },
    "MAX_REQUESTS": 15,
    "WINDOW": 10
}
```

---

## 🚀 DEPLOYMENT CHECKLIST

- [ ] All new files copied to server
- [ ] Modified files updated on server
- [ ] Dependencies installed (asyncio, collections)
- [ ] Server restart scheduled
- [ ] Monitoring enabled for new log messages
- [ ] Rollback plan ready

---

**Architecture Documentation: COMPLETE ✅**
