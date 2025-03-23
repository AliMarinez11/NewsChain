import fs from 'fs';
import path from 'path';
import fetch from 'node-fetch';

// API handler for serving summaries with fallback
export default async function handler(req, res) {
    try {
        // Load filtered narratives
        const filteredPath = path.join(process.cwd(), 'filtered_narratives.json');
        if (!fs.existsSync(filteredPath)) {
            throw new Error('Filtered narratives file not found at ' + filteredPath);
        }
        const rawFilteredData = fs.readFileSync(filteredPath);
        const filteredNarratives = JSON.parse(rawFilteredData);

        // Check if there are valid narratives
        const validNarratives = filteredNarratives.validNarratives || {};
        const hasValidNarratives = Object.keys(validNarratives).length > 0;

        // Load existing summaries
        const outputPath = path.join(process.cwd(), 'summarized_narratives.json');
        let summarizedNarratives = { validNarratives: {}, excludedNarratives: filteredNarratives.excludedNarratives || {} };
        if (fs.existsSync(outputPath)) {
            const rawSummarizedData = fs.readFileSync(outputPath);
            summarizedNarratives = JSON.parse(rawSummarizedData);
        }

        // If there are valid narratives, summarize them directly
        if (hasValidNarratives) {
            console.log('Valid narratives found, summarizing directly...');

            // Ensure xAI API key is set
            const xaiApiKey = process.env.XAI_API_KEY;
            if (!xaiApiKey) {
                throw new Error('xAI API key is not set. Please set the XAI_API_KEY environment variable.');
            }

            // Initialize summaries (start fresh each time)
            summarizedNarratives = { validNarratives: {}, excludedNarratives: filteredNarratives.excludedNarratives || {} };

            // Summarize each narrative (1 per batch to minimize API call time)
            const batchSize = 1;
            const narrativeEntries = Object.entries(validNarratives);
            const batches = [];
            for (let i = 0; i < narrativeEntries.length; i += batchSize) {
                const batchEntries = narrativeEntries.slice(i, i + batchSize);
                const batch = Object.fromEntries(batchEntries);
                batches.push(batch);
            }

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

                fs.writeFileSync(outputPath, JSON.stringify(summarizedNarratives, null, 4));
                console.log(`Updated summarized_narratives.json after batch ${batchIndex + 1}`);
            }

            console.log('Summarization completed successfully.');
        } else {
            console.log('No valid narratives found, serving cached results.');
        }

        // Return the summaries (fresh or cached)
        res.status(200).json(summarizedNarratives.validNarratives);
    } catch (error) {
        console.error('Error in neutralize handler:', error);
        res.status(500).json({ error: error.message });
    }
}