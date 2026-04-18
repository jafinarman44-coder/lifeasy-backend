import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:async';
import 'chat_screen.dart';

class TenantListScreen extends StatefulWidget {
  final String tenantId;
  
  const TenantListScreen({Key? key, required this.tenantId}) : super(key: key);

  @override
  _TenantListScreenState createState() => _TenantListScreenState();
}

class _TenantListScreenState extends State<TenantListScreen> {
  final TextEditingController _searchController = TextEditingController();
  List<Tenant> _allTenants = [];
  List<Tenant> _filteredTenants = [];
  bool _isLoading = true;
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    _fetchTenants();
  }

  Future<void> _fetchTenants() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      // Replace with your actual server IP
      final url = Uri.parse('https://lifeasy-backend-production.up.railway.app/api/tenants/all?include_offline=true');
      
      final response = await http.get(
        url,
        headers: {
          'Content-Type': 'application/json',
          // Add auth token if needed
          // 'Authorization': 'Bearer ${your_token}',
        },
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        setState(() {
          _allTenants = data.map((json) => Tenant.fromJson(json)).toList();
          _filteredTenants = _allTenants;
          _isLoading = false;
        });
      } else {
        setState(() {
          _errorMessage = 'Failed to load tenants';
          _isLoading = false;
        });
      }
    } catch (e) {
      setState(() {
        _errorMessage = 'Error: $e';
        _isLoading = false;
      });
    }
  }

  void _filterTenants(String query) {
    setState(() {
      if (query.isEmpty) {
        _filteredTenants = _allTenants;
      } else {
        _filteredTenants = _allTenants.where((tenant) {
          return tenant.name.toLowerCase().contains(query.toLowerCase()) ||
                 tenant.email.toLowerCase().contains(query.toLowerCase());
        }).toList();
      }
    });
  }

  Color _getStatusColor(String status) {
    switch (status) {
      case 'online':
        return Colors.green;
      case 'away':
        return Colors.orange;
      default:
        return Colors.grey;
    }
  }

  String _getStatusText(String status) {
    switch (status) {
      case 'online':
        return '🟢 Online';
      case 'away':
        return '🟡 Away';
      default:
        return '⚫ Offline';
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Tenants'),
        backgroundColor: Colors.blueAccent,
        elevation: 0,
      ),
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [Color(0xff0f172a), Colors.black87],
          ),
        ),
        child: Column(
          children: [
            // Search Bar
            Padding(
              padding: EdgeInsets.all(16),
              child: TextField(
                controller: _searchController,
                style: TextStyle(color: Colors.white),
                decoration: InputDecoration(
                  hintText: 'Search tenants by name or email...',
                  hintStyle: TextStyle(color: Colors.grey),
                  prefixIcon: Icon(Icons.search, color: Colors.grey),
                  suffixIcon: _searchController.text.isNotEmpty
                      ? IconButton(
                          icon: Icon(Icons.clear, color: Colors.grey),
                          onPressed: () {
                            _searchController.clear();
                            _filterTenants('');
                          },
                        )
                      : null,
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(12),
                    borderSide: BorderSide.none,
                  ),
                  filled: true,
                  fillColor: Colors.grey[800],
                  contentPadding: EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                ),
                onChanged: _filterTenants,
              ),
            ),

            // Tenants List
            Expanded(
              child: _isLoading
                  ? Center(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          CircularProgressIndicator(color: Colors.blueAccent),
                          SizedBox(height: 16),
                          Text(
                            'Loading tenants...',
                            style: TextStyle(color: Colors.grey, fontSize: 16),
                          ),
                        ],
                      ),
                    )
                  : _errorMessage != null
                      ? Center(
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Icon(Icons.error_outline, color: Colors.red, size: 60),
                              SizedBox(height: 16),
                              Text(
                                _errorMessage!,
                                style: TextStyle(color: Colors.red, fontSize: 16),
                                textAlign: TextAlign.center,
                              ),
                              SizedBox(height: 16),
                              ElevatedButton(
                                onPressed: _fetchTenants,
                                child: Text('Retry'),
                              ),
                            ],
                          ),
                        )
                      : _filteredTenants.isEmpty
                          ? Center(
                              child: Column(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                  Icon(Icons.people_outline, color: Colors.grey, size: 60),
                                  SizedBox(height: 16),
                                  Text(
                                    'No tenants found',
                                    style: TextStyle(color: Colors.grey, fontSize: 16),
                                  ),
                                ],
                              ),
                            )
                          : RefreshIndicator(
                              onRefresh: _fetchTenants,
                              child: ListView.builder(
                                padding: EdgeInsets.symmetric(horizontal: 16),
                                itemCount: _filteredTenants.length,
                                itemBuilder: (context, index) {
                                  final tenant = _filteredTenants[index];
                                  return _buildTenantCard(tenant);
                                },
                              ),
                            ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildTenantCard(Tenant tenant) {
    return Card(
      color: Colors.black54,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
      ),
      margin: EdgeInsets.only(bottom: 12),
      child: ListTile(
        leading: Stack(
          children: [
            CircleAvatar(
              radius: 28,
              backgroundColor: tenant.onlineStatus == 'online' 
                  ? Colors.green.withOpacity(0.2) 
                  : Colors.blueAccent.withOpacity(0.2),
              child: Text(
                tenant.name.substring(0, 1).toUpperCase(),
                style: TextStyle(
                  color: tenant.onlineStatus == 'online' ? Colors.green : Colors.blueAccent,
                  fontSize: 26,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
            // WhatsApp-style online indicator
            if (tenant.onlineStatus == 'online')
              Positioned(
                right: 0,
                bottom: 0,
                child: Container(
                  width: 18,
                  height: 18,
                  decoration: BoxDecoration(
                    color: Colors.green,
                    shape: BoxShape.circle,
                    border: Border.all(color: Colors.white, width: 2.5),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.green.withOpacity(0.6),
                        blurRadius: 8,
                        spreadRadius: 2,
                      ),
                    ],
                  ),
                ),
              )
            else if (tenant.onlineStatus == 'away')
              Positioned(
                right: 0,
                bottom: 0,
                child: Container(
                  width: 18,
                  height: 18,
                  decoration: BoxDecoration(
                    color: Colors.orange,
                    shape: BoxShape.circle,
                    border: Border.all(color: Colors.white, width: 2.5),
                  ),
                ),
              )
            else
              Positioned(
                right: 0,
                bottom: 0,
                child: Container(
                  width: 18,
                  height: 18,
                  decoration: BoxDecoration(
                    color: Colors.grey,
                    shape: BoxShape.circle,
                    border: Border.all(color: Colors.white, width: 2.5),
                  ),
                ),
              ),
          ],
        ),
        title: Text(
          tenant.name,
          style: TextStyle(
            color: Colors.white,
            fontWeight: FontWeight.bold,
            fontSize: 16,
          ),
        ),
        subtitle: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            SizedBox(height: 4),
            Text(
              tenant.email,
              style: TextStyle(color: Colors.grey, fontSize: 13),
            ),
            if (tenant.flat != null && tenant.flat!.isNotEmpty)
              Text(
                'Flat: ${tenant.flat}',
                style: TextStyle(color: Colors.grey, fontSize: 12),
              ),
            SizedBox(height: 4),
            // WhatsApp-style status text
            Row(
              children: [
                if (tenant.onlineStatus == 'online')
                  Icon(Icons.circle, color: Colors.green, size: 10),
                if (tenant.onlineStatus == 'away')
                  Icon(Icons.circle, color: Colors.orange, size: 10),
                if (tenant.onlineStatus == 'offline')
                  Icon(Icons.circle, color: Colors.grey, size: 10),
                SizedBox(width: 6),
                Text(
                  tenant.onlineStatus == 'online' 
                      ? 'Online now' 
                      : tenant.onlineStatus == 'away'
                          ? 'Away'
                          : 'Offline',
                  style: TextStyle(
                    color: tenant.onlineStatus == 'online' 
                        ? Colors.green 
                        : tenant.onlineStatus == 'away'
                            ? Colors.orange
                            : Colors.grey,
                    fontSize: 12,
                    fontWeight: tenant.onlineStatus == 'online' ? FontWeight.w600 : FontWeight.normal,
                  ),
                ),
              ],
            ),
          ],
        ),
        trailing: Icon(
          Icons.chat_bubble_outline,
          color: Colors.blueAccent,
        ),
        onTap: () {
          // Navigate to chat screen with this tenant
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (_) => ChatScreen(
                tenantId: widget.tenantId,
                receiverId: tenant.id.toString(),
                receiverName: tenant.name,
              ),
            ),
          );
        },
      ),
    );
  }

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }
}

class Tenant {
  final int id;
  final String name;
  final String email;
  final String? phone;
  final String? flat;
  final String? building;
  final bool isActive;
  final bool isVerified;
  final String onlineStatus;

  Tenant({
    required this.id,
    required this.name,
    required this.email,
    this.phone,
    this.flat,
    this.building,
    required this.isActive,
    required this.isVerified,
    required this.onlineStatus,
  });

  factory Tenant.fromJson(Map<String, dynamic> json) {
    return Tenant(
      id: json['id'],
      name: json['name'],
      email: json['email'],
      phone: json['phone'],
      flat: json['flat'],
      building: json['building'],
      isActive: json['is_active'] ?? false,
      isVerified: json['is_verified'] ?? false,
      onlineStatus: json['online_status'] ?? 'offline',
    );
  }
}
