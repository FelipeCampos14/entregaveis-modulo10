import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class Todo {
  final int id;
  final String title;
  final String status;

  Todo({
    required this.id,
    required this.title,
    required this.status,
  });

  factory Todo.fromJson(Map<String, dynamic> json) {
    return Todo(
      id: json['id'],
      title: json['title'],
      status: json['status'],
    );
  }
}

class TodoPage extends StatefulWidget {
  final String token;

  TodoPage({required this.token});

  @override
  _TodoPageState createState() => _TodoPageState();
}

class _TodoPageState extends State<TodoPage> {
  late Future<List<Todo>> _futureTodos;
  final TextEditingController _titleController = TextEditingController();
  final TextEditingController _statusController = TextEditingController();
  final TextEditingController _titleControllerUpdate = TextEditingController();
  final TextEditingController _statusControllerUpdate = TextEditingController();

  @override
  void initState() {
    super.initState();
    _futureTodos = fetchTodos();
  }

  Future<List<Todo>> fetchTodos() async {
    final response = await http.get(
      Uri.parse('https://7f87-204-199-57-10.ngrok-free.app/todos'),
      headers: {
        'Authorization': 'Bearer ${widget.token}',
      },
    );
    if (response.statusCode == 200) {
      List<dynamic> data = json.decode(response.body);
      return data.map((e) => Todo.fromJson(e)).toList();
    } else {
      throw Exception('Failed to load Todos');
    }
  }

  Future<void> createTodo() async {
    final response = await http.post(
      Uri.parse('https://7f87-204-199-57-10.ngrok-free.app/todos'),
      headers: {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': 'Bearer ${widget.token}',
      },
      body: jsonEncode(<String, String>{
        'title': _titleController.text,
        'status': _statusController.text,
      }),
    );

    if (response.statusCode == 200) {
      setState(() {
        _futureTodos = fetchTodos();
      });
    } else {
      throw Exception('Failed to create Todo');
    }
  }

  Future<void> deleteTodo(int id) async {
    final response = await http.delete(
      Uri.parse('https://7f87-204-199-57-10.ngrok-free.app/todos/$id'),
      headers: {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': 'Bearer ${widget.token}',
      },
    );

    if (response.statusCode == 200) {
      setState(() {
        _futureTodos = fetchTodos();
      });
    } else {
      throw Exception('Failed to delete Todo');
    }
  }

  Future<void> updateTodo(int id, String title, String status) async {
    final response = await http.put(
      Uri.parse('https://7f87-204-199-57-10.ngrok-free.app/todos/$id'),
      headers: {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': 'Bearer ${widget.token}',
      },
      body: jsonEncode(<String, String>{
        'title': title,
        'status': status,
      }),
    );

    if (response.statusCode == 200) {
      setState(() {
        _futureTodos = fetchTodos();
      });
    } else {
      throw Exception('Failed to update Todo');
    }
  }

  Future<void> editPopUp(int id, String title, String status) async {
    _titleControllerUpdate.text = title;
    _statusControllerUpdate.text = status;
    await showDialog<String>(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: <Widget>[
              TextField(
                controller: _titleControllerUpdate,
                decoration: InputDecoration(labelText: 'Title'),
              ),
              TextField(
                controller: _statusControllerUpdate,
                decoration: InputDecoration(labelText: 'Status'),
              ),
            ],
          ),
          actions: <Widget>[
            TextButton(
              onPressed: () {
                Navigator.pop(context);
              },
              child: Text('Cancel'),
            ),
            TextButton(
              onPressed: () {
                updateTodo(
                  id,
                  _titleControllerUpdate.text,
                  _statusControllerUpdate.text,
                );
                Navigator.pop(context);
              },
              child: Text('Update'),
            ),
          ],
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Todos'),
      ),
      body: Center(
        child: Column(
          children: <Widget>[
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: TextField(
                controller: _titleController,
                decoration: InputDecoration(labelText: 'Title'),
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: TextField(
                controller: _statusController,
                decoration: InputDecoration(labelText: 'Status'),
              ),
            ),
            ElevatedButton(
              onPressed: () {
                createTodo();
              },
              child: Text('Create Todo'),
            ),
            Expanded(
              child: FutureBuilder<List<Todo>>(
                future: _futureTodos,
                builder: (context, snapshot) {
                  if (snapshot.hasData) {
                    return ListView.builder(
                      itemCount: snapshot.data!.length,
                      itemBuilder: (context, index) {
                        return ListTile(
                          title: Text(snapshot.data![index].title),
                          subtitle: Text(snapshot.data![index].status),
                          trailing: Row(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              IconButton(
                                icon: Icon(Icons.edit),
                                onPressed: () {
                                  editPopUp(
                                    snapshot.data![index].id,
                                    snapshot.data![index].title,
                                    snapshot.data![index].status,
                                  );
                                },
                              ),
                              IconButton(
                                icon: Icon(Icons.delete),
                                onPressed: () {
                                  deleteTodo(snapshot.data![index].id);
                                },
                              ),
                            ],
                          ),
                        );
                      },
                    );
                  } else if (snapshot.hasError) {
                    return Text('${snapshot.error}');
                  }
                  return CircularProgressIndicator();
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}
