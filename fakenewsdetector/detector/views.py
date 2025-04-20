from django.shortcuts import render, redirect, get_object_or_404
from .models import Article
import re
from textblob import TextBlob
from bs4 import BeautifulSoup
import requests

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
    }, "from_url": url and not text.strip()}  # Updated to check if URL was the source

def index(request):
    if request.method == 'POST':
        text = request.POST.get('news_text', '').strip()
        url = request.POST.get('news_url', '').strip()
        source_text = text  # Default to manual text if provided
        from_url = False
        if url and not text:  # URL only
            try:
                response = requests.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                source_text = ' '.join(p.get_text() for p in soup.find_all('p') if p.get_text().strip())
                if not source_text:
                    source_text = "No usable content found at URL."
                from_url = True
            except requests.RequestException as e:
                source_text = f"Error fetching URL: {str(e)}"
        elif not text and not url:  # Neither provided
            return render(request, 'index.html', {'error': 'Please enter text or a URL to analyze.'})
        result = analyze_news(source_text, url)
        result["from_url"] = from_url  # Override with the correct flag
        Article.objects.create(
            text=source_text,
            url=url,
            score=result['score'],
            verdict=result['verdict']
        )
        return render(request, 'result.html', {'result': result, 'source_text': source_text})
    return render(request, 'index.html')

def history(request):
    articles = Article.objects.all().order_by('-timestamp')
    return render(request, 'history.html', {'articles': articles})

def delete_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST':
        article.delete()
        return redirect('detector:history')
    return render(request, 'confirm_delete.html', {'article': article})