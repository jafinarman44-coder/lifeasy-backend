import 'package:flutter/material.dart';
import 'package:agora_rtc_engine/agora_rtc_engine.dart';
import 'package:permission_handler/permission_handler.dart';
import 'dart:async';
import '../services/call_socket_manager.dart';

class VoiceCallScreen extends StatefulWidget {
  final String tenantId;
  final String channelName;
  final String receiverId;
  
  VoiceCallScreen({
    required this.tenantId,
    required this.channelName,
    required this.receiverId,
  });
  
  @override
  _VoiceCallScreenState createState() => _VoiceCallScreenState();
}

class _VoiceCallScreenState extends State<VoiceCallScreen> {
  late RtcEngine _engine;
  int? _remoteUid;
  bool _localJoined = false;
  bool _isCallActive = false;
  bool isMuted = false;
  bool speakerOn = true;
  int callDuration = 0;
  Timer? _timer;
  final CallSocketManager _callSocket = CallSocketManager();
  
  final String _appId = '8824dd55d0ce44c2873fa74acc730c5b';

  @override
  void initState() {
    super.initState();
    _initializeCall();
  }

  @override
  void dispose() {
    _timer?.cancel();
    _engine.leaveChannel();
    _engine.release();
    _callSocket.disconnect();
    super.dispose();
  }

  Future<void> _initializeCall() async {
    try {
      // Connect to signaling server
      await _callSocket.connect(
        widget.tenantId,
        serverIp: 'lifeasy-api.onrender.com',
      );
      
      // Setup call event handlers
      _callSocket.onConnected = () {
        print('✅ Call signaling connected');
        _sendCallOffer();
      };
      
      _callSocket.onCallEnded = () {
        print('📴 Call ended by remote user');
        if (mounted) {
          _endCall();
        }
      };
      
      // Initialize Agora engine
      await _initAgora();
    } catch (e) {
      print('❌ Call initialization error: $e');
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Call failed: $e'), backgroundColor: Colors.red),
      );
      if (mounted) {
        Navigator.pop(context);
      }
    }
  }
  
  // Send call offer to receiver
  void _sendCallOffer() {
    _callSocket.sendCallOffer(
      receiverId: widget.receiverId,
      callType: 'voice',
      offer: {'channel': widget.channelName},
      callerName: 'User ${widget.tenantId}',
    );
    print('📞 Call offer sent to ${widget.receiverId}');
  }

  Future<void> _initAgora() async {
    try {
      // Request microphone permission
      final micStatus = await Permission.microphone.status;
      if (!micStatus.isGranted) {
        final result = await Permission.microphone.request();
        if (!result.isGranted) {
          throw Exception('Microphone permission denied');
        }
      }

      // Initialize Agora engine
      _engine = createAgoraRtcEngine();
      await _engine.initialize(RtcEngineContext(
        appId: _appId,
        channelProfile: ChannelProfileType.channelProfileCommunication,
      ));

      // Register event handlers
      _engine.registerEventHandler(
        RtcEngineEventHandler(
          onJoinChannelSuccess: (RtcConnection connection, int elapsed) {
            print('✅ Joined voice channel: ${connection.channelId}');
            setState(() {
              _localJoined = true;
              _isCallActive = true;
            });
            _startCallTimer();
          },
          onUserJoined: (RtcConnection connection, int remoteUid, int elapsed) {
            print('👤 Remote user joined: $remoteUid');
            setState(() {
              _remoteUid = remoteUid;
            });
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(
                content: Text('Connected to remote user'),
                backgroundColor: Colors.green,
                duration: Duration(seconds: 2),
              ),
            );
          },
          onUserOffline: (RtcConnection connection, int remoteUid, UserOfflineReasonType reason) {
            print('👋 Remote user left: $remoteUid');
            setState(() {
              _remoteUid = null;
            });
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(
                content: Text('Remote user disconnected'),
                backgroundColor: Colors.orange,
                duration: Duration(seconds: 2),
              ),
            );
          },
          onError: (ErrorCodeType code, String msg) {
            print('❌ Agora Error: $code - $msg');
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(content: Text('Error: $msg'), backgroundColor: Colors.red),
            );
          },
          onConnectionStateChanged: (RtcConnection connection, ConnectionStateType state, ConnectionChangedReasonType reason) {
            print('🔗 Connection state: $state');
            if (state == ConnectionStateType.connectionStateDisconnected) {
              setState(() {
                _localJoined = false;
              });
            }
          },
        ),
      );

      // DISABLE VIDEO - Voice only
      await _engine.disableVideo();

      // Join channel with proper options
      await _engine.joinChannel(
        token: '', // Empty token for testing (use in production)
        channelId: widget.channelName,
        uid: int.parse(widget.tenantId),
        options: const ChannelMediaOptions(
          channelProfile: ChannelProfileType.channelProfileCommunication,
          clientRoleType: ClientRoleType.clientRoleBroadcaster,
          publishMicrophoneTrack: true,
          autoSubscribeAudio: true,
        ),
      );
    } catch (e) {
      print('❌ Agora initialization failed: $e');
      throw e;
    }
  }

  void _startCallTimer() {
    _timer = Timer.periodic(Duration(seconds: 1), (timer) {
      if (mounted) {
        setState(() {
          callDuration++;
        });
      }
    });
  }

  Future<void> _endCall() async {
    _timer?.cancel();
    _isCallActive = false;
    
    // Notify remote user via signaling
    _callSocket.endCall(
      receiverId: widget.receiverId,
      reason: 'ended',
    );
    
    // Cleanup Agora
    await _engine.leaveChannel();
    await _engine.release();
    
    if (mounted) {
      Navigator.of(context).pop(true);
    }
  }

  Future<void> _toggleMute() async {
    await _engine.muteLocalAudioStream(!isMuted);
    setState(() {
      isMuted = !isMuted;
    });
  }

  Future<void> _toggleSpeaker() async {
    await _engine.setEnableSpeakerphone(!speakerOn);
    setState(() {
      speakerOn = !speakerOn;
    });
  }

  String _formatDuration(int seconds) {
    int minutes = seconds ~/ 60;
    int secs = seconds % 60;
    return '${minutes.toString().padLeft(2, '0')}:${secs.toString().padLeft(2, '0')}';
  }


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [Color(0xFF0F172A), Colors.black87],
          ),
        ),
        child: Stack(
          children: [
            // User Avatar and Info
            Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  // Large Avatar
                  Container(
                    width: 180,
                    height: 180,
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      gradient: LinearGradient(
                        begin: Alignment.topLeft,
                        end: Alignment.bottomRight,
                        colors: [
                          Colors.blueAccent.withOpacity(0.3),
                          Colors.purpleAccent.withOpacity(0.3),
                        ],
                      ),
                      boxShadow: [
                        BoxShadow(
                          color: Colors.blueAccent.withOpacity(0.3),
                          blurRadius: 30,
                          spreadRadius: 10,
                        ),
                      ],
                    ),
                    child: Center(
                      child: Icon(
                        Icons.person,
                        size: 100,
                        color: Colors.white,
                      ),
                    ),
                  ),
                  SizedBox(height: 30),
                  
                  // User Name
                  Text(
                    'User ${widget.receiverId}',
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 28,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  SizedBox(height: 10),
                  
                  // Call Status
                  Container(
                    padding: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                    decoration: BoxDecoration(
                      color: _localJoined ? Colors.green.withOpacity(0.2) : Colors.orange.withOpacity(0.2),
                      borderRadius: BorderRadius.circular(25),
                    ),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Icon(
                          Icons.circle,
                          color: _localJoined ? Colors.green : Colors.orange,
                          size: 10,
                        ),
                        SizedBox(width: 8),
                        Text(
                          _localJoined 
                              ? (_remoteUid != null ? 'Connected' : 'Ringing...')
                              : 'Connecting...',
                          style: TextStyle(
                            color: Colors.white,
                            fontSize: 16,
                          ),
                        ),
                      ],
                    ),
                  ),
                  SizedBox(height: 10),
                  
                  // Call Duration
                  if (_localJoined)
                    Text(
                      _formatDuration(callDuration),
                      style: TextStyle(
                        color: Colors.grey[400],
                        fontSize: 20,
                        fontWeight: FontWeight.w300,
                      ),
                    ),
                  
                  // Audio Wave Animation
                  if (_localJoined && _remoteUid != null)
                    Padding(
                      padding: EdgeInsets.only(top: 20),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: List.generate(5, (index) {
                          return AnimatedContainer(
                            duration: Duration(milliseconds: 500 + (index * 100)),
                            margin: EdgeInsets.symmetric(horizontal: 3),
                            width: 4,
                            height: 20 + (DateTime.now().millisecond % 3) * 10,
                            decoration: BoxDecoration(
                              color: Colors.green,
                              borderRadius: BorderRadius.circular(2),
                            ),
                          );
                        }),
                      ),
                    ),
                ],
              ),
            ),
            
            // Bottom Controls
            Positioned(
              bottom: 60,
              left: 0,
              right: 0,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  // Mute Button
                  _controlButton(
                    icon: isMuted ? Icons.mic_off : Icons.mic,
                    color: isMuted ? Colors.red : Colors.white,
                    onTap: _toggleMute,
                  ),
                  
                  // Speaker Button
                  _controlButton(
                    icon: speakerOn ? Icons.volume_up : Icons.volume_off,
                    color: speakerOn ? Colors.blue : Colors.white,
                    onTap: _toggleSpeaker,
                  ),
                  
                  // End Call Button
                  _controlButton(
                    icon: Icons.call_end,
                    color: Colors.white,
                    size: 70,
                    onTap: _endCall,
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _controlButton({
    required IconData icon,
    required Color color,
    required Function() onTap,
    double size = 60,
  }) {
    return InkWell(
      onTap: onTap,
      child: Container(
        width: size,
        height: size,
        decoration: BoxDecoration(
          shape: BoxShape.circle,
          color: Colors.black54,
          boxShadow: [
            BoxShadow(
              color: Colors.black26,
              blurRadius: 8,
            ),
          ],
        ),
        child: Icon(icon, color: color, size: size * 0.5),
      ),
    );
  }
}
