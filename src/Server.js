const express = require('express');
const cors = require('cors');
const yahooFinance = require('yahoo-finance');

const app = express();
app.use(cors()); // Enable CORS

const PORT = process.env.PORT || 3001;

app.get('/api/sp500', async (req, res) => {
  try {
    const now = new Date();
    const threeMinutesAgo = new Date(now - 3 * 60 * 1000); // 3 minutes ago

    const historicalData = await yahooFinance.historical({
      symbol: "^GSPC",
      from: threeMinutesAgo.toISOString().slice(0, 10), // format as YYYY-MM-DD
      to: now.toISOString().slice(0, 10),
      period: 'm'
    });

    res.json(historicalData);
  } catch (error) {
    console.error('Error fetching S&P 500 data:', error);
    res.status(500).send('Failed to fetch data');
  }
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
