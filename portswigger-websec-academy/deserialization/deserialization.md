## Modifying serialized objects

[Modifying serialized objects](https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-modifying-serialized-objects)

Write-up:

1. Logging in sets a session cookie: `TzTzo0OiJVc2VyIjoyOntzOjg6InVzZXJuYW1lIjtzOjY6IndpZW5lciI7czo1OiJhZG1pbiI7YjowO30%3d`

2. Base-64 decoding this gets us `O:4:"User":2:{s:8:"username";s:6:"wiener";s:5:"admin";b:0;}`
Altering the admin value to 1, re-encoding the cookie and changing it in the lab
gets us admin access. Accessing the admin panel allows us to delete user `carlos`
and solve the lab. 

