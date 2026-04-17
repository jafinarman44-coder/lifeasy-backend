import 'package:flutter/material.dart';

class NotificationsScreen extends StatefulWidget {
  final String tenantId;
  
  NotificationsScreen({required this.tenantId});
  
  @override
  _NotificationsScreenState createState() => _NotificationsScreenState();
}

class _NotificationsScreenState extends State<NotificationsScreen> {
  List<Map<String, dynamic>> notifications = [
    {
      'title': 'Rent Due',
      'message': 'Your rent of ৳10,000 is due on 5th April',
      'time': '2 hours ago',
      'icon': Icons.payment,
      'color': Colors.orange,
      'read': false,
    },
    {
      'title': 'Maintenance Notice',
      'message': 'Water supply will be interrupted tomorrow 10 AM - 2 PM',
      'time': '5 hours ago',
      'icon': Icons.build,
      'color': Colors.blue,
      'read': false,
    },
    {
      'title': 'Payment Received',
      'message': 'Your payment of ৳10,000 has been received',
      'time': '1 day ago',
      'icon': Icons.check_circle,
      'color': Colors.green,
      'read': true,
    },
    {
      'title': 'New Message',
      'message': 'You have a new message from building manager',
      'time': '2 days ago',
      'icon': Icons.message,
      'color': Colors.purple,
      'read': true,
    },
  ];
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Notifications'),
        backgroundColor: Colors.blueAccent,
        actions: [
          IconButton(
            icon: Icon(Icons.delete_sweep),
            onPressed: () {
              setState(() {
                notifications.clear();
              });
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(content: Text('All notifications cleared')),
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
        child: notifications.isEmpty
            ? Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(
                      Icons.notifications_off,
                      size: 80,
                      color: Colors.grey,
                    ),
                    SizedBox(height: 20),
                    Text(
                      'No notifications',
                      style: TextStyle(
                        fontSize: 18,
                        color: Colors.grey,
                      ),
                    ),
                  ],
                ),
              )
            : ListView.builder(
                padding: EdgeInsets.all(16),
                itemCount: notifications.length,
                itemBuilder: (context, index) {
                  final notification = notifications[index];
                  return Card(
                    color: notification['read'] 
                        ? Colors.black54 
                        : Colors.blueAccent.withOpacity(0.2),
                    margin: EdgeInsets.only(bottom: 12),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: ListTile(
                      leading: CircleAvatar(
                        backgroundColor: notification['color'],
                        child: Icon(
                          notification['icon'],
                          color: Colors.white,
                        ),
                      ),
                      title: Text(
                        notification['title'],
                        style: TextStyle(
                          color: Colors.white,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      subtitle: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          SizedBox(height: 4),
                          Text(
                            notification['message'],
                            style: TextStyle(color: Colors.grey[300]),
                          ),
                          SizedBox(height: 4),
                          Text(
                            notification['time'],
                            style: TextStyle(
                              color: Colors.grey,
                              fontSize: 12,
                            ),
                          ),
                        ],
                      ),
                      trailing: !notification['read']
                          ? CircleAvatar(
                              radius: 4,
                              backgroundColor: Colors.blueAccent,
                            )
                          : null,
                      onTap: () {
                        setState(() {
                          notifications[index]['read'] = true;
                        });
                      },
                    ),
                  );
                },
              ),
      ),
    );
  }
}
