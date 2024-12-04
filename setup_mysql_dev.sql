-- Creates a database

CREATE DATABASE IF NOT EXISTS hbnb_dev_db;
DROP USER IF EXISTS 'hbnb_dev'@'localhost';
CREATE USER 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';
GRANT ALL PRIVILEGES ON `hbnb_dev_db`.* TO 'hbnb_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'hbnb_dev'@'localhost';
FLUSH PRIVILEGES;
/*How Plaintext Fallback Works
When fallback occurs:

The server sends a request to the client indicating that a plaintext password is required.
The client sends the plaintext password directly over the network.
If the connection is not encrypted (e.g., using SSL/TLS), this password is exposed to potential interception.
Risks of Plaintext Password Fallback
Password Interception: If the connection is unencrypted, the plaintext password can be intercepted by attackers monitoring the network (man-in-the-middle attacks).
Reduced Security: It negates the primary benefit of the caching_sha2_password plugin, which is secure authentication using hashed credentials.
Preventing Plaintext Password Fallback
Require Secure Connections:

Enforce SSL/TLS for all connections to the MySQL server:
sql
Copy code
ALTER USER 'username'@'host' REQUIRE SSL;
Ensure that require_secure_transport is enabled in the MySQL configuration:
ini
Copy code
[mysqld]
require_secure_transport=ON
This setting forces the server to reject non-secure connections.
Disable Plaintext Fallback on the Client:

Some MySQL clients allow disabling fallback to plaintext authentication. For example:
bash
Copy code
mysql --ssl-mode=REQUIRED
This ensures the client only connects over secure channels.
Update the MySQL Client:

Use a MySQL client or library that supports caching_sha2_password to avoid needing plaintext fallback.
Use Secure Authentication:

If plaintext fallback is unavoidable, consider switching users to the mysql_native_password plugin temporarily until secure transport is available:
sql
Copy code
ALTER USER 'username'@'host' IDENTIFIED WITH 'mysql_native_password' BY 'password';


What Does localhost Mean?
Local Machine:

localhost specifically refers to the local computer where the database server is running.
Connections from localhost use the MySQL socket file rather than the network interface, which is often faster and more secure.
Access Restriction:

MySQL allows you to restrict access based on the host. For example:
hbnb_dev@localhost: The user hbnb_dev can connect only from the local machine.
hbnb_dev@%: The user hbnb_dev can connect from any host.
hbnb_dev@'192.168.1.100': The user hbnb_dev can connect only from the host with the IP address 192.168.1.100.
*/