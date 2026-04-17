import 'package:flutter/material.dart';

class IncomingCallPopup extends StatefulWidget {
  final String callerId;
  final String callerName;
  final String callType;  // 'audio' or 'video'
  final Function(String) onAccept;
  final Function(String) onDecline;
  
  const IncomingCallPopup({
    Key? key,
    required this.callerId,
    required this.callerName,
    required this.callType,
    required this.onAccept,
    required this.onDecline,
  }) : super(key: key);

  @override
  _IncomingCallPopupState createState() => _IncomingCallPopupState();
}

class _IncomingCallPopupState extends State<IncomingCallPopup> {
  int _ringDuration = 0;
  
  @override
  void initState() {
    super.initState();
    _startRingTimer();
  }
  
  void _startRingTimer() {
    Future.delayed(Duration(seconds: 1), () {
      if (mounted) {
        setState(() {
          _ringDuration++;
        });
        _startRingTimer();
      }
    });
  }
  
  @override
  Widget build(BuildContext context) {
    return Dialog(
      backgroundColor: Colors.transparent,
      child: Container(
        padding: EdgeInsets.all(24),
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [Color(0xff0f172a), Colors.black87],
          ),
          borderRadius: BorderRadius.circular(20),
          border: Border.all(color: Colors.blueAccent, width: 2),
        ),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            // Animated ring indicator
            Container(
              padding: EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: Colors.blueAccent.withOpacity(0.2),
                shape: BoxShape.circle,
              ),
              child: Stack(
                alignment: Alignment.center,
                children: [
                  // Pulsing rings
                  TweenAnimationBuilder(
                    tween: Tween<double>(begin: 0.0, end: 1.0),
                    duration: Duration(seconds: 1),
                    builder: (context, value, child) {
                      return Container(
                        width: 100 + (value * 20),
                        height: 100 + (value * 20),
                        decoration: BoxDecoration(
                          shape: BoxShape.circle,
                          border: Border.all(
                            color: Colors.blueAccent.withOpacity(0.3 * (1 - value)),
                            width: 2,
                          ),
                        ),
                      );
                    },
                    onEnd: () {
                      if (mounted) {
                        _startRingTimer();
                      }
                    },
                  ),
                  // Caller avatar
                  CircleAvatar(
                    radius: 40,
                    backgroundColor: Colors.blueAccent,
                    child: Text(
                      widget.callerName.substring(0, 1).toUpperCase(),
                      style: TextStyle(
                        fontSize: 40,
                        fontWeight: FontWeight.bold,
                        color: Colors.white,
                      ),
                    ),
                  ),
                ],
              ),
            ),
            
            SizedBox(height: 24),
            
            // Caller name
            Text(
              widget.callerName,
              style: TextStyle(
                color: Colors.white,
                fontSize: 24,
                fontWeight: FontWeight.bold,
              ),
              textAlign: TextAlign.center,
            ),
            
            SizedBox(height: 8),
            
            // Call type
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(
                  widget.callType == 'video' 
                    ? Icons.videocam 
                    : Icons.phone,
                  color: Colors.orange,
                  size: 20,
                ),
                SizedBox(width: 8),
                Text(
                  widget.callType == 'video' 
                    ? 'Video Call' 
                    : 'Voice Call',
                  style: TextStyle(
                    color: Colors.orange,
                    fontSize: 16,
                  ),
                ),
              ],
            ),
            
            SizedBox(height: 8),
            
            // Ring duration
            Text(
              'Ringing for $_ringDuration seconds...',
              style: TextStyle(
                color: Colors.grey,
                fontSize: 14,
              ),
            ),
            
            SizedBox(height: 32),
            
            // Accept/Decline buttons
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                // Decline button
                Column(
                  children: [
                    CircleAvatar(
                      radius: 30,
                      backgroundColor: Colors.red,
                      child: IconButton(
                        icon: Icon(Icons.call_end, color: Colors.white, size: 28),
                        onPressed: () {
                          widget.onDecline(widget.callerId);
                          Navigator.pop(context);
                        },
                      ),
                    ),
                    SizedBox(height: 8),
                    Text(
                      'Decline',
                      style: TextStyle(color: Colors.red, fontSize: 14),
                    ),
                  ],
                ),
                
                // Accept button
                Column(
                  children: [
                    CircleAvatar(
                      radius: 30,
                      backgroundColor: Colors.green,
                      child: IconButton(
                        icon: Icon(
                          widget.callType == 'video' 
                            ? Icons.videocam 
                            : Icons.phone,
                          color: Colors.white, 
                          size: 28,
                        ),
                        onPressed: () {
                          widget.onAccept(widget.callerId);
                          Navigator.pop(context);
                        },
                      ),
                    ),
                    SizedBox(height: 8),
                    Text(
                      'Accept',
                      style: TextStyle(color: Colors.green, fontSize: 14),
                    ),
                  ],
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

/// Show incoming call dialog
void showIncomingCallDialog(
  BuildContext context, {
  required String callerId,
  required String callerName,
  required String callType,
  required Function(String) onAccept,
  required Function(String) onDecline,
}) {
  showDialog(
    context: context,
    barrierDismissible: false,
    builder: (context) => IncomingCallPopup(
      callerId: callerId,
      callerName: callerName,
      callType: callType,
      onAccept: onAccept,
      onDecline: onDecline,
    ),
  );
}
