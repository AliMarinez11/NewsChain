const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

export default async function handler(req, res) {
  try {
    // Run the Python script as a child process
    const pythonProcess = spawn('python3', ['/vercel/path/to/newschain_scraper.py'], {
      cwd: process.cwd(),
      env: { ...process.env, PATH: `${process.env.PATH}:/usr/local/bin` }
    });

    let stdout = '';
    let stderr = '';

    pythonProcess.stdout.on('data', (data) => {
      stdout += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    pythonProcess.on('close', (code) => {
      if (code === 0) {
        res.status(200).json({ message: 'Scraping completed successfully', output: stdout });
      } else {
        res.status(500).json({ error: 'Scraping failed', details: stderr });
      }
    });
  } catch (error) {
    res.status(500).json({ error: error.message, stack: error.stack });
  }
}