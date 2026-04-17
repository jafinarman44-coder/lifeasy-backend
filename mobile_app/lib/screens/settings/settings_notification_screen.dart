import 'package:flutter/material.dart';

class SettingsNotificationScreen extends StatefulWidget {
  final String tenantId;
  
  const SettingsNotificationScreen({Key? key, required this.tenantId}) : super(key: key);

  @override
  _SettingsNotificationScreenState createState() => _SettingsNotificationScreenState();
}

class _SettingsNotificationScreenState extends State<SettingsNotificationScreen> {
  bool _messageNotifications = true;
  bool _groupNotifications = true;
  bool _callNotifications = true;
  bool _vibration = true;
  String _notificationSound = 'Default';
  String _callRingtone = 'Default';
  bool _popupNotification = true;
  String _notificationTone = 'Instant';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Notifications'),
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
            // Message Notifications
            Card(
              color: Colors.black54,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
              ),
              child: Column(
                children: [
                  SwitchListTile(
                    title: Text('Messages', style: TextStyle(color: Colors.white)),
                    subtitle: Text(
                      'Get notified for new messages',
                      style: TextStyle(color: Colors.grey, fontSize: 13),
                    ),
                    value: _messageNotifications,
                    onChanged: (value) => setState(() => _messageNotifications = value),
                    activeColor: Colors.blueAccent,
                  ),
                  Divider(color: Colors.grey[800], height: 1),
                  ListTile(
                    title: Text('Notification Tone', style: TextStyle(color: Colors.white)),
                    subtitle: Text(_notificationSound, style: TextStyle(color: Colors.grey)),
                    trailing: Icon(Icons.chevron_right, color: Colors.grey),
                    onTap: () => _showSoundPicker('Notification'),
                  ),
                  Divider(color: Colors.grey[800], height: 1),
                  SwitchListTile(
                    title: Text('Vibration', style: TextStyle(color: Colors.white)),
                    subtitle: Text(
                      'Vibrate when message arrives',
                      style: TextStyle(color: Colors.grey, fontSize: 13),
                    ),
                    value: _vibration,
                    onChanged: (value) => setState(() => _vibration = value),
                    activeColor: Colors.blueAccent,
                  ),
                  Divider(color: Colors.grey[800], height: 1),
                  SwitchListTile(
                    title: Text('Popup Notification', style: TextStyle(color: Colors.white)),
                    subtitle: Text(
                      'Show popup on screen',
                      style: TextStyle(color: Colors.grey, fontSize: 13),
                    ),
                    value: _popupNotification,
                    onChanged: (value) => setState(() => _popupNotification = value),
                    activeColor: Colors.blueAccent,
                  ),
                ],
              ),
            ),

            SizedBox(height: 16),

            // Group Notifications
            Card(
              color: Colors.black54,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
              ),
              child: Column(
                children: [
                  SwitchListTile(
                    title: Text('Groups', style: TextStyle(color: Colors.white)),
                    subtitle: Text(
                      'Get notified for group messages',
                      style: TextStyle(color: Colors.grey, fontSize: 13),
                    ),
                    value: _groupNotifications,
                    onChanged: (value) => setState(() => _groupNotifications = value),
                    activeColor: Colors.blueAccent,
                  ),
                ],
              ),
            ),

            SizedBox(height: 16),

            // Call Notifications
            Card(
              color: Colors.black54,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
              ),
              child: Column(
                children: [
                  SwitchListTile(
                    title: Text('Calls', style: TextStyle(color: Colors.white)),
                    subtitle: Text(
                      'Get notified for incoming calls',
                      style: TextStyle(color: Colors.grey, fontSize: 13),
                    ),
                    value: _callNotifications,
                    onChanged: (value) => setState(() => _callNotifications = value),
                    activeColor: Colors.blueAccent,
                  ),
                  Divider(color: Colors.grey[800], height: 1),
                  ListTile(
                    title: Text('Call Ringtone', style: TextStyle(color: Colors.white)),
                    subtitle: Text(_callRingtone, style: TextStyle(color: Colors.grey)),
                    trailing: Icon(Icons.chevron_right, color: Colors.grey),
                    onTap: () => _showSoundPicker('Call'),
                  ),
                ],
              ),
            ),

            SizedBox(height: 16),

            // Muted Tenants
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
                        Icon(Icons.volume_off, color: Colors.orange),
                        SizedBox(width: 8),
                        Text(
                          'Muted Tenants',
                          style: TextStyle(
                            color: Colors.white,
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ],
                    ),
                    SizedBox(height: 12),
                    Center(
                      child: Padding(
                        padding: EdgeInsets.all(20),
                        child: Column(
                          children: [
                            Icon(
                              Icons.notifications_paused,
                              color: Colors.grey,
                              size: 60,
                            ),
                            SizedBox(height: 12),
                            Text(
                              'No muted tenants',
                              style: TextStyle(color: Colors.grey, fontSize: 16),
                            ),
                            SizedBox(height: 8),
                            Text(
                              'Long press on a chat to mute',
                              style: TextStyle(color: Colors.grey, fontSize: 13),
                            ),
                          ],
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

  void _showSoundPicker(String type) {
    showModalBottomSheet(
      context: context,
      backgroundColor: Color(0xff1e293b),
      builder: (context) => Container(
        padding: EdgeInsets.all(20),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(
              'Select $type Sound',
              style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold),
            ),
            SizedBox(height: 16),
            _buildSoundOption('Default'),
            _buildSoundOption('Sound 1'),
            _buildSoundOption('Sound 2'),
            _buildSoundOption('Sound 3'),
            _buildSoundOption('None'),
          ],
        ),
      ),
    );
  }

  Widget _buildSoundOption(String sound) {
    return ListTile(
      title: Text(sound, style: TextStyle(color: Colors.white)),
      onTap: () {
        setState(() {
          if (sound == 'Default' || sound == 'None') {
            // Update appropriate variable
          }
        });
        Navigator.pop(context);
      },
    );
  }
}
