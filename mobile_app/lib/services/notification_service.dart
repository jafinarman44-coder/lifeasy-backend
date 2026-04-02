import 'dart:convert';
import 'package:http/http.dart' as http;

class NotificationService {
  static final NotificationService _instance = NotificationService._internal();
  factory NotificationService() => _instance;
  NotificationService._internal();

  String? _tenantId;
  String? _deviceToken;

  // Initialize notification service
  Future<void> initialize(String tenantId) async {
    _tenantId = tenantId;
    print('Notification service initialized for tenant: $tenantId');
  }

  // Register device for push notifications
  Future<void> registerDevice(String deviceToken) async {
    if (_tenantId == null) {
      print('Tenant ID not set. Call initialize() first.');
      return;
    }

    _deviceToken = deviceToken;

    try {
      final url = Uri.parse('https://lifeasy-api.onrender.com/api/notifications/register');
      await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'tenant_id': _tenantId,
          'device_token': deviceToken,
          'platform': 'mobile',
        }),
      );
      print('Device registered for notifications');
    } catch (e) {
      print('Failed to register device: $e');
    }
  }

  // Send local notification (for testing)
  void showNotification({
    required String title,
    required String body,
    Map<String, dynamic>? payload,
  }) {
    print('Notification: $title - $body');
    // In production, integrate with Firebase Cloud Messaging or similar
  }

  // Subscribe to topic (e.g., building announcements)
  Future<void> subscribeToTopic(String topic) async {
    if (_tenantId == null) {
      print('Tenant ID not set');
      return;
    }

    try {
      final url = Uri.parse('https://lifeasy-api.onrender.com/api/notifications/subscribe');
      await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'tenant_id': _tenantId,
          'topic': topic,
        }),
      );
      print('Subscribed to topic: $topic');
    } catch (e) {
      print('Failed to subscribe: $e');
    }
  }

  // Unsubscribe from topic
  Future<void> unsubscribeFromTopic(String topic) async {
    if (_tenantId == null) {
      return;
    }

    try {
      final url = Uri.parse('https://lifeasy-api.onrender.com/api/notifications/unsubscribe');
      await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'tenant_id': _tenantId,
          'topic': topic,
        }),
      );
      print('Unsubscribed from topic: $topic');
    } catch (e) {
      print('Failed to unsubscribe: $e');
    }
  }

  // Get notification history
  Future<List<Map<String, dynamic>>> getNotificationHistory() async {
    if (_tenantId == null) {
      return [];
    }

    try {
      final url = Uri.parse('https://lifeasy-api.onrender.com/api/notifications/history/$_tenantId');
      final response = await http.get(url);
      
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return List<Map<String, dynamic>>.from(data);
      }
    } catch (e) {
      print('Failed to get notification history: $e');
    }
    
    return [];
  }

  // Mark notification as read
  Future<void> markAsRead(String notificationId) async {
    try {
      final url = Uri.parse('https://lifeasy-api.onrender.com/api/notifications/$notificationId/read');
      await http.put(url);
    } catch (e) {
      print('Failed to mark as read: $e');
    }
  }

  // Clear all notifications
  Future<void> clearAllNotifications() async {
    if (_tenantId == null) {
      return;
    }

    try {
      final url = Uri.parse('https://lifeasy-api.onrender.com/api/notifications/clear/$_tenantId');
      await http.delete(url);
      print('All notifications cleared');
    } catch (e) {
      print('Failed to clear notifications: $e');
    }
  }

  // Cleanup
  void dispose() {
    _tenantId = null;
    _deviceToken = null;
    print('Notification service disposed');
  }
}
