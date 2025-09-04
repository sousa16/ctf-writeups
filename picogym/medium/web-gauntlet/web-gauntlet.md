## Web gauntlet

[Link to challenge](https://play.picoctf.org/practice/challenge/88)

Write-up:

1. Attempting to login as `admin:admin` shows us the query used by the request:
`SELECT * FROM users WHERE username='admin' AND password='admin'`

2. Attempting `admin:'` credentials triggers an error that shows us that SQLite3 is being used.

3. `admin:'+OR+1=1--` triggers the filters. We can anaylze the `filter.php` page to
see that what triggered the filter was the `OR` keyword.

4. Using username `admin'-- ` worked. On to round 2.

5. 