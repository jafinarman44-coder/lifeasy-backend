import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class ApiService {
  static const String baseUrl = 'https://lifeasy-api.onrender.com/api';
  
  Future<Map<String, String>> _getHeaders() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('token');
    
    return {
      'Content-Type': 'application/json',
      if (token != null) 'Authorization': 'Bearer $token',
    };
  }
  
  // -----------------------------
  // SEND OTP (PRODUCTION)
  // -----------------------------
  static Future<Map<String, dynamic>> sendOtp(
      String tenantId, String password) async {
    final url = Uri.parse("$baseUrl/otp/send");

    final response = await http.post(
      url,
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({
        "tenant_id": tenantId,
        "password": password,
      }),
    );

    return jsonDecode(response.body);
  }

  // -----------------------------
  // VERIFY OTP (PRODUCTION)
  // -----------------------------
  static Future<Map<String, dynamic>> verifyOtp(
      String tenantId, String otp) async {
    final url = Uri.parse("$baseUrl/otp/verify");

    final response = await http.post(
      url,
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({
        "tenant_id": tenantId,
        "otp": otp,
      }),
    );

    return jsonDecode(response.body);
  }
  
  // Get Bills
  Future<List<Map<String, dynamic>>> getBills(String tenantId) async {
    try {
      final headers = await _getHeaders();
      final response = await http.get(
        Uri.parse('$baseUrl/bills/tenant/$tenantId'),
        headers: headers,
      );
      
      if (response.statusCode == 200) {
        List<dynamic> data = jsonDecode(response.body);
        return data.map((item) => item as Map<String, dynamic>).toList();
      } else {
        throw Exception('Failed to load bills');
      }
    } catch (e) {
      rethrow;
    }
  }
  
  // Get Payments
  Future<List<Map<String, dynamic>>> getPayments(String tenantId) async {
    try {
      final headers = await _getHeaders();
      final response = await http.get(
        Uri.parse('$baseUrl/payments/tenant/$tenantId'),
        headers: headers,
      );
      
      if (response.statusCode == 200) {
        List<dynamic> data = jsonDecode(response.body);
        return data.map((item) => item as Map<String, dynamic>).toList();
      } else {
        throw Exception('Failed to load payments');
      }
    } catch (e) {
      rethrow;
    }
  }
  
  // Make Payment (Legacy - Keep for backward compatibility)
  Future<void> pay(String tenantId, num amount) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/pay'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'tenant_id': tenantId,
          'amount': amount,
        }),
      );
      
      if (response.statusCode != 200) {
        throw Exception('Payment failed');
      }
    } catch (e) {
      rethrow;
    }
  }
  
  // -----------------------------
  // TEMP COMPATIBILITY FOR OLD CODE
  // -----------------------------
  Future<dynamic> sendOTP(String phone) async {
    return {"status": "ok"}; // disable temporary
  }
  
  Future<dynamic> verifyOTP(String phone, String otp) async {
    return {"status": "verified"};
  }
  
  Future<dynamic> login(String phone, String password) async {
    return loginV2(phone, password);
  }
  
  Future<dynamic> register(String phone, String password, String name) async {
    return registerRequest({
      'phone': phone,
      'password': password,
      'name': name,
    });
  }
  
  // V2 Authentication Methods
  Future<Map<String, dynamic>> registerRequest(Map<String, dynamic> data) async {
    final url = Uri.parse("$baseUrl/auth/v2/register-request");
    final response = await http.post(
      url,
      headers: {"Content-Type": "application/json"},
      body: jsonEncode(data),
    );
    return jsonDecode(response.body);
  }
  
  Future<Map<String, dynamic>> registerVerify(Map<String, dynamic> data) async {
    final url = Uri.parse("$baseUrl/auth/v2/register-verify");
    final response = await http.post(
      url,
      headers: {"Content-Type": "application/json"},
      body: jsonEncode(data),
    );
    return jsonDecode(response.body);
  }
  
  Future<Map<String, dynamic>> loginV2(String email, String password) async {
    final url = Uri.parse("$baseUrl/auth/v2/login");
    final response = await http.post(
      url,
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({
        "email": email,
        "password": password,
      }),
    );
    return jsonDecode(response.body);
  }
  
  Future<Map<String, dynamic>> checkEmailAutofill(String email) async {
    final url = Uri.parse("$baseUrl/auth/v2/check-email/$email");
    final response = await http.get(url);
    return jsonDecode(response.body);
  }
}
