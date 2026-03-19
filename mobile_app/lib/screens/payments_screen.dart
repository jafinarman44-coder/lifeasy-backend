import 'package:flutter/material.dart';
import '../services/api_service.dart';

class PaymentsScreen extends StatefulWidget {
  final String tenantId;
  
  PaymentsScreen({super.key, required this.tenantId});
  
  @override
  State<PaymentsScreen> createState() => _PaymentsScreenState();
}

class _PaymentsScreenState extends State<PaymentsScreen> {
  late Future<List<Map<String, dynamic>>> _paymentsFuture;
  
  @override
  void initState() {
    super.initState();
    _paymentsFuture = ApiService().getPayments(widget.tenantId);
  }
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Payment History"),
        backgroundColor: Colors.blueAccent,
      ),
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            colors: [Color(0xff0f172a), Colors.black87],
          ),
        ),
        child: FutureBuilder<List<Map<String, dynamic>>>(
          future: _paymentsFuture,
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return Center(child: CircularProgressIndicator());
            }
            
            if (snapshot.hasError) {
              return Center(
                child: Text('Error: ${snapshot.error}', style: TextStyle(color: Colors.red)),
              );
            }
            
            final payments = snapshot.data ?? [];
            
            if (payments.isEmpty) {
              return Center(child: Text('No payments found', style: TextStyle(color: Colors.white)));
            }
            
            return ListView.builder(
              padding: EdgeInsets.all(16),
              itemCount: payments.length,
              itemBuilder: (context, index) {
                final payment = payments[index];
                
                return Card(
                  color: Colors.black54,
                  margin: EdgeInsets.only(bottom: 12),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: ListTile(
                    leading: CircleAvatar(
                      backgroundColor: Colors.green,
                      child: Icon(Icons.check, color: Colors.white),
                    ),
                    title: Text(
                      'Payment - ${payment['date']}',
                      style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
                    ),
                    subtitle: Text(
                      'Method: ${payment['method']}',
                      style: TextStyle(color: Colors.grey),
                    ),
                    trailing: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      crossAxisAlignment: CrossAxisAlignment.end,
                      children: [
                        Text(
                          '৳${payment['amount']}',
                          style: TextStyle(
                            color: Colors.green,
                            fontWeight: FontWeight.bold,
                            fontSize: 16,
                          ),
                        ),
                        Text(
                          'Receipt: ${payment['receipt_number']}',
                          style: TextStyle(color: Colors.grey, fontSize: 9),
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
