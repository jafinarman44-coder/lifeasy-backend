import 'package:flutter/material.dart';
import '../tenant_list_screen.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class SettingsPrivacyScreen extends StatefulWidget {
  final String tenantId;
  
  const SettingsPrivacyScreen({Key? key, required this.tenantId}) : super(key: key);

  @override
  _SettingsPrivacyScreenState createState() => _SettingsPrivacyScreenState();
}

class _SettingsPrivacyScreenState extends State<SettingsPrivacyScreen> {
  String _lastSeen = 'Everyone';
  String _profilePhotoVisibility = 'Everyone';
  bool _readReceipts = true;
  List<String> _blockedUsers = [];
  String _serverIp = '192.168.43.219';

  @override
  void initState() {
    super.initState();
    _loadPrivacySettings();
    _loadBlockedUsers();
  }

  Future<void> _loadPrivacySettings() async {
    // TODO: Load from API
    setState(() {
      _lastSeen = 'Everyone';
      _profilePhotoVisibility = 'Everyone';
      _readReceipts = true;
    });
  }

  Future<void> _loadBlockedUsers() async {
    try {
      final response = await http.get(
        Uri.parse('http://$_serverIp:8000/api/chat/v3/blocked/list/${widget.tenantId}'),
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final blockedList = data['blocked_users'] as List;
        setState(() {
          _blockedUsers = blockedList.map((u) => u['blocked_id'].toString()).toList();
        });
      }
    } catch (e) {
      print('Error loading blocked users: $e');
    }
  }

  Future<void> _updateLastSeen(String value) async {
    setState(() => _lastSeen = value);
    // TODO: Save to API
  }

  Future<void> _updateProfilePhotoVisibility(String value) async {
    setState(() => _profilePhotoVisibility = value);
    // TODO: Save to API
  }

  Future<void> _toggleReadReceipts(bool value) async {
    setState(() => _readReceipts = value);
    // TODO: Save to API
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Privacy'),
        backgroundColor: Colors.blueAccent,
        elevation: 0,
      ),
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [Color(0xff0f172a), Colors.black87],
          ),
        ),
        child: ListView(
          padding: EdgeInsets.all(16),
          children: [
            // Last Seen Section
            Card(
              color: Colors.black54,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
              ),
              child: Padding(
                padding: EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Icon(Icons.visibility, color: Colors.blueAccent),
                        SizedBox(width: 8),
                        Text(
                          'Last Seen',
                          style: TextStyle(
                            color: Colors.white,
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ],
                    ),
                    SizedBox(height: 8),
                    Text(
                      'Choose who can see when you were last online',
                      style: TextStyle(color: Colors.grey, fontSize: 13),
                    ),
                    SizedBox(height: 16),
                    _buildRadioOption(
                      'Everyone',
                      _lastSeen,
                      (value) => _updateLastSeen(value!),
                    ),
                    _buildRadioOption(
                      'Building Only',
                      _lastSeen,
                      (value) => _updateLastSeen(value!),
                    ),
                    _buildRadioOption(
                      'Nobody',
                      _lastSeen,
                      (value) => _updateLastSeen(value!),
                    ),
                  ],
                ),
              ),
            ),

            SizedBox(height: 16),

            // Profile Photo Section
            Card(
              color: Colors.black54,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
              ),
              child: Padding(
                padding: EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Icon(Icons.photo, color: Colors.blueAccent),
                        SizedBox(width: 8),
                        Text(
                          'Profile Photo',
                          style: TextStyle(
                            color: Colors.white,
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ],
                    ),
                    SizedBox(height: 8),
                    Text(
                      'Choose who can see your profile photo',
                      style: TextStyle(color: Colors.grey, fontSize: 13),
                    ),
                    SizedBox(height: 16),
                    _buildRadioOption(
                      'Everyone',
                      _profilePhotoVisibility,
                      (value) => _updateProfilePhotoVisibility(value!),
                    ),
                    _buildRadioOption(
                      'Building Only',
                      _profilePhotoVisibility,
                      (value) => _updateProfilePhotoVisibility(value!),
                    ),
                    _buildRadioOption(
                      'Nobody',
                      _profilePhotoVisibility,
                      (value) => _updateProfilePhotoVisibility(value!),
                    ),
                  ],
                ),
              ),
            ),

            SizedBox(height: 16),

            // Read Receipts Section
            Card(
              color: Colors.black54,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
              ),
              child: SwitchListTile(
                title: Row(
                  children: [
                    Icon(Icons.done_all, color: Colors.blueAccent),
                    SizedBox(width: 8),
                    Text(
                      'Read Receipts',
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 16,
                      ),
                    ),
                  ],
                ),
                subtitle: Text(
                  'Show when you have read messages',
                  style: TextStyle(color: Colors.grey, fontSize: 13),
                ),
                value: _readReceipts,
                onChanged: _toggleReadReceipts,
                activeColor: Colors.blueAccent,
              ),
            ),

            SizedBox(height: 16),

            // Blocked Users Section
            Card(
              color: Colors.black54,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
              ),
              child: Padding(
                padding: EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Icon(Icons.block, color: Colors.red),
                        SizedBox(width: 8),
                        Text(
                          'Blocked Users',
                          style: TextStyle(
                            color: Colors.white,
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ],
                    ),
                    SizedBox(height: 8),
                    Text(
                      'Users you have blocked cannot message or call you',
                      style: TextStyle(color: Colors.grey, fontSize: 13),
                    ),
                    SizedBox(height: 16),
                    if (_blockedUsers.isEmpty)
                      Center(
                        child: Padding(
                          padding: EdgeInsets.all(20),
                          child: Column(
                            children: [
                              Icon(
                                Icons.check_circle_outline,
                                color: Colors.green,
                                size: 60,
                              ),
                              SizedBox(height: 12),
                              Text(
                                'No blocked users',
                                style: TextStyle(color: Colors.green, fontSize: 16),
                              ),
                            ],
                          ),
                        ),
                      )
                    else
                      ..._blockedUsers.map((userId) => _buildBlockedUserTile(userId)).toList(),
                    SizedBox(height: 12),
                    SizedBox(
                      width: double.infinity,
                      child: OutlinedButton.icon(
                        onPressed: () => _showBlockUserDialog(),
                        icon: Icon(Icons.add, color: Colors.blueAccent),
                        label: Text(
                          'Block User',
                          style: TextStyle(color: Colors.blueAccent),
                        ),
                        style: OutlinedButton.styleFrom(
                          side: BorderSide(color: Colors.blueAccent),
                          padding: EdgeInsets.symmetric(vertical: 12),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildRadioOption(String value, String groupValue, ValueChanged<String?> onChanged) {
    return RadioListTile<String>(
      title: Text(value, style: TextStyle(color: Colors.white)),
      value: value,
      groupValue: groupValue,
      onChanged: onChanged,
      activeColor: Colors.blueAccent,
    );
  }

  Widget _buildBlockedUserTile(String userId) {
    return Container(
      margin: EdgeInsets.only(bottom: 8),
      padding: EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Colors.grey[900],
        borderRadius: BorderRadius.circular(8),
      ),
      child: Row(
        children: [
          CircleAvatar(
            radius: 20,
            backgroundColor: Colors.red.withOpacity(0.2),
            child: Text(
              'U',
              style: TextStyle(color: Colors.red, fontWeight: FontWeight.bold),
            ),
          ),
          SizedBox(width: 12),
          Expanded(
            child: Text(
              'User #$userId',
              style: TextStyle(color: Colors.white, fontSize: 16),
            ),
          ),
          TextButton(
            onPressed: () => _unblockUser(userId),
            child: Text(
              'Unblock',
              style: TextStyle(color: Colors.blueAccent),
            ),
          ),
        ],
      ),
    );
  }

  void _showBlockUserDialog() {
    // Navigate to tenant list to select user
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('Select user from tenant list')),
    );
  }

  Future<void> _unblockUser(String userId) async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        backgroundColor: Color(0xff1e293b),
        title: Text('Unblock User?', style: TextStyle(color: Colors.white)),
        content: Text(
          'This user will be able to message and call you again.',
          style: TextStyle(color: Colors.grey[300]),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: Text('Cancel', style: TextStyle(color: Colors.grey)),
          ),
          ElevatedButton(
            onPressed: () => Navigator.pop(context, true),
            style: ElevatedButton.styleFrom(backgroundColor: Colors.blueAccent),
            child: Text('Unblock'),
          ),
        ],
      ),
    );

    if (confirmed == true) {
      // TODO: Call unblock API
      setState(() {
        _blockedUsers.remove(userId);
      });
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('User unblocked'),
          backgroundColor: Colors.green,
        ),
      );
    }
  }
}
