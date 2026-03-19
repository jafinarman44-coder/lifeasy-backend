import 'package:flutter/material.dart';

class BillCard extends StatelessWidget {
  final String month;
  final int year;
  final double amount;
  final String status;
  final String dueDate;
  
  BillCard({
    required this.month,
    required this.year,
    required this.amount,
    required this.status,
    required this.dueDate,
  });
  
  @override
  Widget build(BuildContext context) {
    final isPaid = status == 'paid';
    
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
          '$month $year',
          style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
        ),
        subtitle: Text(
          'Due: $dueDate',
          style: TextStyle(color: Colors.grey),
        ),
        trailing: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.end,
          children: [
            Text(
              '৳$amount',
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
  }
}
