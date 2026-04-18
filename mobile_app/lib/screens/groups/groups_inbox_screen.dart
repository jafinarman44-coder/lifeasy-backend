import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'create_group_screen.dart';
import 'group_chat_screen.dart';

class GroupsInboxScreen extends StatefulWidget {
  final String tenantId;
  
  const GroupsInboxScreen({Key? key, required this.tenantId}) : super(key: key);

  @override
  _GroupsInboxScreenState createState() => _GroupsInboxScreenState();
}

class _GroupsInboxScreenState extends State<GroupsInboxScreen> {
  List<dynamic> _groups = [];
  bool _isLoading = false;
  String _serverIp = 'lifeasy-backend-production.up.railway.app';

  @override
  void initState() {
    super.initState();
    _fetchGroups();
  }

  Future<void> _fetchGroups() async {
    setState(() => _isLoading = true);
    
    try {
      final url = Uri.parse('http://$_serverIp:8000/api/groups/list/${widget.tenantId}');
      final response = await http.get(url);

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        setState(() {
          _groups = data['groups'] ?? [];
          _isLoading = false;
        });
      } else {
        setState(() => _isLoading = false);
        print('Failed to load groups');
      }
    } catch (e) {
      setState(() => _isLoading = false);
      print('Error fetching groups: $e');
    }
  }

  Future<void> _createGroup() async {
    final result = await Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => CreateGroupScreen(tenantId: widget.tenantId),
      ),
    );

    if (result == true) {
      _fetchGroups(); // Refresh list
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Groups'),
        backgroundColor: Colors.blueAccent,
        elevation: 0,
        actions: [
          IconButton(
            icon: Icon(Icons.add),
            onPressed: _createGroup,
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
        child: _isLoading
            ? Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    CircularProgressIndicator(color: Colors.blueAccent),
                    SizedBox(height: 16),
                    Text(
                      'Loading groups...',
                      style: TextStyle(color: Colors.grey, fontSize: 16),
                    ),
                  ],
                ),
              )
            : _groups.isEmpty
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
                          'No groups yet',
                          style: TextStyle(
                            color: Colors.grey[500],
                            fontSize: 18,
                          ),
                        ),
                        SizedBox(height: 8),
                        Text(
                          'Create a group to start chatting!',
                          style: TextStyle(
                            color: Colors.grey[600],
                            fontSize: 14,
                          ),
                        ),
                        SizedBox(height: 24),
                        ElevatedButton.icon(
                          onPressed: _createGroup,
                          icon: Icon(Icons.add),
                          label: Text('Create Group'),
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.blueAccent,
                            padding: EdgeInsets.symmetric(
                              horizontal: 32,
                              vertical: 12,
                            ),
                          ),
                        ),
                      ],
                    ),
                  )
                : RefreshIndicator(
                    onRefresh: _fetchGroups,
                    child: ListView.builder(
                      padding: EdgeInsets.all(16),
                      itemCount: _groups.length,
                      itemBuilder: (context, index) {
                        final group = _groups[index];
                        return _buildGroupCard(group);
                      },
                    ),
                  ),
      ),
    );
  }

  Widget _buildGroupCard(Map<String, dynamic> group) {
    return Card(
      color: Colors.black54,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
      ),
      margin: EdgeInsets.only(bottom: 12),
      child: ListTile(
        leading: CircleAvatar(
          radius: 30,
          backgroundColor: Colors.blueAccent.withOpacity(0.2),
          child: Icon(
            Icons.group,
            color: Colors.blueAccent,
            size: 30,
          ),
        ),
        title: Text(
          group['name'] ?? 'Group',
          style: TextStyle(
            color: Colors.white,
            fontSize: 18,
            fontWeight: FontWeight.bold,
          ),
        ),
        subtitle: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            SizedBox(height: 4),
            Text(
              '${group['member_count']} members',
              style: TextStyle(color: Colors.grey),
            ),
            if (group['last_message'] != null) ...[
              SizedBox(height: 4),
              Text(
                group['last_message'],
                style: TextStyle(
                  color: Colors.grey[400],
                  fontSize: 13,
                ),
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
              ),
            ],
          ],
        ),
        trailing: group['last_message_time'] != null
            ? Text(
                _formatTime(group['last_message_time']),
                style: TextStyle(
                  color: Colors.grey,
                  fontSize: 12,
                ),
              )
            : null,
        onTap: () {
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (context) => GroupChatScreen(
                tenantId: widget.tenantId,
                groupId: group['id'].toString(),
                groupName: group['name'],
              ),
            ),
          );
        },
      ),
    );
  }

  String _formatTime(String timestamp) {
    try {
      final dateTime = DateTime.parse(timestamp);
      final now = DateTime.now();
      final difference = now.difference(dateTime);

      if (difference.inDays == 0) {
        return '${dateTime.hour.toString().padLeft(2, '0')}:${dateTime.minute.toString().padLeft(2, '0')}';
      } else if (difference.inDays == 1) {
        return 'Yesterday';
      } else {
        return '${dateTime.day}/${dateTime.month}/${dateTime.year}';
      }
    } catch (e) {
      return '';
    }
  }
}
