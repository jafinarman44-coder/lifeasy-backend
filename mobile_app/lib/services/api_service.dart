import 'dart:async';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class ApiService {
  // PRODUCTION BACKEND (Render - for real users)
  static const String baseUrl = 'https://lifeasy-api.onrender.com/api';
  
  // LOCAL BACKEND (uncomment for development/testing only)
  // static const String baseUrl = 'http://192.168.0.181:8000/api';
  
  // Timeout configuration (30 seconds)
  static const Duration requestTimeout = Duration(seconds: 30);
  
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

    // Handle errors
    if (response.statusCode >= 200 && response.statusCode < 300) {
      try {
        return jsonDecode(response.body);
      } catch (e) {
        throw Exception('Invalid server response format');
      }
    } else {
      String errorMessage = 'Failed to send OTP';
      try {
        final errorData = jsonDecode(response.body);
        errorMessage = errorData['message'] ?? errorMessage;
      } catch (e) {
        errorMessage = 'Server error: ${response.statusCode}';
      }
      throw Exception(errorMessage);
    }
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

    // Handle errors
    if (response.statusCode >= 200 && response.statusCode < 300) {
      try {
        return jsonDecode(response.body);
      } catch (e) {
        throw Exception('Invalid server response format');
      }
    } else {
      String errorMessage = 'Failed to verify OTP';
      try {
        final errorData = jsonDecode(response.body);
        errorMessage = errorData['message'] ?? errorMessage;
      } catch (e) {
        errorMessage = 'Server error: ${response.statusCode}';
      }
      throw Exception(errorMessage);
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
    
    if (response.statusCode >= 200 && response.statusCode < 300) {
      try {
        return jsonDecode(response.body);
      } catch (e) {
        throw Exception('Invalid server response format');
      }
    } else {
      String errorMessage = 'Registration failed';
      try {
        final errorData = jsonDecode(response.body);
        errorMessage = errorData['message'] ?? errorMessage;
      } catch (e) {
        errorMessage = 'Server error: ${response.statusCode}';
      }
      throw Exception(errorMessage);
    }
  }
  
  Future<Map<String, dynamic>> registerVerify(Map<String, dynamic> data) async {
    final url = Uri.parse("$baseUrl/auth/v2/register-verify");
    
    final response = await http.post(
      url,
      headers: {"Content-Type": "application/json"},
      body: jsonEncode(data),
    );
    
    if (response.statusCode >= 200 && response.statusCode < 300) {
      try {
        return jsonDecode(response.body);
      } catch (e) {
        throw Exception('Invalid server response format');
      }
    } else {
      String errorMessage = 'Verification failed';
      try {
        final errorData = jsonDecode(response.body);
        errorMessage = errorData['message'] ?? errorMessage;
      } catch (e) {
        errorMessage = 'Server error: ${response.statusCode}';
      }
      throw Exception(errorMessage);
    }
  }
  
  Future<Map<String, dynamic>> loginV2(String email, String password) async {
    final url = Uri.parse("$baseUrl/auth/v2/login");
    
    try {
      final response = await http.post(
        url,
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({
          "email": email,
          "password": password,
        }),
      );
      
      // Check if response is successful
      if (response.statusCode >= 200 && response.statusCode < 300) {
        // Try to parse JSON
        try {
          return jsonDecode(response.body);
        } catch (e) {
          throw Exception('Invalid server response format');
        }
      } else {
        // Handle server errors
        String errorMessage = 'Server error';
        try {
          final errorData = jsonDecode(response.body);
          errorMessage = errorData['message'] ?? errorMessage;
        } catch (e) {
          // If can't parse JSON, use status text
          errorMessage = 'Server error: ${response.statusCode} ${response.reasonPhrase}';
        }
        throw Exception(errorMessage);
      }
    } catch (e) {
      if (e is Exception) rethrow;
      throw Exception('Network error: ${e.toString()}');
    }
  }
  
  Future<Map<String, dynamic>> checkEmailAutofill(String email) async {
    final url = Uri.parse("$baseUrl/auth/v2/check-email/$email");
    
    try {
      final response = await http.get(url).timeout(requestTimeout);
      
      if (response.statusCode >= 200 && response.statusCode < 300) {
        try {
          return jsonDecode(response.body);
        } catch (e) {
          throw Exception('Invalid server response format');
        }
      } else {
        throw Exception('Server error: ${response.statusCode}');
      }
    } catch (e) {
      print('API ERROR - checkEmailAutofill: ${e.toString()}');
      rethrow;
    }
  }
  
  // -----------------------------
  // MOBILE TENANT APPROVAL
  // -----------------------------
  Future<Map<String, dynamic>> approveTenant(String tenantId, {String? token}) async {
    final url = Uri.parse("$baseUrl/tenants/approve/$tenantId");
    
    try {
      final headers = {
        'Content-Type': 'application/json',
        if (token != null) 'Authorization': 'Bearer $token',
      };
      
      // DEBUG LOG
      print('🔵 CALLING: POST $url');
      print('🔵 HEADERS: $headers');
      
      final response = await http.post(
        url,
        headers: headers,
      ).timeout(requestTimeout);
      
      // DEBUG LOG
      print('🟢 RESPONSE STATUS: ${response.statusCode}');
      print('🟢 RESPONSE BODY: ${response.body}');
      
      if (response.statusCode >= 200 && response.statusCode < 300) {
        try {
          return jsonDecode(response.body);
        } catch (e) {
          throw Exception('Invalid server response format');
        }
      } else {
        String errorMessage = 'Failed to approve tenant';
        try {
          final errorData = jsonDecode(response.body);
          errorMessage = errorData['message'] ?? errorMessage;
          print('🔴 API ERROR DETAILS: $errorMessage');
        } catch (e) {
          errorMessage = 'Server error: ${response.statusCode} ${response.reasonPhrase}';
          print('🔴 HTTP ERROR: $errorMessage');
        }
        throw Exception(errorMessage);
      }
    } catch (e) {
      print('🔴 API ERROR - approveTenant: ${e.toString()}');
      if (e is TimeoutException) {
        throw Exception('Request timeout - please check your connection');
      }
      rethrow;
    }
  }
  
  // -----------------------------
  // GET ALL TENANTS (For Approval List)
  // -----------------------------
  Future<List<Map<String, dynamic>>> getAllTenants({String? token}) async {
    final url = Uri.parse("$baseUrl/tenants/all");
    
    try {
      final headers = {
        'Content-Type': 'application/json',
        if (token != null) 'Authorization': 'Bearer $token',
      };
      
      // DEBUG LOG
      print('🔵 CALLING: GET $url');
      
      final response = await http.get(
        url,
        headers: headers,
      ).timeout(requestTimeout);
      
      // DEBUG LOG
      print('🟢 RESPONSE: ${response.statusCode}');
      
      if (response.statusCode == 200) {
        List<dynamic> data = jsonDecode(response.body);
        print('🟢 SUCCESS: ${data.length} tenants retrieved');
        return data.map((item) => item as Map<String, dynamic>).toList();
      } else {
        print('🔴 ERROR: Failed to load tenants - Status ${response.statusCode}');
        throw Exception('Failed to load tenants');
      }
    } catch (e) {
      print('🔴 API ERROR - getAllTenants: ${e.toString()}');
      if (e is TimeoutException) {
        throw Exception('Request timeout - please check your connection');
      }
      rethrow;
    }
  }
}
