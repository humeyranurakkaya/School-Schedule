import requests, os

TOKEN = os.environ.get("NOTION_TOKEN")
DB_ID = os.environ.get("NOTION_DATABASE_ID")

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

res = requests.post(
    f"https://api.notion.com/v1/databases/{DB_ID}/query",
    headers=headers
)

if res.status_code != 200:
    raise Exception("Notion API error:", res.text)

data = res.json()

def get_title(prop):
    try:
        return prop["title"][0]["plain_text"]
    except:
        return ""

def get_text(prop):
    try:
        return prop["rich_text"][0]["plain_text"]
    except:
        return ""

def get_select(prop):
    try:
        return prop["select"]["name"]
    except:
        return ""

md = "# 📚 Okul Programım\n\n"
md += "_Notion → GitHub otomatik senkronizasyon_\n\n"
md += "| Ders | Gün | Saat | Öğretmen | Tür |\n"
md += "|------|-----|------|----------|-----|\n"

for page in data.get("results", []):
    props = page.get("properties", {})

    ders = get_title(props.get("Ad", {})) or get_title(props.get("Ders", {})) or get_title(props.get("Name", {}))
    gun = get_select(props.get("Gün", {}))
    saat = get_text(props.get("Saat Aralığı", {})) or get_text(props.get("Saat", {}))
    ogretmen = get_text(props.get("Öğretmen adı", {})) or get_text(props.get("Öğretmen", {}))
    tur = get_select(props.get("Tür", {}))

    md += f"| {ders} | {gun} | {saat} | {ogretmen} | {tur} |\n"

with open("README.md", "w", encoding="utf-8") as f:
    f.write(md)
