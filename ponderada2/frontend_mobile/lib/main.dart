import 'package:flutter/material.dart';
import 'dart:math';

void main() {
  runApp(MaterialApp(
    home: Scaffold(
      appBar: AppBar(
        title: Text('Escolha seu inicial'),
      ),
      body: Center(
        child: PokemonButton(),
      ),
    ),
  ));
}

class PokemonButton extends StatefulWidget {
  @override
  _PokemonButtonState createState() => _PokemonButtonState();
}

class _PokemonButtonState extends State<PokemonButton> {
  String _pokemonName = '';

  final List<String> pokemonNames = [
    'Bulbasaur',
    'Charmander',
    'Squirtle',
  ];

  void _getRandomPokemon() {
    setState(() {
      _pokemonName = pokemonNames[Random().nextInt(pokemonNames.length)];
    });
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: <Widget>[
        ElevatedButton(
          onPressed: _getRandomPokemon,
          child: Text('Escolha seu inicial'),
        ),
        SizedBox(height: 20.0),
        Text(
          _pokemonName,
          style: TextStyle(fontSize: 20.0, fontWeight: FontWeight.bold),
        ),
      ],
    );
  }
}
