import 'package:flutter/material.dart';
import 'package:web_socket_channel/web_socket_channel.dart';
import 'dart:convert';
import 'group_call_screen.dart';

class GroupChatScreen extends StatefulWidget {
  final String tenantId;
  final String groupId;
  final String groupName;
  
  const GroupChatScreen({
    Key? key, 
    required this.tenantId, 
    required this.groupId,
    required this.groupName,
  }) : super(key: key);

  @override
  _GroupChatScreenState createState() => _GroupChatScreenState();
}

class _GroupChatScreenState extends State<GroupChatScreen> {
  final TextEditingController _messageController = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  final List<Map<String, dynamic>> _messages = [];
  bool _isLoading = false;
  WebSocketChannel? _channel;
  String _serverIp = '192.168.43.219';

  @override
  void initState() {
    super.initState();
    _connectToGroupChat();
    _loadGroupMessages();
  }

  void _connectToGroupChat() {
    final wsUrl = 'ws://$_serverIp:8000/api/groups/ws/${widget.tenantId}';
    
    _channel = WebSocketChannel.connect(Uri.parse(wsUrl));
    
    _channel!.stream.listen(
      (message) {
        final data = json.decode(message);
        _handleWebSocketMessage(data);
      },
      onError: (error) {
        print('WebSocket error: $error');
      },
      onDone: () {
        print('WebSocket connection closed');
      },
    );
  }

  void _handleWebSocketMessage(Map<String, dynamic> data) {
    final action = data['action'];
    
    if (action == 'group_message') {
      setState(() {
        _messages.add({
          'id': data['message']['id'],
          'sender_id': data['sender_id'],
          'text': data['message']['text'],
          'message_type': data['message']['message_type'],
          'timestamp': data['message']['timestamp'],
          'is_mine': data['sender_id'].toString() == widget.tenantId,
        });
      });
      
      _scrollToBottom();
    }
  }

  Future<void> _loadGroupMessages() async {
    // TODO: Load historical messages from API
    setState(() {
      _isLoading = false;
    });
  }

  void _sendMessage() {
    if (_messageController.text.trim().isEmpty) return;
    
    final messageText = _messageController.text.trim();
    
    // Send via WebSocket
    _channel?.sink.add(json.encode({
      'action': 'send_group_message',
      'room_id': int.parse(widget.groupId),
      'text': messageText,
      'message_type': 'text',
    }));
    
    // Add to local list optimistically
    setState(() {
      _messages.add({
        'id': DateTime.now().millisecondsSinceEpoch,
        'sender_id': int.parse(widget.tenantId),
        'text': messageText,
        'message_type': 'text',
        'timestamp': DateTime.now().toIso8601String(),
        'is_mine': true,
      });
    });
    
    _messageController.clear();
    _scrollToBottom();
  }

  void _scrollToBottom() {
    Future.delayed(Duration(milliseconds: 100), () {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  @override
  void dispose() {
    _channel?.sink.close();
    _messageController.dispose();
    _scrollController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              widget.groupName,
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
            Text(
              'Group Chat',
              style: TextStyle(
                fontSize: 12,
                color: Colors.white70,
              ),
            ),
          ],
        ),
        backgroundColor: Colors.blueAccent,
        elevation: 0,
        actions: [
          IconButton(
            icon: Icon(Icons.call),
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => GroupCallScreen(
                    tenantId: widget.tenantId,
                    groupId: widget.groupId,
                    groupName: widget.groupName,
                    isVideoCall: false,
                  ),
                ),
              );
            },
          ),
          IconButton(
            icon: Icon(Icons.videocam),
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => GroupCallScreen(
                    tenantId: widget.tenantId,
                    groupId: widget.groupId,
                    groupName: widget.groupName,
                    isVideoCall: true,
                  ),
                ),
              );
            },
          ),
          IconButton(
            icon: Icon(Icons.info_outline),
            onPressed: () {
              // TODO: Navigate to group info
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(content: Text('Group Info coming soon')),
              );
            },
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
              child: _isLoading
                  ? Center(child: CircularProgressIndicator(color: Colors.blueAccent))
                  : _messages.isEmpty
                      ? Center(
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Icon(
                                Icons.group_outlined,
                                size: 80,
                                color: Colors.grey[600],
                              ),
                              SizedBox(height: 16),
                              Text(
                                'No messages yet',
                                style: TextStyle(
                                  color: Colors.grey[500],
                                  fontSize: 18,
                                ),
                              ),
                              SizedBox(height: 8),
                              Text(
                                'Start the conversation!',
                                style: TextStyle(
                                  color: Colors.grey[600],
                                  fontSize: 14,
                                ),
                              ),
                            ],
                          ),
                        )
                      : ListView.builder(
                          controller: _scrollController,
                          padding: EdgeInsets.all(16),
                          itemCount: _messages.length,
                          itemBuilder: (context, index) {
                            final message = _messages[index];
                            return _buildMessageBubble(message);
                          },
                        ),
            ),

            // Message Input
            Container(
              padding: EdgeInsets.all(8),
              decoration: BoxDecoration(
                color: Colors.black54,
                boxShadow: [
                  BoxShadow(
                    color: Colors.black26,
                    blurRadius: 10,
                    offset: Offset(0, -2),
                  ),
                ],
              ),
              child: Row(
                children: [
                  Expanded(
                    child: TextField(
                      controller: _messageController,
                      style: TextStyle(color: Colors.white),
                      decoration: InputDecoration(
                        hintText: 'Type a message...',
                        hintStyle: TextStyle(color: Colors.grey),
                        border: InputBorder.none,
                        contentPadding: EdgeInsets.symmetric(
                          horizontal: 16,
                          vertical: 12,
                        ),
                      ),
                      onSubmitted: (_) => _sendMessage(),
                    ),
                  ),
                  SizedBox(width: 8),
                  CircleAvatar(
                    backgroundColor: Colors.blueAccent,
                    child: IconButton(
                      icon: Icon(Icons.send, color: Colors.white),
                      onPressed: _sendMessage,
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildMessageBubble(Map<String, dynamic> message) {
    final isMine = message['is_mine'] as bool;
    
    return Align(
      alignment: isMine ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        constraints: BoxConstraints(
          maxWidth: MediaQuery.of(context).size.width * 0.75,
        ),
        margin: EdgeInsets.only(bottom: 8),
        padding: EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: isMine ? Colors.blueAccent : Colors.grey[800],
          borderRadius: BorderRadius.only(
            topLeft: Radius.circular(12),
            topRight: Radius.circular(12),
            bottomLeft: Radius.circular(isMine ? 12 : 4),
            bottomRight: Radius.circular(isMine ? 4 : 12),
          ),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            if (!isMine)
              Padding(
                padding: EdgeInsets.only(bottom: 4),
                child: Text(
                  'User ${message['sender_id']}',
                  style: TextStyle(
                    color: Colors.blueAccent,
                    fontSize: 12,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            Text(
              message['text'],
              style: TextStyle(color: Colors.white),
            ),
            SizedBox(height: 4),
            Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Text(
                  _formatTime(message['timestamp']),
                  style: TextStyle(
                    color: Colors.white54,
                    fontSize: 11,
                  ),
                ),
                if (isMine) ...[
                  SizedBox(width: 4),
                  Icon(
                    Icons.done_all,
                    size: 14,
                    color: Colors.white54,
                  ),
                ],
              ],
            ),
          ],
        ),
      ),
    );
  }

  String _formatTime(String timestamp) {
    try {
      final dateTime = DateTime.parse(timestamp);
      return '${dateTime.hour.toString().padLeft(2, '0')}:${dateTime.minute.toString().padLeft(2, '0')}';
    } catch (e) {
      return '';
    }
  }
}
