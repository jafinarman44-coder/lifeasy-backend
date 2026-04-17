import 'package:flutter/material.dart';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:image_picker/image_picker.dart';
import 'package:file_picker/file_picker.dart';
import '../services/chat_socket_manager.dart';
import 'voice_call_screen.dart';
import 'video_call_screen.dart';

class WhatsAppStyleChatScreen extends StatefulWidget {
  final String tenantId;
  final String? receiverId;
  final String? receiverName;

  WhatsAppStyleChatScreen({
    required this.tenantId,
    this.receiverId,
    this.receiverName,
  });

  @override
  _WhatsAppStyleChatScreenState createState() => _WhatsAppStyleChatScreenState();
}

class _WhatsAppStyleChatScreenState extends State<WhatsAppStyleChatScreen> {
  final TextEditingController _messageController = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  final ImagePicker _imagePicker = ImagePicker();
  List<Map<String, dynamic>> _messages = [];
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
    _messageController.dispose();
    _scrollController.dispose();
    super.dispose();
  }

  Future<void> _initializeRealtimeChat() async {
    try {
      await _chatSocket.connect(
        widget.tenantId,
        receiverId: widget.receiverId,
        serverIp: 'lifeasy-api.onrender.com',
      );

      _chatSocket.onMessageReceived = (messageData) {
        if (mounted) {
          setState(() {
            _messages.add({
              'text': messageData['text'] ?? messageData['message'] ?? '',
              'isSent': false,
              'time': _extractTimeFromTimestamp(messageData['timestamp'] ?? DateTime.now().toIso8601String()),
              'type': messageData['message_type'] ?? messageData['type'] ?? 'text',
              'imagePath': messageData['media_url'],
            });
          });
          _scrollToBottom();
        }
      };

      _chatSocket.onConnected = () {
        if (mounted) {
          setState(() => _isConnected = true);
        }
      };

      _chatSocket.onDisconnected = (reason) {
        if (mounted) {
          setState(() => _isConnected = false);
        }
      };
    } catch (e) {
      print('Chat initialization error: $e');
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

  void _scrollToBottom() {
    if (_scrollController.hasClients) {
      _scrollController.animateTo(
        _scrollController.position.maxScrollExtent,
        duration: Duration(milliseconds: 300),
        curve: Curves.easeOut,
      );
    }
  }

  Future<void> _sendMessage(String text) async {
    if (text.trim().isEmpty) return;

    setState(() {
      _messages.add({
        'text': text,
        'isSent': true,
        'time': DateTime.now().toString().substring(11, 16),
        'type': 'text',
      });
    });

    _messageController.clear();
    _scrollToBottom();

    try {
      if (_chatSocket.isConnected) {
        _chatSocket.sendMessage(
          text,
          receiverId: widget.receiverId,
          messageType: 'text',
        );
      }

      final url = Uri.parse('https://lifeasy-api.onrender.com/api/chat/v3/send');
      final response = await http.post(
        url,
        body: {
          'sender_id': widget.tenantId,
          'receiver_id': widget.receiverId ?? '0',
          'message': text,
          'message_type': 'text',
        },
      );
      
      if (response.statusCode != 200) {
        print('Warning: Failed to save message to database');
      }
    } catch (e) {
      print('Error sending message: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Color(0xFF0B141A),
      appBar: _buildAppBar(),
      body: Column(
        children: [
          Expanded(
            child: _buildChatBackground(),
          ),
          _buildMessageInput(),
        ],
      ),
    );
  }

  PreferredSizeWidget _buildAppBar() {
    return AppBar(
      backgroundColor: Color(0xFF1F2C34),
      elevation: 0,
      leading: IconButton(
        icon: Icon(Icons.arrow_back, color: Colors.white),
        onPressed: () => Navigator.pop(context),
      ),
      title: Row(
        children: [
          Container(
            width: 40,
            height: 40,
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              gradient: LinearGradient(
                colors: [Color(0xFF25D366), Color(0xFF128C7E)],
              ),
            ),
            child: Center(
              child: Text(
                widget.receiverName?.substring(0, 1).toUpperCase() ?? 'U',
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
          ),
          SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  widget.receiverName ?? 'Building App',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 17,
                    fontWeight: FontWeight.w600,
                  ),
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                ),
                Text(
                  _isConnected ? 'online' : 'offline',
                  style: TextStyle(
                    color: _isConnected ? Color(0xFF25D366) : Colors.white54,
                    fontSize: 12,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
      actions: [
        IconButton(
          icon: Icon(Icons.videocam, color: Colors.white),
          onPressed: () {
            if (widget.receiverId != null) {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (_) => VideoCallScreen(
                    tenantId: widget.tenantId,
                    channelName: 'video_${widget.tenantId}_${widget.receiverId}',
                    receiverId: widget.receiverId!,
                  ),
                ),
              );
            }
          },
        ),
        IconButton(
          icon: Icon(Icons.call, color: Colors.white),
          onPressed: () {
            if (widget.receiverId != null) {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (_) => VoiceCallScreen(
                    tenantId: widget.tenantId,
                    channelName: 'voice_${widget.tenantId}_${widget.receiverId}',
                    receiverId: widget.receiverId!,
                  ),
                ),
              );
            }
          },
        ),
        PopupMenuButton<String>(
          icon: Icon(Icons.more_vert, color: Colors.white),
          color: Color(0xFF2A3942),
          onSelected: (value) {},
          itemBuilder: (context) => [
            PopupMenuItem(
              value: 'view_contact',
              child: Text('View contact', style: TextStyle(color: Colors.white)),
            ),
            PopupMenuItem(
              value: 'media',
              child: Text('Media, links, and docs', style: TextStyle(color: Colors.white)),
            ),
            PopupMenuItem(
              value: 'search',
              child: Text('Search', style: TextStyle(color: Colors.white)),
            ),
            PopupMenuItem(
              value: 'mute',
              child: Text('Mute notifications', style: TextStyle(color: Colors.white)),
            ),
            PopupMenuItem(
              value: 'wallpaper',
              child: Text('Wallpaper', style: TextStyle(color: Colors.white)),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildChatBackground() {
    return Container(
      decoration: BoxDecoration(
        color: Color(0xFF0B141A),
      ),
      child: _messages.isEmpty
          ? _buildEmptyState()
          : ListView.builder(
              controller: _scrollController,
              padding: EdgeInsets.symmetric(horizontal: 8, vertical: 16),
              itemCount: _messages.length,
              itemBuilder: (context, index) {
                final message = _messages[index];
                final showTail = index == 0 || 
                    _messages[index - 1]['isSent'] != message['isSent'];
                
                return AnimatedContainer(
                  duration: Duration(milliseconds: 300),
                  curve: Curves.easeOut,
                  child: _buildMessageBubble(message, showTail),
                );
              },
            ),
    );
  }

  Widget _buildEmptyState() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Container(
            width: 120,
            height: 120,
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              gradient: LinearGradient(
                colors: [
                  Color(0xFF25D366).withOpacity(0.2),
                  Color(0xFF128C7E).withOpacity(0.2),
                ],
              ),
            ),
            child: Icon(
              Icons.chat_bubble_outline,
              size: 60,
              color: Color(0xFF25D366),
            ),
          ),
          SizedBox(height: 24),
          Text(
            'Start a conversation',
            style: TextStyle(
              color: Colors.white70,
              fontSize: 20,
              fontWeight: FontWeight.w500,
            ),
          ),
          SizedBox(height: 8),
          Text(
            'Send messages, photos, and documents',
            style: TextStyle(
              color: Colors.white54,
              fontSize: 14,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildMessageBubble(Map<String, dynamic> message, bool showTail) {
    final isSent = message['isSent'] as bool;
    final messageType = message['type'] ?? 'text';

    return Padding(
      padding: EdgeInsets.only(bottom: 2),
      child: Row(
        mainAxisAlignment: isSent ? MainAxisAlignment.end : MainAxisAlignment.start,
        children: [
          Container(
            constraints: BoxConstraints(maxWidth: 280),
            margin: EdgeInsets.symmetric(horizontal: 8),
            child: Stack(
              children: [
                Container(
                  decoration: BoxDecoration(
                    color: isSent ? Color(0xFF005C4B) : Color(0xFF1F2C34),
                    borderRadius: BorderRadius.only(
                      topLeft: Radius.circular(showTail && !isSent ? 0 : 8),
                      topRight: Radius.circular(showTail && isSent ? 0 : 8),
                      bottomLeft: Radius.circular(8),
                      bottomRight: Radius.circular(8),
                    ),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black12,
                        blurRadius: 2,
                        offset: Offset(0, 1),
                      ),
                    ],
                  ),
                  padding: EdgeInsets.fromLTRB(
                    showTail && !isSent ? 8 : 12,
                    6,
                    12,
                    6,
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      if (messageType == 'image' && message['imagePath'] != null)
                        ClipRRect(
                          borderRadius: BorderRadius.circular(8),
                          child: Image.file(
                            File(message['imagePath']),
                            width: 220,
                            fit: BoxFit.cover,
                          ),
                        ),
                      if (messageType == 'text' || messageType == null)
                        Text(
                          message['text'],
                          style: TextStyle(
                            color: Colors.white,
                            fontSize: 14.5,
                            height: 1.3,
                          ),
                        ),
                      SizedBox(height: 2),
                      Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Text(
                            message['time'],
                            style: TextStyle(
                              color: Colors.white54,
                              fontSize: 11,
                            ),
                          ),
                          if (isSent) ...[
                            SizedBox(width: 4),
                            Icon(
                              Icons.done_all,
                              size: 14,
                              color: Colors.blue,
                            ),
                          ],
                        ],
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildMessageInput() {
    return Container(
      padding: EdgeInsets.symmetric(horizontal: 8, vertical: 8),
      decoration: BoxDecoration(
        color: Color(0xFF1F2C34),
        boxShadow: [
          BoxShadow(
            color: Colors.black26,
            blurRadius: 8,
            offset: Offset(0, -2),
          ),
        ],
      ),
      child: SafeArea(
        child: Row(
          children: [
            Expanded(
              child: Container(
                decoration: BoxDecoration(
                  color: Color(0xFF2A3942),
                  borderRadius: BorderRadius.circular(24),
                ),
                padding: EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                child: Row(
                  children: [
                    Icon(Icons.emoji_emotions_outlined, color: Colors.white54, size: 24),
                    SizedBox(width: 8),
                    Expanded(
                      child: TextField(
                        controller: _messageController,
                        style: TextStyle(color: Colors.white, fontSize: 15),
                        decoration: InputDecoration(
                          hintText: 'Message',
                          hintStyle: TextStyle(color: Colors.white54, fontSize: 15),
                          border: InputBorder.none,
                          contentPadding: EdgeInsets.symmetric(vertical: 8),
                        ),
                        maxLines: 5,
                        minLines: 1,
                      ),
                    ),
                    SizedBox(width: 8),
                    IconButton(
                      icon: Icon(Icons.attach_file, color: Colors.white54, size: 24),
                      onPressed: () => _showAttachmentOptions(),
                      padding: EdgeInsets.zero,
                      constraints: BoxConstraints(),
                    ),
                    SizedBox(width: 8),
                    IconButton(
                      icon: Icon(Icons.camera_alt_outlined, color: Colors.white54, size: 24),
                      onPressed: () => _openCamera(),
                      padding: EdgeInsets.zero,
                      constraints: BoxConstraints(),
                    ),
                  ],
                ),
              ),
            ),
            SizedBox(width: 8),
            Container(
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                gradient: LinearGradient(
                  colors: [Color(0xFF25D366), Color(0xFF128C7E)],
                ),
              ),
              child: IconButton(
                icon: Icon(
                  _messageController.text.isEmpty ? Icons.mic : Icons.send,
                  color: Colors.white,
                ),
                onPressed: () {
                  if (_messageController.text.isEmpty) {
                    // Voice recording - future enhancement
                    print('Voice recording - future enhancement');
                  } else {
                    _sendMessage(_messageController.text);
                  }
                },
                padding: EdgeInsets.all(12),
              ),
            ),
          ],
        ),
      ),
    );
  }

  // REAL attachment handlers
  void _showAttachmentOptions() {
    showModalBottomSheet(
      context: context,
      backgroundColor: Color(0xFF1F2C34),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (context) => SafeArea(
        child: Container(
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
                  _buildAttachmentOption(
                    Icons.insert_drive_file,
                    'Document',
                    Colors.orange,
                    () => _openDocumentPicker(),
                  ),
                  _buildAttachmentOption(
                    Icons.person,
                    'Contact',
                    Colors.blue,
                    () => Navigator.pop(context),
                  ),
                  _buildAttachmentOption(
                    Icons.location_on,
                    'Location',
                    Colors.green,
                    () => Navigator.pop(context),
                  ),
                ],
              ),
              SizedBox(height: 16),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  _buildAttachmentOption(
                    Icons.photo_library,
                    'Gallery',
                    Colors.purple,
                    () => _openGallery(),
                  ),
                  _buildAttachmentOption(
                    Icons.camera_alt,
                    'Camera',
                    Colors.teal,
                    () => _openCamera(),
                  ),
                  _buildAttachmentOption(
                    Icons.music_note,
                    'Audio',
                    Colors.pink,
                    () => Navigator.pop(context),
                  ),
                ],
              ),
              SizedBox(height: 10),
            ],
          ),
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
            radius: 28,
            backgroundColor: color.withOpacity(0.2),
            child: Icon(icon, color: color, size: 28),
          ),
          SizedBox(height: 6),
          Text(
            label,
            style: TextStyle(color: Colors.white70, fontSize: 12),
          ),
        ],
      ),
    );
  }

  // REAL camera integration
  Future<void> _openCamera() async {
    try {
      Navigator.pop(context); // Close attachment menu if open
      final XFile? image = await _imagePicker.pickImage(
        source: ImageSource.camera,
        maxWidth: 1920,
        maxHeight: 1080,
        imageQuality: 85,
      );
      
      if (image != null) {
        setState(() {
          _messages.add({
            'text': '📷 Photo',
            'isSent': true,
            'time': DateTime.now().toString().substring(11, 16),
            'type': 'image',
            'imagePath': image.path,
          });
        });
        _scrollToBottom();
        // TODO: Upload image to server
        print('Image captured: ${image.path}');
      }
    } catch (e) {
      print('Error opening camera: $e');
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Could not open camera'), backgroundColor: Colors.red),
      );
    }
  }

  // REAL gallery integration
  Future<void> _openGallery() async {
    try {
      Navigator.pop(context); // Close attachment menu
      final XFile? image = await _imagePicker.pickImage(
        source: ImageSource.gallery,
        maxWidth: 1920,
        maxHeight: 1080,
        imageQuality: 85,
      );
      
      if (image != null) {
        setState(() {
          _messages.add({
            'text': '📷 Photo',
            'isSent': true,
            'time': DateTime.now().toString().substring(11, 16),
            'type': 'image',
            'imagePath': image.path,
          });
        });
        _scrollToBottom();
        // TODO: Upload image to server
        print('Image selected: ${image.path}');
      }
    } catch (e) {
      print('Error picking image: $e');
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Could not open gallery'), backgroundColor: Colors.red),
      );
    }
  }

  // REAL document picker integration
  Future<void> _openDocumentPicker() async {
    try {
      Navigator.pop(context); // Close attachment menu
      FilePickerResult? result = await FilePicker.platform.pickFiles(
        type: FileType.custom,
        allowedExtensions: ['pdf', 'doc', 'docx', 'txt', 'xls', 'xlsx', 'ppt', 'pptx'],
      );
      
      if (result != null && result.files.isNotEmpty) {
        final file = result.files.first;
        setState(() {
          _messages.add({
            'text': '📄 ${file.name}',
            'isSent': true,
            'time': DateTime.now().toString().substring(11, 16),
            'type': 'document',
            'fileName': file.name,
          });
        });
        _scrollToBottom();
        // TODO: Upload document to server
        print('Document selected: ${file.name}');
      }
    } catch (e) {
      print('Error picking document: $e');
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Could not open file picker'), backgroundColor: Colors.red),
      );
    }
  }
}
