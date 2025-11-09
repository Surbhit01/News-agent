from openai import OpenAI
import json, os

client = OpenAI(
    api_key=os.environ.get("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


def get_article_summary(text:str) -> str:
    if len(text) < 900:
        return {"summary": text}
    
    summarization_prompt = ''' You are an expert news analyst. You are given with a news article.
                        Carefully summarize that article for the user. Be sure to not miss out on any important
                        piece of information. Give only the summary, do not add anything else.
                        Return the response in this json format - 
                        {
                        "summary" : "..."
                        }
                        '''
    
    response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": summarization_prompt},
        {
            "role": "user",
            "content": text
        }
    ]
)
    
    summary = response.choices[0].message.content
    summary = summary.replace("```json","").replace("```","")
    return json.loads(summary)