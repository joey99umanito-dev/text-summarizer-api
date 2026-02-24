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
<title>Text Summarizer AI - API Service by Rikko AI Automation</title>
<style>
body{font-family:Arial,sans-serif;max-width:900px;margin:0 auto;padding:40px 20px;color:#333;background:#f9f9f9}
h1{color:#2c3e50;font-size:2.2em}h2{color:#34495e}
.badge{background:#27ae60;color:#fff;padding:4px 12px;border-radius:20px;font-size:.85em}
.endpoint{background:#fff;border:1px solid #ddd;border-radius:8px;padding:16px;margin:12px 0}
code{background:#ecf0f1;padding:2px 6px;border-radius:4px;font-family:monospace}
a{color:#2980b9}footer{margin-top:60px;color:#999;font-size:.85em}
</style>
</head>
<body>
<h1>🤖 Text Summarizer AI <span class="badge">API v1.0</span></h1>
<p><strong>Professional AI-powered text summarization API</strong> by Rikko AI Automation. Instantly condense long articles, reports, and documents into concise summaries.</p>
<h2>🚀 Features</h2>
<ul>
<li>Extractive AI summarization</li>
<li>Adjustable summary length (number of sentences)</li>
<li>Compression ratio metrics</li>
<li>REST API — easy to integrate in any app</li>
</ul>
<h2>📡 Endpoints</h2>
<div class="endpoint"><strong>POST</strong> <code>/summarize</code> — Summarize text</div>
<div class="endpoint"><strong>GET</strong> <code>/health</code> — API health check</div>
<h2>🔑 Get API Access</h2>
<p>Available on <a href="https://rapidapi.com/joey99umanito/api/text-summarizer-ai3" target="_blank">RapidAPI Marketplace</a>. Free tier available!</p>
<h2>📬 Contact</h2>
<p>Email: <a href="mailto:joey99umanito@gmail.com">joey99umanito@gmail.com</a></p>
<footer>© 2025 Rikko AI Automation. All rights reserved. | Professional AI automation services.</footer>
</body>
</html>"""
    from flask import Response
    return Response(html, mimetype='text/html')

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
