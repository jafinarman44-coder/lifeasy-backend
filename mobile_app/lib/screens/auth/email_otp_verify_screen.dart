import 'package:flutter/material.dart';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../../services/api_service.dart';
import 'set_new_password_screen.dart';

class EmailOtpVerifyScreen extends StatefulWidget {
  final String email;
  final String? password; // Optional for password reset
  final bool isPasswordReset; // Flag for password reset mode

  const EmailOtpVerifyScreen({
    super.key,
    required this.email,
    this.password, // Made optional
    this.isPasswordReset = false,
  });

  @override
  State<EmailOtpVerifyScreen> createState() => _EmailOtpVerifyScreenState();
}

class _EmailOtpVerifyScreenState extends State<EmailOtpVerifyScreen> {
  final otpCtrl = TextEditingController();
  bool loading = false;
  bool _emailSent = true;
  bool _smsSent = true;

  ApiService api = ApiService();

  @override
  void initState() {
    super.initState();
    // Show dual delivery info if password reset mode
    if (widget.isPasswordReset) {
      _emailSent = true;
    }
  }

  Future<void> verifyOTP() async {
    if (otpCtrl.text.trim().isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Please enter OTP")),
      );
      return;
    }

    setState(() => loading = true);

    try {
      final response = await api.registerVerify({
        "email": widget.email,
        "otp": otpCtrl.text.trim(),
      });

      setState(() => loading = false);

      if (response["success"] == true || response["status"] == "success") {
        // For password reset, navigate to set new password screen with OTP
        if (widget.isPasswordReset) {
          if (mounted) {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (_) => SetNewPasswordScreen(
                  email: widget.email,
                  otp: otpCtrl.text.trim(), // Pass the verified OTP
                ),
              ),
            );
          }
        } else {
          // Normal registration flow
          // Save user details for auto-fill on this device
          final prefs = await SharedPreferences.getInstance();
          await prefs.setString('last_signup_email', widget.email);
          
          if (mounted) {
            Navigator.pop(context); // Go back to signup
            
            // Also pop signup screen
            Navigator.pop(context); // Go back to auth selection

            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(
                content: Text("Email Verified! Details saved for next time. Please login."),
                backgroundColor: Colors.green,
                duration: Duration(seconds: 4),
              ),
            );
          }
        }
      } else {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text(response["message"] ?? "Invalid OTP"),
              backgroundColor: Colors.red,
            ),
          );
        }
      }
    } catch (e) {
      setState(() => loading = false);
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text("Error: ${e.toString()}"),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xff0f172a),
      appBar: AppBar(
        automaticallyImplyLeading: false, // Disable back button (memory requirement)
        title: const Text("Verify OTP"),
        backgroundColor: Colors.transparent,
        elevation: 0,
      ),
      body: Center(
        child: Container(
          padding: const EdgeInsets.all(25),
          width: 350,
          decoration: BoxDecoration(
            color: Colors.black87,
            borderRadius: BorderRadius.circular(20),
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Icon(Icons.mark_email_read, size: 60, color: Colors.orange),
              const SizedBox(height: 20),
              const Text(
                "Enter OTP",
                style: TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                  color: Colors.white,
                ),
              ),
              const SizedBox(height: 10),
              Text(
                "Sent to ${widget.email}",
                style: const TextStyle(color: Colors.white70),
                textAlign: TextAlign.center,
              ),
              
              // Dual delivery indicators
              if (!widget.isPasswordReset)
                Container(
                  margin: EdgeInsets.only(top: 12),
                  padding: EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: Colors.blue.withOpacity(0.2),
                    borderRadius: BorderRadius.circular(8),
                    border: Border.all(color: Colors.blue),
                  ),
                  child: Column(
                    children: [
                      Row(
                        children: [
                          Icon(Icons.email, color: Colors.blue, size: 20),
                          SizedBox(width: 8),
                          Text(
                            'Email OTP sent ✓',
                            style: TextStyle(color: Colors.blue),
                          ),
                        ],
                      ),
                      SizedBox(height: 6),
                      Row(
                        children: [
                          Icon(Icons.sms, color: Colors.green, size: 20),
                          SizedBox(width: 8),
                          Text(
                            'SMS OTP also sent ✓',
                            style: TextStyle(color: Colors.green),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              const SizedBox(height: 30),
              TextField(
                controller: otpCtrl,
                keyboardType: TextInputType.number,
                textAlign: TextAlign.center,
                style: const TextStyle(
                  color: Colors.white,
                  fontSize: 24,
                  letterSpacing: 8,
                ),
                decoration: InputDecoration(
                  labelText: "OTP",
                  labelStyle: const TextStyle(color: Colors.white70),
                  prefixIcon: const Icon(Icons.numbers, color: Colors.orange),
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                  enabledBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(12),
                    borderSide: const BorderSide(color: Colors.grey),
                  ),
                  focusedBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(12),
                    borderSide: const BorderSide(color: Colors.orange),
                  ),
                ),
                maxLength: 6,
              ),
              const SizedBox(height: 25),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: loading ? null : verifyOTP,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.orange,
                    padding: const EdgeInsets.symmetric(vertical: 16),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                  child: loading
                      ? const CircularProgressIndicator(color: Colors.white)
                      : const Text(
                          "VERIFY OTP",
                          style: TextStyle(fontSize: 18, color: Colors.white),
                        ),
                ),
              ),
              const SizedBox(height: 15),
              // Resend OTP options
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  TextButton.icon(
                    onPressed: () {
                      // Resend email OTP
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(content: Text('Email OTP resent!')),
                      );
                    },
                    icon: Icon(Icons.email, size: 16),
                    label: Text('Resend Email'),
                    style: TextButton.styleFrom(
                      foregroundColor: Colors.blue,
                    ),
                  ),
                  TextButton.icon(
                    onPressed: () {
                      // Resend SMS OTP
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(content: Text('SMS OTP resent!')),
                      );
                    },
                    icon: Icon(Icons.sms, size: 16),
                    label: Text('Resend SMS'),
                    style: TextButton.styleFrom(
                      foregroundColor: Colors.green,
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }

  @override
  void dispose() {
    otpCtrl.dispose();
    super.dispose();
  }
}
