import 'package:flutter/material.dart';

class SettingsAboutScreen extends StatelessWidget {
  const SettingsAboutScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('About'),
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
            // App Logo & Version
            Card(
              color: Colors.black54,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
              ),
              child: Padding(
                padding: EdgeInsets.all(30),
                child: Column(
                  children: [
                    Container(
                      padding: EdgeInsets.all(20),
                      decoration: BoxDecoration(
                        color: Colors.blueAccent.withOpacity(0.2),
                        shape: BoxShape.circle,
                      ),
                      child: Icon(
                        Icons.apartment,
                        size: 80,
                        color: Colors.blueAccent,
                      ),
                    ),
                    SizedBox(height: 20),
                    Text(
                      'LIFEASY',
                      style: TextStyle(
                        fontSize: 32,
                        fontWeight: FontWeight.bold,
                        color: Colors.blueAccent,
                      ),
                    ),
                    SizedBox(height: 8),
                    Text(
                      'Version 27.0.0',
                      style: TextStyle(
                        color: Colors.grey,
                        fontSize: 16,
                      ),
                    ),
                    SizedBox(height: 4),
                    Text(
                      'Phase 6 - Step 10',
                      style: TextStyle(
                        color: Colors.grey[600],
                        fontSize: 13,
                      ),
                    ),
                  ],
                ),
              ),
            ),

            SizedBox(height: 16),

            // App Info
            Card(
              color: Colors.black54,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
              ),
              child: Column(
                children: [
                  ListTile(
                    leading: Icon(Icons.info, color: Colors.blueAccent),
                    title: Text('App Name', style: TextStyle(color: Colors.white)),
                    subtitle: Text('LIFEASY V27', style: TextStyle(color: Colors.grey)),
                  ),
                  Divider(color: Colors.grey[800], height: 1),
                  ListTile(
                    leading: Icon(Icons.update, color: Colors.blueAccent),
                    title: Text('Check for Updates', style: TextStyle(color: Colors.white)),
                    subtitle: Text('You\'re using the latest version', style: TextStyle(color: Colors.grey)),
                    trailing: Icon(Icons.chevron_right, color: Colors.grey),
                    onTap: () {
                      // TODO: Check for updates
                    },
                  ),
                  Divider(color: Colors.grey[800], height: 1),
                  ListTile(
                    leading: Icon(Icons.build, color: Colors.blueAccent),
                    title: Text('Build Number', style: TextStyle(color: Colors.white)),
                    subtitle: Text('2026.04.06.1', style: TextStyle(color: Colors.grey)),
                  ),
                ],
              ),
            ),

            SizedBox(height: 16),

            // Developer Info
            Card(
              color: Colors.black54,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
              ),
              child: Column(
                children: [
                  ListTile(
                    leading: Icon(Icons.person, color: Colors.blueAccent),
                    title: Text('Developer', style: TextStyle(color: Colors.white)),
                    subtitle: Text('LIFEASY Development Team', style: TextStyle(color: Colors.grey)),
                  ),
                  Divider(color: Colors.grey[800], height: 1),
                  ListTile(
                    leading: Icon(Icons.email, color: Colors.blueAccent),
                    title: Text('Contact', style: TextStyle(color: Colors.white)),
                    subtitle: Text('support@lifeasy.com', style: TextStyle(color: Colors.grey)),
                    trailing: Icon(Icons.chevron_right, color: Colors.grey),
                  ),
                  Divider(color: Colors.grey[800], height: 1),
                  ListTile(
                    leading: Icon(Icons.language, color: Colors.blueAccent),
                    title: Text('Website', style: TextStyle(color: Colors.white)),
                    subtitle: Text('www.lifeasy.com', style: TextStyle(color: Colors.grey)),
                    trailing: Icon(Icons.chevron_right, color: Colors.grey),
                  ),
                ],
              ),
            ),

            SizedBox(height: 16),

            // Legal
            Card(
              color: Colors.black54,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
              ),
              child: Column(
                children: [
                  ListTile(
                    leading: Icon(Icons.privacy_tip, color: Colors.blueAccent),
                    title: Text('Privacy Policy', style: TextStyle(color: Colors.white)),
                    trailing: Icon(Icons.chevron_right, color: Colors.grey),
                    onTap: () {
                      // TODO: Open privacy policy
                    },
                  ),
                  Divider(color: Colors.grey[800], height: 1),
                  ListTile(
                    leading: Icon(Icons.description, color: Colors.blueAccent),
                    title: Text('Terms of Service', style: TextStyle(color: Colors.white)),
                    trailing: Icon(Icons.chevron_right, color: Colors.grey),
                    onTap: () {
                      // TODO: Open terms of service
                    },
                  ),
                  Divider(color: Colors.grey[800], height: 1),
                  ListTile(
                    leading: Icon(Icons.gavel, color: Colors.blueAccent),
                    title: Text('Licenses', style: TextStyle(color: Colors.white)),
                    trailing: Icon(Icons.chevron_right, color: Colors.grey),
                    onTap: () {
                      showLicensePage(
                        context: context,
                        applicationName: 'LIFEASY',
                        applicationVersion: '27.0.0',
                      );
                    },
                  ),
                ],
              ),
            ),

            SizedBox(height: 16),

            // Copyright
            Center(
              child: Text(
                '© 2026 LIFEASY. All rights reserved.',
                style: TextStyle(
                  color: Colors.grey[600],
                  fontSize: 12,
                ),
              ),
            ),

            SizedBox(height: 8),

            Center(
              child: Text(
                'Made with ❤️ for apartment management',
                style: TextStyle(
                  color: Colors.grey[600],
                  fontSize: 12,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
