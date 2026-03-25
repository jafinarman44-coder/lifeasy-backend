import 'package:flutter/material.dart';
import '../services/api_service.dart';
import 'otp_screen.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final idController = TextEditingController(text: '1001');
  final passController = TextEditingController(text: '123456');
  bool _isLoading = false;
  String? _errorMessage;

  Future<void> _handleLogin() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      final result = await ApiService.sendOtp(
        idController.text,
        passController.text,
      );

      setState(() => _isLoading = false);

      if (result['status'] == 'success') {
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (_) => OTPScreen(tenantId: idController.text),
          ),
        );
      } else {
        setState(() {
          _errorMessage = result['message'] ?? 'Login failed';
        });
      }
    } catch (e) {
      setState(() {
        _isLoading = false;
        _errorMessage = e.toString();
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xff0f172a),
      body: Center(
        child: Container(
          padding: const EdgeInsets.all(25),
          width: 320,
          decoration: BoxDecoration(
            color: Colors.black54,
            borderRadius: BorderRadius.circular(20),
            boxShadow: [
              BoxShadow(
                color: Colors.blue.withOpacity(0.3),
                blurRadius: 15,
                spreadRadius: 2,
              ),
            ],
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(Icons.apartment, size: 60, color: Colors.blueAccent),
              SizedBox(height: 15),
              Text("LIFEASY",
                  style: TextStyle(
                      fontSize: 30,
                      color: Colors.blueAccent,
                      fontWeight: FontWeight.bold)),
              SizedBox(height: 30),
              TextField(
                controller: idController,
                style: TextStyle(color: Colors.white),
                decoration: InputDecoration(
                  labelText: "Tenant ID",
                  labelStyle: TextStyle(color: Colors.grey),
                  prefixIcon: Icon(Icons.person, color: Colors.blueAccent),
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),
              ),
              SizedBox(height: 15),
              TextField(
                controller: passController,
                obscureText: true,
                style: TextStyle(color: Colors.white),
                decoration: InputDecoration(
                  labelText: "Password",
                  labelStyle: TextStyle(color: Colors.grey),
                  prefixIcon: Icon(Icons.lock, color: Colors.blueAccent),
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),
              ),
              SizedBox(height: 20),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: _isLoading ? null : _handleLogin,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.blueAccent,
                    padding: EdgeInsets.symmetric(vertical: 15),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                  child: _isLoading
                      ? CircularProgressIndicator(color: Colors.white)
                      : Text("LOGIN",
                          style:
                              TextStyle(fontSize: 16, color: Colors.white)),
                ),
              ),
              if (_errorMessage != null) ...[
                SizedBox(height: 12),
                Text(
                  _errorMessage!,
                  textAlign: TextAlign.center,
                  style: TextStyle(color: Colors.red, fontSize: 12),
                )
              ]
            ],
          ),
        ),
      ),
    );
  }
}
