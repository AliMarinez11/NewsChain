export default async function handler(req, res) {
    try {
      const rawNarratives = req.body;
      const neutralized = {};
  
      for (const [key, articles] of Object.entries(rawNarratives)) {
        const titles = articles.map(a => a.title).join(" ");
        
        // Make a direct API call to xAI's chat completions endpoint
        const response = await fetch('https://api.x.ai/v1/chat/completions', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${process.env.XAI_API_KEY}`
          },
          body: JSON.stringify({
            messages: [
              {
                role: 'system',
                content: 'You are a helpful assistant that provides neutral summaries.'
              },
              {
                role: 'user',
                content: `Summarize neutrally: ${titles}`
              }
            ],
            model: 'grok-2-latest',
            stream: false,
            temperature: 0,
            max_tokens: 100
          })
        });
  
        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.error?.message || 'Failed to call xAI API');
        }
  
        const neutralSummary = data.choices[0].message.content;
  
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