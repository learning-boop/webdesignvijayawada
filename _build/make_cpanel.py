"""Make a cPanel-ready copy of the site for websitedesigninvijayawada.com.

Run after build.py:  python _build/make_cpanel.py
Output: _cpanel/site/ (the files) and _cpanel/websitedesigninvijayawada-cpanel.zip
Upload the zip into public_html in cPanel File Manager and choose Extract.

The GitHub Pages version is left unchanged; only the copy is rewritten.
"""
import os, shutil, subprocess, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, '_cpanel')
SITE = os.path.join(OUT, 'site')
ZIP = os.path.join(OUT, 'websitedesigninvijayawada-cpanel.zip')

OLD_BASE = 'https://learning-boop.github.io/webdesignvijayawada/'
NEW_BASE = 'https://websitedesigninvijayawada.com/'
OLD_PATH = '/webdesignvijayawada/'   # absolute links used by 404.html
NEW_PATH = '/'

HTACCESS = r"""# Website Design Vijayawada — cPanel / Apache settings
DirectoryIndex index.html
ErrorDocument 404 /404.html
Options -Indexes

# Always use https://websitedesigninvijayawada.com (no www)
<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteCond %{HTTPS} off [OR]
  RewriteCond %{HTTP_HOST} ^www\. [NC]
  RewriteRule ^(.*)$ https://websitedesigninvijayawada.com/$1 [L,R=301]
</IfModule>

# Compress text files
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css application/javascript text/javascript application/xml text/xml text/plain image/svg+xml
</IfModule>

# Browser caching (styles.css, script.js and motion.js carry a ?v= version, so they can be cached long)
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresDefault "access plus 1 hour"
  ExpiresByType text/html "access plus 0 seconds"
  ExpiresByType text/css "access plus 1 year"
  ExpiresByType application/javascript "access plus 1 year"
  ExpiresByType text/javascript "access plus 1 year"
  ExpiresByType image/webp "access plus 1 month"
  ExpiresByType image/png "access plus 1 month"
  ExpiresByType image/jpeg "access plus 1 month"
  ExpiresByType image/x-icon "access plus 1 month"
</IfModule>

<IfModule mod_mime.c>
  AddType image/webp .webp
</IfModule>
"""

TEXT = ('.html', '.xml', '.txt', '.css', '.js', '.json')


def site_files():
    """Files tracked by git, minus build tools and notes."""
    out = subprocess.run(['git', 'ls-files'], cwd=ROOT, capture_output=True, text=True, check=True).stdout
    for f in out.splitlines():
        if f.startswith(('_', '.')) or f.endswith('.md'):
            continue
        yield f


def main():
    shutil.rmtree(SITE, ignore_errors=True)
    os.makedirs(SITE)
    n = 0
    for f in site_files():
        src, dst = os.path.join(ROOT, f), os.path.join(SITE, f)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if f.endswith(TEXT):
            t = open(src, encoding='utf-8').read().replace(OLD_BASE, NEW_BASE)
            if f == '404.html':
                t = t.replace(f'"{OLD_PATH}', f'"{NEW_PATH}')
            open(dst, 'w', encoding='utf-8', newline='\n').write(t)
        else:
            shutil.copyfile(src, dst)
        n += 1
    open(os.path.join(SITE, '.htaccess'), 'w', encoding='utf-8', newline='\n').write(HTACCESS)

    if os.path.exists(ZIP):
        os.remove(ZIP)
    with zipfile.ZipFile(ZIP, 'w', zipfile.ZIP_DEFLATED) as z:
        for dirpath, _, files in os.walk(SITE):
            for name in files:
                full = os.path.join(dirpath, name)
                z.write(full, os.path.relpath(full, SITE).replace(os.sep, '/'))
    print(f'cPanel copy: {n} files + .htaccess -> {os.path.relpath(ZIP, ROOT)} ({os.path.getsize(ZIP) // 1024} KB)')


if __name__ == '__main__':
    main()
