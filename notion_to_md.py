import requests, os

TOKEN = os.environ["NOTION_TOKEN"]
DB_ID = os.environ["NOTION_DATABASE_ID"]

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

res = requests.post(
    f"https://api.notion.com/v1/databases/{DB_ID}/query",
    headers=headers
)

data = res.json()

md = "# 📚 Okul Programım\n\n"
md += "_Notion ile senkronize edilir. Otomatik güncellenir._\n\n"
md += "| Ders | Gün | Saat | Öğretmen | Tür |\n"
md += "|------|----|------|----------|-----|\n"

for page in data["results"]:
    props = page["properties"]

    ders = props["Ad"]["title"][0]["plain_text"] if props["Ad"]["title"] else ""
    gun = props["Gün"]["select"]["name"] if props["Gün"]["select"] else ""
    saat = props["Saat Aralığı"]["rich_text"][0]["plain_text"] if props["Saat Aralığı"]["rich_text"] else ""
    ogretmen = props["Öğretmen adı"]["rich_text"][0]["plain_text"] if props["Öğretmen adı"]["rich_text"] else ""
    tur = props["Tür"]["select"]["name"] if props["Tür"]["select"] else ""

    md += f"| {ders} | {gun} | {saat} | {ogretmen} | {tur} |\n"

with open("README.md", "w", encoding="utf-8") as f:
    f.write(md)
