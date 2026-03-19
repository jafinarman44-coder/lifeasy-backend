import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';
import 'dart:async';
import '../services/api_service.dart';

class PaymentWebViewScreen extends StatefulWidget {
  final String paymentUrl;
  final String paymentId;
  final String transactionId;
  final double amount;
  final String paymentMethod;

  const PaymentWebViewScreen({
    super.key,
    required this.paymentUrl,
    required this.paymentId,
    required this.transactionId,
    required this.amount,
    required this.paymentMethod,
  });

  @override
  State<PaymentWebViewScreen> createState() => _PaymentWebViewScreenState();
}

class _PaymentWebViewScreenState extends State<PaymentWebViewScreen> {
  late final WebViewController _controller;
  bool _isLoading = true;
  bool _paymentCompleted = false;
  String _currentUrl = '';

  @override
  void initState() {
    super.initState();

    _controller = WebViewController()
      ..setJavaScriptMode(JavaScriptMode.unrestricted)
      ..setBackgroundColor(const Color(0x00000000))
      ..setNavigationDelegate(
        NavigationDelegate(
          onPageStarted: (String url) {
            setState(() {
              _currentUrl = url;
              _isLoading = true;
            });
          },
          onPageFinished: (String url) async {
            setState(() {
              _isLoading = false;
            });

            // Check if payment completed (callback URL)
            if (url.contains('/callback/')) {
              await _handlePaymentCallback(url);
            }
          },
          onHttpError: (HttpResponseError error) {
            print('HTTP error: ${error.statusCode}');
          },
          onWebResourceError: (WebResourceError error) {
            print('Web resource error: ${error.description}');
          },
        ),
      )
      ..addJavaScriptChannel(
        'PaymentComplete',
        onMessageReceived: (JavaScriptMessage message) {
          _handleWebViewPaymentComplete(message.message);
        },
      )
      ..loadRequest(Uri.parse(widget.paymentUrl));
  }

  Future<void> _handlePaymentCallback(String url) async {
    // Extract transaction ID from URL
    final uri = Uri.parse(url);
    final transactionId = uri.queryParameters['transactionId'] ?? widget.transactionId;
    
    try {
      final apiService = ApiService();
      final result = await apiService.executePayment(
        widget.paymentId,
        transactionId,
      );

      if (mounted && !_paymentCompleted) {
        setState(() {
          _paymentCompleted = true;
        });

        showDialog(
          context: context,
          builder: (context) => AlertDialog(
            title: const Text('Payment Status'),
            content: Text(result['message'] ?? 'Payment completed successfully!'),
            actions: [
              TextButton(
                onPressed: () {
                  Navigator.pop(context); // Close dialog
                  Navigator.pop(context, {'success': true}); // Return to previous screen
                },
                child: const Text('OK'),
              ),
            ],
          ),
        );
      }
    } catch (e) {
      print('Payment callback error: $e');
    }
  }

  void _handleWebViewPaymentComplete(String message) {
    // Handle JavaScript callback from WebView
    print('Payment complete message: $message');
    
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Payment Completed'),
        content: const Text('Your payment has been processed successfully!'),
        actions: [
          TextButton(
            onPressed: () {
              Navigator.pop(context);
              Navigator.pop(context, {'success': true});
            },
            child: const Text('OK'),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              '${widget.paymentMethod.toUpperCase()} Payment',
              style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
            ),
            Text(
              '৳${widget.amount.toStringAsFixed(2)}',
              style: const TextStyle(fontSize: 12, color: Colors.white70),
            ),
          ],
        ),
        backgroundColor: widget.paymentMethod == 'bkash' 
            ? const Color(0xFFE2136E) 
            : const Color(0xFFFF6B00),
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.close),
          onPressed: () {
            showDialog(
              context: context,
              builder: (context) => AlertDialog(
                title: const Text('Cancel Payment'),
                content: const Text('Are you sure you want to cancel this payment?'),
                actions: [
                  TextButton(
                    onPressed: () => Navigator.pop(context),
                    child: const Text('No'),
                  ),
                  TextButton(
                    onPressed: () {
                      Navigator.pop(context);
                      Navigator.pop(context, {'success': false});
                    },
                    child: const Text('Yes, Cancel'),
                  ),
                ],
              ),
            );
          },
        ),
      ),
      body: Stack(
        children: [
          WebViewWidget(controller: _controller),
          
          // Loading indicator
          if (_isLoading)
            Container(
              color: Colors.black.withOpacity(0.7),
              child: Center(
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    const CircularProgressIndicator(
                      valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                    ),
                    const SizedBox(height: 20),
                    Text(
                      'Loading ${widget.paymentMethod.toUpperCase()}...',
                      style: const TextStyle(
                        color: Colors.white,
                        fontSize: 16,
                      ),
                    ),
                  ],
                ),
              ),
            ),
          
          // Payment completed overlay
          if (_paymentCompleted)
            Container(
              color: Colors.black.withOpacity(0.8),
              child: const Center(
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Icon(
                      Icons.check_circle,
                      size: 80,
                      color: Colors.green,
                    ),
                    SizedBox(height: 20),
                    Text(
                      'Payment Completed!',
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 24,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ],
                ),
              ),
            ),
        ],
      ),
    );
  }
}

// ============================================
// 💳 PAYMENT SCREEN WITH WEBVIEW INTEGRATION
// ============================================
class PaymentScreenPro extends StatefulWidget {
  final String tenantId;

  const PaymentScreenPro({super.key, required this.tenantId});

  @override
  State<PaymentScreenPro> createState() => _PaymentScreenProState();
}

class _PaymentScreenProState extends State<PaymentScreenPro> {
  final _amountController = TextEditingController();
  bool _isLoading = false;
  String _selectedMethod = 'bkash'; // bkash or nagad

  Future<void> _initiatePayment() async {
    if (_amountController.text.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Please enter amount')),
      );
      return;
    }

    final amount = double.tryParse(_amountController.text);
    if (amount == null || amount <= 0) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Please enter valid amount')),
      );
      return;
    }

    setState(() => _isLoading = true);

    try {
      final apiService = ApiService();
      
      // Create payment
      final result = await apiService.createPayment(
        tenant_id: widget.tenantId,
        amount: amount,
        description: 'Rent Payment',
        payment_method: _selectedMethod,
      );

      if (mounted) {
        setState(() => _isLoading = false);

        // Open WebView for payment
        final paymentResult = await Navigator.push(
          context,
          MaterialPageRoute(
            builder: (_) => PaymentWebViewScreen(
              paymentUrl: result['payment_url'],
              paymentId: result['payment_id'],
              transactionId: result['transaction_id'],
              amount: amount,
              paymentMethod: _selectedMethod,
            ),
          ),
        );

        // Handle payment result
        if (paymentResult != null && paymentResult['success'] == true) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text('Payment successful!'),
              backgroundColor: Colors.green,
            ),
          );
        }
      }
    } catch (e) {
      if (mounted) {
        setState(() => _isLoading = false);
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Payment failed: ${e.toString()}'),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Make Payment'),
        backgroundColor: _selectedMethod == 'bkash' 
            ? const Color(0xFFE2136E) 
            : const Color(0xFFFF6B00),
        elevation: 0,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Payment Method Selection
            const Text(
              'Select Payment Method:',
              style: TextStyle(
                color: Colors.white,
                fontSize: 16,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 15),
            Row(
              children: [
                Expanded(
                  child: ChoiceChip(
                    label: Row(
                      children: [
                        Container(
                          width: 20,
                          height: 20,
                          decoration: BoxDecoration(
                            color: const Color(0xFFE2136E),
                            borderRadius: BorderRadius.circular(4),
                          ),
                          child: const Icon(Icons.payment, size: 14, color: Colors.white),
                        ),
                        const SizedBox(width: 8),
                        const Text('bKash'),
                      ],
                    ),
                    selected: _selectedMethod == 'bkash',
                    onSelected: (selected) {
                      setState(() => _selectedMethod = 'bkash');
                    },
                    backgroundColor: Colors.grey[800],
                    selectedColor: const Color(0xFFE2136E),
                    labelStyle: TextStyle(
                      color: _selectedMethod == 'bkash' ? Colors.white : Colors.grey,
                    ),
                  ),
                ),
                const SizedBox(width: 10),
                Expanded(
                  child: ChoiceChip(
                    label: Row(
                      children: [
                        Container(
                          width: 20,
                          height: 20,
                          decoration: BoxDecoration(
                            color: const Color(0xFFFF6B00),
                            borderRadius: BorderRadius.circular(4),
                          ),
                          child: const Icon(Icons.payment, size: 14, color: Colors.white),
                        ),
                        const SizedBox(width: 8),
                        const Text('Nagad'),
                      ],
                    ),
                    selected: _selectedMethod == 'nagad',
                    onSelected: (selected) {
                      setState(() => _selectedMethod = 'nagad');
                    },
                    backgroundColor: Colors.grey[800],
                    selectedColor: const Color(0xFFFF6B00),
                    labelStyle: TextStyle(
                      color: _selectedMethod == 'nagad' ? Colors.white : Colors.grey,
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 30),
            
            // Amount Input
            TextField(
              controller: _amountController,
              style: const TextStyle(color: Colors.white, fontSize: 20),
              decoration: InputDecoration(
                labelText: 'Amount (BDT)',
                hintText: '৳ 1000',
                labelStyle: const TextStyle(color: Colors.grey),
                prefixIcon: const Icon(Icons.attach_money, color: Colors.green),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
                enabledBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                  borderSide: const BorderSide(color: Colors.grey),
                ),
                focusedBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                  borderSide: BorderSide(color: _selectedMethod == 'bkash' 
                      ? const Color(0xFFE2136E) 
                      : const Color(0xFFFF6B00)),
                ),
              ),
              keyboardType: TextInputType.number,
            ),
            const SizedBox(height: 30),
            
            // Payment Info
            Container(
              padding: const EdgeInsets.all(15),
              decoration: BoxDecoration(
                color: Colors.blue.withOpacity(0.1),
                borderRadius: BorderRadius.circular(10),
                border: Border.all(color: Colors.blue.withOpacity(0.3)),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Row(
                    children: [
                      Icon(Icons.info_outline, color: Colors.blue, size: 20),
                      SizedBox(width: 10),
                      Text(
                        'Secure Payment',
                        style: TextStyle(
                          color: Colors.blue,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 10),
                  const Text(
                    '• You will be redirected to secure payment gateway',
                    style: TextStyle(color: Colors.grey, fontSize: 12),
                  ),
                  const SizedBox(height: 5),
                  const Text(
                    '• All transactions are encrypted and secure',
                    style: TextStyle(color: Colors.grey, fontSize: 12),
                  ),
                  const SizedBox(height: 5),
                  const Text(
                    '• Payment confirmation will be shown after completion',
                    style: TextStyle(color: Colors.grey, fontSize: 12),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 30),
            
            // Pay Button
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: _isLoading ? null : _initiatePayment,
                style: ElevatedButton.styleFrom(
                  backgroundColor: _selectedMethod == 'bkash' 
                      ? const Color(0xFFE2136E) 
                      : const Color(0xFFFF6B00),
                  padding: const EdgeInsets.symmetric(vertical: 18),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),
                child: _isLoading
                    ? const CircularProgressIndicator(color: Colors.white)
                    : Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          const Icon(Icons.payment, color: Colors.white),
                          const SizedBox(width: 10),
                          Text(
                            'PAY NOW - ৳${_amountController.text.isEmpty ? "0" : _amountController.text}',
                            style: const TextStyle(fontSize: 18, color: Colors.white),
                          ),
                        ],
                      ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  @override
  void dispose() {
    _amountController.dispose();
    super.dispose();
  }
}
