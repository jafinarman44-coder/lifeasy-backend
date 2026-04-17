import 'package:flutter/material.dart';

class SettingsChatScreen extends StatefulWidget {
  final String tenantId;
  
  const SettingsChatScreen({Key? key, required this.tenantId}) : super(key: key);

  @override
  _SettingsChatScreenState createState() => _SettingsChatScreenState();
}

class _SettingsChatScreenState extends State<SettingsChatScreen> {
  String _mediaDownloadWiFi = 'Auto';
  String _mediaDownloadMobile = 'Photos Only';
  String _mediaDownloadRoaming = 'Never';
  String _wallpaper = 'Default';
  bool _enterToSend = true;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Chat Settings'),
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
            // Wallpaper Section
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
                        Icon(Icons.wallpaper, color: Colors.blueAccent),
                        SizedBox(width: 8),
                        Text(
                          'Wallpaper',
                          style: TextStyle(
                            color: Colors.white,
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ],
                    ),
                    SizedBox(height: 12),
                    _buildWallpaperOption('Default'),
                    _buildWallpaperOption('Dark'),
                    _buildWallpaperOption('Light'),
                    _buildWallpaperOption('Custom'),
                  ],
                ),
              ),
            ),

            SizedBox(height: 16),

            // Media Auto-Download
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
                        Icon(Icons.download, color: Colors.blueAccent),
                        SizedBox(width: 8),
                        Text(
                          'Media Auto-Download',
                          style: TextStyle(
                            color: Colors.white,
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ],
                    ),
                    SizedBox(height: 16),
                    _buildDropdownOption(
                      'When using Wi-Fi',
                      _mediaDownloadWiFi,
                      ['Auto', 'Photos Only', 'Never'],
                      (value) => setState(() => _mediaDownloadWiFi = value!),
                    ),
                    SizedBox(height: 12),
                    _buildDropdownOption(
                      'When using mobile data',
                      _mediaDownloadMobile,
                      ['Auto', 'Photos Only', 'Never'],
                      (value) => setState(() => _mediaDownloadMobile = value!),
                    ),
                    SizedBox(height: 12),
                    _buildDropdownOption(
                      'When roaming',
                      _mediaDownloadRoaming,
                      ['Auto', 'Photos Only', 'Never'],
                      (value) => setState(() => _mediaDownloadRoaming = value!),
                    ),
                  ],
                ),
              ),
            ),

            SizedBox(height: 16),

            // Chat Behavior
            Card(
              color: Colors.black54,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
              ),
              child: Column(
                children: [
                  SwitchListTile(
                    title: Text('Enter to Send', style: TextStyle(color: Colors.white)),
                    subtitle: Text(
                      'Press Enter key to send message',
                      style: TextStyle(color: Colors.grey, fontSize: 13),
                    ),
                    value: _enterToSend,
                    onChanged: (value) => setState(() => _enterToSend = value),
                    activeColor: Colors.blueAccent,
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildWallpaperOption(String type) {
    final isSelected = _wallpaper == type;
    return GestureDetector(
      onTap: () => setState(() => _wallpaper = type),
      child: Container(
        margin: EdgeInsets.only(bottom: 8),
        padding: EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: isSelected ? Colors.blueAccent.withOpacity(0.2) : Colors.grey[900],
          borderRadius: BorderRadius.circular(8),
          border: Border.all(
            color: isSelected ? Colors.blueAccent : Colors.grey,
            width: isSelected ? 2 : 1,
          ),
        ),
        child: Row(
          children: [
            Icon(
              isSelected ? Icons.check_circle : Icons.circle_outlined,
              color: isSelected ? Colors.blueAccent : Colors.grey,
            ),
            SizedBox(width: 12),
            Text(
              type,
              style: TextStyle(
                color: isSelected ? Colors.blueAccent : Colors.white,
                fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildDropdownOption(
    String label,
    String value,
    List<String> options,
    ValueChanged<String?> onChanged,
  ) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Text(label, style: TextStyle(color: Colors.grey)),
        DropdownButton<String>(
          value: value,
          dropdownColor: Color(0xff1e293b),
          style: TextStyle(color: Colors.white),
          underline: Container(height: 1, color: Colors.blueAccent),
          items: options.map((option) {
            return DropdownMenuItem(
              value: option,
              child: Text(option),
            );
          }).toList(),
          onChanged: onChanged,
        ),
      ],
    );
  }
}
