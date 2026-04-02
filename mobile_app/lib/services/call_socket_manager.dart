import 'dart:async';
import 'package:web_socket_channel/web_socket_channel.dart';

class CallSocketManager {
  static final CallSocketManager _instance = CallSocketManager._internal();
  factory CallSocketManager() => _instance;
  CallSocketManager._internal();

  WebSocketChannel? _channel;
  bool _isConnected = false;
  String? _tenantId;

  // Callbacks for call events
  Function(String callerName, String callType)? onIncomingCall;
  Function()? onCallEnded;
  Function(String)? onError;
  Function()? onConnected;

  bool get isConnected => _isConnected;

  Future<void> connect(String tenantId) async {
    if (_isConnected) {
      print('Call socket already connected');
      return;
    }

    try {
      _tenantId = tenantId;
      
      // Connect to call signaling server
      final url = Uri.parse('ws://YOUR_SERVER_IP:8000/ws/call/$tenantId');
      _channel = WebSocketChannel.connect(url);

      await _channel!.ready;
      _isConnected = true;
      print('Call socket connected');
      
      onConnected?.call();

      _channel!.stream.listen(
        (message) {
          final data = Map<String, dynamic>.from(message);
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
    switch (data['type']) {
      case 'incoming_call':
        onIncomingCall?.call(
          data['caller_name'] ?? 'Unknown',
          data['call_type'] ?? 'video',
        );
        break;
        
      case 'call_ended':
        onCallEnded?.call();
        break;
        
      default:
        print('Unknown call message type: ${data['type']}');
    }
  }

  void sendCallSignal(Map<String, dynamic> signal) {
    if (!_isConnected || _channel == null) {
      print('Call socket not connected');
      return;
    }

    try {
      _channel!.sink.add(signal);
    } catch (e) {
      print('Send signal error: $e');
      onError?.call(e.toString());
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
      await connect(_tenantId!);
    }
  }
}
