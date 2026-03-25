import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../services/api_service.dart';
import 'dashboard_screen.dart';

class OTPScreen extends StatefulWidget {
  final String tenantId;

  const OTPScreen({super.key, required this.tenantId});

  @override
  State<OTPScreen> createState() => _OTPScreenState();
}

class _OTPScreenState extends State<OTPScreen> {
  final otpController = TextEditingController();
  bool _isLoading = false;
  String? _errorMessage;

  Future<void> _verifyOTP() async {
    if (otpController.text.isEmpty) {
      setState(() {
        _errorMessage = 'Please enter OTP';
      });
      return;
    }

    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      final result =
          await ApiService.verifyOtp(widget.tenantId, otpController.text);

      if (result['status'] == 'success') {
        SharedPreferences prefs = await SharedPreferences.getInstance();
        await prefs.setString('tenant_id', widget.tenantId);

        Navigator.pushAndRemoveUntil(
          context,
          MaterialPageRoute(
              builder: (_) => DashboardScreen(tenantId: widget.tenantId)),
          (route) => false,
        );
      } else {
        setState(() {
          _errorMessage = result['message'] ?? 'Invalid OTP';
        });
      }
    } catch (e) {
      setState(() {
        _errorMessage = e.toString();
      });
    }

    setState(() => _isLoading = false);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Color(0xff0f172a),
      appBar: AppBar(
        title: Text('Verify OTP'),
        backgroundColor: Colors.transparent,
        automaticallyImplyLeading: false,
      ),
      body: Center(
        child: Container(
          padding: EdgeInsets.all(25),
          width: 320,
          decoration: BoxDecoration(
            color: Colors.black54,
            borderRadius: BorderRadius.circular(20),
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(Icons.lock_clock, size: 60, color: Colors.blueAccent),
              SizedBox(height: 20),
              Text("Enter OTP",
                  style: TextStyle(
                      color: Colors.white,
                      fontSize: 22,
                      fontWeight: FontWeight.bold)),
              SizedBox(height: 10),
              Text("Sent to Tenant ${widget.tenantId}",
                  style: TextStyle(color: Colors.grey)),
              SizedBox(height: 20),
              TextField(
                controller: otpController,
                style: TextStyle(color: Colors.white),
                decoration: InputDecoration(
                  labelText: "OTP",
                  labelStyle: TextStyle(color: Colors.grey),
                  prefixIcon: Icon(Icons.key, color: Colors.blueAccent),
                  border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12)),
                ),
                keyboardType: TextInputType.number,
              ),
              SizedBox(height: 20),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: _isLoading ? null : _verifyOTP,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.blueAccent,
                    padding: EdgeInsets.symmetric(vertical: 15),
                  ),
                  child: _isLoading
                      ? CircularProgressIndicator(color: Colors.white)
                      : Text("VERIFY OTP",
                          style:
                              TextStyle(color: Colors.white, fontSize: 16)),
                ),
              ),
              if (_errorMessage != null) ...[
                SizedBox(height: 12),
                Text(_errorMessage!,
                    textAlign: TextAlign.center,
                    style: TextStyle(color: Colors.red, fontSize: 12)),
              ]
            ],
          ),
        ),
      ),
    );
  }
}
