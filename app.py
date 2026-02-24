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
