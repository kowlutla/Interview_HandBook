import re, os, sys
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(root)

def retro(old, new, pid, subs):
    s = open('chapters/' + old, encoding='utf-8').read()
    # replace hand-written sidebar with a generated one
    s = re.sub(r'<nav class="toc">.*?</nav>', '<nav class="toc" id="toc"></nav>', s, flags=re.S)
    s = s.replace('<body>', '<body data-page="%s">' % pid, 1)
    s = s.replace('<script>\n// Helpers', '<script src="../assets/chapters.js"></script>\n<script src="../assets/nav.js"></script>\n<script>\n// Helpers', 1)
    for a, b in subs:
        s = s.replace(a, b)
    open('chapters/' + new, 'w', encoding='utf-8').write(s)
    os.remove('chapters/' + old)

retro('09b-cdn.html', '12-cdn.html', '12-cdn', [
    ('Chapter 9b: Content Delivery Networks (CDN)', 'Chapter 12: Content Delivery Networks (CDN)'),
    ('Chapter 9b · Module 2', 'Chapter 12 · Module 2'),
    ('Chapter 3 (DNS, TLS, HTTP), Chapter 8 (load balancing), and Chapter 10 (caching patterns and invalidation)',
     '<a href="03-networking-essentials.html">Chapter 3</a> (TCP, TLS, HTTP), <a href="04-dns.html">Chapter 4</a> (DNS), <a href="09-load-balancing.html">Chapter 9</a> (load balancing), and <a href="13-caching-patterns.html">Chapter 13</a> (caching patterns and invalidation)'),
    ('Leads to Chapter 11 (stampede and avalanche), Chapter 17 (object storage as an origin), Chapter 12 (rate limiting at the edge)',
     'Leads to <a href="14-caching-failures.html">Chapter 14</a> (stampede and avalanche), <a href="21-object-storage.html">Chapter 21</a> (object storage as an origin), <a href="16-rate-limiting.html">Chapter 16</a> (rate limiting at the edge)'),
    ('described in Chapter 11', 'described in Chapter 14'),
    ('This is the same hard problem as in Chapter 10', 'This is the same hard problem as in Chapter 13'),
    ('Chapter 17 covers object storage', 'Chapter 21 covers object storage'),
])
retro('10-caching-patterns.html', '13-caching-patterns.html', '13-caching-patterns', [
    ('Chapter 9b</a> covers them in detail', 'Chapter 12</a> covers them in detail'),
    ('Chapter 9b</a> (CDN in depth)', 'Chapter 12</a> (CDN in depth)'),
])
print('done')
