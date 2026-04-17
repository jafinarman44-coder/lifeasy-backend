import 'dart:async';
import 'dart:convert';
import 'package:web_socket_channel/web_socket_channel.dart';

class CallSocketManager {
  static final CallSocketManager _instance = CallSocketManager._internal();
  factory CallSocketManager() => _instance;
  CallSocketManager._internal();

  WebSocketChannel? _channel;
  bool _isConnected = false;
  String? _tenantId;
  String? _serverIp;

  // Callbacks for call events
  Function(String callerId, String callerName, String callType)? onIncomingCall;  // UPDATED
  Function()? onCallEnded;
  Function(String)? onError;
  Function()? onConnected;
  Function(Map<String, dynamic>)? onCallOffer;  // NEW: For signaling
  Function(Map<String, dynamic>)? onIceCandidate;  // NEW: For WebRTC

  bool get isConnected => _isConnected;

  Future<void> connect(String tenantId, {String? serverIp}) async {
    if (_isConnected) {
      print('Call socket already connected');
      return;
    }

    try {
      _tenantId = tenantId;
      _serverIp = serverIp ?? 'lifeasy-api.onrender.com';
      
      // CRITICAL FIX: Use correct WebSocket protocol for Render
      // Production: wss://lifeasy-api.onrender.com (no port)
      // Local: ws://localhost:8000 (with port)
      final isProduction = _serverIp!.contains('onrender.com');
      final protocol = isProduction ? 'wss' : 'ws';
      final portSuffix = isProduction ? '' : ':8000';
      
      // Connect to call signaling server
      final url = Uri.parse('$protocol://$_serverIp$portSuffix/api/call/v2/ws/$tenantId');
      
      print('📞 Connecting to Call WebSocket: $url');
      print('🔗 Protocol: ${isProduction ? "WSS (Production)" : "WS (Local)"}');
      _channel = WebSocketChannel.connect(url);

      await _channel!.ready;
      _isConnected = true;
      print('Call socket connected');
      
      onConnected?.call();

      _channel!.stream.listen(
        (message) {
          final data = Map<String, dynamic>.from(jsonDecode(message));
          _handleCallMessage(data);
        },
        onError: (error) {
          print('Call socket error: $error');
          _isConnected = false;
          onError?.call(error.toString());
        },
        onDone: () {
          print('Call socket closed');
          _isConnected = false;
        },
      );
    } catch (e) {
      print('Call connection error: $e');
      _isConnected = false;
      onError?.call(e.toString());
    }
  }

  void _handleCallMessage(Map<String, dynamic> data) {
    final action = data['action'] ?? data['type'];
    
    switch (action) {
      case 'incoming_call':
      case 'call_offer':
        // Handle incoming call
        final callerId = data['caller_id']?.toString() ?? data['sender']?.toString();
        final callerName = data['caller_name'] ?? 'Unknown';
        final callType = data['call_type'] ?? data['type'] ?? 'video';
        
        if (callerId != null) {
          onIncomingCall?.call(callerId, callerName, callType);
        }
        
        // Also emit offer for signaling
        if (action == 'call_offer') {
          onCallOffer?.call(data);
        }
        break;
        
      case 'call_answer':
        // Call accepted
        print('Call answered');
        break;
        
      case 'call_end':
      case 'call_ended':
        onCallEnded?.call();
        break;
      
      case 'call_decline':
      case 'call_missed':
        onCallEnded?.call();
        break;
        
      case 'ice_candidate':
        // WebRTC ICE candidate
        onIceCandidate?.call(data);
        break;
        
      case 'call_busy':
        onError?.call('User is busy with another call');
        break;
        
      default:
        print('Unknown call message type: $action');
    }
  }

  void sendCallSignal(Map<String, dynamic> signal) {
    if (!_isConnected || _channel == null) {
      print('Call socket not connected');
      return;
    }

    try {
      _channel!.sink.add(jsonEncode(signal));
      print('📡 Signal sent: ${signal['action'] ?? signal['type']}');
    } catch (e) {
      print('Send signal error: $e');
      onError?.call(e.toString());
    }
  }

  /// NEW: Send call offer to receiver
  void sendCallOffer({
    required String receiverId,
    required String callType,
    required Map<String, dynamic> offer,
    String? callerName,
  }) {
    if (!_isConnected || _channel == null) {
      print('Cannot send call offer - not connected');
      return;
    }

    try {
      final signal = {
        'action': 'call_offer',
        'receiver_id': receiverId,
        'caller_id': _tenantId,
        'caller_name': callerName ?? 'Unknown',
        'call_type': callType,
        'offer': offer,
        'timestamp': DateTime.now().toIso8601String(),
      };
      
      _channel!.sink.add(jsonEncode(signal));
      print('📞 Call offer sent to: $receiverId');
    } catch (e) {
      print('Send call offer error: $e');
      onError?.call(e.toString());
    }
  }

  /// NEW: Send call answer
  void sendCallAnswer({
    required String receiverId,
    required Map<String, dynamic> answer,
  }) {
    if (!_isConnected || _channel == null) return;

    try {
      final signal = {
        'action': 'call_answer',
        'receiver_id': receiverId,
        'answer': answer,
      };
      
      _channel!.sink.add(jsonEncode(signal));
      print('✅ Call answer sent to: $receiverId');
    } catch (e) {
      print('Send call answer error: $e');
    }
  }

  /// NEW: Send ICE candidate
  void sendIceCandidate({
    required String receiverId,
    required Map<String, dynamic> candidate,
  }) {
    if (!_isConnected || _channel == null) return;

    try {
      final signal = {
        'action': 'ice_candidate',
        'receiver_id': receiverId,
        'candidate': candidate,
      };
      
      _channel!.sink.add(jsonEncode(signal));
    } catch (e) {
      print('Send ICE candidate error: $e');
    }
  }

  /// NEW: End call
  void endCall({required String receiverId, String reason = 'ended'}) {
    if (!_isConnected || _channel == null) return;

    try {
      final signal = {
        'action': 'call_end',
        'receiver_id': receiverId,
        'reason': reason,
      };
      
      _channel!.sink.add(jsonEncode(signal));
      print('📴 Call ended with: $receiverId');
    } catch (e) {
      print('End call error: $e');
    }
  }

  void disconnect() {
    if (_channel != null) {
      _channel!.sink.close();
      _channel = null;
      _isConnected = false;
      print('Call socket disconnected');
    }
  }

  Future<void> reconnect() async {
    disconnect();
    await Future.delayed(Duration(seconds: 2));
    if (_tenantId != null) {
      await connect(_tenantId!, serverIp: _serverIp);
    }
  }
}
