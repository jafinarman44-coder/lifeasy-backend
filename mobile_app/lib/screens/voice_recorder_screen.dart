import 'package:flutter/material.dart';
import 'dart:async';
import 'package:path_provider/path_provider.dart';
import 'package:path/path.dart' as path;

class VoiceRecorderScreen extends StatefulWidget {
  final Function(File audioFile, int duration) onRecordingComplete;
  
  const VoiceRecorderScreen({Key? key, required this.onRecordingComplete}) : super(key: key);

  @override
  _VoiceRecorderScreenState createState() => _VoiceRecorderScreenState();
}

class _VoiceRecorderScreenState extends State<VoiceRecorderScreen> {
  bool _isRecording = false;
  bool _isPaused = false;
  int _duration = 0;
  Timer? _timer;
  String? _audioPath;
  
  // Note: Actual recording requires 'record' package
  // This is a UI implementation

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  void _startRecording() async {
    setState(() {
      _isRecording = true;
      _isPaused = false;
      _duration = 0;
    });

    _timer = Timer.periodic(Duration(seconds: 1), (timer) {
      setState(() {
        _duration++;
      });
    });

    // TODO: Initialize actual audio recording
    // var recorder = Record();
    // var dir = await getApplicationDocumentsDirectory();
    // _audioPath = '${dir.path}/voice_${DateTime.now().millisecondsSinceEpoch}.m4a';
    // await recorder.start(path: _audioPath);
  }

  void _pauseRecording() {
    setState(() {
      _isPaused = !_isPaused;
    });
    
    if (_isPaused) {
      _timer?.cancel();
    } else {
      _timer = Timer.periodic(Duration(seconds: 1), (timer) {
        setState(() {
          _duration++;
        });
      });
    }
    
    // TODO: Pause actual recorder
  }

  void _stopRecording() {
    _timer?.cancel();
    setState(() {
      _isRecording = false;
    });

    if (_duration > 0 && _audioPath != null) {
      widget.onRecordingComplete(File(_audioPath!), _duration);
      Navigator.pop(context);
    } else {
      Navigator.pop(context);
    }
    
    // TODO: Stop actual recorder
  }

  void _cancelRecording() {
    _timer?.cancel();
    setState(() {
      _isRecording = false;
      _duration = 0;
    });
    Navigator.pop(context);
    
    // TODO: Cancel and delete recording
  }

  String _formatDuration(int seconds) {
    final minutes = seconds ~/ 60;
    final secs = seconds % 60;
    return '${minutes.toString().padLeft(2, '0')}:${secs.toString().padLeft(2, '0')}';
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Color(0xFF0F172A),
      appBar: AppBar(
        title: Text('Voice Message'),
        backgroundColor: Colors.transparent,
        elevation: 0,
        leading: IconButton(
          icon: Icon(Icons.close),
          onPressed: _cancelRecording,
        ),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // Microphone Icon
            Container(
              width: 150,
              height: 150,
              decoration: BoxDecoration(
                color: _isRecording ? Colors.red.withOpacity(0.2) : Colors.blueAccent.withOpacity(0.2),
                shape: BoxShape.circle,
              ),
              child: Icon(
                _isRecording ? Icons.mic : Icons.mic_none,
                size: 80,
                color: _isRecording ? Colors.red : Colors.blueAccent,
              ),
            ),
            
            SizedBox(height: 40),
            
            // Duration Display
            Text(
              _formatDuration(_duration),
              style: TextStyle(
                fontSize: 48,
                fontWeight: FontWeight.bold,
                color: Colors.white,
              ),
            ),
            
            SizedBox(height: 20),
            
            // Status Text
            Text(
              _isRecording ? (_isPaused ? 'Paused' : 'Recording...') : 'Tap to Start',
              style: TextStyle(
                fontSize: 18,
                color: Colors.grey,
              ),
            ),
            
            SizedBox(height: 60),
            
            // Controls
            if (!_isRecording)
              // Start Button
              ElevatedButton.icon(
                onPressed: _startRecording,
                icon: Icon(Icons.mic),
                label: Text('Start Recording'),
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.blueAccent,
                  padding: EdgeInsets.symmetric(horizontal: 40, vertical: 16),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(30),
                  ),
                ),
              )
            else
              // Recording Controls
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  // Cancel Button
                  IconButton(
                    icon: Icon(Icons.delete, size: 40, color: Colors.red),
                    onPressed: _cancelRecording,
                  ),
                  
                  // Pause/Resume Button
                  CircleAvatar(
                    radius: 35,
                    backgroundColor: Colors.blueAccent,
                    child: IconButton(
                      icon: Icon(
                        _isPaused ? Icons.play_arrow : Icons.pause,
                        size: 40,
                        color: Colors.white,
                      ),
                      onPressed: _pauseRecording,
                    ),
                  ),
                  
                  // Stop/Complete Button
                  IconButton(
                    icon: Icon(Icons.check_circle, size: 40, color: Colors.green),
                    onPressed: _stopRecording,
                  ),
                ],
              ),
            
            SizedBox(height: 30),
            
            // Max Duration Warning
            if (_duration >= 290)
              Padding(
                padding: EdgeInsets.all(16),
                child: Text(
                  'Maximum duration approaching (5 minutes)',
                  style: TextStyle(color: Colors.orange, fontSize: 14),
                ),
              ),
          ],
        ),
      ),
    );
  }
}
