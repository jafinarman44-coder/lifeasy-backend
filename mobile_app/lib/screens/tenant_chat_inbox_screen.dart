import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'chat_screen.dart';

class TenantChatInboxScreen extends StatefulWidget {
  final String tenantId;
  
  const TenantChatInboxScreen({Key? key, required this.tenantId}) : super(key: key);

  @override
  _TenantChatInboxScreenState createState() => _TenantChatInboxScreenState();
}

class _TenantChatInboxScreenState extends State<TenantChatInboxScreen> {
  final TextEditingController _searchController = TextEditingController();
  List<ChatConversation> _conversations = [];
  List<ChatConversation> _filteredConversations = [];
  bool _isLoading = true;
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    _fetchConversations();
  }

  Future<void> _fetchConversations() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      // TODO: Replace with actual API endpoint
      // final url = Uri.parse('http://YOUR_SERVER_IP:8000/api/chat/v3/conversations/${widget.tenantId}');
      // final response = await http.get(url);
      
      // Mock data for now
      await Future.delayed(Duration(seconds: 1));
      setState(() {
        _conversations = [
          ChatConversation(
            userId: '2',
            userName: 'John Doe',
            userAvatar: 'JD',
            lastMessage: 'Hey! How are you doing?',
            lastMessageTime: DateTime.now().subtract(Duration(minutes: 5)),
            unreadCount: 2,
            isOnline: true,
            isTenant: true,
          ),
          ChatConversation(
            userId: '3',
            userName: 'Jane Smith',
            userAvatar: 'JS',
            lastMessage: 'Thanks for the update!',
            lastMessageTime: DateTime.now().subtract(Duration(hours: 1)),
            unreadCount: 0,
            isOnline: true,
            isTenant: true,
          ),
          ChatConversation(
            userId: '1',
            userName: 'Building Manager',
            userAvatar: 'BM',
            lastMessage: 'Your rent is due next week',
            lastMessageTime: DateTime.now().subtract(Duration(days: 1)),
            unreadCount: 1,
            isOnline: false,
            isTenant: false,
          ),
        ];
        _filteredConversations = _conversations;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _errorMessage = 'Error: $e';
        _isLoading = false;
      });
    }
  }

  void _filterConversations(String query) {
    setState(() {
      if (query.isEmpty) {
        _filteredConversations = _conversations;
      } else {
        _filteredConversations = _conversations.where((conv) {
          return conv.userName.toLowerCase().contains(query.toLowerCase());
        }).toList();
      }
    });
  }

  String _formatTimestamp(DateTime timestamp) {
    final now = DateTime.now();
    final difference = now.difference(timestamp);

    if (difference.inMinutes < 1) {
      return 'Just now';
    } else if (difference.inMinutes < 60) {
      return '${difference.inMinutes}m';
    } else if (difference.inHours < 24) {
      return '${difference.inHours}h';
    } else if (difference.inDays < 7) {
      return '${difference.inDays}d';
    } else {
      return '${timestamp.day}/${timestamp.month}';
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Messages'),
        backgroundColor: Colors.blueAccent,
        elevation: 0,
        actions: [
          IconButton(
            icon: Icon(Icons.refresh),
            onPressed: _fetchConversations,
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
            // Search Bar
            Padding(
              padding: EdgeInsets.all(16),
              child: TextField(
                controller: _searchController,
                style: TextStyle(color: Colors.white),
                decoration: InputDecoration(
                  hintText: 'Search conversations...',
                  hintStyle: TextStyle(color: Colors.grey),
                  prefixIcon: Icon(Icons.search, color: Colors.grey),
                  suffixIcon: _searchController.text.isNotEmpty
                      ? IconButton(
                          icon: Icon(Icons.clear, color: Colors.grey),
                          onPressed: () {
                            _searchController.clear();
                            _filterConversations('');
                          },
                        )
                      : null,
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(12),
                    borderSide: BorderSide.none,
                  ),
                  filled: true,
                  fillColor: Colors.grey[800],
                  contentPadding: EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                ),
                onChanged: _filterConversations,
              ),
            ),

            // Conversations List
            Expanded(
              child: _isLoading
                  ? Center(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          CircularProgressIndicator(color: Colors.blueAccent),
                          SizedBox(height: 16),
                          Text(
                            'Loading conversations...',
                            style: TextStyle(color: Colors.grey, fontSize: 16),
                          ),
                        ],
                      ),
                    )
                  : _errorMessage != null
                      ? Center(
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Icon(Icons.error_outline, color: Colors.red, size: 60),
                              SizedBox(height: 16),
                              Text(
                                _errorMessage!,
                                style: TextStyle(color: Colors.red, fontSize: 16),
                                textAlign: TextAlign.center,
                              ),
                              SizedBox(height: 16),
                              ElevatedButton(
                                onPressed: _fetchConversations,
                                child: Text('Retry'),
                              ),
                            ],
                          ),
                        )
                      : _filteredConversations.isEmpty
                          ? Center(
                              child: Column(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                  Icon(Icons.chat_bubble_outline, color: Colors.grey, size: 60),
                                  SizedBox(height: 16),
                                  Text(
                                    'No conversations yet',
                                    style: TextStyle(color: Colors.grey, fontSize: 16),
                                  ),
                                  SizedBox(height: 8),
                                  Text(
                                    'Start chatting with other tenants',
                                    style: TextStyle(color: Colors.grey, fontSize: 14),
                                  ),
                                ],
                              ),
                            )
                          : RefreshIndicator(
                              onRefresh: _fetchConversations,
                              child: ListView.builder(
                                padding: EdgeInsets.symmetric(horizontal: 16),
                                itemCount: _filteredConversations.length,
                                itemBuilder: (context, index) {
                                  final conversation = _filteredConversations[index];
                                  return _buildConversationTile(conversation);
                                },
                              ),
                            ),
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          // TODO: Navigate to tenant list to start new chat
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Tenant list coming soon!')),
          );
        },
        backgroundColor: Colors.blueAccent,
        child: Icon(Icons.add_comment),
      ),
    );
  }

  Widget _buildConversationTile(ChatConversation conv) {
    return Card(
      color: Colors.black54,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
      ),
      margin: EdgeInsets.only(bottom: 8),
      child: ListTile(
        leading: Stack(
          children: [
            CircleAvatar(
              radius: 28,
              backgroundColor: conv.isTenant
                  ? Colors.orange.withOpacity(0.2)
                  : Colors.blueAccent.withOpacity(0.2),
              child: Text(
                conv.userAvatar,
                style: TextStyle(
                  color: conv.isTenant ? Colors.orange : Colors.blueAccent,
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
            // Online status indicator
            if (conv.isOnline)
              Positioned(
                right: 0,
                bottom: 0,
                child: Container(
                  width: 14,
                  height: 14,
                  decoration: BoxDecoration(
                    color: Colors.green,
                    shape: BoxShape.circle,
                    border: Border.all(color: Colors.white, width: 2),
                  ),
                ),
              ),
          ],
        ),
        title: Text(
          conv.userName,
          style: TextStyle(
            color: Colors.white,
            fontWeight: FontWeight.bold,
            fontSize: 16,
          ),
        ),
        subtitle: Text(
          conv.lastMessage,
          style: TextStyle(
            color: Colors.grey,
            fontSize: 14,
          ),
          maxLines: 1,
          overflow: TextOverflow.ellipsis,
        ),
        trailing: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.end,
          children: [
            Text(
              _formatTimestamp(conv.lastMessageTime),
              style: TextStyle(
                color: Colors.grey,
                fontSize: 12,
              ),
            ),
            if (conv.unreadCount > 0)
              Padding(
                padding: EdgeInsets.only(top: 4),
                child: Container(
                  padding: EdgeInsets.all(6),
                  decoration: BoxDecoration(
                    color: Colors.blueAccent,
                    shape: BoxShape.circle,
                  ),
                  constraints: BoxConstraints(
                    minWidth: 20,
                    minHeight: 20,
                  ),
                  child: Center(
                    child: Text(
                      conv.unreadCount.toString(),
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 10,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                ),
              ),
          ],
        ),
        onTap: () {
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (_) => ChatScreen(
                tenantId: widget.tenantId,
                receiverId: conv.userId,
                receiverName: conv.userName,
              ),
            ),
          );
        },
      ),
    );
  }

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }
}

class ChatConversation {
  final String userId;
  final String userName;
  final String userAvatar;
  final String lastMessage;
  final DateTime lastMessageTime;
  final int unreadCount;
  final bool isOnline;
  final bool isTenant;

  ChatConversation({
    required this.userId,
    required this.userName,
    required this.userAvatar,
    required this.lastMessage,
    required this.lastMessageTime,
    required this.unreadCount,
    required this.isOnline,
    required this.isTenant,
  });
}
