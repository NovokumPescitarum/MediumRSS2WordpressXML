# MediumRSS2WordpressXML

## Overview
**Medium2WordpressXML** is a Python utility that converts a Medium RSS feed into a WordPress-compatible XML file. This tool simplifies migrating content from Medium to WordPress by transforming Medium's RSS data into the WordPress WXR format. The tool is also compatible with Wix's WordPress importer for seamless integration.

## Features
- Fetches and parses a Medium RSS feed.
- Converts Medium blog posts into WordPress-compatible XML.
- Preserves metadata like titles, links, publication dates, categories, and authors.
- Converts HTML content into WordPress-compatible CDATA sections.
- Saves the output XML file for easy import into WordPress or Wix.

## Prerequisites
- Python 3.6+
- Required Python libraries:
  - `requests`
  - `beautifulsoup4`

Install dependencies using:
```bash
pip install requests beautifulsoup4
```

## Usage
### Function Signature
```python
medium_to_wordpress_rss(medium_rss_url: str, output_file_url: str) -> None
```

### Parameters
- **medium_rss_url**: The URL of the Medium RSS feed (e.g., `https://medium.com/feed/@username`).
- **output_file_url**: The directory path where the generated WordPress XML file will be saved.

### Example
```python
from medium_to_wordpress import medium_to_wordpress_rss

# Convert a Medium RSS feed to WordPress XML
medium_to_wordpress_rss("https://medium.com/feed/@exampleuser", "/path/to/output")
```

### Output
The output file `medium_to_wordpress.xml` will be saved in the specified output directory.

## How It Works
1. Fetches the Medium RSS feed using the provided URL.
2. Parses the RSS feed to extract blog posts, including titles, links, authors, categories, and content.
3. Converts HTML content into plain text or WordPress-compatible CDATA sections.
4. Generates a WordPress-compatible XML file (WXR format) with the extracted data.

## Using with Wix WordPress Importer
Wix provides a WordPress importer tool that allows you to directly import WordPress XML files into your Wix site. This tool simplifies the migration of blog posts and associated metadata.

### Steps to Use with Wix:
1. **Generate WordPress XML**:
   - Use this script to create a WordPress-compatible XML file from your Medium RSS feed.
   - The generated file will be structured in the WXR format that Wix's WordPress importer supports.

2. **Upload to Wix**:
   - Log in to your Wix account.
   - Navigate to the **Dashboard** of your site.
   - Go to **Blog** > **Posts**. > **More Actions** > **Import Posts** > **Wordpress Site** > **Use Wordpress XML File**
   - ![images/image](https://github.com/user-attachments/assets/02d4abab-895e-4d19-8436-95cbfcfe9894)
   - Select the option to import from WordPress and upload the generated XML file.

3. **Map and Review Content**:
   - During the import process, Wix will guide you through mapping your blog content.
   - Ensure titles, content, categories, and authors are correctly mapped to your Wix blog.

4. **Publish Your Blog**:
   - Once the import is complete, review your blog posts in Wix.
   - Make any necessary adjustments to formatting and publish your blog.

By using the WordPress importer in Wix, you can seamlessly migrate your Medium content without manual data entry or formatting.

## File Structure
### WordPress XML Format
Each Medium post is converted into the following structure:
```xml
<item>
  <title>Post Title</title>
  <link>Post URL</link>
  <pubDate>Publication Date</pubDate>
  <dc:creator>Author</dc:creator>
  <guid isPermaLink="false">Post URL</guid>
  <content:encoded><![CDATA[Post Content]]></content:encoded>
  <category domain="category">Category Name</category>
  <wp:post_date>Publication Date</wp:post_date>
  <wp:status>publish</wp:status>
  <wp:post_type>post</wp:post_type>
</item>
```

## Error Handling
- Ensures HTTP status is checked before processing the RSS feed.
- Handles missing fields gracefully, providing default values when necessary.

## Contributing
1. Fork the repository.
2. Create a new branch (`feature/your-feature`).
3. Commit your changes.
4. Open a pull request.

## License
This project is licensed under the MIT License.
