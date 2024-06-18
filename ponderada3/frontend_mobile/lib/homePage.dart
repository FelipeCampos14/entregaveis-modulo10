import 'dart:convert';
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:awesome_notifications/awesome_notifications.dart';
import 'package:http/http.dart' as http;
import 'package:image_picker/image_picker.dart';
import 'package:path/path.dart' as path;
import 'package:path_provider/path_provider.dart';

class HomePage extends StatefulWidget {
  final String token;

  HomePage({required this.token});

  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  File? _image;
  File? _processedImage;
  final ImagePicker _picker = ImagePicker();
  String _message = '';
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
  }

  Future<void> _showNotification(String title, String body) async {
    AwesomeNotifications().createNotification(
      content: NotificationContent(
        id: 10,
        channelKey: 'basic_channel',
        title: title,
        body: body,
      ),
    );
  }

  Future<void> _pickImage() async {
    final pickedFile = await _picker.pickImage(source: ImageSource.gallery);

    setState(() {
      if (pickedFile != null) {
        _image = File(pickedFile.path);
        _processedImage = null;
        _message = '';
      }
    });
  }

  Future<void> _uploadImage() async {
    if (_image == null) return;

    setState(() {
      _isLoading = true;
    });

    final request = http.MultipartRequest(
      'POST',
      Uri.parse('http://172.18.0.1:8001/process-image'),
    );
    request.headers['Authorization'] = 'Bearer ${widget.token}';
    request.files.add(await http.MultipartFile.fromPath(
      'file',
      _image!.path,
      filename: path.basename(_image!.path),
    ));

    try {
      final response = await request.send();
      if (response.statusCode == 200) {
        final responseData = await response.stream.toBytes();
        final directory = await getApplicationDocumentsDirectory();
        final filePath = path.join(directory.path, 'processed_image.png');
        final file = File(filePath);
        await file.writeAsBytes(responseData);

        setState(() {
          _processedImage = file;
          _image = null; // Clear the original image
          _message = 'Image uploaded and processed successfully!';
        });
        // _showNotification('Processing Complete', 'Your image has been processed successfully.');
      } else {
        setState(() {
          _message = 'Image upload failed: ${response.reasonPhrase}, ${response.statusCode}';
        });
        // _showNotification('Processing Failed', 'There was an error processing your image.');
      }
    } catch (e) {
      setState(() {
        _message = 'Error: $e';
      });
      // _showNotification('Error', 'There was an error: $e');
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Home Page'),
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              _processedImage == null
                  ? (_image == null
                      ? Text('No image selected.')
                      : Image.file(_image!))
                  : Image.file(_processedImage!),
              SizedBox(height: 20),
              _isLoading
                  ? CircularProgressIndicator()
                  : Column(
                      children: [
                        ElevatedButton(
                          onPressed: _pickImage,
                          child: Text('Pick Image'),
                        ),
                        ElevatedButton(
                          onPressed: _uploadImage,
                          child: Text('Upload Image'),
                        ),
                      ],
                    ),
              SizedBox(height: 20),
              Text(_message),
            ],
          ),
        ),
      ),
    );
  }
}
