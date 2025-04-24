
# nlp_signal_engine.py
import openai

def interpret_headline(headline, openai_api_key, model="gpt-3.5-turbo") -> dict:
    openai.api_key = openai_api_key

    prompt = f"""
You are a market-aware AI assistant. Given the headline below, assess whether it is likely to have a positive, negative, or neutral impact on the stock market.

Return your response as JSON with fields:
- symbol (if mentioned)
- signal (BUY, SELL, IGNORE)
- reason (1-sentence justification)
- confidence (0.0 to 1.0)

Headline:
"{headline}"
"""

    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )

    try:
        content = response.choices[0].message.content
        import json
        return json.loads(content)
    except Exception as e:
        return {
            "headline": headline,
            "signal": "IGNORE",
            "reason": f"Parsing failed: {e}",
            "confidence": 0.0
        }
