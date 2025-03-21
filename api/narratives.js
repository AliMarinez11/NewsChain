import fs from 'fs';
import path from 'path';

export default async function handler(req, res) {
  try {
    // Define the path to narratives.json
    const filePath = path.join(process.cwd(), 'narratives.json');
    
    // Check if the file exists
    if (!fs.existsSync(filePath)) {
      return res.status(404).json({ error: 'Narratives file not found' });
    }

    // Read the file
    const data = fs.readFileSync(filePath, 'utf8');
    const narratives = JSON.parse(data);

    // Return the data as JSON
    res.status(200).json(narratives);
  } catch (error) {
    res.status(500).json({ error: error.message, stack: error.stack });
  }
}