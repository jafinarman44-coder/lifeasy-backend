import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class ApiService {
  // Render Cloud API Server
  static const String baseUrl = 'https://lifeasy-api.onrender.com/api';
  
  Future<Map<String, String>> _getHeaders() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('token');
    
    return {
      'Content-Type': 'application/json',
      if (token != null) 'Authorization': 'Bearer $token',
    };
  }
  
  // Login - Tenant ID & Password Authentication
  Future<Map<String, dynamic>> login(String tenantId, String password) async {
    try {
      print('🔐 LOGIN REQUEST: Tenant ID = $tenantId');
      final response = await http.post(
        Uri.parse('$baseUrl/login'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'tenant_id': tenantId,
          'password': password,
        }),
      );
      
      print('📥 LOGIN RESPONSE STATUS: ${response.statusCode}');
      print('📥 LOGIN RESPONSE BODY: ${response.body}');
      
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        
        // Critical validation - must have access_token
        if (data['access_token'] == null) {
          print('❌ INVALID LOGIN RESPONSE: No access_token');
          throw Exception("Invalid login response");
        }
        
        print('✅ LOGIN SUCCESS');
        return data;
      } else {
        final error = jsonDecode(response.body);
        print('❌ LOGIN FAILED: ${error['detail']}');
        throw Exception(error['detail'] ?? 'Login failed');
      }
    } catch (e) {
      print('❌ LOGIN ERROR: ${e.toString()}');
      rethrow;
    }
  }
  
  // Send OTP
  Future<Map<String, dynamic>> sendOTP(String phone) async {
    try {
      print('📱 SEND OTP REQUEST: $phone');
      final response = await http.post(
        Uri.parse('$baseUrl/send-otp'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'phone': phone}),
      );
      
      print('📥 OTP RESPONSE STATUS: ${response.statusCode}');
      
      // Critical: Must return 200 for success
      if (response.statusCode != 200) {
        print('❌ OTP SEND FAILED: Status ${response.statusCode}');
        throw Exception("OTP send failed");
      }
      
      final data = jsonDecode(response.body);
      print('✅ OTP SENT SUCCESSFULLY');
      return data;
    } catch (e) {
      print('❌ OTP ERROR: ${e.toString()}');
      rethrow;
    }
  }
  
  // Verify OTP
  Future<Map<String, dynamic>> verifyOTP(String phone, String otp) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/verify-otp'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'phone': phone,
          'otp': otp,
        }),
      );
      
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Invalid OTP');
      }
    } catch (e) {
      rethrow;
    }
  }
  
  // Register
  Future<Map<String, dynamic>> register(String phone, String password, String? name) async {
    try {
      print('📝 REGISTER REQUEST: $phone, Name: $name');
      final response = await http.post(
        Uri.parse('$baseUrl/register'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'phone': phone,
          'password': password,
          if (name != null) 'name': name,
        }),
      );
      
      print('📥 REGISTER RESPONSE STATUS: ${response.statusCode}');
      print('📥 REGISTER RESPONSE BODY: ${response.body}');
      
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        
        // Critical validation - must have access_token
        if (data['access_token'] == null) {
          print('❌ INVALID REGISTRATION RESPONSE: No access_token');
          throw Exception("Registration failed");
        }
        
        print('✅ REGISTRATION SUCCESS');
        return data;
      } else {
        final error = jsonDecode(response.body);
        print('❌ REGISTRATION FAILED: ${error['detail']}');
        throw Exception(error['detail'] ?? 'Registration failed');
      }
    } catch (e) {
      print('❌ REGISTER ERROR: ${e.toString()}');
      rethrow;
    }
  }
  
  // Get Dashboard Data
  Future<Map<String, dynamic>> getDashboard(String tenantId) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/dashboard/$tenantId'),
      );
      
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Failed to load dashboard');
      }
    } catch (e) {
      rethrow;
    }
  }
  
  // Get Tenant Profile
  Future<Map<String, dynamic>> getTenantProfile(String tenantId) async {
    try {
      final headers = await _getHeaders();
      final response = await http.get(
        Uri.parse('$baseUrl/tenants/$tenantId'),
        headers: headers,
      );
      
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Failed to load profile');
      }
    } catch (e) {
      rethrow;
    }
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
  
  // Create Payment (bKash/Nagad)
  Future<Map<String, dynamic>> createPayment({
    required String tenant_id,
    required double amount,
    required String description,
    required String payment_method,
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/payment/create'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'tenant_id': tenant_id,
          'amount': amount,
          'description': description,
          'payment_method': payment_method,
        }),
      );
      
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        final error = jsonDecode(response.body);
        throw Exception(error['detail'] ?? 'Payment creation failed');
      }
    } catch (e) {
      rethrow;
    }
  }
  
  // Execute Payment
  Future<Map<String, dynamic>> executePayment(String paymentId, String transactionId) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/payment/execute'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'payment_id': paymentId,
          'transaction_id': transactionId,
        }),
      );
      
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        final error = jsonDecode(response.body);
        throw Exception(error['detail'] ?? 'Payment execution failed');
      }
    } catch (e) {
      rethrow;
    }
  }
  
  // Get Payment Status
  Future<Map<String, dynamic>> getPaymentStatus(String paymentId) async {
    try {
      final headers = await _getHeaders();
      final response = await http.get(
        Uri.parse('$baseUrl/payment/status/$paymentId'),
        headers: headers,
      );
      
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Failed to get payment status');
      }
    } catch (e) {
      rethrow;
    }
  }
}
