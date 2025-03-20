import { Grok } from 'ai';

export default async function handler(req, res) {
  const grok = new Grok({ provider: 'xai' });
  const rawNarratives = req.body;
  
  const neutralized = {};
  for (const [key, articles] of Object.entries(rawNarratives)) {
    const titles = articles.map(a => a.title).join(" ");
    const summaryResponse = await grok.chat.completions.create({
      model: 'grok',
      messages: [{ role: 'user', content: `Summarize neutrally: ${titles}` }],
      max_tokens: 100
    });
    const neutralSummary = summaryResponse.choices[0].message.content;

    articles.forEach(article => {
      article.sentiment = Math.random() * 2 - 1; // Placeholder
    });

    neutralized[key] = { neutral_summary: neutralSummary, articles };
  }
  
  res.json({ narratives: neutralized, timestamp: new Date().toISOString() });
}