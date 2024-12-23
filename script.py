# Medium2WordpressXML

import os
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import html
import requests

def medium_to_wordpress_rss(medium_rss_url, output_file_url):
    """
    Convert a Medium RSS feed to a WordPress-compatible XML file.

    Args:
        medium_rss_url (str): URL to the Medium RSS feed.
        output_file_url (str): URL for the output file download location.

    Returns:
        None
    """
    # Fetch the Medium RSS feed
    response = requests.get(medium_rss_url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch Medium RSS feed. HTTP Status: {response.status_code}")

    # Parse the RSS feed
    rss_tree = ET.fromstring(response.content)
    channel = rss_tree.find("channel")

    # Create the WordPress XML structure
    wp_root = ET.Element("rss", version="2.0", attrib={
        "xmlns:excerpt": "http://wordpress.org/export/1.2/excerpt/",
        "xmlns:content": "http://purl.org/rss/1.0/modules/content/",
        "xmlns:wfw": "http://wellformedweb.org/CommentAPI/",
        "xmlns:dc": "http://purl.org/dc/elements/1.1/",
        "xmlns:wp": "http://wordpress.org/export/1.2/"
    })
    wp_channel = ET.SubElement(wp_root, "channel")

    # Extract and set channel metadata dynamically
    wp_channel_metadata = {
        "title": channel.find("title").text if channel.find("title") is not None else "Imported Medium Blog",
        "link": channel.find("link").text if channel.find("link") is not None else "https://example.com",
        "description": channel.find("description").text if channel.find("description") is not None else "Medium posts imported into WordPress",
    }
    ET.SubElement(wp_channel, "title").text = wp_channel_metadata["title"]
    ET.SubElement(wp_channel, "link").text = wp_channel_metadata["link"]
    ET.SubElement(wp_channel, "description").text = wp_channel_metadata["description"]
    ET.SubElement(wp_channel, "wp:wxr_version").text = "1.2"

    # Convert each Medium item to WordPress-compatible format
    for item in channel.findall("item"):
        wp_item = ET.SubElement(wp_channel, "item")

        # Extract fields from the Medium RSS
        title = item.find("title").text if item.find("title") is not None else "Untitled"
        link = item.find("link").text if item.find("link") is not None else ""
        pub_date = item.find("pubDate").text if item.find("pubDate") is not None else ""
        creator = item.find("dc:creator").text if item.find("dc:creator") is not None else "Unknown"
        categories = item.findall("category")
        content = item.find("content:encoded").text if item.find("content:encoded") is not None else ""

        # Set WordPress fields
        ET.SubElement(wp_item, "title").text = title
        ET.SubElement(wp_item, "link").text = link
        ET.SubElement(wp_item, "pubDate").text = pub_date
        ET.SubElement(wp_item, "dc:creator").text = creator
        guid = ET.SubElement(wp_item, "guid", isPermaLink="false")
        guid.text = link

        # Convert content to plain text
        plain_text_content = BeautifulSoup(html.unescape(content.strip()), "html.parser").get_text()
        ET.SubElement(wp_item, "content:encoded").text = f"<![CDATA[{plain_text_content}]]>"

        # Add categories
        for category in categories:
            cat = ET.SubElement(wp_item, "category", domain="category", nicename=category.text)
            cat.text = category.text

        # Add WordPress-specific fields
        ET.SubElement(wp_item, "wp:post_date").text = pub_date
        ET.SubElement(wp_item, "wp:status").text = "publish"
        ET.SubElement(wp_item, "wp:post_type").text = "post"

    # Save to file
    output_path = os.path.join(output_file_url, "medium_to_wordpress.xml")
    ET.ElementTree(wp_root).write(output_path, encoding="utf-8", xml_declaration=True)

    print(f"WordPress XML generated at: {output_path}")
