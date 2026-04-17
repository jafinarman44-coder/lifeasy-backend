import 'package:flutter/material.dart';
import '../services/api_service.dart';
import 'bills_screen.dart';
import 'payments_screen.dart';
import 'notifications_screen.dart';
import 'profile_screen.dart';
import 'chat_screen.dart';
import 'voice_call_screen.dart';
import 'real_video_call_screen.dart';
import 'tenant_list_screen.dart';
import 'tenant_chat_inbox_screen.dart';
import 'settings/settings_screen.dart';
import 'groups/groups_inbox_screen.dart';
import 'whatsapp_chat_list.dart';

class DashboardScreen extends StatelessWidget {
  final String tenantId;
  
  DashboardScreen({required this.tenantId});
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Tenant Dashboard"),
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
          padding: EdgeInsets.all(20),
          children: [
            // Welcome Card
            Card(
              color: Colors.blueAccent.withOpacity(0.2),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(15),
              ),
              child: Padding(
                padding: EdgeInsets.all(20),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      "Welcome Back!",
                      style: TextStyle(
                        fontSize: 24,
                        fontWeight: FontWeight.bold,
                        color: Colors.white,
                      ),
                    ),
                    SizedBox(height: 5),
                    Text(
                      "Tenant ID: $tenantId",
                      style: TextStyle(color: Colors.grey),
                    ),
                  ],
                ),
              ),
            ),
            
            SizedBox(height: 25),
            
            // Quick Actions
            Text(
              "Quick Actions",
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
                color: Colors.white,
              ),
            ),
            
            SizedBox(height: 15),
            
            _buildActionCard(
              context,
              icon: Icons.receipt_long,
              title: "Bills",
              subtitle: "View your bills",
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (_) => BillsScreen(tenantId: tenantId)),
                );
              },
            ),
            
            _buildActionCard(
              context,
              icon: Icons.payment,
              title: "Payments",
              subtitle: "Payment history",
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (_) => PaymentsScreen(tenantId: tenantId)),
                );
              },
            ),
            
            _buildActionCard(
              context,
              icon: Icons.notifications,
              title: "Notifications",
              subtitle: "View alerts",
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (_) => NotificationsScreen(tenantId: tenantId)),
                );
              },
            ),
            
            _buildActionCard(
              context,
              icon: Icons.person,
              title: "Profile",
              subtitle: "Account settings",
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (_) => SettingsScreen(tenantId: tenantId)),
                );
              },
            ),
            
            SizedBox(height: 15),
            
            // Communication Features
            Text(
              "Communication",
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
                color: Colors.white,
              ),
            ),
            
            SizedBox(height: 15),
            
            // Tenant Chat Inbox (WhatsApp-style)
            _buildActionCard(
              context,
              icon: Icons.chat_bubble,
              title: "Messages",
              subtitle: "WhatsApp-style chat with tenants",
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (_) => WhatsAppStyleChatList(tenantId: tenantId)),
                );
              },
            ),
            
            // Tenant List
            _buildActionCard(
              context,
              icon: Icons.people,
              title: "Tenants",
              subtitle: "Browse all tenants",
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (_) => TenantListScreen(tenantId: tenantId)),
                );
              },
            ),
            
            // Groups
            _buildActionCard(
              context,
              icon: Icons.group,
              title: "Groups",
              subtitle: "Group chats",
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (_) => GroupsInboxScreen(tenantId: tenantId)),
                );
              },
            ),
            
            // Owner/Manager Chat (Legacy)
            _buildActionCard(
              context,
              icon: Icons.chat,
              title: "Chat with Manager",
              subtitle: "Message owner/manager",
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (_) => ChatScreen(tenantId: tenantId)),
                );
              },
            ),
            
            _buildActionCard(
              context,
              icon: Icons.call,
              title: "Voice Call",
              subtitle: "Call owner/manager",
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (_) => VoiceCallScreen(tenantId: tenantId, channelName: 'voice_$tenantId', receiverId: '0')),
                );
              },
            ),
            
            _buildActionCard(
              context,
              icon: Icons.videocam,
              title: "Video Call",
              subtitle: "Video call owner/manager",
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (_) => RealVideoCallScreen(tenantId: tenantId)),
                );
              },
            ),
            
            SizedBox(height: 15),
            
            // Payment Button
            Card(
              color: Colors.green.withOpacity(0.2),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(15),
                side: BorderSide(color: Colors.green, width: 2),
              ),
              child: Padding(
                padding: EdgeInsets.all(15),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      "Quick Payment",
                      style: TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                        color: Colors.white,
                      ),
                    ),
                    SizedBox(height: 10),
                    SizedBox(
                      width: double.infinity,
                      child: ElevatedButton(
                        onPressed: () async {
                          try {
                            final apiService = ApiService();
                            await apiService.pay(tenantId, 1000);
                            ScaffoldMessenger.of(context).showSnackBar(
                              SnackBar(
                                content: Text("Payment of ৳1000 Done Successfully!"),
                                backgroundColor: Colors.green,
                              ),
                            );
                          } catch (e) {
                            ScaffoldMessenger.of(context).showSnackBar(
                              SnackBar(
                                content: Text('Payment failed'),
                                backgroundColor: Colors.red,
                              ),
                            );
                          }
                        },
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.green,
                          padding: EdgeInsets.symmetric(vertical: 12),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(10),
                          ),
                        ),
                        child: Text("PAY ৳1000", style: TextStyle(fontSize: 16, color: Colors.white)),
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
  
  Widget _buildActionCard(
    BuildContext context, {
    required IconData icon,
    required String title,
    required String subtitle,
    required VoidCallback onTap,
  }) {
    return Card(
      color: Colors.black54,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
      ),
      margin: EdgeInsets.only(bottom: 12),
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
