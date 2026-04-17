import 'package:flutter/material.dart';
import 'settings_profile_screen.dart';
import 'settings_notification_screen.dart';
import 'settings_privacy_screen.dart';
import 'settings_chat_screen.dart';
import 'settings_about_screen.dart';

class SettingsScreen extends StatelessWidget {
  final String tenantId;

  const SettingsScreen({super.key, required this.tenantId});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Settings'),
        backgroundColor: Color(0xff0f172a),
      ),
      backgroundColor: Color(0xff0f172a),
      body: ListView(
        padding: EdgeInsets.all(16),
        children: [
          _buildSettingTile(
            context,
            icon: Icons.person,
            title: 'Profile',
            subtitle: 'Manage your account settings',
            onTap: () {
              // TODO: Implement Profile Screen
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(content: Text('Profile coming soon!')),
              );
            },
          ),
          SizedBox(height: 12),
          _buildSettingTile(
            context,
            icon: Icons.notifications,
            title: 'Notifications',
            subtitle: 'Configure notification preferences',
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => SettingsNotificationScreen(tenantId: tenantId)),
              );
            },
          ),
          SizedBox(height: 12),
          _buildSettingTile(
            context,
            icon: Icons.security,
            title: 'Privacy & Security',
            subtitle: 'Manage privacy settings',
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => SettingsPrivacyScreen(tenantId: tenantId)),
              );
            },
          ),
          SizedBox(height: 12),
          _buildSettingTile(
            context,
            icon: Icons.chat,
            title: 'Chat Settings',
            subtitle: 'Customize chat experience',
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => SettingsChatScreen(tenantId: tenantId)),
              );
            },
          ),
          SizedBox(height: 12),
          _buildSettingTile(
            context,
            icon: Icons.info,
            title: 'About',
            subtitle: 'App version and information',
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => SettingsAboutScreen()),
              );
            },
          ),
        ],
      ),
    );
  }

  Widget _buildSettingTile(
    BuildContext context, {
    required IconData icon,
    required String title,
    required String subtitle,
    required VoidCallback onTap,
  }) {
    return Card(
      color: Colors.black54,
      child: ListTile(
        leading: Icon(icon, color: Colors.blueAccent, size: 30),
        title: Text(
          title,
          style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
        ),
        subtitle: Text(
          subtitle,
          style: TextStyle(color: Colors.grey),
        ),
        trailing: Icon(Icons.arrow_forward, color: Colors.grey),
        onTap: onTap,
      ),
    );
  }
}