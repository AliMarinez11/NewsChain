import { createXai } from '@ai-sdk/xai';
import { generateText } from 'ai';

export default async function handler(req, res) {
  try {
    // Create an xAI provider instance
    const xai = createXai({
      apiKey: process.env.XAI_API_KEY, // Defaults to XAI_API_KEY env variable
    });

    // Use the provider to create a model
    const model = xai('grok');

    const rawNarratives = req.body;
    const neutralized = {};
    for (const [key, articles] of Object.entries(rawNarratives)) {
      const titles = articles.map(a => a.title).join(" ");
      const { text: neutralSummary } = await generateText({
        model,
        prompt: `Summarize neutrally: ${titles}`,
        maxTokens: 100
      });

      articles.forEach(article => {
        article.sentiment = Math.random() * 2 - 1; // Placeholder
      });

      neutralized[key] = { neutral_summary: neutralSummary, articles };
    }

    res.json({ narratives: neutralized, timestamp: new Date().toISOString() });
  } catch (error) {
    res.status(500).json({ error: error.message, stack: error.stack });
  }
}