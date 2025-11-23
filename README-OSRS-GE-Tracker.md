# ⚔️ OSRS Grand Exchange Tracker - Bot Dump Detector

## Description

This project is an **easy-to-use web-based tracker** for the **Old School RuneScape (OSRS) Grand Exchange** that helps players spot **bot dumps** - sudden price drops caused by automated bots selling large quantities of items. The tool provides real-time price tracking, volume analysis, and automatic bot dump detection to help players find profitable flipping opportunities.

## What is a Bot Dump?

**Bot dumps** occur when automated bots quickly sell large quantities of items on the Grand Exchange, causing sudden price drops. These price crashes are often temporary, and prices typically recover within hours or days. Smart players can buy items during bot dumps at low prices and sell them later for profit.

## Features

- **🔍 Item Search**: Search through all OSRS Grand Exchange items with autocomplete
- **📊 Real-time Price Tracking**: Automatic price updates every 30 seconds
- **⚠️ Bot Dump Detection**: Automatic detection of potential bot dumps based on:
  - Price drops of 5% or more within 5 minutes
  - Trading volume 2x or higher than average
- **📈 Volume Analysis**: Monitor trading volume and volume multipliers
- **💰 Price Display**: View high, low, and average prices with price change indicators
- **📋 Watchlist**: Track multiple items simultaneously
- **🎨 Visual Alerts**: Red pulsing alerts for detected bot dumps
- **📱 Responsive Design**: Works on desktop and mobile devices
- **🌙 Dark Theme**: Easy on the eyes with modern dark UI

## How to Use

### Opening the Application

Simply open the `OSRS-GE-Tracker.html` file in any modern web browser. No installation or setup required!

### Adding Items to Watch

1. **Search for items**: Type an item name in the search box (e.g., "Dragon bones", "Rune platebody")
2. **Select an item**: Click on an item from the search results
3. **Monitor prices**: The item will be added to your watchlist and start updating automatically

### Understanding the Display

Each item in your watchlist shows:

- **High Price**: Current buy price (what players are buying for)
- **Low Price**: Current sell price (what players are selling for)
- **Average Price**: The midpoint between high and low
- **Price Change**: Shows price movement with percentage and colored arrows
  - 🟢 Green ▲ = Price increasing
  - 🔴 Red ▼ = Price decreasing
- **Volume (5m)**: Number of items traded in the last 5 minutes
- **Volume Multiplier**: Current volume compared to average (red if >2x)

### Bot Dump Alerts

When a **potential bot dump** is detected, you'll see:

- ⚠️ **Red pulsing border** around the item card
- **"POTENTIAL BOT DUMP" alert** at the top
- **Warning message** explaining the detected conditions
- The item meets both criteria:
  - Price dropped 5% or more
  - Volume is 2x or higher than average

### Taking Action on Bot Dumps

When you spot a bot dump:

1. **Verify the dump**: Check that both price and volume indicators are red
2. **Check GE limits**: Make sure you can buy enough of the item (GE buy limits vary)
3. **Buy low**: Purchase items at the dumped price
4. **Wait for recovery**: Most bot dumps recover within hours to days
5. **Sell high**: Sell when the price returns to normal levels

## Bot Dump Strategy Tips

### Good Items for Bot Dump Flipping

- **Resource items**: Ores, logs, herbs, fish (commonly botted)
- **High volume items**: Items with consistent trading activity
- **Crafting supplies**: Leather, hides, bars
- **Consumables**: Food, potions, ammunition

### Items to Avoid

- **Low volume items**: May take too long to sell
- **Quest items**: Limited demand
- **Discontinued items**: Price changes may not be bot-related

### Risk Management

- **Diversify**: Track multiple items to spread risk
- **Start small**: Test with smaller investments first
- **Check history**: Use external tools (GE Tracker, OSRS Wiki) to verify historical prices
- **Be patient**: Not all dumps recover quickly
- **Set limits**: Don't invest more than you can afford to lose

## Technical Details

### Data Source

This tool uses the official **prices.runescape.wiki API** which provides:

- Real-time Grand Exchange prices (updated every minute)
- 5-minute average prices and volumes
- Complete item mapping database

### API Endpoints Used

1. **Item Mapping**: `https://prices.runescape.wiki/api/v1/osrs/mapping`
   - Loads all item names and IDs
2. **Latest Prices**: `https://prices.runescape.wiki/api/v1/osrs/latest`
   - Gets current high/low prices
3. **5-Minute Data**: `https://prices.runescape.wiki/api/v1/osrs/5m`
   - Gets average prices and trading volumes

### Bot Dump Detection Algorithm

The tool detects potential bot dumps using:

```javascript
// Conditions for bot dump detection:
1. Price drop >= 5% in recent update
2. Current volume >= 2x average volume
3. Sufficient historical data (minimum 2 data points)
```

### Update Frequency

- **Automatic updates**: Every 30 seconds
- **Data retention**: Last 10 data points per item
- **Volume calculation**: Rolling average over all stored data points

## Privacy and Usage

- **No login required**: Works completely client-side
- **No data collection**: All tracking happens in your browser
- **No API key needed**: Uses public OSRS price API
- **CORS-friendly**: API supports cross-origin requests

## Browser Compatibility

Works on all modern browsers:

- ✅ Chrome/Edge (Recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Opera
- ✅ Mobile browsers

## Troubleshooting

### "Failed to load item data"
- **Cause**: No internet connection or API is down
- **Solution**: Check your internet connection and refresh the page

### Items not updating
- **Cause**: API rate limiting or temporary issues
- **Solution**: Wait a minute and the updates will resume automatically

### No search results
- **Cause**: Item name spelled incorrectly
- **Solution**: Try different spelling or check OSRS Wiki for correct item name

### Price shows as 0
- **Cause**: Item is not actively traded
- **Solution**: This is normal for rarely traded items

## Advanced Tips

### Interpreting Volume Multipliers

- **1.0x - 1.5x**: Normal trading activity
- **1.5x - 2.0x**: Increased activity, monitor closely
- **2.0x+**: High activity, potential bot dump if price is dropping
- **5.0x+**: Very high activity, strong bot dump indicator

### Best Times to Check

- **Peak hours**: 6pm-10pm GMT (most players online)
- **After updates**: Game updates can cause market fluctuations
- **Weekends**: Higher player count, more market activity

### Complementary Tools

Use alongside:

- **GE Tracker**: Historical price charts and flip margins
- **OSRS Wiki**: Item information and typical prices
- **Platinum Tokens**: For items over max cash stack

## Limitations

- **Price lag**: API updates every ~1 minute, not instant
- **Historical data**: Limited to recent history (last 10 updates)
- **Manual action required**: Tool detects dumps but doesn't auto-trade
- **No predictions**: Shows current data, doesn't predict future prices
- **GE limits apply**: You still need to follow GE buy/sell limits

## Development

### Technologies Used

- **HTML5**: Structure
- **CSS3**: Modern dark theme with animations
- **JavaScript (ES6+)**: Real-time data fetching and analysis
- **Fetch API**: For retrieving price data
- **No dependencies**: Pure vanilla JavaScript

### Contributing

This is a standalone tool. To modify:

1. Open `OSRS-GE-Tracker.html` in a text editor
2. Make your changes
3. Save and refresh in browser to test

## Disclaimer

⚠️ **Important Notice**:

- This tool is for **informational purposes only**
- **Not affiliated** with Jagex or OSRS
- **No guarantees** on profit or price recovery
- **Use at your own risk** - Grand Exchange trading involves risk
- Always follow **OSRS game rules** - this is a price viewer, not a bot
- **Do your own research** before making trades

## Credits

- **Price Data**: prices.runescape.wiki
- **Game**: Old School RuneScape by Jagex Ltd.
- **Design**: Inspired by modern dark UI themes

## License

This project is provided as-is for personal use. OSRS and RuneScape are trademarks of Jagex Ltd.

---

**Happy flipping! May your margins be high and your bot dumps plentiful! 📈⚔️**
