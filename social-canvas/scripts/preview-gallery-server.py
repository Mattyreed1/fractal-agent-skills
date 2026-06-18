#!/usr/bin/env python3
"""Editable gallery preview server for social-canvas (Claude Code runtime).

DURABLE: this script lives in the skill (scripts/), NOT in /tmp, so the Phase-2
`rm -rf /tmp/social-canvas` setup step can never wipe it. launch.json must point
here (with the slide dir + port as args), never at a /tmp-resident copy.

Serves a working slide directory, renders each slide-*.html in a scaled iframe
sized to that slide's OWN canvas dimensions (auto-detected from its body rule, so
square/portrait/landscape all frame correctly), and exposes a **Save Edits** button
(design-rule 90) that POSTs each iframe's edited HTML back to its served file.
Every save writes a timestamped backup first (rule 92d) and strips browser-injected
inline styles (rule 91b).

Usage:  python3 preview-gallery-server.py [SLIDE_DIR] [PORT]
Default: SLIDE_DIR=/tmp/social-canvas  PORT=8547
"""
import http.server
import socketserver
import os
import sys
import re
import glob
import json
import time
import shutil
from urllib.parse import urlparse

SLIDE_DIR = sys.argv[1] if len(sys.argv) > 1 else "/tmp/social-canvas"
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 8547
BACKUP_DIR = os.path.join(SLIDE_DIR, ".backups")
DISPLAY_SCALE = 0.62


def list_slides():
    return sorted(os.path.basename(p) for p in glob.glob(os.path.join(SLIDE_DIR, "slide-*.html")))


def slide_dims(path):
    """Read the slide's own canvas size from its `body { width:Npx; height:Mpx }`
    so the gallery frame matches (square, portrait, landscape all frame right)."""
    try:
        with open(path, encoding="utf-8") as fh:
            m = re.search(r"width:\s*(\d+)px;\s*height:\s*(\d+)px", fh.read())
            if m:
                return int(m.group(1)), int(m.group(2))
    except Exception:
        pass
    return 1080, 1350


def sanitize(html):
    """plaintext-only contenteditable avoids style-span injection, but strip any inline
    style attr the browser added to non-<img> elements (rule 91b: only the logo <img>
    legitimately carries an inline style)."""
    def strip_style(m):
        tag = m.group(0)
        if tag[:4].lower() == "<img":
            return tag
        return re.sub(r'\s+style="[^"]*"', "", tag)
    html = re.sub(r'<[a-zA-Z][^>]*>', strip_style, html)
    if not html.lstrip().lower().startswith("<!doctype"):
        html = "<!DOCTYPE html>\n" + html
    return html


def gallery_html():
    slides = list_slides()
    cards = []
    for s in slides:
        w, h = slide_dims(os.path.join(SLIDE_DIR, s))
        fw, fh = int(w * DISPLAY_SCALE), int(h * DISPLAY_SCALE)
        cards.append(
            '<div class="card"><div class="frame" style="width:%dpx;height:%dpx;">'
            '<iframe data-file="%s" src="%s?t=%d" style="width:%dpx;height:%dpx;'
            'transform:scale(%s);transform-origin:top left;border:0;display:block;"></iframe>'
            '</div></div>' % (fw, fh, s, s, int(time.time()), w, h, DISPLAY_SCALE)
        )
    frames = "\n".join(cards) if cards else ('<div class="empty">No slide-*.html in %s yet.</div>' % SLIDE_DIR)
    head = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Social Canvas - editable gallery</title>
<style>
  html,body{margin:0;background:#17171a;font-family:-apple-system,system-ui,sans-serif;color:#e4e4e7;}
  .bar{position:fixed;top:0;left:0;right:0;height:56px;background:#111113;border-bottom:1px solid #1c1c22;display:flex;align-items:center;justify-content:space-between;padding:0 20px;z-index:10;}
  .bar .title{font-size:13px;color:#a1a1aa;letter-spacing:.03em;}
  .bar .actions{display:flex;gap:12px;align-items:center;}
  #status{font-size:13px;color:#71717a;min-width:150px;text-align:right;}
  button{font:inherit;font-size:14px;font-weight:700;background:#00c6a2;color:#06241e;border:0;padding:11px 20px;cursor:pointer;}
  .stage{padding:88px 20px 48px;display:flex;flex-wrap:wrap;gap:28px;justify-content:center;}
  .card{background:#000;}
  .frame{overflow:hidden;border:1px solid rgba(255,255,255,0.16);box-shadow:0 24px 70px rgba(0,0,0,0.65);}
  .empty{padding:60px;color:#71717a;}
  .hint{position:fixed;bottom:14px;left:20px;font-size:12px;color:#52525b;}
</style></head>
<body>
  <div class="bar">
    <div class="title">SOCIAL CANVAS &middot; click any text in a slide to edit, then press Save</div>
    <div class="actions"><span id="status"></span><button id="save">Save Edits</button></div>
  </div>
  <div class="stage">"""
    tail = """</div>
  <div class="hint">Saved to the served HTML (a timestamped backup is written first). The PNG re-renders only when you ask.</div>
  <script>
    var status=document.getElementById('status');
    var btn=document.getElementById('save');
    if(btn){ btn.addEventListener('click', function(){
      var frames=[].slice.call(document.querySelectorAll('iframe'));
      if(!frames.length){status.textContent='No slides';return;}
      status.textContent='Saving...'; status.style.color='#a1a1aa';
      var ok=0, fail=0, done=0;
      frames.forEach(function(f){
        var html;
        try{ html='<!DOCTYPE html>'+f.contentDocument.documentElement.outerHTML; }
        catch(e){ fail++; done++; finish(); return; }
        fetch('/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({file:f.getAttribute('data-file'),html:html})})
          .then(function(r){ if(r.ok){ok++;}else{fail++;} })
          .catch(function(){fail++;})
          .then(function(){ done++; finish(); });
      });
      function finish(){
        if(done<frames.length)return;
        if(fail===0){status.textContent='Saved '+ok+' slide(s)';status.style.color='#00c6a2';}
        else{status.textContent='Saved '+ok+', failed '+fail;status.style.color='#f59e0b';}
      }
    }); }
  </script>
</body></html>"""
    return head + frames + tail


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=SLIDE_DIR, **kwargs)

    def log_message(self, *a):
        pass

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_GET(self):
        if urlparse(self.path).path in ("/", "/index.html"):
            body = gallery_html().encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        return super().do_GET()

    def do_POST(self):
        if urlparse(self.path).path != "/save":
            self.send_response(404)
            self.end_headers()
            return
        try:
            n = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(n).decode("utf-8"))
            fname = os.path.basename(data["file"])
            if not re.match(r'^slide-[\w-]+\.html$', fname):
                raise ValueError("bad filename: %s" % fname)
            target = os.path.join(SLIDE_DIR, fname)
            os.makedirs(BACKUP_DIR, exist_ok=True)
            if os.path.exists(target):
                stamp = time.strftime("%Y%m%d-%H%M%S")
                shutil.copy2(target, os.path.join(BACKUP_DIR, "%s.bak-%s" % (fname, stamp)))
            with open(target, "w", encoding="utf-8") as fh:
                fh.write(sanitize(data["html"]))
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"ok":true}')
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"ok": False, "error": str(e)}).encode())


socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as httpd:
    print("social-canvas editable gallery: dir=%s port=%d" % (SLIDE_DIR, PORT))
    httpd.serve_forever()
