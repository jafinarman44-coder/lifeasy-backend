import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:file_picker/file_picker.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:io';
import '../services/chat_socket_manager.dart';
import 'voice_call_screen.dart';
import 'video_call_screen.dart';

class ChatScreen extends StatefulWidget {
  final String tenantId;
  final String? receiverId;  // For tenant-to-tenant chat
  final String? receiverName;  // Display name in app bar
  
  ChatScreen({
    required this.tenantId,
    this.receiverId,  // Optional - defaults to owner/manager
    this.receiverName,  // Optional - defaults to "Manager"
  });
  
  @override
  _ChatScreenState createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final TextEditingController messageController = TextEditingController();
  final ImagePicker _imagePicker = ImagePicker();
  List<Map<String, dynamic>> messages = [];
  bool _isConnected = false;
  final ChatSocketManager _chatSocket = ChatSocketManager();
  
  @override
  void initState() {
    super.initState();
    _initializeRealtimeChat();
  }
  
  @override
  void dispose() {
    _chatSocket.disconnect();
    super.dispose();
  }
  
  // Initialize real-time WebSocket chat
  Future<void> _initializeRealtimeChat() async {
    try {
      // Connect to WebSocket for real-time messaging
      await _chatSocket.connect(
        widget.tenantId,
        receiverId: widget.receiverId,
        serverIp: '192.168.43.219',  // LOCAL BACKEND
      );
      
      // Listen for incoming messages
      _chatSocket.onMessageReceived = (messageData) {
        if (mounted) {
          setState(() {
            messages.add({
              'text': messageData['text'] ?? messageData['message'] ?? '',
              'isSent': false,
              'time': _extractTimeFromTimestamp(messageData['timestamp'] ?? DateTime.now().toIso8601String()),
              'type': messageData['message_type'] ?? messageData['type'] ?? 'text',
              'imagePath': messageData['media_url'],
            });
          });
        }
      };
      
      _chatSocket.onConnected = () {
        if (mounted) {
          setState(() {
            _isConnected = true;
          });
          print('✅ Real-time chat connected');
        }
      };
      
      _chatSocket.onDisconnected = (reason) {
        if (mounted) {
          setState(() {
            _isConnected = false;
          });
          print('⚠️ Chat disconnected: $reason');
        }
      };
      
      print('✅ REAL chat initialized with ${widget.receiverName ?? "Manager"}');
      print('   My ID: ${widget.tenantId}');
      print('   Receiver ID: ${widget.receiverId ?? "N/A"}');
    } catch (e) {
      print('❌ Chat initialization error: $e');
    }
  }
  
  String _extractTimeFromTimestamp(String timestamp) {
    try {
      final dt = DateTime.parse(timestamp);
      return '${dt.hour.toString().padLeft(2, '0')}:${dt.minute.toString().padLeft(2, '0')}';
    } catch (e) {
      return DateTime.now().toString().substring(11, 16);
    }
  }
  
  // Send message via WebSocket and HTTP backup
  Future<void> _sendMessage(String text) async {
    if (text.trim().isEmpty) return;
    
    try {
      // PRIMARY: Send via WebSocket (real-time)
      if (_chatSocket.isConnected) {
        _chatSocket.sendMessage(
          text,
          receiverId: widget.receiverId,
          messageType: 'text',
        );
        print('✅ Message sent via WebSocket');
      }
      
      // BACKUP: Also send via HTTP API for persistence
      final url = Uri.parse('http://192.168.43.219:8000/api/chat/v3/send');
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'sender_id': int.parse(widget.tenantId),
          'receiver_id': int.parse(widget.receiverId ?? '0'),
          'message': text,
          'message_type': 'text',
        }),
      );
      
      if (response.statusCode == 200) {
        print('✅ Message saved to database');
      }
    } catch (e) {
      print('❌ Error sending message: $e');
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Failed to send message'), backgroundColor: Colors.red),
      );
    }
  }
  
  @override
  Widget build(BuildContext context) {
    // Determine chat title based on receiverId
    String chatTitle = widget.receiverName ?? 'Chat with Manager';
    bool isTenantToTenant = widget.receiverId != null;
    
    return Scaffold(
      appBar: AppBar(
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(chatTitle),
            Row(
              children: [
                Icon(
                  _isConnected ? Icons.circle : Icons.circle_outlined,
                  color: _isConnected ? Colors.green : Colors.red,
                  size: 8,
                ),
                SizedBox(width: 6),
                Text(
                  _isConnected ? 'Online' : 'Connecting...',
                  style: TextStyle(
                    fontSize: 11,
                    color: _isConnected ? Colors.green : Colors.orange,
                    fontWeight: FontWeight.normal,
                  ),
                ),
              ],
            ),
            if (isTenantToTenant)
              Text(
                'Tenant-to-Tenant',
                style: TextStyle(
                  fontSize: 12,
                  color: Colors.white70,
                  fontWeight: FontWeight.normal,
                ),
              ),
          ],
        ),
        backgroundColor: Colors.blueAccent,
        actions: [
          // Voice Call Button
          IconButton(
            icon: Icon(Icons.call),
            onPressed: () {
              if (isTenantToTenant && widget.receiverId != null) {
                // Navigate to REAL voice call screen with Agora
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (_) => VoiceCallScreen(
                      tenantId: widget.tenantId,
                      channelName: 'call_${widget.tenantId}_${widget.receiverId}',
                      receiverId: widget.receiverId!,
                    ),
                  ),
                );
              } else {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text('Call feature unavailable')),  );
              }
            },
          ),
          // Video Call Button
          IconButton(
            icon: Icon(Icons.videocam),
            onPressed: () {
              if (isTenantToTenant && widget.receiverId != null) {
                // Navigate to REAL video call screen with Agora
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (_) => VideoCallScreen(
                      tenantId: widget.tenantId,
                      channelName: 'videocall_${widget.tenantId}_${widget.receiverId}',
                      receiverId: widget.receiverId!,
                    ),
                  ),
                );
              } else {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text('Video call feature unavailable')),  );
              }
            },
          ),
          if (isTenantToTenant)
            PopupMenuButton<String>(
              onSelected: (value) {
                if (value == 'block') {
                  _showBlockDialog();
                }
              },
              itemBuilder: (context) => [
                PopupMenuItem(
                  value: 'block',
                  child: Row(
                    children: [
                      Icon(Icons.block, color: Colors.red),
                      SizedBox(width: 8),
                      Text('Block User'),
                    ],
                  ),
                ),
              ],
            ),
        ],
      ),
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [Color(0xff0f172a), Colors.black87],
          ),
        ),
        child: Column(
          children: [
            // Messages List
            Expanded(
              child: ListView.builder(
                padding: EdgeInsets.all(16),
                itemCount: messages.length,
                itemBuilder: (context, index) {
                  final message = messages[index];
                  return Align(
                    alignment: message['isSent'] 
                        ? Alignment.centerRight 
                        : Alignment.centerLeft,
                    child: Container(
                      margin: EdgeInsets.only(bottom: 12),
                      padding: EdgeInsets.all(12),
                      constraints: BoxConstraints(maxWidth: 250),
                      decoration: BoxDecoration(
                        color: message['isSent'] 
                            ? Colors.blueAccent 
                            : Colors.grey[800],
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          // Show image if message type is 'image'
                          if (message['type'] == 'image' && message['imagePath'] != null)
                            ClipRRect(
                              borderRadius: BorderRadius.circular(8),
                              child: Image.file(
                                File(message['imagePath']),
                                width: 200,
                                height: 200,
                                fit: BoxFit.cover,
                              ),
                            ),
                          
                          // Show document icon if type is 'document'
                          if (message['type'] == 'document')
                            Padding(
                              padding: EdgeInsets.only(bottom: 8),
                              child: Row(
                                children: [
                                  Icon(Icons.insert_drive_file, color: Colors.orange, size: 24),
                                  SizedBox(width: 8),
                                  Expanded(
                                    child: Text(
                                      message['text'],
                                      style: TextStyle(color: Colors.white, fontSize: 14),
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          
                          // Show text message
                          if (message['type'] == null || message['type'] == 'text')
                            Text(
                              message['text'],
                              style: TextStyle(color: Colors.white),
                            ),
                          
                          SizedBox(height: 4),
                          Text(
                            message['time'],
                            style: TextStyle(
                              color: Colors.white70,
                              fontSize: 10,
                            ),
                          ),
                        ],
                      ),
                    ),
                  );
                },
              ),
            ),
            
            // Message Input
            Container(
              padding: EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: Colors.black54,
                boxShadow: [
                  BoxShadow(
                    color: Colors.black26,
                    blurRadius: 4,
                    offset: Offset(0, -2),
                  ),
                ],
              ),
              child: Column(
                children: [
                  Row(
                    children: [
                      // Attachment Button (Gallery/Camera)
                      IconButton(
                        icon: Icon(Icons.attach_file, color: Colors.grey),
                        onPressed: () {
                          _showAttachmentOptions(context);
                        },
                      ),
                      Expanded(
                        child: TextField(
                          controller: messageController,
                          style: TextStyle(color: Colors.white),
                          decoration: InputDecoration(
                            hintText: 'Type a message...',
                            hintStyle: TextStyle(color: Colors.grey),
                            border: OutlineInputBorder(
                              borderRadius: BorderRadius.circular(25),
                              borderSide: BorderSide.none,
                            ),
                            filled: true,
                            fillColor: Colors.grey[800],
                            contentPadding: EdgeInsets.symmetric(
                              horizontal: 16,
                              vertical: 8,
                            ),
                          ),
                        ),
                      ),
                      SizedBox(width: 8),
                      CircleAvatar(
                        backgroundColor: Colors.blueAccent,
                        child: IconButton(
                          icon: Icon(Icons.send, color: Colors.white),
                          onPressed: () async {
                            if (messageController.text.isNotEmpty) {
                              final messageText = messageController.text;
                              final timestamp = DateTime.now().toString().substring(11, 16);
                              
                              // Add to local list immediately (optimistic UI)
                              setState(() {
                                messages.add({
                                  'text': messageText,
                                  'isSent': true,
                                  'time': timestamp,
                                  'type': 'text',
                                });
                              });
                              messageController.clear();
                              
                              // Send to backend
                              await _sendMessage(messageText);
                            }
                          },
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
  
  void _showAttachmentOptions(BuildContext context) {
    showModalBottomSheet(
      context: context,
      backgroundColor: Color(0xff1e293b),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (context) => Container(
        padding: EdgeInsets.all(20),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(
              'Choose Attachment',
              style: TextStyle(
                color: Colors.white,
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
            SizedBox(height: 20),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                // Gallery Option
                _buildAttachmentOption(
                  Icons.photo_library,
                  'Gallery',
                  Colors.purple,
                  () async {
                    Navigator.pop(context);
                    try {
                      final XFile? image = await _imagePicker.pickImage(
                        source: ImageSource.gallery,
                        maxWidth: 1024,
                        maxHeight: 1024,
                      );
                      if (image != null) {
                        setState(() {
                          messages.add({
                            'text': 'Photo sent',
                            'isSent': true,
                            'time': DateTime.now().toString().substring(11, 16),
                            'type': 'image',
                            'imagePath': image.path,
                          });
                        });
                      }
                    } catch (e) {
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(content: Text('Error picking image: $e')),
                      );
                    }
                  },
                ),
                // Camera Option
                _buildAttachmentOption(
                  Icons.camera_alt,
                  'Camera',
                  Colors.blue,
                  () async {
                    Navigator.pop(context);
                    try {
                      final XFile? image = await _imagePicker.pickImage(
                        source: ImageSource.camera,
                        maxWidth: 1024,
                        maxHeight: 1024,
                      );
                      if (image != null) {
                        setState(() {
                          messages.add({
                            'text': 'Photo captured',
                            'isSent': true,
                            'time': DateTime.now().toString().substring(11, 16),
                            'type': 'image',
                            'imagePath': image.path,
                          });
                        });
                      }
                    } catch (e) {
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(content: Text('Error taking photo: $e')),
                      );
                    }
                  },
                ),
                // Document Option
                _buildAttachmentOption(
                  Icons.description,
                  'Document',
                  Colors.orange,
                  () async {
                    Navigator.pop(context);
                    try {
                      FilePickerResult? result = await FilePicker.platform.pickFiles(
                        type: FileType.custom,
                        allowedExtensions: ['pdf', 'doc', 'docx', 'txt', 'xls', 'xlsx'],
                      );
                      if (result != null && result.files.isNotEmpty) {
                        final file = result.files.first;
                        setState(() {
                          messages.add({
                            'text': '📄 ${file.name}',
                            'isSent': true,
                            'time': DateTime.now().toString().substring(11, 16),
                            'type': 'document',
                            'fileName': file.name,
                          });
                        });
                      }
                    } catch (e) {
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(content: Text('Error picking file: $e')),
                      );
                    }
                  },
                ),
              ],
            ),
            SizedBox(height: 20),
          ],
        ),
      ),
    );
  }
  
  Widget _buildAttachmentOption(IconData icon, String label, Color color, VoidCallback onTap) {
    return GestureDetector(
      onTap: onTap,
      child: Column(
        children: [
          CircleAvatar(
            radius: 30,
            backgroundColor: color.withOpacity(0.2),
            child: Icon(icon, color: color, size: 30),
          ),
          SizedBox(height: 8),
          Text(label, style: TextStyle(color: Colors.grey)),
        ],
      ),
    );
  }
  
  void _showBlockDialog() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        backgroundColor: Color(0xff1e293b),
        title: Text(
          'Block User',
          style: TextStyle(color: Colors.white),
        ),
        content: Text(
          'Are you sure you want to block ${widget.receiverName}? You won\'t receive messages from them anymore.',
          style: TextStyle(color: Colors.grey[300]),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: Text('Cancel', style: TextStyle(color: Colors.grey)),
          ),
          ElevatedButton(
            onPressed: () async {
              // TODO: Call block API
              // final response = await http.post(
              //   Uri.parse('http://YOUR_SERVER_IP:8000/api/chat/v3/block/${widget.receiverId}'),
              //   queryParameters: {'blocker_id': widget.tenantId},
              // );
              
              Navigator.pop(context);
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(
                  content: Text('${widget.receiverName} has been blocked'),
                  backgroundColor: Colors.red,
                ),
              );
              Navigator.pop(context); // Go back to tenant list
            },
            style: ElevatedButton.styleFrom(backgroundColor: Colors.red),
            child: Text('Block'),
          ),
        ],
      ),
    );
  }
}
