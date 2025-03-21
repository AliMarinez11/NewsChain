export default async function handler(req, res) {
    // Log the entire headers object for debugging
    console.log('All Headers:', JSON.stringify(req.headers));
    console.log('Authorization Header:', req.headers['Authorization']);
    console.log('Authorization Header (lowercase):', req.headers['authorization']);
    console.log('Expected:', `Bearer ${process.env.CRON_SECRET}`);
  
    // Temporarily disable CRON_SECRET check for debugging
    // if (req.headers['Authorization'] !== `Bearer ${process.env.CRON_SECRET}`) {
    //   return res.status(401).end('Unauthorized');
    // }
  
    try {
      // Call the /api/scrape endpoint internally
      const scrapeResponse = await fetch('https://news-chain.vercel.app/api/scrape', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({})
      });
  
      const scrapeData = await scrapeResponse.json();
      if (!scrapeResponse.ok) {
        throw new Error(scrapeData.error || 'Failed to run scraper');
      }
  
      res.status(200).json({ message: 'Cron job executed successfully', scrapeOutput: scrapeData });
    } catch (error) {
      res.status(500).json({ error: error.message, stack: error.stack });
    }
  }