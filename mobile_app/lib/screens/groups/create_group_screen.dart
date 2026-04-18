import 'package:flutter/material.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import '../tenant_list_screen.dart';

class CreateGroupScreen extends StatefulWidget {
  final String tenantId;
  
  const CreateGroupScreen({Key? key, required this.tenantId}) : super(key: key);

  @override
  _CreateGroupScreenState createState() => _CreateGroupScreenState();
}

class _CreateGroupScreenState extends State<CreateGroupScreen> {
  final TextEditingController nameController = TextEditingController();
  final TextEditingController descriptionController = TextEditingController();
  List<Tenant> _allTenants = [];
  final List<String> _selectedMemberIds = [];
  bool _isLoading = false;
  String _serverIp = '192.168.43.219';

  @override
  void initState() {
    super.initState();
    _fetchTenants();
  }

  Future<void> _fetchTenants() async {
    setState(() => _isLoading = true);
    
    try {
      final url = Uri.parse('http://$_serverIp:8000/api/tenants/all');
      final response = await http.get(url);

      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        setState(() {
          _allTenants = data.map((json) => Tenant.fromJson(json)).toList();
          _isLoading = false;
        });
      }
    } catch (e) {
      setState(() => _isLoading = false);
      print('Error fetching tenants: $e');
    }
  }

  Future<void> _createGroup() async {
    if (nameController.text.trim().isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Please enter group name')),
      );
      return;
    }

    if (_selectedMemberIds.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Please select at least one member')),
      );
      return;
    }

    setState(() => _isLoading = true);

    try {
      final url = Uri.parse('http://$_serverIp:8000/api/groups/create');
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'name': nameController.text.trim(),
          'description': descriptionController.text.trim(),
          'member_ids': _selectedMemberIds.map((id) => int.parse(id)).toList(),
          'creator_id': int.parse(widget.tenantId),
        }),
      );

      setState(() => _isLoading = false);

      if (response.statusCode == 200) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Group created successfully!'),
            backgroundColor: Colors.green,
          ),
        );
        Navigator.pop(context, true); // Return success
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Failed to create group')),
        );
      }
    } catch (e) {
      setState(() => _isLoading = false);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error: $e')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Create Group'),
        backgroundColor: Colors.blueAccent,
        elevation: 0,
        actions: [
          if (!_isLoading)
            TextButton(
              onPressed: _createGroup,
              child: Text(
                'CREATE',
                style: TextStyle(
                  color: Colors.white,
                  fontWeight: FontWeight.bold,
                  fontSize: 16,
                ),
              ),
            ),
        ],
      ),
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [Color(0xff0f172a), Colors.black87],
          ),
        ),
        child: _isLoading
            ? Center(child: CircularProgressIndicator(color: Colors.blueAccent))
            : ListView(
                padding: EdgeInsets.all(16),
                children: [
                  // Group Name
                  Card(
                    color: Colors.black54,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Padding(
                      padding: EdgeInsets.all(16),
                      child: TextField(
                        controller: nameController,
                        style: TextStyle(color: Colors.white),
                        decoration: InputDecoration(
                          labelText: 'Group Name',
                          labelStyle: TextStyle(color: Colors.grey),
                          prefixIcon: Icon(Icons.group, color: Colors.blueAccent),
                          border: InputBorder.none,
                        ),
                        maxLength: 50,
                      ),
                    ),
                  ),

                  SizedBox(height: 16),

                  // Group Description
                  Card(
                    color: Colors.black54,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Padding(
                      padding: EdgeInsets.all(16),
                      child: TextField(
                        controller: descriptionController,
                        style: TextStyle(color: Colors.white),
                        maxLines: 3,
                        decoration: InputDecoration(
                          labelText: 'Description (optional)',
                          labelStyle: TextStyle(color: Colors.grey),
                          prefixIcon: Icon(Icons.description, color: Colors.blueAccent),
                          border: InputBorder.none,
                        ),
                        maxLength: 200,
                      ),
                    ),
                  ),

                  SizedBox(height: 16),

                  // Select Members
                  Card(
                    color: Colors.black54,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Padding(
                      padding: EdgeInsets.all(16),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            children: [
                              Icon(Icons.people, color: Colors.blueAccent),
                              SizedBox(width: 8),
                              Text(
                                'Select Members',
                                style: TextStyle(
                                  color: Colors.white,
                                  fontSize: 18,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                            ],
                          ),
                          SizedBox(height: 8),
                          Text(
                            'Selected: ${_selectedMemberIds.length}',
                            style: TextStyle(color: Colors.grey),
                          ),
                          SizedBox(height: 16),
                          ..._allTenants
                              .where((tenant) => tenant.id.toString() != widget.tenantId)
                              .map((tenant) => _buildMemberTile(tenant))
                              .toList(),
                        ],
                      ),
                    ),
                  ),
                ],
              ),
      ),
    );
  }

  Widget _buildMemberTile(Tenant tenant) {
    final isSelected = _selectedMemberIds.contains(tenant.id.toString());
    
    return GestureDetector(
      onTap: () {
        setState(() {
          if (isSelected) {
            _selectedMemberIds.remove(tenant.id.toString());
          } else {
            _selectedMemberIds.add(tenant.id.toString());
          }
        });
      },
      child: Container(
        margin: EdgeInsets.only(bottom: 8),
        padding: EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: isSelected ? Colors.blueAccent.withOpacity(0.2) : Colors.grey[900],
          borderRadius: BorderRadius.circular(8),
          border: Border.all(
            color: isSelected ? Colors.blueAccent : Colors.grey,
            width: isSelected ? 2 : 1,
          ),
        ),
        child: Row(
          children: [
            Icon(
              isSelected ? Icons.check_circle : Icons.circle_outlined,
              color: isSelected ? Colors.blueAccent : Colors.grey,
            ),
            SizedBox(width: 12),
            CircleAvatar(
              radius: 20,
              backgroundColor: Colors.blueAccent.withOpacity(0.2),
              child: Text(
                tenant.name.substring(0, 1).toUpperCase(),
                style: TextStyle(
                  color: Colors.blueAccent,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
            SizedBox(width: 12),
            Expanded(
              child: Text(
                tenant.name,
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 16,
                ),
              ),
            ),
            if (tenant.onlineStatus == 'online')
              Container(
                width: 10,
                height: 10,
                decoration: BoxDecoration(
                  color: Colors.green,
                  shape: BoxShape.circle,
                ),
              ),
          ],
        ),
      ),
    );
  }
}
