import 'dart:async';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:web_socket_channel/web_socket_channel.dart';

class ChatSocketManager {
  static final ChatSocketManager _instance = ChatSocketManager._internal();
  factory ChatSocketManager() => _instance;
  ChatSocketManager._internal();

  WebSocketChannel? _channel;
  bool _isConnected = false;
  String? _tenantId;
  String? _receiverId;  // NEW: For tenant-to-tenant routing
  String? _serverIp;  // Server IP for WebSocket connection

  // Callbacks
  Function(Map<String, dynamic>)? onMessageReceived;  // Changed to receive full message data
  Function()? onConnected;
  Function(String)? onDisconnected;
  Function(dynamic)? onError;
  Function(String?, bool)? onTypingIndicator;  // NEW: Typing indicators
  Function(String?)? onMessageDelivered;  // NEW: Delivery receipts
  Function(String?)? onMessageSeen;  // NEW: Seen receipts

  bool get isConnected => _isConnected;
  String? get currentReceiverId => _receiverId;  // NEW: Get current receiver

  /// NEW: Initialize with receiver for tenant-to-tenant chat
  Future<void> connect(String tenantId, {String? receiverId, String? serverIp}) async {
    if (_isConnected && _tenantId == tenantId && _receiverId == receiverId) {
      print('Already connected to same chat');
      return;
    }

    // Disconnect existing connection if receiver changed
    if (_receiverId != receiverId && _isConnected) {
      disconnect();
    }

    try {
      _tenantId = tenantId;
      _receiverId = receiverId;  // Store receiver
      _serverIp = serverIp ?? '192.168.43.219';
      
      // CRITICAL FIX: Use correct WebSocket protocol for Render
      // Production: ws://192.168.43.219:8000 (no port)
      // Local: ws://localhost:8000 (with port)
      final isProduction = _serverIp!.contains('onrender.com');
      final protocol = isProduction ? 'wss' : 'ws';
      final portSuffix = isProduction ? '' : ':8000';
      
      // Connect to WebSocket server
      // If receiverId is provided, it's tenant-to-tenant chat
      // Otherwise, it's tenant-to-owner/manager chat
      final wsUrl = receiverId != null
          ? '$protocol://$_serverIp$portSuffix/api/chat/v3/ws/$tenantId/1'  // Building ID = 1 for now
          : '$protocol://$_serverIp$portSuffix/api/chat/v2/ws/$tenantId/1';
      
      print('🔌 Connecting to Chat WebSocket: $wsUrl');
      print('🔗 Protocol: ${isProduction ? "WSS (Production)" : "WS (Local)"}');
      
      final url = Uri.parse(wsUrl);
      _channel = WebSocketChannel.connect(url);

      // Listen for messages
      await _channel!.ready;
      _isConnected = true;
      print('ChatSocketManager connected (receiver: ${receiverId ?? "Owner/Manager"})');
      
      onConnected?.call();

      _channel!.stream.listen(
        (message) {
          print('📨 Message received: $message');
          try {
            final data = jsonDecode(message);
            _handleMessage(data);
          } catch (e) {
            print('Error parsing message: $e');
            onMessageReceived?.call({'text': message});
          }
        },
        onError: (error) {
          print('WebSocket error: $error');
          _isConnected = false;
          onError?.call(error);
        },
        onDone: () {
          print('WebSocket connection closed');
          _isConnected = false;
          onDisconnected?.call('Connection closed');
        },
      );
    } catch (e) {
      print('Connection error: $e');
      _isConnected = false;
      onError?.call(e);
    }
  }

  /// NEW: Handle different message types
  void _handleMessage(Map<String, dynamic> data) {
    final action = data['action'];
    
    switch (action) {
      case 'new_message':
        onMessageReceived?.call(data['message'] ?? data);
        break;
      
      case 'message_sent':
        // Message sent confirmation
        final messageId = data['message']?['id'];
        onMessageDelivered?.call(messageId?.toString());
        break;
      
      case 'message_seen':
        final messageId = data['message_id'];
        onMessageSeen?.call(messageId?.toString());
        break;
      
      case 'typing_indicator':
        final userId = data['user_id'];
        onTypingIndicator?.call(
          userId?.toString(),
          data['is_typing'] ?? false,
        );
        break;
      
      case 'presence_update':
        // Handle presence updates
        print('Presence update: ${data['user_id']} - ${data['status']}');
        break;
      
      case 'rate_limited':
        print('Rate limited: ${data['message']}');
        onError?.call('Rate limited. Please slow down.');
        break;
      
      default:
        print('Unknown action: $action');
        onMessageReceived?.call(data);
    }
  }

  /// Send message to receiver
  void sendMessage(String message, {String? receiverId, String messageType = 'text', String? mediaUrl}) {
    if (!_isConnected || _channel == null) {
      print('Not connected');
      return;
    }

    try {
      final payload = jsonEncode({
        'action': 'send_message',
        'receiver_id': receiverId ?? _receiverId,
        'text': message,
        'message_type': messageType,
        'media_url': mediaUrl,
        'timestamp': DateTime.now().toIso8601String(),
      });
      
      _channel!.sink.add(payload);
      print('📤 Message sent to: ${receiverId ?? _receiverId}');
    } catch (e) {
      print('Send error: $e');
      onError?.call(e);
    }
  }

  /// NEW: Update receiver ID (switch chat partner)
  void updateReceiver(String? receiverId) {
    _receiverId = receiverId;
    print('Receiver updated to: ${receiverId ?? "Owner/Manager"}');
  }

  /// NEW: Mark messages as seen
  void markMessagesSeen(List<String> messageIds) {
    if (!_isConnected || _channel == null) return;
    
    try {
      final payload = jsonEncode({
        'action': 'mark_seen',
        'message_ids': messageIds,
      });
      _channel!.sink.add(payload);
    } catch (e) {
      print('Error marking seen: $e');
    }
  }

  /// NEW: Mark messages as delivered
  void markMessagesDelivered(List<String> messageIds) {
    if (!_isConnected || _channel == null) return;
    
    try {
      final payload = jsonEncode({
        'action': 'mark_delivered',
        'message_ids': messageIds,
      });
      _channel!.sink.add(payload);
    } catch (e) {
      print('Error marking delivered: $e');
    }
  }

  /// NEW: Send typing indicator
  void sendTypingIndicator({required bool isTyping, int? roomId, String? receiverId}) {
    if (!_isConnected || _channel == null) return;
    
    try {
      final payload = jsonEncode({
        'action': isTyping ? 'typing_start' : 'typing_stop',
        'room_id': roomId,
        'receiver_id': receiverId ?? _receiverId,
      });
      _channel!.sink.add(payload);
    } catch (e) {
      print('Error sending typing: $e');
    }
  }

  /// NEW: Block user
  void blockUser(String userId) {
    if (!_isConnected || _channel == null) return;
    
    try {
      final payload = jsonEncode({
        'action': 'block_user',
        'user_id': userId,
      });
      _channel!.sink.add(payload);
    } catch (e) {
      print('Error blocking user: $e');
    }
  }

  /// NEW: Unblock user
  void unblockUser(String userId) {
    if (!_isConnected || _channel == null) return;
    
    try {
      final payload = jsonEncode({
        'action': 'unblock_user',
        'user_id': userId,
      });
      _channel!.sink.add(payload);
    } catch (e) {
      print('Error unblocking user: $e');
    }
  }

  /// NEW: Send ping to keep connection alive
  void sendPing() {
    if (!_isConnected || _channel == null) return;
    
    try {
      final payload = jsonEncode({
        'action': 'ping',
      });
      _channel!.sink.add(payload);
    } catch (e) {
      print('Error sending ping: $e');
    }
  }

  void disconnect() {
    if (_channel != null) {
      _channel!.sink.close();
      _channel = null;
      _isConnected = false;
      _receiverId = null;  // Clear receiver
      print('Disconnected');
    }
  }

  Future<void> reconnect() async {
    disconnect();
    await Future.delayed(Duration(seconds: 2));
    if (_tenantId != null) {
      await connect(_tenantId!, receiverId: _receiverId, serverIp: _serverIp);
    }
  }
}
