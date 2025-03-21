const scrape = require('../newschain_scraper.js');

export default async function handler(req, res) {
  try {
    const result = await scrape();
    res.status(200).json(result);
  } catch (error) {
    res.status(500).json({ error: error.message, stack: error.stack });
  }
}