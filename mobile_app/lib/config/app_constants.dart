/// LIFEASY V27 - Backend Configuration
/// Centralized configuration for all backend services

class AppConstants {
  // ==================== BACKEND URLs ====================
  
  // PRODUCTION BACKEND (Railway - For users on DIFFERENT networks)
  static const String backendHost = 'lifeasy-backend-production.up.railway.app';
  static const int backendPort = 8080;
  
  // LOCAL TESTING (Comment out when deploying)
  // static const String backendHost = 'lifeasy-backend-production.up.railway.app';
  // static const int backendPort = 8000;
  
  // Full API URL
  static const String baseUrl = 'https://$backendHost/api';  // HTTPS for production
  
  // WebSocket URLs
  static const String wsProtocol = 'wss';  // Secure WebSocket for production
  static const String wsBaseUrl = '$wsProtocol://$backendHost';
  
  // ==================== API ENDPOINTS ====================
  
  // Authentication
  static const String authLogin = '$baseUrl/auth/v2/login';
  static const String authRegisterRequest = '$baseUrl/auth/v2/register-request';
  static const String authRegisterVerify = '$baseUrl/auth/v2/register-verify';
  static const String authCheckEmail = '$baseUrl/auth/v2/check-email';
  static const String authForgotPassword = '$baseUrl/auth/v2/forgot-password';
  static const String authResetPassword = '$baseUrl/auth/v2/reset-password';
  
  // OTP
  static const String otpSend = '$baseUrl/otp/send';
  static const String otpVerify = '$baseUrl/otp/verify';
  
  // Tenants
  static const String tenantsAll = '$baseUrl/tenants/all';
  static const String tenantsApprove = '$baseUrl/tenants/approve';
  
  // Bills
  static const String billsTenant = '$baseUrl/bills/tenant';
  
  // Payments
  static const String paymentsTenant = '$baseUrl/payments/tenant';
  static const String pay = '$baseUrl/pay';
  
  // Chat
  static const String chatV2 = '$baseUrl/chat/v2/ws';
  static const String chatV3 = '$baseUrl/chat/v3/ws';
  
  // Calls
  static const String callV2 = '$baseUrl/call/v2/ws';
  
  // ==================== WEBSOCKET CONFIG ====================
  
  static String getChatWebSocketUrl(String tenantId, String buildingId, {bool isV3 = false}) {
    final basePath = isV3 ? chatV3 : chatV2;
    return '$basePath/$tenantId/$buildingId';
  }
  
  static String getCallWebSocketUrl(String tenantId) {
    return '$callV2/$tenantId';
  }
  
  // ==================== TIMEOUTS ====================
  
  static const Duration requestTimeout = Duration(seconds: 30);
  static const Duration socketTimeout = Duration(seconds: 10);
  static const Duration reconnectDelay = Duration(seconds: 2);
  
  // ==================== STORAGE KEYS ====================
  
  static const String keyAuthToken = 'auth_token_v2';
  static const String keyTenantId = 'tenant_id_v2';
  static const String keyTenantName = 'tenant_name_v2';
  static const String keyRememberedEmails = 'remembered_emails';
  static const String keyRememberMe = 'remember_me';
  static const String keySavedPassword = 'saved_password';
  
  // ==================== APP SETTINGS ====================
  
  static const String appName = 'LIFEASY V27';
  static const String appVersion = '1.0.0';
  
  // Maximum remembered emails
  static const int maxRememberedEmails = 5;
  
  // ==================== DEFAULT VALUES ====================
  
  static const int defaultBuildingId = 1;
  static const String defaultAvatarUrl = '';
  
  // ==================== HELPERS ====================
  
  /// Check if using production backend
  static bool get isProduction => backendHost.contains('railway.app') || backendHost.contains('render.com');
  
  /// Get base URL without /api suffix
  static String get baseDomain => 'https://$backendHost';
}
