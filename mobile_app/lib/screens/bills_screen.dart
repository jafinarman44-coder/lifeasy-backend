import 'package:flutter/material.dart';
import '../services/api_service.dart';

class BillsScreen extends StatefulWidget {
  final String tenantId;
  
  BillsScreen({super.key, required this.tenantId});
  
  @override
  State<BillsScreen> createState() => _BillsScreenState();
}

class _BillsScreenState extends State<BillsScreen> {
  late Future<List<Map<String, dynamic>>> _billsFuture;
  
  @override
  void initState() {
    super.initState();
    _billsFuture = ApiService().getBills(widget.tenantId);
  }
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("My Bills"),
        backgroundColor: Colors.blueAccent,
      ),
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            colors: [Color(0xff0f172a), Colors.black87],
          ),
        ),
        child: FutureBuilder<List<Map<String, dynamic>>>(
          future: _billsFuture,
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return Center(child: CircularProgressIndicator());
            }
            
            if (snapshot.hasError) {
              return Center(
                child: Text('Error: ${snapshot.error}', style: TextStyle(color: Colors.red)),
              );
            }
            
            final bills = snapshot.data ?? [];
            
            if (bills.isEmpty) {
              return Center(child: Text('No bills found', style: TextStyle(color: Colors.white)));
            }
            
            return ListView.builder(
              padding: EdgeInsets.all(16),
              itemCount: bills.length,
              itemBuilder: (context, index) {
                final bill = bills[index];
                final isPaid = bill['status'] == 'paid';
                
                return Card(
                  color: Colors.black54,
                  margin: EdgeInsets.only(bottom: 12),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: ListTile(
                    leading: CircleAvatar(
                      backgroundColor: isPaid ? Colors.green : Colors.orange,
                      child: Icon(isPaid ? Icons.check : Icons.warning, color: Colors.white),
                    ),
                    title: Text(
                      '${bill['month']} ${bill['year']}',
                      style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
                    ),
                    subtitle: Text(
                      'Due: ${bill['due_date']}',
                      style: TextStyle(color: Colors.grey),
                    ),
                    trailing: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      crossAxisAlignment: CrossAxisAlignment.end,
                      children: [
                        Text(
                          '৳${bill['amount']}',
                          style: TextStyle(
                            color: Colors.blueAccent,
                            fontWeight: FontWeight.bold,
                            fontSize: 16,
                          ),
                        ),
                        Text(
                          isPaid ? 'PAID' : 'UNPAID',
                          style: TextStyle(
                            color: isPaid ? Colors.green : Colors.orange,
                            fontSize: 10,
                          ),
                        ),
                      ],
                    ),
                  ),
                );
              },
            );
          },
        ),
      ),
    );
  }
}
