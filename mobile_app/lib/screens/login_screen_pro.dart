import 'package:flutter/material.dart';
import '../services/api_service.dart';

class LoginScreenPro extends StatefulWidget {
  const LoginScreenPro({super.key});

  @override
  State<LoginScreenPro> createState() => _LoginScreenProState();
}

class _LoginScreenProState extends State<LoginScreenPro> {
  final emailCtrl = TextEditingController();
  final passwordCtrl = TextEditingController();
  final nameCtrl = TextEditingController();
  final otpCtrl = TextEditingController();

  bool otpSent = false;
  bool loading = false;

  ApiService api = ApiService();

  void sendEmailOTP() async {
    setState(() => loading = true);

    final response = await api.registerRequest({
      "email": emailCtrl.text.trim(),
      "password": passwordCtrl.text.trim(),
      "name": nameCtrl.text.trim(),
    });

    setState(() => loading = false);

    if (response["success"] == true) {
      setState(() => otpSent = true);

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("OTP sent to your EMAIL")),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(response["message"] ?? "Error")),
      );
    }
  }

  void verifyEmailOTP() async {
    setState(() => loading = true);

    final response = await api.registerVerify({
      "email": emailCtrl.text.trim(),
      "otp": otpCtrl.text.trim(),
    });

    setState(() => loading = false);

    if (response["success"] == true) {
      Navigator.pop(context);

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Email Verified! Login Approve Pending...")),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(response["message"] ?? "Invalid OTP")),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: Center(
        child: Container(
          padding: const EdgeInsets.all(20),
          width: 350,
          decoration: BoxDecoration(
            color: Colors.black87,
            borderRadius: BorderRadius.circular(18),
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Text(
                "Email Based Registration",
                style: TextStyle(fontSize: 24, color: Colors.blueAccent),
              ),
              const SizedBox(height: 20),

              TextField(
                controller: nameCtrl,
                decoration: const InputDecoration(
                  labelText: "Full Name",
                  labelStyle: TextStyle(color: Colors.white70),
                  enabledBorder: OutlineInputBorder(),
                  focusedBorder: OutlineInputBorder(),
                ),
                style: const TextStyle(color: Colors.white),
              ),

              const SizedBox(height: 10),

              TextField(
                controller: emailCtrl,
                decoration: const InputDecoration(
                  labelText: "Email",
                  labelStyle: TextStyle(color: Colors.white70),
                  enabledBorder: OutlineInputBorder(),
                  focusedBorder: OutlineInputBorder(),
                ),
                style: const TextStyle(color: Colors.white),
              ),

              const SizedBox(height: 10),

              TextField(
                controller: passwordCtrl,
                obscureText: true,
                decoration: const InputDecoration(
                  labelText: "Password",
                  labelStyle: TextStyle(color: Colors.white70),
                  enabledBorder: OutlineInputBorder(),
                  focusedBorder: OutlineInputBorder(),
                ),
                style: const TextStyle(color: Colors.white),
              ),

              const SizedBox(height: 20),

              if (!otpSent)
                ElevatedButton(
                  onPressed: loading ? null : sendEmailOTP,
                  child: const Text("SEND EMAIL OTP"),
                ),

              if (otpSent) ...[
                TextField(
                  controller: otpCtrl,
                  decoration: const InputDecoration(
                    labelText: "Enter OTP",
                    labelStyle: TextStyle(color: Colors.white70),
                    enabledBorder: OutlineInputBorder(),
                    focusedBorder: OutlineInputBorder(),
                  ),
                  style: const TextStyle(color: Colors.white),
                ),
                const SizedBox(height: 20),
                ElevatedButton(
                  onPressed: loading ? null : verifyEmailOTP,
                  child: const Text("VERIFY OTP"),
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }
}
