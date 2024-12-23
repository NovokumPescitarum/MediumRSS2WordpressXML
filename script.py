import sys
import requests
import xml.etree.ElementTree as ET
import html

# Check if username is provided
if len(sys.argv) < 2:
    print("Usage: python3 script.py <medium_username>")
    sys.exit(1)

# Get Medium username from arguments
username = sys.argv[1]
feed_url = f"https://medium.com/feed/@{username}"

# Fetch the Medium RSS feed
response = requests.get(feed_url)
if response.status_code != 200:
    print(f"Failed to fetch feed from {feed_url}. HTTP Status: {response.status_code}")
    sys.exit(1)

rss_content = response.content

# Parse the Medium RSS feed
root = ET.fromstring(rss_content)

# Define namespaces
namespaces = {
    'dc': "http://purl.org/dc/elements/1.1/",
    'content': "http://purl.org/rss/1.0/modules/content/",
}

# Create the WordPress XML structure
wp_root = ET.Element("rss", version="2.0", attrib={
    "xmlns:excerpt": "http://wordpress.org/export/1.2/excerpt/",
    "xmlns:content": "http://purl.org/rss/1.0/modules/content/",
    "xmlns:wfw": "http://wellformedweb.org/CommentAPI/",
    "xmlns:dc": "http://purl.org/dc/elements/1.1/",
    "xmlns:wp": "http://wordpress.org/export/1.2/"
})
wp_channel = ET.SubElement(wp_root, "channel")

# Extract metadata dynamically
channel = root.find("channel")
wp_channel_metadata = {
    "title": channel.find("title").text if channel.find("title") is not None else "Imported Medium Blog",
    "link": channel.find("link").text if channel.find("link") is not None else "https://example.com",
    "description": channel.find("description").text if channel.find("description") is not None else "Medium posts imported into WordPress",
}
ET.SubElement(wp_channel, "title").text = wp_channel_metadata["title"]
ET.SubElement(wp_channel, "link").text = wp_channel_metadata["link"]
ET.SubElement(wp_channel, "description").text = wp_channel_metadata["description"]
ET.SubElement(wp_channel, "wp:wxr_version").text = "1.2"

# Convert items from Medium RSS feed to WordPress format
for item in channel.findall("item"):
    wp_item = ET.SubElement(wp_channel, "item")

    # Extract and set basic fields
    title = item.find("title")
    link = item.find("link")
    pub_date = item.find("pubDate")
    creator = item.find("dc:creator", namespaces)
    categories = item.findall("category")
    content = item.find("content:encoded", namespaces)

    ET.SubElement(wp_item, "title").text = title.text if title is not None else "Untitled"
    ET.SubElement(wp_item, "link").text = link.text if link is not None else ""
    ET.SubElement(wp_item, "pubDate").text = pub_date.text if pub_date is not None else ""
    ET.SubElement(wp_item, "dc:creator").text = creator.text if creator is not None else "Unknown"
    guid = ET.SubElement(wp_item, "guid", isPermaLink="false")
    guid.text = link.text if link is not None else ""

    # Clean and format content:encoded with proper CDATA
    if content is not None and content.text:
        cleaned_content = html.unescape(content.text.strip())
        cleaned_content = cleaned_content.replace("&lt;![CDATA[", "").replace("]]&gt;", "")
        # Add newlines between paragraphs and headers
        cleaned_content = cleaned_content.replace("<p>", "\n<p>").replace("<h3>", "\n<h3>")
        cleaned_content = cleaned_content.replace("</p>", "</p>\n").replace("</h3>", "</h3>\n")
        ET.SubElement(wp_item, "content:encoded").text = f"<![CDATA[\n{cleaned_content}\n]]>"
    else:
        ET.SubElement(wp_item, "content:encoded").text = "<![CDATA[]]>"

    # Add categories
    for category in categories:
        cat = ET.SubElement(wp_item, "category", domain="category", nicename=category.text)
        cat.text = category.text

    # Add WordPress-specific fields
    ET.SubElement(wp_item, "wp:post_date").text = pub_date.text if pub_date is not None else ""
    ET.SubElement(wp_item, "wp:status").text = "publish"
    ET.SubElement(wp_item, "wp:post_type").text = "post"

# Save the WordPress-compatible XML file
output_file = f"{username}_medium_to_wordpress.xml"
ET.ElementTree(wp_root).write(output_file, encoding="utf-8", xml_declaration=True)

print(f"WordPress XML file generated: {output_file}")
