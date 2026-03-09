from flask import Flask, request, jsonify
import re

app = Flask(__name__)

def summarize_text(text, sentences=3):
    """Extract key sentences from text using extractive summarization."""
    # Split into sentences
    sents = re.split(r'(?<=[.!?])\s+', text.strip())
    if len(sents) <= sentences:
        return text.strip()
    
    # Score sentences by word frequency
    words = re.findall(r'\w+', text.lower())
    freq = {}
    stop_words = {'the','a','an','is','are','was','were','in','on','at','to','for','of','and','or','but','with','this','that','it','be','as','by','from','has','have','had','not','will','can','do','does'}
    for w in words:
        if w not in stop_words and len(w) > 2:
            freq[w] = freq.get(w, 0) + 1
    
    scored = []
    for i, s in enumerate(sents):
        score = sum(freq.get(w, 0) for w in re.findall(r'\w+', s.lower()))
        # Boost early sentences
        score *= (1 + 0.1 * max(0, 5 - i))
        scored.append((score, i, s))
    
    scored.sort(reverse=True)
    top = sorted(scored[:sentences], key=lambda x: x[1])
    return ' '.join(t[2] for t in top)

def count_words(text):
    return len(re.findall(r'\w+', text))

@app.route('/', methods=['GET'])
def index():
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Rikko AI Automation - Services & APIs</title>
<style>
body{font-family:Arial,sans-serif;max-width:1000px;margin:0 auto;padding:40px 20px;color:#333;background:#f9f9f9}
h1{color:#2c3e50;font-size:2.2em}h2{color:#34495e}
.badge{background:#27ae60;color:#fff;padding:4px 12px;border-radius:20px;font-size:.85em}
.nav{text-align:center;margin:20px 0}
.nav a{color:#2980b9;margin:0 15px;text-decoration:none;font-weight:bold}
.nav a:hover{text-decoration:underline}
.section{background:#fff;padding:30px;border-radius:8px;margin:20px 0;border:1px solid #ddd}
footer{margin-top:60px;color:#999;font-size:.85em;text-align:center}
</style>
</head>
<body>
<h1>🤖 Rikko AI Automation</h1>
<p><strong>Professional AI automation services & APIs</strong> — helping businesses automate repetitive tasks and save time.</p>

<div class="nav">
<a href="/">Home</a>
<a href="/services">📋 Services</a>
<a href="/api">🔌 API Docs</a>
</div>

<div class="section">
<h2>🚀 What We Offer</h2>
<ul>
<li><strong>Custom AI Solutions</strong> — Tailored automation for your business</li>
<li><strong>Chatbot Development</strong> — FAQ bots, customer support automation</li>
<li><strong>Workflow Automation</strong> — Automate emails, data entry, reports</li>
<li><strong>API Services</strong> — Text summarization, content generation, email validation</li>
</ul>
</div>

<div class="section">
<h2>📡 Available APIs</h2>
<p><strong>Text Summarizer AI</strong> — Instantly condense long articles into summaries</p>
<p><strong>Email Validator Pro</strong> — Verify email addresses in real-time</p>
<p><strong>Content Generator</strong> — Generate blog posts, product descriptions, marketing copy</p>
<p>All APIs available on <a href="https://rapidapi.com/joey99umanito/apis" target="_blank">RapidAPI Marketplace</a></p>
</div>

<div class="section">
<h2>💼 Ready to Get Started?</h2>
<p><a href="/services" style="color:#2980b9;font-weight:bold;font-size:1.2em">View Available Services & Pricing →</a></p>
</div>

<footer>© 2025 Rikko AI Automation | joey99umanito@gmail.com | Malaysia/Global</footer>
</body>
</html>"""
    from flask import Response
    return Response(html, mimetype='text/html')

@app.route('/services', methods=['GET'])
def services():
    try:
        with open('/tmp/services.html', 'r') as f:
            return f.read()
    except:
        # Fallback to inline services page
        with open('services.html', 'r') as f:
            return f.read()

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'Missing "text" field'}), 400
    
    text = data['text']
    num_sentences = data.get('sentences', 3)
    
    if not text.strip():
        return jsonify({'error': 'Text cannot be empty'}), 400
    
    summary = summarize_text(text, num_sentences)
    
    return jsonify({
        'summary': summary,
        'original_word_count': count_words(text),
        'summary_word_count': count_words(summary),
        'compression_ratio': round(count_words(summary) / max(count_words(text), 1), 2)
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'service': 'Text Summarizer API v1.0'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)


@app.route('/services', methods=['GET'])
def services():
    """AI Automation Services page"""
    html = """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>AI Services - Rikko</title><style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:'Segoe UI',sans-serif;background:linear-gradient(135deg,#667eea,#764ba2);min-height:100vh;padding:40px 20px}.container{max-width:1000px;margin:0 auto}header{text-align:center;color:#fff;margin-bottom:60px}h1{font-size:2.8em;margin-bottom:10px}.subtitle{font-size:1.2em;opacity:0.95}.services-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:30px}.service-card{background:#fff;border-radius:12px;padding:30px;box-shadow:0 10px 40px rgba(0,0,0,0.2)}.service-card h3{color:#667eea;font-size:1.6em;margin-bottom:15px}.price{font-size:2.5em;color:#764ba2;font-weight:bold}.btn{background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;border:none;padding:12px 30px;border-radius:8px;cursor:pointer;font-weight:bold}.btn:hover{opacity:0.9}.contact{background:rgba(255,255,255,0.1);border-radius:12px;padding:30px;text-align:center;color:#fff;margin-top:40px}</style></head><body><div class="container"><header><h1>🤖 AI Automation Services</h1></header><div class="services-grid"><div class="service-card"><h3>Email Automation</h3><p>Automated email sequences & follow-ups</p><div class="price">$25</div><p>3 days</p><button class="btn" onclick="contact('Email Automation')">Start</button></div><div class="service-card"><h3>FAQ Chatbot</h3><p>24/7 customer support chatbot</p><div class="price">$40</div><p>5 days</p><button class="btn" onclick="contact('FAQ Chatbot')">Start</button></div><div class="service-card"><h3>Workflow Automation</h3><p>Automate data entry & reports</p><div class="price">$50</div><p>7 days</p><button class="btn" onclick="contact('Workflow')">Start</button></div><div class="service-card"><h3>Custom AI</h3><p>Tailored AI solutions</p><div class="price">$100</div><p>14 days</p><button class="btn" onclick="contact('Custom AI')">Start</button></div></div><div class="contact"><p>📧 <a href="mailto:joey99umanito@gmail.com" style="color:#fff">joey99umanito@gmail.com</a></p></div></div><script>function contact(s){location.href='mailto:joey99umanito@gmail.com?subject=Service:'+s}</script></body></html>"""
    from flask import Response
    return Response(html, mimetype='text/html')
