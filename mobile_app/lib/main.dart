import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

// =========================
// APP THEME
// =========================
import 'theme/app_theme.dart';

// V2 AUTH SCREENS
import 'screens/auth/email_login_screen.dart';
import 'screens/auth/email_signup_screen.dart';
import 'screens/auth/email_otp_verify_screen.dart';

// MAIN DASHBOARD
import 'screens/dashboard_screen.dart';

// SERVICES
import 'services/chat_socket_manager.dart';
import 'services/call_socket_manager.dart';
import 'services/notification_service.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  final prefs = await SharedPreferences.getInstance();
  final savedToken = prefs.getString("auth_token_v2");
  final tenantIdStr = prefs.getString("tenant_id_v2");

  // If logged in → init notifications
  if (tenantIdStr != null) {
    await NotificationService().initialize(tenantIdStr);
  }

  runApp(LifeasyApp(
    isLoggedIn: savedToken != null && tenantIdStr != null,
    tenantId: tenantIdStr,
  ));
}

class LifeasyApp extends StatelessWidget {
  final bool isLoggedIn;
  final String? tenantId;

  const LifeasyApp({
    super.key,
    required this.isLoggedIn,
    this.tenantId,
  });

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: "LIFEASY V27",
      debugShowCheckedModeBanner: false,
      theme: AppTheme.theme,
      // Define routes
      initialRoute: isLoggedIn ? '/dashboard' : '/',
      routes: {
        '/': (context) => const AuthSelectionScreen(),
        '/login': (context) => const EmailLoginScreen(),
        '/signup': (context) => const EmailSignupScreen(),
        '/dashboard': (context) => DashboardScreen(tenantId: tenantId ?? ''),
      },
      home: isLoggedIn
          ? DashboardScreen(tenantId: tenantId.toString())
          : const AuthSelectionScreen(),
    );
  }
}

// ======================================================
// SELECTION SCREEN (Email Login + Email Signup)
// ======================================================
class AuthSelectionScreen extends StatelessWidget {
  const AuthSelectionScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xff0f172a),
      body: Center(
        child: Container(
          padding: const EdgeInsets.all(25),
          width: 320,
          decoration: BoxDecoration(
            color: Colors.black87,
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
              const Icon(Icons.apartment, size: 60, color: Colors.blueAccent),
              const SizedBox(height: 15),
              const Text(
                "LIFEASY",
                style: TextStyle(
                  fontSize: 28,
                  fontWeight: FontWeight.bold,
                  color: Colors.blueAccent,
                ),
              ),
              const SizedBox(height: 30),

              // LOGIN WITH EMAIL
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.blue,
                    padding: const EdgeInsets.symmetric(vertical: 14),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => const EmailLoginScreen(),
                      ),
                    );
                  },
                  child: const Text(
                    "LOGIN WITH EMAIL",
                    style: TextStyle(color: Colors.white),
                  ),
                ),
              ),

              const SizedBox(height: 15),

              // SIGNUP (EMAIL + OTP + PASSWORD)
              SizedBox(
                width: double.infinity,
                child: OutlinedButton(
                  style: OutlinedButton.styleFrom(
                    side: const BorderSide(color: Colors.green, width: 2),
                    padding: const EdgeInsets.symmetric(vertical: 14),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => const EmailSignupScreen(),
                      ),
                    );
                  },
                  child: const Text(
                    "CREATE ACCOUNT",
                    style: TextStyle(color: Colors.green),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}