import 'dart:io';
import 'package:http/http.dart' as http;

class MediaUploadService {
  static final MediaUploadService _instance = MediaUploadService._internal();
  factory MediaUploadService() => _instance;
  MediaUploadService._internal();

  static String _serverIp = 'lifeasy-backend-production.up.railway.app';
  
  void setServerIp(String ip) {
    _serverIp = ip;
  }

  /// Upload image to server
  Future<Map<String, dynamic>?> uploadImage({
    required File imageFile,
    required int senderId,
    int? receiverId,
    int? roomId,
  }) async {
    try {
      final uri = Uri.parse('http://$_serverIp:8000/api/media/upload');
      final request = http.MultipartRequest('POST', uri);
      
      request.fields['sender_id'] = senderId.toString();
      if (receiverId != null) request.fields['receiver_id'] = receiverId.toString();
      if (roomId != null) request.fields['room_id'] = roomId.toString();
      
      request.files.add(
        await http.MultipartFile.fromPath(
          'file',
          imageFile.path,
        ),
      );

      final response = await request.send();
      final responseBody = await response.stream.bytesToString();
      
      if (response.statusCode == 200) {
        return {
          'success': true,
          'message_type': 'image',
          'file_path': responseBody, // Will be parsed properly
          'image_url': 'http://$_serverIp:8000/$responseBody',
        };
      } else {
        return {'success': false, 'error': 'Upload failed'};
      }
    } catch (e) {
      print('Error uploading image: $e');
      return {'success': false, 'error': e.toString()};
    }
  }

  /// Upload document to server
  Future<Map<String, dynamic>?> uploadDocument({
    required File file,
    required String fileName,
    required int senderId,
    int? receiverId,
    int? roomId,
  }) async {
    try {
      final uri = Uri.parse('http://$_serverIp:8000/api/media/upload');
      final request = http.MultipartRequest('POST', uri);
      
      request.fields['sender_id'] = senderId.toString();
      if (receiverId != null) request.fields['receiver_id'] = receiverId.toString();
      if (roomId != null) request.fields['room_id'] = roomId.toString();
      
      request.files.add(
        await http.MultipartFile.fromPath(
          'file',
          file.path,
          filename: fileName,
        ),
      );

      final response = await request.send();
      
      if (response.statusCode == 200) {
        final responseBody = await response.stream.bytesToString();
        return {
          'success': true,
          'message_type': 'document',
          'file_name': fileName,
          'response': responseBody,
        };
      } else {
        return {'success': false, 'error': 'Upload failed'};
      }
    } catch (e) {
      print('Error uploading document: $e');
      return {'success': false, 'error': e.toString()};
    }
  }

  /// Upload voice message
  Future<Map<String, dynamic>?> uploadVoice({
    required File audioFile,
    required int senderId,
    required int duration,
    int? receiverId,
    int? roomId,
  }) async {
    try {
      final uri = Uri.parse('http://$_serverIp:8000/api/media/upload-voice');
      final request = http.MultipartRequest('POST', uri);
      
      request.fields['sender_id'] = senderId.toString();
      request.fields['duration'] = duration.toString();
      if (receiverId != null) request.fields['receiver_id'] = receiverId.toString();
      if (roomId != null) request.fields['room_id'] = roomId.toString();
      
      request.files.add(
        await http.MultipartFile.fromPath(
          'file',
          audioFile.path,
        ),
      );

      final response = await request.send();
      
      if (response.statusCode == 200) {
        final responseBody = await response.stream.bytesToString();
        return {
          'success': true,
          'message_type': 'voice',
          'duration': duration,
          'response': responseBody,
        };
      } else {
        return {'success': false, 'error': 'Upload failed'};
      }
    } catch (e) {
      print('Error uploading voice: $e');
      return {'success': false, 'error': e.toString()};
    }
  }

  /// Get media URL from file path
  String getMediaUrl(String filePath) {
    if (filePath.startsWith('http')) {
      return filePath;
    }
    return 'http://$_serverIp:8000/$filePath';
  }
}
