const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs').promises;
const path = require('path');

// Headers for web scraping
const scrapeHeaders = {
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
};

// News sources
const sources = {
  "cnn": { "url": "https://www.cnn.com/politics", "selector": "span.container__headline-text" },
  "fox": { "url": "https://www.foxnews.com/politics", "selector": "h4.title" }
};

// Scrape articles
async function scrapeSource(sourceInfo) {
  const { url, selector } = sourceInfo;
  const sourceName = Object.keys(sources).find(key => sources[key] === sourceInfo);
  const response = await axios.get(url, { headers: scrapeHeaders });
  const $ = cheerio.load(response.data);
  const articles = [];
  $(selector).each((_, element) => {
    const title = $(element).text().trim();
    const linkElem = $(element).parent('a') || $(element).find('a');
    let link = linkElem.attr('href');
    if (link && !link.startsWith('http')) {
      link = `https://www.${sourceName}.com${link}`;
    }
    if (title && link) {
      articles.push({ title, url: link, source: sourceName });
    }
  });
  return articles;
}

// Simple keyword-based clustering for categorization
function categorizeArticles(articles) {
  if (!articles.length) return {};

  const stopWords = new Set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by']);
  const articleKeywords = articles.map(article => {
    const words = article.title.toLowerCase().match(/\b\w+\b/g) || [];
    const keywords = words.filter(word => !stopWords.has(word) && word.length > 3);
    return { article, keywords };
  });

  const clusters = {};
  const usedArticles = new Set();
  let clusterId = 0;

  for (let i = 0; i < articleKeywords.length; i++) {
    if (usedArticles.has(i)) continue;

    const { article, keywords } = articleKeywords[i];
    const cluster = [article];
    const clusterKeywords = new Set(keywords);
    usedArticles.add(i);

    for (let j = i + 1; j < articleKeywords.length; j++) {
      if (usedArticles.has(j)) continue;
      const { article: otherArticle, keywords: otherKeywords } = articleKeywords[j];
      if (clusterKeywords.size > 0 && otherKeywords.some(kw => clusterKeywords.has(kw))) {
        cluster.push(otherArticle);
        otherKeywords.forEach(kw => clusterKeywords.add(kw));
        usedArticles.add(j);
      }
    }

    const allWords = cluster
      .map(art => (art.title.toLowerCase().match(/\b\w+\b/g) || []).filter(word => !stopWords.has(word) && word.length > 3))
      .flat();
    const wordCounts = {};
    allWords.forEach(word => {
      wordCounts[word] = (wordCounts[word] || 0) + 1;
    });
    const topWords = Object.entries(wordCounts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 2)
      .map(entry => entry[0]);
    const categoryName = topWords.length > 0 ? topWords.join('_') : `cluster_${clusterId}`;
    clusters[categoryName] = cluster;
    clusterId++;
  }

  const otherArticles = articleKeywords
    .filter((_, idx) => !usedArticles.has(idx))
    .map(item => item.article);
  if (otherArticles.length > 0) {
    clusters['other'] = otherArticles;
  }

  return clusters;
}

// Main function
async function main() {
  const allArticles = [];
  for (const sourceInfo of Object.values(sources)) {
    const sourceName = Object.keys(sources).find(key => sources[key] === sourceInfo);
    console.log(`Scraping ${sourceName}...`);
    const articles = await scrapeSource(sourceInfo);
    allArticles.push(...articles);
  }

  // Categorize dynamically
  const rawNarratives = categorizeArticles(allArticles);

  // Save raw data
  const rawPath = path.join(process.cwd(), 'narratives_raw.json');
  await fs.writeFile(rawPath, JSON.stringify(rawNarratives, null, 4));
  console.log(`Raw narratives saved to ${rawPath}`);

  // Call Vercel API with Grok
  const vercelUrl = "https://news-chain.vercel.app/api/neutralize";
  const response = await axios.post(vercelUrl, rawNarratives);
  if (response.status === 200) {
    const neutralizedNarratives = response.data;
    const outputPath = path.join(process.cwd(), 'narratives.json');
    await fs.writeFile(outputPath, JSON.stringify(neutralizedNarratives, null, 4));
    console.log(`Neutralized narratives saved to ${outputPath}`);
    return { message: 'Scraping completed successfully', output: 'Scraping and neutralization completed' };
  } else {
    throw new Error(`Vercel API failed: ${response.status} - ${response.data}`);
  }
}

module.exports = main;