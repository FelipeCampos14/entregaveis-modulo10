import 'dart:convert';
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:image_picker/image_picker.dart';
import 'package:path/path.dart' as path;
import 'package:path_provider/path_provider.dart';
import 'package:frontend_mobile/homePage.dart';

class LoginPage extends StatefulWidget {
  @override
  _LoginPageState createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final TextEditingController _usernameController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  String _message = '';

  Future<void> _login() async { 
    final response = await http.post(
      Uri.parse('https://7f87-204-199-57-10.ngrok-free.app/token'),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonEncode(<String, String>{
        'username': _usernameController.text,
        'password': _passwordController.text,
      }),
    );

    if (response.statusCode == 200) {
      final token = jsonDecode(response.body)['access_token'];

      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => TodoPage(token: token),
        ),
      );
    } else {
      setState(() {
        _message = 'Login failed!';
      });
    }
  }

  Future<void> _createAccount() async {
    final response = await http.post(
      Uri.parse('https://7f87-204-199-57-10.ngrok-free.app/users'),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonEncode(<String, String>{
        'username': _usernameController.text,
        'password': _passwordController.text,
      }),
    );

    if (response.statusCode == 201 || response.statusCode == 200) {
      setState(() {
        _message = 'Account created successfully. Please log in.';
      });
    } else {
      setState(() {
        _message = 'Account creation failed: ${response.body}';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Login / Create Account'),
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              TextField(
                controller: _usernameController,
                decoration: InputDecoration(labelText: 'Username'),
              ),
              TextField(
                controller: _passwordController,
                decoration: InputDecoration(labelText: 'Password'),
                obscureText: true,
              ),
              SizedBox(height: 20),
              ElevatedButton(
                onPressed: _login,
                child: Text('Login'),
              ),
              ElevatedButton(
                onPressed: _createAccount,
                child: Text('Create Account'),
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