import requests
from urllib.parse import urljoin

def scan_directories(base_url, wordlist_file, output_file):
    # Make sure base_url ends with a slash for clean joining
    if not base_url.endswith("/"):
        base_url += "/"

    # Read paths from wordlist
    with open(wordlist_file, "r") as f:
        paths = [line.strip() for line in f if line.strip()]

    found = []

    for path in paths:
        url = urljoin(base_url, path)
        try:
            response = requests.get(url, timeout=5)
            status = response.status_code

            # Show only "interesting" results
            if status in [200, 301, 302, 401, 403]:
                print(f"[+] {url} -> {status}")
                found.append((url, status))
            else:
                print(f"[-] {url} -> {status}")

        except requests.RequestException as e:
            print(f"[!] Error requesting {url}: {e}")

    # Save results
    with open(output_file, "w") as f:
        for url, status in found:
            f.write(f"{url} -> {status}\n")

    print(f"\nScan complete. {len(found)} interesting results saved to {output_file}.")


if __name__ == "__main__":
    # 👇 CHANGE THIS TO YOUR LAB TARGET, NOT RANDOM LIVE SITES
    base_url = "http://127.0.0.1:5000"
    wordlist_file = "wordlist.txt"
    output_file = "scan_results.txt"

    scan_directories(base_url, wordlist_file, output_file)
