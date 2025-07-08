# -*- coding: utf-8 -*-
import os
import csv
import json
#sayfalar klasoru kontrol edilir, yoksa olusturulur
base_dir = os.path.dirname(os.path.abspath(__file__))
klasor_yolu = os.path.join(base_dir, "sayfalar")
if not os.path.exists(klasor_yolu):
    os.mkdir(klasor_yolu)
#csv verileri islenir
csv_yolu = os.path.join(base_dir, "veriler.csv")
with open(csv_yolu, newline='', encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    veriler = sorted(list(reader), key=lambda x: x[0].lower())

# ortak stil sayfalarını olusturan kod blogu
ortak_css = """
<style>
    body {
        font-family: 'Segoe UI', Tahoma, sans-serif;
        margin: 0;
        background-color: #f4f4f4;
        color: #222;
    }
    .navbar {
        background: #228F42;
        color: white;
        padding: 15px 20px;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .navbar a {
        color: white;
        text-decoration: none;
        font-weight: bold;
        margin: 0 15px;
    }
    .container {
        max-width: 900px;
        margin: 40px auto;
        padding: 30px;
        background: white;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .footer {
        text-align:center;
        padding: 30px 0;
        font-size: 16px;
    }
    .footer a {
        color: #0066cc;
        text-decoration: none;
        margin: 0 10px;
    }
</style>
"""

#islenen verilerle sayfalar olusturur
for veri in veriler:
    kelime, tur, turkce, ekstra = veri
    dosya_yolu = os.path.join(klasor_yolu, f"{kelime}.html")
    with open(dosya_yolu, "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>{kelime}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    {ortak_css}
    <style>
        h1 {{ font-size: 42px; }}
        .tur {{ font-style: italic; color: gray; font-size: 18px; margin-bottom: 20px; }}
        p {{ font-size: 22px; line-height: 1.6em; }}
        .ekstra {{
            margin-top: 30px;
            font-size: 18px;
            background: #e8f5e9;
            padding: 15px;
            border-left: 5px solid #228F42;
            border-radius: 6px;
            color: #222;
        }}
    </style>
</head>
<body>
    <div class="navbar">
        <a href="../index.html">Ana sayfa</a>
    </div>
    <div class="container">
        <h1>{kelime}</h1>
        <div class="tur">{tur}</div>
        <p>{turkce}</p>
        <div class="ekstra">{ekstra}</div>
    </div>
    <div class="footer">
        <a href="../hakkinda.html">hakkında</a> |
        <a href="../iletisim.html">iletişim</a>
    </div>
</body>
</html>""")

#arama sistemi için json hazır ediliyor
veri_json_yolu = os.path.join(base_dir, "veriler.js")
with open(veri_json_yolu, "w", encoding="utf-8") as f:
    f.write("const veriler = " + json.dumps(veriler, ensure_ascii=False) + ";")

# index.html ana sayfa olusturumu
index_yolu = os.path.join(base_dir, "index.html")
with open(index_yolu, "w", encoding="utf-8") as index:
    index.write(f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>Xurme Kürtçe - Türkçe Sözlük</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    {ortak_css}
    <style>
        h2 {{ font-size: 28px; }}
        .switcher {{ display: flex; gap: 20px; justify-content:center; margin-bottom: 20px; }}
        .switcher button {{
            padding: 8px 20px;
            border: none;
            border-radius: 20px;
            background: #228F42;
            color: white;
            cursor: pointer;
            font-weight: bold;
        }}
        .switcher button.active {{ background: #155f2a; }}
        #arama {{
            width: 60%;
            padding: 12px 16px;
            margin: 0 auto 25px auto;
            font-size: 18px;
            border: 1px solid #ccc;
            border-radius: 10px;
            display: block;
            outline: none;
        }}
        ul {{ list-style-type: none; padding: 0; }}
        li {{ margin: 12px 0; }}
        a {{ text-decoration: none; color: #0066cc; font-size: 20px; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <div class="navbar">
        <h1 style="margin: 0 auto;">Xurme Kürtçe - Türkçe Sözlük</h1>
    </div>
    <div class="container">
        <div class="switcher">
            <button id="btn-kurtce" class="active" onclick="degistir('kurtce')">Kürtçe</button>
            <button id="btn-turkce" onclick="degistir('turkce')">Türkçe</button>
        </div>
        <input type="text" id="arama" placeholder="Ara..." oninput="ara()">
        <ul id="sonuclar"></ul>
    </div>
    <div class="footer">
        <a href="hakkinda.html">Hakkında</a> |
        <a href="iletisim.html">İletişim</a>
    </div>
    <script src="veriler.js"></script>
    <script>
        let aramaModu = "kurtce";

        function degistir(mod) {{
            aramaModu = mod;
            document.getElementById("btn-kurtce").classList.toggle("active", mod === "kurtce");
            document.getElementById("btn-turkce").classList.toggle("active", mod === "turkce");
            ara();
        }}

        function ara() {{
            const q = document.getElementById("arama").value.toLowerCase();
            const ul = document.getElementById("sonuclar");
            ul.innerHTML = "";

            if(q.length < 2) return;

            veriler.forEach(v => {{
                const kelime = v[0].toLowerCase();
                const anlam = v[2].toLowerCase();
                if((aramaModu === "kurtce" && kelime.includes(q)) || (aramaModu === "turkce" && anlam.includes(q))) {{
                    let gosterilen = aramaModu === "kurtce" ? v[0] : v[2];
                    const li = document.createElement("li");
                    li.innerHTML = '<a href="sayfalar/' + v[0] + '.html">' + gosterilen + '</a>';
                    ul.appendChild(li);
                }}
            }});
        }}
    </script>
</body>
</html>""")

# sabit sayfaları oluşturmak için ayrılan alan
for sayfa, baslik, icerik in [
    ("hakkinda.html", "Hakkında", "Xurme Kürtçe-Türkçe sözlük, Kürtçe ve Türkçe dilleri arası sözlük hizmeti sağlamayı hedefleyen bir projedir. Site tasarımı dikkat dağıtıcı unsurlardan uzak; modern ve sade tasarlanmıştır. Site Python, HTML, CSS, JavaScript teknolojileri kullanılarak geliştirilmiş olup sitenin kaynak kodları kullanıcıların erişimine açıktır. Sitenin kaynak kodlarına ilgili adresten ulaşılabilir."),
    ("iletisim.html", "İletişim", "Xurme Kürtçe - Türkçe Sözlük ve içerikleri hakkında talepleriniz, önerileriniz ve şikayetleriniz için belirtilen mail adresini kullanabilirsiniz: <a href='mailto:projectxurme@gmail.com'>projectxurme@gmail.com</a>")
]:
    with open(os.path.join(base_dir, sayfa), "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>{baslik}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    {ortak_css}
    <style>
        h1 {{ font-size: 32px; margin-bottom: 20px; }}
        p {{ font-size: 18px; line-height: 1.6em; }}
    </style>
</head>
<body>
    <div class="navbar">
        <a href="index.html">Ana Sayfa</a>
    </div>
    <div class="container">
        <h1>{baslik}</h1>
        <p>{icerik}</p>
    </div>
</body>
</html>""")
