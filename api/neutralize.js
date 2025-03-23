import fs from 'fs';
import path from 'path';
import fetch from 'node-fetch';

// API handler for Vercel
export default async function handler(req, res) {
    try {
        // Ensure xAI API key is set
        const xaiApiKey = process.env.XAI_API_KEY;
        if (!xaiApiKey) {
            throw new Error('xAI API key is not set. Please set the XAI_API_KEY environment variable.');
        }

        // Use dynamic file path for filtered_narratives.json
        const filePath = path.join(process.cwd(), 'filtered_narratives.json');
        if (!fs.existsSync(filePath)) {
            throw new Error('Filtered narratives file not found at ' + filePath);
        }

        // Read the filtered narratives
        const rawData = fs.readFileSync(filePath);
        const filteredNarratives = JSON.parse(rawData);

        // Extract valid narratives
        const validNarratives = filteredNarratives.validNarratives;

        // Check if there are any valid narratives to process
        if (!validNarratives || Object.keys(validNarratives).length === 0) {
            console.log('No valid narratives to process.');
            const finalResult = {
                validNarratives: {},
                excludedNarratives: filteredNarratives.excludedNarratives || {}
            };
            // Save the result
            const outputPath = path.join(process.cwd(), 'narratives_filtered.json');
            fs.writeFileSync(outputPath, JSON.stringify(finalResult, null, 4));
            console.log(`Filtered narratives with summaries saved to ${outputPath}`);
            return res.status(200).json(finalResult.validNarratives);
        }

        // Split narratives into batches (e.g., 3 narratives per batch)
        const batchSize = 3;
        const narrativeEntries = Object.entries(validNarratives);
        const batches = [];
        for (let i = 0; i < narrativeEntries.length; i += batchSize) {
            const batchEntries = narrativeEntries.slice(i, i + batchSize);
            const batch = Object.fromEntries(batchEntries);
            batches.push(batch);
        }

        // Summarize each batch
        const summarizedNarratives = { validNarratives: {} };
        const apiUrl = 'https://api.x.ai/v1/chat/completions';
        console.log('Using model: grok-2');

        for (let batchIndex = 0; batchIndex < batches.length; batchIndex++) {
            const batch = batches[batchIndex];
            console.log(`Summarizing batch ${batchIndex + 1} of ${batches.length} with ${Object.keys(batch).length} narratives`);

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

            // Make the API call for summarization
            console.log(`Sending request to xAI API for summarization (batch ${batchIndex + 1}):`, apiUrl);
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
                    max_tokens: 8192
                })
            });

            if (!summarizationResponse.ok) {
                const errorText = await summarizationResponse.text();
                throw new Error(`xAI API request for summarization failed: ${summarizationResponse.status} ${summarizationResponse.statusText} - ${errorText}`);
            }

            const summarizationData = await summarizationResponse.json();
            if (!summarizationData.choices || !summarizationData.choices[0].message.content) {
                throw new Error('Invalid response from xAI API for summarization: ' + JSON.stringify(summarizationData));
            }

            let summarizationContent = summarizationData.choices[0].message.content;
            console.log(`Raw API response content (summarization, batch ${batchIndex + 1}):`, summarizationContent);

            // Parse the summarization result
            let batchSummarizedNarratives;
            try {
                batchSummarizedNarratives = JSON.parse(summarizationContent);
            } catch (parseError) {
                console.error(`Failed to parse API response for batch ${batchIndex + 1}:`, parseError);
                throw new Error(`Failed to parse xAI API response: ${parseError.message}\nResponse content: ${summarizationContent}`);
            }

            // Merge the summarized narratives into the final result
            Object.assign(summarizedNarratives.validNarratives, batchSummarizedNarratives.validNarratives);
        }

        // Prepare the final result
        const finalResult = {
            validNarratives: summarizedNarratives.validNarratives,
            excludedNarratives: filteredNarratives.excludedNarratives || {}
        };

        // Save the filtered narratives with summaries
        const outputPath = path.join(process.cwd(), 'narratives_filtered.json');
        fs.writeFileSync(outputPath, JSON.stringify(finalResult, null, 4));
        console.log(`Filtered narratives with summaries saved to ${outputPath}`);

        // Return the result to the app
        res.status(200).json(finalResult.validNarratives);
    } catch (error) {
        console.error('Error in API handler:', error);
        res.status(500).json({ error: error.message });
    }
}