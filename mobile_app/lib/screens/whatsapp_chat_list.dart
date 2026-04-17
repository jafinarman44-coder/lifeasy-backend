import 'package:flutter/material.dart';
import 'whatsapp_style_chat_screen.dart';

class WhatsAppStyleChatList extends StatefulWidget {
  final String tenantId;

  WhatsAppStyleChatList({required this.tenantId});

  @override
  _WhatsAppStyleChatListState createState() => _WhatsAppStyleChatListState();
}

class _WhatsAppStyleChatListState extends State<WhatsAppStyleChatList> with TickerProviderStateMixin {
  final TextEditingController _searchController = TextEditingController();
  bool _isSearching = false;
  late TabController _tabController;

  final List<Map<String, dynamic>> _chats = [
    {
      'id': '1',
      'name': 'Building Manager',
      'avatar': 'BM',
      'lastMessage': 'Your payment has been confirmed',
      'time': '10:30 AM',
      'unread': 2,
      'isOnline': true,
      'isPinned': true,
    },
    {
      'id': '2',
      'name': 'John Doe - Flat 301',
      'avatar': 'JD',
      'lastMessage': '📷 Photo',
      'time': '9:45 AM',
      'unread': 0,
      'isOnline': true,
      'isPinned': false,
    },
    {
      'id': '3',
      'name': 'Sarah - Flat 205',
      'avatar': 'SF',
      'lastMessage': 'Can we reschedule the meeting?',
      'time': 'Yesterday',
      'unread': 1,
      'isOnline': false,
      'isPinned': true,
    },
    {
      'id': '4',
      'name': 'Maintenance Team',
      'avatar': 'MT',
      'lastMessage': 'Water leakage has been fixed',
      'time': 'Yesterday',
      'unread': 0,
      'isOnline': false,
      'isPinned': false,
    },
    {
      'id': '5',
      'name': 'Emily - Flat 402',
      'avatar': 'EF',
      'lastMessage': 'Thanks for the update!',
      'time': 'Monday',
      'unread': 0,
      'isOnline': true,
      'isPinned': false,
    },
  ];

  List<Map<String, dynamic>> _filteredChats = [];

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 3, vsync: this);
    _filteredChats = List.from(_chats);
  }

  @override
  void dispose() {
    _tabController.dispose();
    _searchController.dispose();
    super.dispose();
  }

  void _filterChats(String query) {
    setState(() {
      if (query.isEmpty) {
        _filteredChats = List.from(_chats);
      } else {
        _filteredChats = _chats.where((chat) {
          return chat['name'].toString().toLowerCase().contains(query.toLowerCase()) ||
              chat['lastMessage'].toString().toLowerCase().contains(query.toLowerCase());
        }).toList();
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Color(0xFF0B141A),
      appBar: _buildAppBar(),
      body: Column(
        children: [
          TabBar(
            controller: _tabController,
            indicatorColor: Color(0xFF25D366),
            indicatorWeight: 3,
            labelColor: Color(0xFF25D366),
            unselectedLabelColor: Colors.white54,
            labelStyle: TextStyle(
              fontSize: 14,
              fontWeight: FontWeight.w600,
            ),
            tabs: [
              Tab(text: 'Pinned'),
              Tab(text: 'Chats'),
              Tab(text: 'Groups'),
            ],
          ),
          if (_isSearching) _buildSearchBar(),
          _buildStoriesRow(),
          Divider(height: 1, color: Color(0xFF1F2C34)),
          Expanded(
            child: _buildChatList(),
          ),
        ],
      ),
      floatingActionButton: _buildFAB(),
    );
  }

  PreferredSizeWidget _buildAppBar() {
    return AppBar(
      backgroundColor: Color(0xFF1F2C34),
      elevation: 0,
      title: Text(
        _isSearching ? 'Search' : 'Building App',
        style: TextStyle(
          color: Colors.white,
          fontSize: 22,
          fontWeight: FontWeight.w700,
        ),
      ),
      actions: [
        if (!_isSearching)
          IconButton(
            icon: Icon(Icons.search, color: Colors.white),
            onPressed: () {
              setState(() => _isSearching = true);
            },
          ),
        IconButton(
          icon: Icon(Icons.more_vert, color: Colors.white),
          onPressed: () {},
        ),
      ],
      bottom: PreferredSize(
        preferredSize: Size.fromHeight(48),
        child: Container(),
      ),
    );
  }

  Widget _buildSearchBar() {
    return Container(
      padding: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      color: Color(0xFF1F2C34),
      child: TextField(
        controller: _searchController,
        autofocus: true,
        style: TextStyle(color: Colors.white),
        decoration: InputDecoration(
          hintText: 'Search or start new chat',
          hintStyle: TextStyle(color: Colors.white54),
          prefixIcon: Icon(Icons.search, color: Colors.white54),
          suffixIcon: IconButton(
            icon: Icon(Icons.close, color: Colors.white54),
            onPressed: () {
              setState(() {
                _isSearching = false;
                _searchController.clear();
                _filteredChats = List.from(_chats);
              });
            },
          ),
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(24),
            borderSide: BorderSide.none,
          ),
          filled: true,
          fillColor: Color(0xFF2A3942),
          contentPadding: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        ),
        onChanged: _filterChats,
      ),
    );
  }

  Widget _buildStoriesRow() {
    return Container(
      height: 110,
      padding: EdgeInsets.symmetric(vertical: 12),
      child: ListView(
        scrollDirection: Axis.horizontal,
        padding: EdgeInsets.symmetric(horizontal: 12),
        children: [
          _buildStoryItem(
            avatar: '+',
            name: 'New Chat',
            isAdd: true,
          ),
          ..._chats.take(5).map((chat) => _buildStoryItem(
                avatar: chat['avatar'],
                name: chat['name'].toString().split(' ')[0],
                isOnline: chat['isOnline'],
                onTap: () => _openChat(chat),
              )),
        ],
      ),
    );
  }

  Widget _buildStoryItem({
    required String avatar,
    required String name,
    bool isOnline = false,
    bool isAdd = false,
    VoidCallback? onTap,
  }) {
    return GestureDetector(
      onTap: onTap,
      child: Padding(
        padding: EdgeInsets.symmetric(horizontal: 8),
        child: Column(
          children: [
            Stack(
              children: [
                Container(
                  padding: EdgeInsets.all(3),
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    gradient: LinearGradient(
                      colors: isOnline
                          ? [Color(0xFF25D366), Color(0xFF128C7E)]
                          : [Colors.grey, Colors.grey.shade600],
                    ),
                  ),
                  child: CircleAvatar(
                    radius: 28,
                    backgroundColor: Color(0xFF1F2C34),
                    child: isAdd
                        ? Icon(Icons.add, color: Color(0xFF25D366), size: 32)
                        : Text(
                            avatar,
                            style: TextStyle(
                              color: Colors.white,
                              fontSize: 20,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                  ),
                ),
                if (isOnline)
                  Positioned(
                    bottom: 2,
                    right: 2,
                    child: Container(
                      width: 14,
                      height: 14,
                      decoration: BoxDecoration(
                        color: Color(0xFF25D366),
                        shape: BoxShape.circle,
                        border: Border.all(
                          color: Color(0xFF0B141A),
                          width: 2,
                        ),
                      ),
                    ),
                  ),
              ],
            ),
            SizedBox(height: 6),
            Text(
              name,
              style: TextStyle(
                color: Colors.white,
                fontSize: 12,
              ),
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildChatList() {
    final pinnedChats = _filteredChats.where((c) => c['isPinned'] == true).toList();
    final allChats = _tabController.index == 0 ? pinnedChats : _filteredChats;

    if (allChats.isEmpty) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              Icons.chat_bubble_outline,
              size: 80,
              color: Colors.white24,
            ),
            SizedBox(height: 16),
            Text(
              'No chats yet',
              style: TextStyle(
                color: Colors.white54,
                fontSize: 18,
                fontWeight: FontWeight.w500,
              ),
            ),
          ],
        ),
      );
    }

    return ListView.builder(
      itemCount: allChats.length,
      itemBuilder: (context, index) {
        final chat = allChats[index];
        return _buildChatItem(chat);
      },
    );
  }

  Widget _buildChatItem(Map<String, dynamic> chat) {
    return Dismissible(
      key: Key(chat['id']),
      direction: DismissDirection.endToStart,
      background: Container(
        color: Color(0xFF25D366),
        alignment: Alignment.centerRight,
        padding: EdgeInsets.only(right: 20),
        child: Icon(Icons.archive, color: Colors.white),
      ),
      onDismissed: (direction) {},
      child: ListTile(
        onTap: () => _openChat(chat),
        onLongPress: () {},
        leading: Stack(
          children: [
            Container(
              width: 56,
              height: 56,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                gradient: LinearGradient(
                  colors: [Color(0xFF25D366), Color(0xFF128C7E)],
                ),
              ),
              child: CircleAvatar(
                backgroundColor: Color(0xFF1F2C34),
                child: Text(
                  chat['avatar'],
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 22,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            ),
            if (chat['isOnline'])
              Positioned(
                bottom: 0,
                right: 0,
                child: Container(
                  width: 16,
                  height: 16,
                  decoration: BoxDecoration(
                    color: Color(0xFF25D366),
                    shape: BoxShape.circle,
                    border: Border.all(
                      color: Color(0xFF0B141A),
                      width: 2,
                    ),
                  ),
                ),
              ),
          ],
        ),
        title: Text(
          chat['name'],
          style: TextStyle(
            color: Colors.white,
            fontSize: 16,
            fontWeight: FontWeight.w600,
          ),
          maxLines: 1,
          overflow: TextOverflow.ellipsis,
        ),
        subtitle: Text(
          chat['lastMessage'],
          style: TextStyle(
            color: Colors.white54,
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
              chat['time'],
              style: TextStyle(
                color: chat['unread'] > 0
                    ? Color(0xFF25D366)
                    : Colors.white54,
                fontSize: 12,
              ),
            ),
            if (chat['isPinned'])
              Padding(
                padding: EdgeInsets.only(top: 4),
                child: Icon(Icons.push_pin, size: 14, color: Colors.white54),
              ),
            if (chat['unread'] > 0)
              Container(
                margin: EdgeInsets.only(top: 4),
                padding: EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                decoration: BoxDecoration(
                  color: Color(0xFF25D366),
                  borderRadius: BorderRadius.circular(12),
                ),
                constraints: BoxConstraints(minWidth: 20),
                child: Center(
                  child: Text(
                    chat['unread'].toString(),
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 12,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ),
          ],
        ),
        contentPadding: EdgeInsets.symmetric(horizontal: 12, vertical: 4),
      ),
    );
  }

  Widget _buildFAB() {
    return Container(
      decoration: BoxDecoration(
        shape: BoxShape.circle,
        gradient: LinearGradient(
          colors: [Color(0xFF25D366), Color(0xFF128C7E)],
        ),
        boxShadow: [
          BoxShadow(
            color: Color(0xFF25D366).withOpacity(0.4),
            blurRadius: 12,
            spreadRadius: 2,
          ),
        ],
      ),
      child: FloatingActionButton(
        backgroundColor: Colors.transparent,
        elevation: 0,
        child: Icon(Icons.chat, color: Colors.white),
        onPressed: () {},
      ),
    );
  }

  void _openChat(Map<String, dynamic> chat) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) => WhatsAppStyleChatScreen(
          tenantId: widget.tenantId,
          receiverId: chat['id'],
          receiverName: chat['name'],
        ),
      ),
    );
  }
}
