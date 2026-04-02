import 'dart:async';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:web_socket_channel/web_socket_channel.dart';

class SocketManager {
  static final SocketManager _instance = SocketManager._internal();
  factory SocketManager() => _instance;
  SocketManager._internal();

  WebSocketChannel? _channel;
  bool _isConnected = false;
  String? _tenantId;

  // Callbacks
  Function(String)? onMessageReceived;
  Function()? onConnected;
  Function(String)? onDisconnected;
  Function(dynamic)? onError;

  bool get isConnected => _isConnected;

  Future<void> connect(String tenantId) async {
    if (_isConnected) {
      print('Already connected');
      return;
    }

    try {
      _tenantId = tenantId;
      
      // Connect to WebSocket server
      final url = Uri.parse('ws://YOUR_SERVER_IP:8000/ws/chat/$tenantId');
      _channel = WebSocketChannel.connect(url);

      // Listen for messages
      await _channel!.ready;
      _isConnected = true;
      print('WebSocket connected');
      
      onConnected?.call();

      _channel!.stream.listen(
        (message) {
          print('Message received: $message');
          final data = jsonDecode(message);
          onMessageReceived?.call(data['message'] ?? message);
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

  void sendMessage(String message) {
    if (!_isConnected || _channel == null) {
      print('Not connected');
      return;
    }

    try {
      final payload = jsonEncode({
        'type': 'chat_message',
        'tenant_id': _tenantId,
        'message': message,
        'timestamp': DateTime.now().toIso8601String(),
      });
      
      _channel!.sink.add(payload);
      print('Message sent: $message');
    } catch (e) {
      print('Send error: $e');
      onError?.call(e);
    }
  }

  void disconnect() {
    if (_channel != null) {
      _channel!.sink.close();
      _channel = null;
      _isConnected = false;
      print('Disconnected');
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
