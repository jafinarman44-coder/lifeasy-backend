import 'package:flutter/material.dart';
import 'package:agora_rtc_engine/agora_rtc_engine.dart';
import 'dart:async';

class RealVideoCallScreen extends StatefulWidget {
  final String tenantId;
  final String? receiverId;  // For tenant-to-tenant calls
  final String? receiverName;  // Display name
  
  RealVideoCallScreen({
    required this.tenantId,
    this.receiverId,  // Optional - defaults to owner/manager
    this.receiverName,  // Optional - defaults to "Building Manager"
  });
  
  @override
  _RealVideoCallScreenState createState() => _RealVideoCallScreenState();
}

class _RealVideoCallScreenState extends State<RealVideoCallScreen> {
  static const String appId = "8824dd55d0ce44c2873fa74acc730c5b"; // Your Agora App ID
  static const String token = ""; // Token can be empty for testing
  static const String channelName = "video-call-channel";
  
  RtcEngine? _engine;
  bool _isMuted = false;
  bool _isCameraOff = false;
  int _callDuration = 0;
  bool _isConnected = false;
  bool _remoteUserJoined = false;
  
  @override
  void initState() {
    super.initState();
    print('Video call initialized with receiverId: ${widget.receiverId ?? "Owner/Manager"}');
    _initializeAgora();
    _startCallTimer();
  }
  
  Future<void> _initializeAgora() async {
    try {
      // Create RTC engine
      _engine = createAgoraRtcEngine();
      await _engine!.initialize(const RtcEngineContext(
        appId: appId,
        channelProfile: ChannelProfileType.channelProfileCommunication,
      ));
      
      // Enable video
      await _engine!.enableVideo();
      await _engine!.setVideoEncoderConfiguration(
        const VideoEncoderConfiguration(
          dimensions: VideoDimensions(width: 640, height: 360),
          frameRate: 15,
          bitrate: 600,
        ),
      );
      
      // Set up event handlers
      _engine!.registerEventHandler(
        RtcEngineEventHandler(
          onJoinChannelSuccess: (connection, elapsed) {
            setState(() {
              _isConnected = true;
            });
            print("Successfully joined channel");
          },
          onUserJoined: (connection, remoteUid, elapsed) {
            setState(() {
              _remoteUserJoined = true;
            });
            print("Remote user joined: $remoteUid");
          },
          onUserOffline: (connection, remoteUid, reason) {
            setState(() {
              _remoteUserJoined = false;
            });
            print("Remote user left: $remoteUid");
          },
          onError: (err, msg) {
            print("Agora error: $err - $msg");
          },
        ),
      );
      
      // Join channel
      await _engine!.joinChannel(
        token: token,
        channelId: channelName,
        uid: 0, // Auto-assign UID
        options: const ChannelMediaOptions(
          clientRoleType: ClientRoleType.clientRoleBroadcaster,
          channelProfile: ChannelProfileType.channelProfileCommunication,
        ),
      );
      
    } catch (e) {
      print("Error initializing Agora: $e");
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Video call initialization failed')),
      );
    }
  }
  
  void _startCallTimer() {
    Future.delayed(Duration(seconds: 1), () {
      if (mounted && _isConnected) {
        setState(() {
          _callDuration++;
        });
        _startCallTimer();
      }
    });
  }
  
  String _formatDuration(int seconds) {
    int minutes = seconds ~/ 60;
    int secs = seconds % 60;
    return '${minutes.toString().padLeft(2, '0')}:${secs.toString().padLeft(2, '0')}';
  }
  
  Future<void> _toggleMute() async {
    if (_engine != null) {
      await _engine!.muteLocalAudioStream(!_isMuted);
      setState(() {
        _isMuted = !_isMuted;
      });
    }
  }
  
  Future<void> _toggleCamera() async {
    if (_engine != null) {
      await _engine!.muteLocalVideoStream(!_isCameraOff);
      setState(() {
        _isCameraOff = !_isCameraOff;
      });
    }
  }
  
  Future<void> _switchCamera() async {
    if (_engine != null) {
      await _engine!.switchCamera();
    }
  }
  
  Future<void> _endCall() async {
    if (_engine != null) {
      await _engine!.leaveChannel();
      await _engine!.release();
    }
    Navigator.pop(context);
  }
  
  @override
  void dispose() {
    _engine?.release();
    super.dispose();
  }
  
  @override
  Widget build(BuildContext context) {
    // Determine call title based on receiverId
    String callTitle = widget.receiverName ?? 'Building Manager';
    bool isTenantToTenant = widget.receiverId != null;
    
    return Scaffold(
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [Color(0xff0f172a), Colors.black87],
          ),
        ),
        child: Stack(
          children: [
            // Remote User Video (Full Screen)
            Positioned.fill(
              child: _remoteUserJoined
                  ? AgoraVideoView(
                      controller: VideoViewController(
                        rtcEngine: _engine!,
                        canvas: const VideoCanvas(uid: 0), // Show remote user
                      ),
                    )
                  : Center(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          CircleAvatar(
                            radius: 50,
                            backgroundColor: Colors.blueAccent,
                            child: Text(
                              callTitle.substring(0, 1).toUpperCase(),
                              style: TextStyle(
                                fontSize: 50,
                                fontWeight: FontWeight.bold,
                                color: Colors.white,
                              ),
                            ),
                          ),
                          SizedBox(height: 20),
                          Text(
                            'Waiting for $callTitle...',
                            style: TextStyle(color: Colors.grey, fontSize: 16),
                          ),
                          if (isTenantToTenant)
                            Padding(
                              padding: EdgeInsets.only(top: 10),
                              child: Text(
                                'Tenant-to-Tenant Call',
                                style: TextStyle(
                                  color: Colors.orange,
                                  fontSize: 14,
                                ),
                              ),
                            ),
                        ],
                      ),
                    ),
            ),
            
            // Local Video (Picture-in-Picture) - YOUR Camera
            Positioned(
              top: 40,
              right: 20,
              child: Container(
                width: 120,
                height: 160,
                decoration: BoxDecoration(
                  color: _isCameraOff ? Colors.grey[900] : Colors.blueAccent.withOpacity(0.3),
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: Colors.white, width: 2),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black54,
                      blurRadius: 10,
                      offset: Offset(0, 4),
                    ),
                  ],
                ),
                child: ClipRRect(
                  borderRadius: BorderRadius.circular(10),
                  child: _isCameraOff
                      ? Center(
                          child: Icon(
                            Icons.videocam_off,
                            size: 40,
                            color: Colors.grey,
                          ),
                        )
                      : AgoraVideoView(
                          controller: VideoViewController(
                            rtcEngine: _engine!,
                            canvas: VideoCanvas(uid: 0), // Show local user
                          ),
                        ),
                ),
              ),
            ),
            
            // Call Info Overlay
            Positioned(
              top: 40,
              left: 20,
              child: Container(
                padding: EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: Colors.black54,
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Text(
                          callTitle,
                          style: TextStyle(
                            color: Colors.white,
                            fontSize: 16,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        if (isTenantToTenant)
                          Padding(
                            padding: EdgeInsets.only(left: 8),
                            child: Container(
                              padding: EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                              decoration: BoxDecoration(
                                color: Colors.orange,
                                borderRadius: BorderRadius.circular(4),
                              ),
                              child: Text(
                                'T',
                                style: TextStyle(
                                  color: Colors.white,
                                  fontSize: 10,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                            ),
                          ),
                      ],
                    ),
                    SizedBox(height: 5),
                    Row(
                      children: [
                        Icon(
                          _isConnected ? Icons.check_circle : Icons.access_time,
                          color: _isConnected ? Colors.green : Colors.orange,
                          size: 16,
                        ),
                        SizedBox(width: 5),
                        Text(
                          _isConnected ? 'Connected' : 'Connecting...',
                          style: TextStyle(
                            color: _isConnected ? Colors.green : Colors.orange,
                            fontSize: 12,
                          ),
                        ),
                      ],
                    ),
                    Text(
                      _formatDuration(_callDuration),
                      style: TextStyle(color: Colors.grey, fontSize: 14),
                    ),
                  ],
                ),
              ),
            ),
            
            // Bottom Controls
            Positioned(
              bottom: 40,
              left: 0,
              right: 0,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  // Mute Button
                  Column(
                    children: [
                      CircleAvatar(
                        radius: 28,
                        backgroundColor: _isMuted ? Colors.white : Colors.grey[800],
                        child: IconButton(
                          icon: Icon(
                            _isMuted ? Icons.mic_off : Icons.mic,
                            color: _isMuted ? Colors.black : Colors.white,
                          ),
                          onPressed: _toggleMute,
                        ),
                      ),
                      SizedBox(height: 5),
                      Text('Mute', style: TextStyle(color: Colors.grey, fontSize: 12)),
                    ],
                  ),
                  
                  // Camera Button
                  Column(
                    children: [
                      CircleAvatar(
                        radius: 28,
                        backgroundColor: _isCameraOff ? Colors.white : Colors.grey[800],
                        child: IconButton(
                          icon: Icon(
                            _isCameraOff ? Icons.videocam_off : Icons.videocam,
                            color: _isCameraOff ? Colors.black : Colors.white,
                          ),
                          onPressed: _toggleCamera,
                        ),
                      ),
                      SizedBox(height: 5),
                      Text('Camera', style: TextStyle(color: Colors.grey, fontSize: 12)),
                    ],
                  ),
                  
                  // End Call Button
                  CircleAvatar(
                    radius: 32,
                    backgroundColor: Colors.red,
                    child: IconButton(
                      icon: Icon(Icons.call_end, color: Colors.white, size: 28),
                      onPressed: _endCall,
                    ),
                  ),
                  
                  // Switch Camera Button
                  Column(
                    children: [
                      CircleAvatar(
                        radius: 28,
                        backgroundColor: Colors.grey[800],
                        child: IconButton(
                          icon: Icon(Icons.flip_camera_android, color: Colors.white),
                          onPressed: _switchCamera,
                        ),
                      ),
                      SizedBox(height: 5),
                      Text('Switch', style: TextStyle(color: Colors.grey, fontSize: 12)),
                    ],
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
