
# Create your views here.
from django.shortcuts import render
from .models import Article
import re
from textblob import TextBlob

def analyze_news(text, url=''):
    score = 0
    # Sensational keywords
    sensational_words = ['shocking', 'unbelievable', 'crisis', 'scandal']
    text_lower = text.lower()
    sensational_count = sum(text_lower.count(word) for word in sensational_words)
    score += sensational_count * 10

    # Excessive punctuation
    punctuation_hits = len(re.findall(r'!{2,}|\?{2,}', text))
    score += punctuation_hits * 5

    # Spelling errors
    blob = TextBlob(text)
    corrected = blob.correct()
    spelling_errors = sum(1 for w1, w2 in zip(blob.words, corrected.words) if w1 != w2)
    score += spelling_errors * 3

    score = min(score, 100)
    verdict = "Likely Fake" if score > 50 else "Likely Reliable"
    return {"score": score, "verdict": verdict, "details": {
        "sensational": sensational_count, "punctuation": punctuation_hits, "spelling": spelling_errors
    }}

def index(request):
    if request.method == 'POST':
        text = request.POST.get('news_text')
        url = request.POST.get('news_url', '')
        result = analyze_news(text, url)
        Article.objects.create(
            text=text,
            url=url,
            score=result['score'],
            verdict=result['verdict']
        )
        return render(request, 'result.html', {'result': result})
    return render(request, 'index.html')
