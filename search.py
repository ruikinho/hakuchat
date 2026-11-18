import json
import re
import subprocess
import urllib.parse


def _strip_tags(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text)


def _curl_get(url: str) -> str:
    result = subprocess.run(
        ["curl", "-s", "--fail", "-L", url],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def web_search(query: str) -> str:
    encoded = urllib.parse.quote(query)
    url = (
        "https://en.wikipedia.org/w/api.php"
        f"?action=query&list=search&srsearch={encoded}"
        "&format=json&srlimit=5"
    )
    raw = _curl_get(url)
    data = json.loads(raw)
    results = data.get("query", {}).get("search", [])
    if not results:
        return f"No results found for: {query}"
    lines = [f"Search results for '{query}':\n"]
    for item in results:
        title = item.get("title", "")
        snippet = _strip_tags(item.get("snippet", ""))
        link = "https://en.wikipedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_"))
        lines.append(f"- {title}: {snippet}")
        lines.append(f"  {link}")
    return "\n".join(lines)


if __name__ == "__main__":
    print(web_search("Helsinki"))
