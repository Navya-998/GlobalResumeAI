from flask import Blueprint, Response

seo = Blueprint("seo", __name__)


@seo.route("/robots.txt")
def robots():
    txt = """User-agent: *
Allow: /

Sitemap: https://globalresumeai.onrender.com/sitemap.xml
"""
    return Response(txt, mimetype="text/plain")


@seo.route("/sitemap.xml")
def sitemap():

    xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">

<url>
<loc>https://globalresumeai.onrender.com/</loc>
<priority>1.0</priority>
<changefreq>daily</changefreq>
</url>

<url>
<loc>https://globalresumeai.onrender.com/login</loc>
<priority>0.8</priority>
<changefreq>monthly</changefreq>
</url>

<url>
<loc>https://globalresumeai.onrender.com/register</loc>
<priority>0.8</priority>
<changefreq>monthly</changefreq>
</url>

<url>
<loc>https://globalresumeai.onrender.com/dashboard</loc>
<priority>0.9</priority>
<changefreq>weekly</changefreq>
</url>

<url>
<loc>https://globalresumeai.onrender.com/resume</loc>
<priority>1.0</priority>
<changefreq>weekly</changefreq>
</url>

<url>
<loc>https://globalresumeai.onrender.com/career-hub</loc>
<priority>0.9</priority>
<changefreq>weekly</changefreq>
</url>

</urlset>
"""

    return Response(xml, mimetype="application/xml")