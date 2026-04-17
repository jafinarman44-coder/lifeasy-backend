import 'package:http/http.dart' as http;
import 'dart:convert';

class BlockService {
  static final BlockService _instance = BlockService._internal();
  factory BlockService() => _instance;
  BlockService._internal();

  String? _serverIp;
  
  void initialize({String serverIp = 'lifeasy-api.onrender.com'}) {
    _serverIp = serverIp;
  }

  /// Block a user
  Future<Map<String, dynamic>> blockUser({
    required String blockerId,
    required String blockedId,
  }) async {
    try {
      final url = Uri.parse(
        'http://$_serverIp:8000/api/chat/v3/block/$blockedId',
      ).replace(queryParameters: {'blocker_id': blockerId});

      final response = await http.post(
        url,
        headers: {
          'Content-Type': 'application/json',
        },
      );

      if (response.statusCode == 200) {
        return {
          'success': true,
          'message': 'User blocked successfully',
        };
      } else {
        return {
          'success': false,
          'message': 'Failed to block user',
          'error': response.body,
        };
      }
    } catch (e) {
      return {
        'success': false,
        'message': 'Error: $e',
      };
    }
  }

  /// Unblock a user
  Future<Map<String, dynamic>> unblockUser({
    required String blockerId,
    required String blockedId,
  }) async {
    try {
      final url = Uri.parse(
        'http://$_serverIp:8000/api/chat/v3/unblock/$blockedId',
      ).replace(queryParameters: {'blocker_id': blockerId});

      final response = await http.post(
        url,
        headers: {
          'Content-Type': 'application/json',
        },
      );

      if (response.statusCode == 200) {
        return {
          'success': true,
          'message': 'User unblocked successfully',
        };
      } else {
        return {
          'success': false,
          'message': 'Failed to unblock user',
          'error': response.body,
        };
      }
    } catch (e) {
      return {
        'success': false,
        'message': 'Error: $e',
      };
    }
  }

  /// Get list of blocked users
  Future<List<String>> getBlockedUsers(String userId) async {
    try {
      final url = Uri.parse(
        'http://$_serverIp:8000/api/chat/v3/blocked/list/$userId',
      );

      final response = await http.get(
        url,
        headers: {
          'Content-Type': 'application/json',
        },
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final blockedUsers = data['blocked_users'] as List;
        return blockedUsers
            .map((user) => user['blocked_id'].toString())
            .toList();
      }
    } catch (e) {
      print('Error fetching blocked users: $e');
    }
    
    return [];
  }

  /// Check if a user is blocked
  Future<bool> isUserBlocked({
    required String userId,
    required String otherUserId,
  }) async {
    try {
      final blockedUsers = await getBlockedUsers(userId);
      return blockedUsers.contains(otherUserId);
    } catch (e) {
      print('Error checking block status: $e');
      return false;
    }
  }

  /// Check if you're blocked by another user
  Future<bool> areYouBlockedBy({
    required String userId,
    required String otherUserId,
  }) async {
    try {
      final theirBlockedList = await getBlockedUsers(otherUserId);
      return theirBlockedList.contains(userId);
    } catch (e) {
      print('Error checking if blocked: $e');
      return false;
    }
  }
}
