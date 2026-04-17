import 'package:flutter/material.dart';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:async';
import '../../services/api_service.dart';
import '../dashboard_screen.dart';
import 'email_otp_verify_screen.dart';

class EmailLoginScreen extends StatefulWidget {
  const EmailLoginScreen({super.key});

  @override
  State<EmailLoginScreen> createState() => _EmailLoginScreenState();
}

class _EmailLoginScreenState extends State<EmailLoginScreen> {
  final emailCtrl = TextEditingController();
  final passwordCtrl = TextEditingController();
  bool loading = false;
  bool obscurePassword = true;

  // Email autocomplete
  List<String> _emailSuggestions = [];
  List<String> _recentEmails = [];
  final List<String> _commonDomains = ['@gmail.com', '@yahoo.com', '@hotmail.com', '@outlook.com'];

  ApiService api = ApiService();

  @override
  void initState() {
    super.initState();
    _loadRecentEmails();
    emailCtrl.addListener(_onEmailChanged);
  }

  @override
  void dispose() {
    emailCtrl.removeListener(_onEmailChanged);
    emailCtrl.dispose();
    passwordCtrl.dispose();
    super.dispose();
  }

  Future<void> _loadRecentEmails() async {
    final prefs = await SharedPreferences.getInstance();
    setState(() {
      _recentEmails = prefs.getStringList('recent_emails') ?? [];
    });
  }

  void _onEmailChanged() {
    final text = emailCtrl.text;
    if (text.length >= 2) {
      List<String> suggestions = [];
      
      // Add recent emails that match
      for (var email in _recentEmails) {
        if (email.toLowerCase().startsWith(text.toLowerCase())) {
          suggestions.add(email);
        }
      }
      
      // Add common domain suggestions
      if (text.contains('@')) {
        final parts = text.split('@');
        if (parts.length == 2 && parts[0].isNotEmpty) {
          for (var domain in _commonDomains) {
            if (domain.startsWith(parts[1])) {
              suggestions.add('${parts[0]}$domain');
            }
          }
        }
      } else {
        // Suggest full emails with common domains
        for (var domain in _commonDomains) {
          suggestions.add('$text$domain');
        }
      }
      
      setState(() {
        _emailSuggestions = suggestions.take(5).toList();
      });
    } else {
      setState(() {
        _emailSuggestions = [];
      });
    }
  }

  void _selectSuggestion(String email) {
    emailCtrl.text = email;
    emailCtrl.selection = TextSelection.fromPosition(
      TextPosition(offset: email.length),
    );
    setState(() {
      _emailSuggestions = [];
    });
  }

  Future<void> login() async {
    if (emailCtrl.text.trim().isEmpty || passwordCtrl.text.trim().isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Please enter email and password")),
      );
      return;
    }

    setState(() => loading = true);

    try {
      final response = await api.loginV2(
        emailCtrl.text.trim(),
        passwordCtrl.text.trim(),
      );

      setState(() => loading = false);

      if (response["success"] == true || response["access_token"] != null) {
        // Login successful - save credentials
        final prefs = await SharedPreferences.getInstance();
        await prefs.setString("auth_token_v2", response["access_token"]);
        final tenantId = response["tenant_id"].toString();
        await prefs.setString("tenant_id_v2", tenantId);
        
        // Save email to recent emails
        List<String> recentEmails = prefs.getStringList('recent_emails') ?? [];
        final currentEmail = emailCtrl.text.trim();
        recentEmails.remove(currentEmail);
        recentEmails.insert(0, currentEmail);
        if (recentEmails.length > 5) recentEmails = recentEmails.sublist(0, 5);
        await prefs.setStringList('recent_emails', recentEmails);

        if (mounted) {
          // Navigate to dashboard directly
          Navigator.of(context).pushReplacement(
            MaterialPageRoute(
              builder: (_) => DashboardScreen(tenantId: tenantId),
            ),
          );
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text("Login Successful!"),
              backgroundColor: Colors.green,
            ),
          );
        }
      } else if (response["message"]?.contains("approval") == true) {
        // Account pending approval
        if (mounted) {
          showDialog(
            context: context,
            builder: (context) => AlertDialog(
              title: const Text('Account Pending Approval'),
              content: const Text(
                'Your account is awaiting owner approval. Please contact the building administrator to approve your registration.',
              ),
              actions: [
                TextButton(
                  onPressed: () => Navigator.pop(context),
                  child: const Text('OK'),
                ),
              ],
            ),
          );
        }
      } else {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text(response["message"] ?? "Login failed"),
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
        title: const Text("Login with Email"),
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
              // Custom App Icon
              Image.asset(
                'assets/app_icon.ico',
                width: 80,
                height: 80,
                fit: BoxFit.contain,
              ),
              const SizedBox(height: 20),
              const Text(
                "Welcome Back!",
                style: TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                  color: Colors.white,
                ),
              ),
              const SizedBox(height: 30),
              // Email Field with Autocomplete
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  TextField(
                    controller: emailCtrl,
                    keyboardType: TextInputType.emailAddress,
                    decoration: InputDecoration(
                      labelText: "Email",
                      labelStyle: const TextStyle(color: Colors.white70),
                      prefixIcon: const Icon(Icons.email, color: Colors.blueAccent),
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(12),
                      ),
                      enabledBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(12),
                        borderSide: const BorderSide(color: Colors.grey),
                      ),
                      focusedBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(12),
                        borderSide: const BorderSide(color: Colors.blueAccent),
                      ),
                    ),
                    style: const TextStyle(color: Colors.white),
                  ),
                  // Email Suggestions Dropdown
                  if (_emailSuggestions.isNotEmpty)
                    Container(
                      margin: const EdgeInsets.only(top: 4),
                      decoration: BoxDecoration(
                        color: Colors.grey[900],
                        borderRadius: BorderRadius.circular(8),
                        border: Border.all(color: Colors.grey[700]!),
                      ),
                      constraints: const BoxConstraints(maxHeight: 200),
                      child: ListView.builder(
                        shrinkWrap: true,
                        itemCount: _emailSuggestions.length,
                        itemBuilder: (context, index) {
                          final suggestion = _emailSuggestions[index];
                          return ListTile(
                            dense: true,
                            leading: const Icon(Icons.email, size: 20, color: Colors.blueAccent),
                            title: Text(
                              suggestion,
                              style: const TextStyle(color: Colors.white),
                            ),
                            onTap: () => _selectSuggestion(suggestion),
                          );
                        },
                      ),
                    ),
                ],
              ),
              const SizedBox(height: 15),
              TextField(
                controller: passwordCtrl,
                obscureText: obscurePassword,
                decoration: InputDecoration(
                  labelText: "Password",
                  labelStyle: const TextStyle(color: Colors.white70),
                  prefixIcon: const Icon(Icons.lock, color: Colors.blueAccent),
                  suffixIcon: IconButton(
                    icon: Icon(
                      obscurePassword
                          ? Icons.visibility_off
                          : Icons.visibility,
                    ),
                    onPressed: () {
                      setState(() => obscurePassword = !obscurePassword);
                    },
                  ),
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                  enabledBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(12),
                    borderSide: const BorderSide(color: Colors.grey),
                  ),
                  focusedBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(12),
                    borderSide: const BorderSide(color: Colors.blueAccent),
                  ),
                ),
                style: const TextStyle(color: Colors.white),
              ),
              const SizedBox(height: 25),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: loading ? null : login,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.blueAccent,
                    padding: const EdgeInsets.symmetric(vertical: 16),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                  child: loading
                      ? const CircularProgressIndicator(color: Colors.white)
                      : const Text(
                          "LOGIN",
                          style: TextStyle(fontSize: 18, color: Colors.white),
                        ),
                ),
              ),
              const SizedBox(height: 15),
              // Forgot Password Button
              TextButton(
                onPressed: () => _showForgotPasswordDialog(),
                child: const Text(
                  "Forgot Password?",
                  style: TextStyle(color: Colors.orange),
                ),
              ),
              TextButton(
                onPressed: () {
                  Navigator.pop(context);
                },
                child: const Text(
                  "Don't have an account? Sign Up",
                  style: TextStyle(color: Colors.green),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Future<Map<String, dynamic>> _sendForgotPasswordOTP(String email) async {
    try {
      final url = Uri.parse('${ApiService.baseUrl}/auth/v2/forgot-password');
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'email': email}),
      );
      
      return jsonDecode(response.body);
    } catch (e) {
      throw Exception('Failed to send OTP: $e');
    }
  }

  void _showForgotPasswordDialog() {
    final resetEmailCtrl = TextEditingController();
    bool isSending = false;
    
    showDialog(
      context: context,
      builder: (context) => StatefulBuilder(
        builder: (context, setDialogState) => AlertDialog(
          title: const Text('Reset Password'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Text(
                'Enter your email address. We\'ll send you an OTP to reset your password.',
                style: TextStyle(fontSize: 14),
              ),
              const SizedBox(height: 16),
              TextField(
                controller: resetEmailCtrl,
                keyboardType: TextInputType.emailAddress,
                decoration: const InputDecoration(
                  labelText: 'Email',
                  prefixIcon: Icon(Icons.email),
                  border: OutlineInputBorder(),
                ),
              ),
            ],
          ),
          actions: [
            TextButton(
              onPressed: isSending ? null : () => Navigator.pop(context),
              child: const Text('Cancel'),
            ),
            ElevatedButton(
              onPressed: isSending ? null : () async {
                if (resetEmailCtrl.text.trim().isEmpty) {
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(content: Text('Please enter your email')),
                  );
                  return;
                }
                
                setDialogState(() => isSending = true);
                
                try {
                  // Call dedicated forgot password endpoint
                  final response = await _sendForgotPasswordOTP(
                    resetEmailCtrl.text.trim(),
                  );
                  
                  if (response["status"] == "success") {
                    Navigator.pop(context); // Close dialog
                    
                    // Navigate to OTP verification for password reset
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => EmailOtpVerifyScreen(
                          email: resetEmailCtrl.text.trim(),
                          password: "", // Empty for password reset
                          isPasswordReset: true,
                        ),
                      ),
                    );
                    
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(
                        content: Text('OTP sent to your email! Check inbox.'),
                        backgroundColor: Colors.green,
                      ),
                    );
                  } else {
                    setDialogState(() => isSending = false);
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(
                        content: Text(response["message"] ?? "Failed to send OTP"),
                        backgroundColor: Colors.red,
                      ),
                    );
                  }
                } catch (e) {
                  setDialogState(() => isSending = false);
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(
                      content: Text('Error: ${e.toString()}'),
                      backgroundColor: Colors.red,
                    ),
                  );
                }
              },
              child: isSending
                  ? const SizedBox(
                      width: 20,
                      height: 20,
                      child: CircularProgressIndicator(strokeWidth: 2),
                    )
                  : const Text('Send OTP'),
            ),
          ],
        ),
      ),
    );
  }
}
