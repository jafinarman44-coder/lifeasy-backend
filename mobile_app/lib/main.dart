import 'package:flutter/material.dart';
import 'screens/login_screen.dart';

void main() {
  runApp(const LifeasyApp());
}

class LifeasyApp extends StatelessWidget {
  const LifeasyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'LIFEASY V27',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
        useMaterial3: true,
      ),
      home: const LoginScreen(),
    );
  }
}
