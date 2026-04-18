import 'package:flutter/material.dart';
import 'package:agora_rtc_engine/agora_rtc_engine.dart';
import 'package:permission_handler/permission_handler.dart';
import 'dart:async';

class VideoCallScreen extends StatefulWidget {
  final String tenantId;
  final String channelName;
  final String receiverId;
  
  VideoCallScreen({
    required this.tenantId,
    required this.channelName,
    required this.receiverId,
  });
  
  @override
  _VideoCallScreenState createState() => _VideoCallScreenState();
}

class _VideoCallScreenState extends State<VideoCallScreen> {
  late RtcEngine _engine;
  int? _remoteUid;
  bool _localJoined = false;
  bool isMuted = false;
  bool isCameraOff = false;
  bool speakerOn = true;
  int callDuration = 0;
  Timer? _timer;
  
  // AGORA APP ID - From backend .env file
  final String _appId = '937aca389d5843e4be2cafde36650adf';
  final String _appCertificate = 'eaf84252500d48a78858233a95eb8ade';

  @override
  void initState() {
    super.initState();
    _initAgora();
  }

  Future<void> _initAgora() async {
    // Request permissions
    await [Permission.microphone, Permission.camera].request();

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
          print('✅ Joined channel successfully');
          setState(() {
            _localJoined = true;
          });
          _startCallTimer();
        },
        onUserJoined: (RtcConnection connection, int remoteUid, int elapsed) {
          print('👤 Remote user joined: $remoteUid');
          setState(() {
            _remoteUid = remoteUid;
          });
        },
        onUserOffline: (RtcConnection connection, int remoteUid, UserOfflineReasonType reason) {
          print('👋 Remote user left: $remoteUid');
          setState(() {
            _remoteUid = null;
          });
        },
        onError: (ErrorCodeType code, String msg) {
          print('❌ Agora Error: $code - $msg');
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Error: $msg')),
          );
        },
      ),
    );

    // Enable video
    await _engine.enableVideo();
    
    // Start local preview
    await _engine.startPreview();

    // Join channel
    await _engine.joinChannel(
      token: '', // Empty for testing (disable App Certificate in Agora console)
      channelId: widget.channelName,
      uid: int.parse(widget.tenantId),
      options: const ChannelMediaOptions(
        channelProfile: ChannelProfileType.channelProfileCommunication,
        clientRoleType: ClientRoleType.clientRoleBroadcaster,
      ),
    );
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
    await _engine.leaveChannel();
    await _engine.release();
    if (mounted) {
      Navigator.pop(context);
    }
  }

  Future<void> _toggleMute() async {
    await _engine.muteLocalAudioStream(!isMuted);
    setState(() {
      isMuted = !isMuted;
    });
  }

  Future<void> _toggleCamera() async {
    await _engine.muteLocalVideoStream(!isCameraOff);
    setState(() {
      isCameraOff = !isCameraOff;
    });
  }

  Future<void> _toggleSpeaker() async {
    await _engine.setEnableSpeakerphone(!speakerOn);
    setState(() {
      speakerOn = !speakerOn;
    });
  }

  Future<void> _switchCamera() async {
    await _engine.switchCamera();
  }

  String _formatDuration(int seconds) {
    int minutes = seconds ~/ 60;
    int secs = seconds % 60;
    return '${minutes.toString().padLeft(2, '0')}:${secs.toString().padLeft(2, '0')}';
  }

  @override
  void dispose() {
    _timer?.cancel();
    _engine.leaveChannel();
    _engine.release();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: Stack(
        children: [
          // Remote Video (Full Screen)
          Positioned.fill(
            child: _remoteUid != null
                ? AgoraVideoView(
                    controller: VideoViewController.remote(
                      rtcEngine: _engine,
                      canvas: VideoCanvas(uid: _remoteUid),
                      connection: RtcConnection(channelId: widget.channelName),
                    ),
                  )
                : Container(
                    color: Colors.grey[900],
                    child: Center(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          CircleAvatar(
                            radius: 60,
                            backgroundColor: Colors.blueAccent.withOpacity(0.3),
                            child: Icon(
                              Icons.person,
                              size: 60,
                              color: Colors.blueAccent,
                            ),
                          ),
                          SizedBox(height: 20),
                          Text(
                            'User ${widget.receiverId}',
                            style: TextStyle(
                              color: Colors.white,
                              fontSize: 20,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          SizedBox(height: 10),
                          Text(
                            _localJoined ? 'Waiting for answer...' : 'Connecting...',
                            style: TextStyle(
                              color: Colors.grey,
                              fontSize: 14,
                            ),
                          ),
                          SizedBox(height: 20),
                          CircularProgressIndicator(color: Colors.blueAccent),
                        ],
                      ),
                    ),
                  ),
          ),

          // Local Video (Picture-in-Picture - Top Right)
          Positioned(
            top: 50,
            right: 20,
            width: 120,
            height: 160,
            child: GestureDetector(
              onTap: () {
                // Optional: Swap local/remote view
              },
              child: Container(
                decoration: BoxDecoration(
                  color: Colors.grey[900],
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: Colors.white, width: 2),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black54,
                      blurRadius: 10,
                    ),
                  ],
                ),
                child: ClipRRect(
                  borderRadius: BorderRadius.circular(10),
                  child: AgoraVideoView(
                    controller: VideoViewController(
                      rtcEngine: _engine,
                      canvas: VideoCanvas(uid: 0),
                    ),
                  ),
                ),
              ),
            ),
          ),

          // Call Info (Top Left)
          Positioned(
            top: 50,
            left: 20,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'User ${widget.receiverId}',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                SizedBox(height: 5),
                Container(
                  padding: EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                  decoration: BoxDecoration(
                    color: _localJoined ? Colors.green.withOpacity(0.2) : Colors.orange.withOpacity(0.2),
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Icon(
                        Icons.circle,
                        color: _localJoined ? Colors.green : Colors.orange,
                        size: 8,
                      ),
                      SizedBox(width: 6),
                      Text(
                        _localJoined ? 'Connected • ${_formatDuration(callDuration)}' : 'Connecting...',
                        style: TextStyle(
                          color: Colors.white,
                          fontSize: 12,
                        ),
                      ),
                    ],
                  ),
                ),
              ],
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
                _controlButton(
                  icon: isMuted ? Icons.mic_off : Icons.mic,
                  color: isMuted ? Colors.red : Colors.white,
                  onTap: _toggleMute,
                ),

                // Camera Button
                _controlButton(
                  icon: isCameraOff ? Icons.videocam_off : Icons.videocam_rounded,
                  color: isCameraOff ? Colors.red : Colors.white,
                  onTap: _toggleCamera,
                ),

                // Switch Camera Button
                _controlButton(
                  icon: Icons.cameraswitch,
                  color: Colors.white,
                  onTap: _switchCamera,
                ),

                // End Call Button
                _controlButton(
                  icon: Icons.call_end,
                  color: Colors.white,
                  size: 60,
                  onTap: _endCall,
                ),

                // Speaker Button
                _controlButton(
                  icon: speakerOn ? Icons.volume_up : Icons.volume_off,
                  color: speakerOn ? Colors.blue : Colors.white,
                  onTap: _toggleSpeaker,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _controlButton({
    required IconData icon,
    required Color color,
    required Function() onTap,
    double size = 50,
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
              blurRadius: 5,
            ),
          ],
        ),
        child: Icon(icon, color: color, size: size * 0.56),
      ),
    );
  }
}
