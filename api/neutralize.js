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

        // If there are valid narratives, call /api/summarize to generate fresh summaries
        if (hasValidNarratives) {
            console.log('Valid narratives found, calling /api/summarize to generate fresh summaries.');
            console.log('Environment variables:', {
                NODE_ENV: process.env.NODE_ENV,
                VERCEL_URL: process.env.VERCEL_URL,
                host: req.headers.host
            });

            // Use HTTP for local development, HTTPS for production
            const isLocal = !process.env.VERCEL_URL || req.headers.host.includes('localhost');
            const summarizeUrl = isLocal 
                ? 'http://localhost:3000/api/summarize'
                : `https://${process.env.VERCEL_URL}/api/summarize`;

            console.log(`Calling summarize URL: ${summarizeUrl}`);
            const summarizeResponse = await fetch(summarizeUrl, { 
                method: 'GET',
                timeout: 15000,  // 15 seconds to account for API call
                headers: {
                    'Content-Type': 'application/json',
                    'X-Internal-Call': 'newschain-internal'  // Custom header to bypass auth
                }
            });

            if (!summarizeResponse.ok) {
                const errorText = await summarizeResponse.text();
                console.error(`Failed to call /api/summarize: ${summarizeResponse.status} ${summarizeResponse.statusText} - ${errorText}`);
                console.log('Falling back to cached results.');
            } else {
                console.log('Successfully called /api/summarize, reloading summaries.');
                // Wait a moment to ensure the file is written
                await new Promise(resolve => setTimeout(resolve, 1000));
                // Reload summaries after successful summarization
                const updatedSummarizedData = fs.readFileSync(outputPath);
                summarizedNarratives = JSON.parse(updatedSummarizedData);
            }
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