import fs from 'fs';
import path from 'path';
import fetch from 'node-fetch';

// API handler for background summarization
export default async function handler(req, res) {
    try {
        // Allow internal calls from /api/neutralize.js using a custom header
        const internalCallHeader = req.headers['x-internal-call'];
        if (!internalCallHeader || internalCallHeader !== 'newschain-internal') {
            console.log('Unauthorized access to /api/summarize.js');
            return res.status(401).json({ error: 'Unauthorized' });
        }

        console.log('Starting summarization process...');

        // Ensure xAI API key is set
        const xaiApiKey = process.env.XAI_API_KEY;
        console.log('Checking xAI API key...');
        if (!xaiApiKey) {
            console.log('xAI API key not found.');
            throw new Error('xAI API key is not set. Please set the XAI_API_KEY environment variable.');
        }
        console.log('xAI API key found.');

        // Load filtered narratives
        console.log('Loading filtered narratives...');
        const filteredPath = path.join(process.cwd(), 'filtered_narratives.json');
        if (!fs.existsSync(filteredPath)) {
            console.log('Filtered narratives file not found.');
            throw new Error('Filtered narratives file not found at ' + filteredPath);
        }
        const rawFilteredData = fs.readFileSync(filteredPath);
        const filteredNarratives = JSON.parse(rawFilteredData);
        console.log('Loaded filtered narratives:', filteredNarratives);

        // Extract valid narratives
        console.log('Extracting valid narratives...');
        const validNarratives = filteredNarratives.validNarratives;
        if (!validNarratives || Object.keys(validNarratives).length === 0) {
            console.log('No valid narratives to summarize.');
            // Reset summarized_narratives.json to empty if no valid narratives
            const emptySummaries = { validNarratives: {}, excludedNarratives: filteredNarratives.excludedNarratives || {} };
            fs.writeFileSync(path.join(process.cwd(), 'summarized_narratives.json'), JSON.stringify(emptySummaries, null, 4));
            console.log('Reset summarized_narratives.json to empty.');
            return res.status(200).json({ message: 'No valid narratives to summarize.' });
        }
        console.log('Valid narratives found:', Object.keys(validNarratives));

        // Initialize summaries (start fresh each time)
        let summarizedNarratives = { validNarratives: {}, excludedNarratives: filteredNarratives.excludedNarratives || {} };
        console.log('Initialized summarizedNarratives:', summarizedNarratives);

        // Summarize each narrative (1 per batch to minimize API call time)
        const batchSize = 1;
        const narrativeEntries = Object.entries(validNarratives);
        const batches = [];
        for (let i = 0; i < narrativeEntries.length; i += batchSize) {
            const batchEntries = narrativeEntries.slice(i, i + batchSize);
            const batch = Object.fromEntries(batchEntries);
            batches.push(batch);
        }
        console.log('Created batches:', batches.length);

        const apiUrl = 'https://api.x.ai/v1/chat/completions';
        console.log('Using model: grok-2');

        for (let batchIndex = 0; batchIndex < batches.length; batchIndex++) {
            const batch = batches[batchIndex];
            const batchCategories = Object.keys(batch);
            console.log(`Summarizing batch ${batchIndex + 1} of ${batches.length} with ${batchCategories.length} narratives: ${batchCategories}`);

            const summarizationPrompt = `
            You are Grok, created by xAI. I have a JSON file containing a collection of "narratives" that have been identified as valid, meaning their articles discuss the same general subject. Each narrative object has a key (the category name) and a value that is an array of at least 2 news articles, along with their titles, URLs, sources, and content. Your task is to:

            1. For each narrative, provide a neutral summary that captures the core topic and key points from all articles in that narrative. Ensure the summary avoids bias by balancing perspectives from all articles, even if individual articles are biased, as the goal is to create an unbiased summary from potentially biased sources.
            2. Return the results in pure JSON format (no Markdown, no code blocks, do not wrap the JSON in \`\`\`json or any other formatting), with the following structure:
               {
                   "validNarratives": {
                       "Category": {
                           "articles": [
                               { "title": "...", "url": "...", "source": "...", "content": "..." },
                               { "title": "...", "url": "...", "source": "...", "content": "..." }
                           ],
                           "summary": "Neutral summary..."
                       }
                   }
               }

            Here are the valid narratives:

            ${JSON.stringify(batch, null, 2)}

            Return the results with summaries in pure JSON format.
            `;

            console.log(`Sending request to xAI API for summarization (batch ${batchIndex + 1}):`, apiUrl);
            const startTime = Date.now();
            const summarizationResponse = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${xaiApiKey}`
                },
                body: JSON.stringify({
                    model: 'grok-2',
                    messages: [
                        {
                            role: 'user',
                            content: summarizationPrompt
                        }
                    ],
                    max_tokens: 4096
                })
            });
            const endTime = Date.now();
            console.log(`xAI API response time for batch ${batchIndex + 1}: ${(endTime - startTime) / 1000} seconds`);

            if (!summarizationResponse.ok) {
                const errorText = await summarizationResponse.text();
                console.log('xAI API request failed:', errorText);
                throw new Error(`xAI API request for summarization failed: ${summarizationResponse.status} ${summarizationResponse.statusText} - ${errorText}`);
            }

            const summarizationData = await summarizationResponse.json();
            if (!summarizationData.choices || !summarizationData.choices[0].message.content) {
                console.log('Invalid xAI API response:', JSON.stringify(summarizationData));
                throw new Error('Invalid response from xAI API for summarization: ' + JSON.stringify(summarizationData));
            }

            let summarizationContent = summarizationData.choices[0].message.content;
            console.log(`Raw API response content (summarization, batch ${batchIndex + 1}):`, summarizationContent);

            let batchSummarizedNarratives;
            try {
                batchSummarizedNarratives = JSON.parse(summarizationContent);
                console.log(`Parsed batchSummarizedNarratives for batch ${batchIndex + 1}:`, batchSummarizedNarratives);
            } catch (parseError) {
                console.error(`Failed to parse API response for batch ${batchIndex + 1}:`, parseError);
                throw new Error(`Failed to parse xAI API response: ${parseError.message}\nResponse content: ${summarizationContent}`);
            }

            Object.assign(summarizedNarratives.validNarratives, batchSummarizedNarratives.validNarratives);
            console.log('Updated summarizedNarratives.validNarratives:', summarizedNarratives.validNarratives);

            fs.writeFileSync(path.join(process.cwd(), 'summarized_narratives.json'), JSON.stringify(summarizedNarratives, null, 4));
            console.log(`Updated summarized_narratives.json after batch ${batchIndex + 1}`);
        }

        console.log('Summarization completed successfully.');
        // Add a small delay to ensure the file is written before /api/neutralize.js reads it
        await new Promise(resolve => setTimeout(resolve, 1000));
        res.status(200).json({ message: 'Summarization completed successfully.' });
    } catch (error) {
        console.error('Error in summarize handler:', error);
        res.status(500).json({ error: error.message });
    }
}