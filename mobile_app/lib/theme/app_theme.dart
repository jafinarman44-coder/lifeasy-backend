import 'package:flutter/material.dart';

/// LIFEASY V27 - App Theme Configuration
/// Professional, consistent branding across the entire app

class AppTheme {
  // ==================== BRAND COLORS ====================
  
  // Primary Colors
  static const Color primaryBlue = Color(0xFF3B82F6);
  static const Color primaryBlueDark = Color(0xFF2563EB);
  static const Color primaryBlueLight = Color(0xFF60A5FA);
  
  // Accent Colors
  static const Color accentGreen = Color(0xFF10B981);
  static const Color accentGreenLight = Color(0xFF34D399);
  static const Color accentOrange = Color(0xFFF59E0B);
  static const Color accentRed = Color(0xFFEF4444);
  static const Color accentPurple = Color(0xFF8B5CF6);
  
  // Background Colors
  static const Color bgDark = Color(0xFF0F172A);
  static const Color bgDarker = Color(0xFF020617);
  static const Color bgCard = Color(0xFF1E293B);
  static const Color bgCardLight = Color(0xFF334155);
  
  // Text Colors
  static const Color textPrimary = Color(0xFFF8FAFC);
  static const Color textSecondary = Color(0xFF94A3B8);
  static const Color textMuted = Color(0xFF64748B);
  
  // Border & Divider Colors
  static const Color divider = Color(0xFF334155);
  static const Color border = Color(0xFF475569);
  
  // Gradient Presets
  static const LinearGradient primaryGradient = LinearGradient(
    begin: Alignment.topCenter,
    end: Alignment.bottomCenter,
    colors: [bgDark, bgDarker],
  );
  
  static const LinearGradient blueGradient = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [primaryBlue, primaryBlueDark],
  );
  
  static const LinearGradient cardGradient = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [bgCard, bgCardLight],
  );
  
  // ==================== TEXT STYLES ====================
  
  static const TextStyle heading1 = TextStyle(
    fontSize: 32,
    fontWeight: FontWeight.bold,
    color: textPrimary,
    letterSpacing: -0.5,
  );
  
  static const TextStyle heading2 = TextStyle(
    fontSize: 24,
    fontWeight: FontWeight.bold,
    color: textPrimary,
    letterSpacing: -0.3,
  );
  
  static const TextStyle heading3 = TextStyle(
    fontSize: 20,
    fontWeight: FontWeight.bold,
    color: textPrimary,
  );
  
  static const TextStyle subtitle = TextStyle(
    fontSize: 16,
    fontWeight: FontWeight.w500,
    color: textSecondary,
  );
  
  static const TextStyle bodyText = TextStyle(
    fontSize: 14,
    color: textPrimary,
  );
  
  static const TextStyle caption = TextStyle(
    fontSize: 12,
    color: textMuted,
  );
  
  // ==================== COMPONENT THEMES ====================
  
  // AppBar Theme
  static AppBarTheme appBarTheme = AppBarTheme(
    backgroundColor: primaryBlue,
    foregroundColor: textPrimary,
    elevation: 0,
    centerTitle: false,
    titleTextStyle: const TextStyle(
      fontSize: 20,
      fontWeight: FontWeight.bold,
      color: textPrimary,
    ),
    iconTheme: const IconThemeData(color: textPrimary),
  );
  
  // Card Theme
  static CardThemeData cardTheme = CardThemeData(
    color: bgCard,
    elevation: 2,
    shadowColor: Colors.black26,
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular(12),
    ),
    margin: const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
  );
  
  // Button Theme - Primary
  static ButtonStyle primaryButtonStyle = ElevatedButton.styleFrom(
    backgroundColor: primaryBlue,
    foregroundColor: textPrimary,
    padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 14),
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular(12),
    ),
    elevation: 2,
    textStyle: const TextStyle(
      fontSize: 16,
      fontWeight: FontWeight.w600,
    ),
  );
  
  // Button Theme - Secondary
  static ButtonStyle secondaryButtonStyle = OutlinedButton.styleFrom(
    foregroundColor: primaryBlue,
    side: const BorderSide(color: primaryBlue, width: 2),
    padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 14),
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular(12),
    ),
    textStyle: const TextStyle(
      fontSize: 16,
      fontWeight: FontWeight.w600,
    ),
  );
  
  // Input Decoration Theme
  static InputDecorationTheme inputDecorationTheme = InputDecorationTheme(
    filled: true,
    fillColor: bgCard,
    contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
    border: OutlineInputBorder(
      borderRadius: BorderRadius.circular(12),
      borderSide: const BorderSide(color: border),
    ),
    enabledBorder: OutlineInputBorder(
      borderRadius: BorderRadius.circular(12),
      borderSide: const BorderSide(color: border),
    ),
    focusedBorder: OutlineInputBorder(
      borderRadius: BorderRadius.circular(12),
      borderSide: const BorderSide(color: primaryBlue, width: 2),
    ),
    errorBorder: OutlineInputBorder(
      borderRadius: BorderRadius.circular(12),
      borderSide: const BorderSide(color: accentRed),
    ),
    labelStyle: const TextStyle(color: textSecondary),
    hintStyle: const TextStyle(color: textMuted),
  );
  
  // FAB Theme
  static FloatingActionButtonThemeData fabTheme = FloatingActionButtonThemeData(
    backgroundColor: primaryBlue,
    foregroundColor: textPrimary,
    elevation: 4,
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular(16),
    ),
  );
  
  // Bottom Sheet Theme
  static BottomSheetThemeData bottomSheetTheme = BottomSheetThemeData(
    backgroundColor: bgCard,
    shape: const RoundedRectangleBorder(
      borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
    ),
  );
  
  // Dialog Theme
  static DialogThemeData dialogTheme = DialogThemeData(
    backgroundColor: bgCard,
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular(16),
    ),
    titleTextStyle: heading3,
    contentTextStyle: bodyText,
  );
  
  // ==================== SNACKBAR STYLES ====================
  
  static SnackBarThemeData snackBarTheme = SnackBarThemeData(
    backgroundColor: bgCard,
    contentTextStyle: const TextStyle(color: textPrimary, fontSize: 14),
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular(12),
    ),
    behavior: SnackBarBehavior.floating,
    actionTextColor: primaryBlueLight,
  );
  
  // ==================== HELPER METHODS ====================
  
  /// Get status color based on status text
  static Color getStatusColor(String status) {
    switch (status.toLowerCase()) {
      case 'online':
      case 'active':
      case 'paid':
        return accentGreen;
      case 'away':
      case 'pending':
        return accentOrange;
      case 'offline':
      case 'inactive':
      case 'unpaid':
      case 'rejected':
        return accentRed;
      default:
        return textMuted;
    }
  }
  
  /// Get priority color
  static Color getPriorityColor(String priority) {
    switch (priority.toLowerCase()) {
      case 'high':
      case 'urgent':
        return accentRed;
      case 'medium':
        return accentOrange;
      case 'low':
        return accentGreen;
      default:
        return textMuted;
    }
  }
  
  /// Create a shimmer loading effect gradient
  static LinearGradient getShimmerGradient() {
    return const LinearGradient(
      begin: Alignment.centerLeft,
      end: Alignment.centerRight,
      colors: [
        bgCard,
        bgCardLight,
        bgCard,
      ],
      stops: [0.0, 0.5, 1.0],
    );
  }
  
  /// Box shadow for elevated cards
  static List<BoxShadow> getCardShadow() {
    return [
      BoxShadow(
        color: Colors.black.withOpacity(0.25),
        blurRadius: 12,
        offset: const Offset(0, 4),
      ),
    ];
  }
  
  /// Box shadow for buttons
  static List<BoxShadow> getButtonShadow() {
    return [
      BoxShadow(
        color: primaryBlue.withOpacity(0.3),
        blurRadius: 8,
        offset: const Offset(0, 2),
      ),
    ];
  }
  
  /// Build complete app theme
  static ThemeData get theme {
    return ThemeData.dark().copyWith(
      // Core colors
      scaffoldBackgroundColor: bgDark,
      primaryColor: primaryBlue,
      colorScheme: const ColorScheme.dark(
        primary: primaryBlue,
        secondary: accentGreen,
        surface: bgCard,
        error: accentRed,
      ),
      
      // Typography
      textTheme: const TextTheme(
        displayLarge: heading1,
        displayMedium: heading2,
        displaySmall: heading3,
        bodyLarge: bodyText,
        bodyMedium: bodyText,
        labelLarge: subtitle,
      ),
      
      // Component themes
      appBarTheme: appBarTheme,
      cardTheme: cardTheme,
      elevatedButtonTheme: ElevatedButtonThemeData(style: primaryButtonStyle),
      outlinedButtonTheme: OutlinedButtonThemeData(style: secondaryButtonStyle),
      inputDecorationTheme: inputDecorationTheme,
      floatingActionButtonTheme: fabTheme,
      bottomSheetTheme: bottomSheetTheme,
      dialogTheme: dialogTheme,
      snackBarTheme: snackBarTheme,
      
      // Icon theme
      iconTheme: const IconThemeData(
        color: textSecondary,
        size: 24,
      ),
      
      // Divider theme
      dividerTheme: const DividerThemeData(
        color: divider,
        thickness: 1,
        space: 1,
      ),
    );
  }
}
