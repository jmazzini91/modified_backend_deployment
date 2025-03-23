import json
import time
from datetime import datetime, timedelta
import requests  # Standard library for HTTP requests

class DataFetcher:
    def __init__(self):
        # No API client needed, using standard requests library
        pass
        
    def get_stock_data(self, symbol, timeframe):
        """
        Fetch stock data from Yahoo Finance API based on timeframe
        
        Args:
            symbol (str): Stock symbol (e.g., AAPL, MSFT)
            timeframe (str): Timeframe for analysis (12h, 24h, 3d, 1w)
            
        Returns:
            dict: Stock data including price, indicators, and metadata
        """
        # Map timeframe to Yahoo Finance interval and range
        interval_map = {
            "12h": {"interval": "5m", "range": "1d"},
            "24h": {"interval": "15m", "range": "1d"},
            "3d": {"interval": "1h", "range": "3d"},
            "1w": {"interval": "1d", "range": "1wk"}
        }
        
        interval = interval_map[timeframe]["interval"]
        range_val = interval_map[timeframe]["range"]
        
        try:
            # Get stock chart data using standard requests
            chart_url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval={interval}&range={range_val}&includePrePost=true"
            chart_response = requests.get(chart_url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            })
            chart_data = chart_response.json()
            
            # Get stock insights for technical indicators
            insights_url = f"https://query1.finance.yahoo.com/v1/finance/insights?symbol={symbol}"
            insights_response = requests.get(insights_url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            })
            insights_data = insights_response.json()
            
            # Process and combine data
            processed_data = self._process_stock_data(chart_data, insights_data, timeframe)
            return processed_data
            
        except Exception as e:
            print(f"Error fetching data for {symbol}: {str(e)}")
            return None
    
    def _process_stock_data(self, chart_data, insights_data, timeframe):
        """Process raw API data into a format suitable for trading recommendations"""
        try:
            # Extract relevant data from chart response
            result = chart_data.get('chart', {}).get('result', [{}])[0]
            meta = result.get('meta', {})
            
            # Get current price and other metadata
            current_price = meta.get('regularMarketPrice', 0)
            currency = meta.get('currency', 'USD')
            
            # Get price indicators
            indicators = result.get('indicators', {})
            quotes = indicators.get('quote', [{}])[0]
            
            # Get timestamps and corresponding prices
            timestamps = result.get('timestamp', [])
            close_prices = quotes.get('close', [])
            
            # Get technical events from insights
            tech_events = {}
            if insights_data and 'finance' in insights_data:
                finance_data = insights_data['finance']
                if 'result' in finance_data:
                    instrument_info = finance_data['result'].get('instrumentInfo', {})
                    tech_events = instrument_info.get('technicalEvents', {})
                    key_technicals = instrument_info.get('keyTechnicals', {})
            
            # Calculate technical indicators based on timeframe
            indicators = self._calculate_indicators(close_prices, timeframe)
            
            # Determine support and resistance levels
            support = 0
            resistance = 0
            if insights_data and 'finance' in insights_data and 'result' in insights_data.get('finance', {}) and 'instrumentInfo' in insights_data['finance']['result']:
                key_tech = insights_data['finance']['result']['instrumentInfo'].get('keyTechnicals', {})
                support = key_tech.get('support', current_price * 0.95)
                resistance = key_tech.get('resistance', current_price * 1.05)
            else:
                # Calculate approximate support/resistance if not available
                support = current_price * 0.95
                resistance = current_price * 1.05
            
            # Determine trend direction
            trend = "neutral"
            if len(close_prices) > 1:
                if close_prices[-1] > close_prices[0]:
                    trend = "bullish"
                elif close_prices[-1] < close_prices[0]:
                    trend = "bearish"
            
            # Calculate confidence based on indicators
            confidence = self._calculate_confidence(indicators, trend, tech_events)
            
            # Calculate stop loss and take profit levels based on volatility and timeframe
            volatility = self._calculate_volatility(close_prices)
            stop_loss, take_profit = self._calculate_risk_levels(current_price, volatility, trend, timeframe)
            
            # Determine recommendation (BUY/SELL)
            recommendation = self._determine_recommendation(trend, indicators, confidence)
            
            # Calculate potential profit percentage
            potential = 0
            if recommendation == "BUY":
                potential = ((take_profit - current_price) / current_price) * 100
            else:
                potential = ((current_price - take_profit) / current_price) * 100
            
            # Set expiration time based on timeframe
            expiration = self._calculate_expiration(timeframe)
            
            return {
                "price": current_price,
                "currency": currency,
                "trend": trend,
                "recommendation": recommendation,
                "confidence": confidence,
                "stop_loss": stop_loss,
                "take_profit": take_profit,
                "potential": potential,
                "support": support,
                "resistance": resistance,
                "expiration": expiration,
                "indicators": indicators
            }
            
        except Exception as e:
            print(f"Error processing stock data: {str(e)}")
            return None
    
    def _calculate_indicators(self, prices, timeframe):
        """Calculate technical indicators based on price data"""
        if not prices or len(prices) < 10:
            return {}
        
        # Filter out None values
        prices = [p for p in prices if p is not None]
        if not prices:
            return {}
        
        # Simple Moving Averages
        sma_short = sum(prices[-5:]) / 5 if len(prices) >= 5 else sum(prices) / len(prices)
        sma_medium = sum(prices[-10:]) / 10 if len(prices) >= 10 else sum(prices) / len(prices)
        
        # Relative Strength Index (simplified)
        gains = 0
        losses = 0
        for i in range(1, min(14, len(prices))):
            diff = prices[-i] - prices[-(i+1)]
            if diff > 0:
                gains += diff
            else:
                losses -= diff
        
        rsi = 50  # Neutral default
        if gains + losses > 0:
            rs = gains / losses if losses > 0 else 100
            rsi = 100 - (100 / (1 + rs))
        
        # MACD (simplified)
        ema12 = prices[-1]
        ema26 = prices[-1]
        if len(prices) >= 12:
            ema12 = sum(prices[-12:]) / 12
        if len(prices) >= 26:
            ema26 = sum(prices[-26:]) / 26
        macd = ema12 - ema26
        
        return {
            "sma_short": sma_short,
            "sma_medium": sma_medium,
            "rsi": rsi,
            "macd": macd
        }
    
    def _calculate_volatility(self, prices):
        """Calculate price volatility"""
        if not prices or len(prices) < 2:
            return 0.02  # Default volatility
        
        # Filter out None values
        prices = [p for p in prices if p is not None]
        if len(prices) < 2:
            return 0.02
        
        # Calculate average percentage change
        changes = []
        for i in range(1, len(prices)):
            if prices[i-1] > 0:
                change = abs((prices[i] - prices[i-1]) / prices[i-1])
                changes.append(change)
        
        if not changes:
            return 0.02
            
        return sum(changes) / len(changes)
    
    def _calculate_risk_levels(self, price, volatility, trend, timeframe):
        """Calculate stop loss and take profit levels based on volatility and timeframe"""
        # Adjust volatility based on timeframe
        timeframe_multipliers = {
            "12h": 1.0,
            "24h": 1.5,
            "3d": 2.0,
            "1w": 3.0
        }
        
        multiplier = timeframe_multipliers.get(timeframe, 1.0)
        adjusted_volatility = volatility * multiplier
        
        # Calculate stop loss and take profit percentages
        if trend == "bullish":
            stop_loss_pct = adjusted_volatility * 2
            take_profit_pct = adjusted_volatility * 4
            
            stop_loss = round(price * (1 - stop_loss_pct), 2)
            take_profit = round(price * (1 + take_profit_pct), 2)
        else:
            stop_loss_pct = adjusted_volatility * 2
            take_profit_pct = adjusted_volatility * 3
            
            stop_loss = round(price * (1 + stop_loss_pct), 2)
            take_profit = round(price * (1 - take_profit_pct), 2)
        
        return stop_loss, take_profit
    
    def _calculate_confidence(self, indicators, trend, tech_events):
        """Calculate confidence level (High, Medium, Low) based on indicators"""
        confidence_score = 0
        
        # Check if RSI indicates overbought/oversold
        rsi = indicators.get("rsi", 50)
        if (trend == "bullish" and rsi < 40) or (trend == "bearish" and rsi > 60):
    confidence_score += 1
        
        # Check if price is above/below moving averages
        sma_short = indicators.get("sma_short", 0)
        sma_medium = indicators.get("sma_medium", 0)
        
        if (trend == "bullish" and sma_short > sma_medium) or (trend == "bearish" and sma_short < sma_medium):
            confidence_score += 1
        
        # Check MACD
        macd = indicators.get("macd", 0)
        if (trend == "bullish" and macd > 0) or (trend == "bearish" and macd < 0):
            confidence_score += 1
        
        # Check technical events from Yahoo Finance
        if tech_events:
            short_term = tech_events.get("shortTermOutlook", {})
            direction = short_term.get("direction", "")
            
            if (trend == "bullish" and direction == "up") or (trend == "bearish" and direction == "down"):
                confidence_score += 2
        
        # Map score to confidence level
        if confidence_score >= 4:
            return "High"
        elif confidence_score >= 2:
            return "Medium"
        else:
            return "Low"
    
    def _determine_recommendation(self, trend, indicators, confidence):
        """Determine BUY/SELL recommendation based on trend and indicators"""
        if trend == "bullish" and (confidence == "High" or confidence == "Medium"):
            return "BUY"
        elif trend == "bearish" and (confidence == "High" or confidence == "Medium"):
            return "SELL"
        
        # If trend is neutral or confidence is low, use indicators
        rsi = indicators.get("rsi", 50)
        macd = indicators.get("macd", 0)
        
        if rsi < 30 and macd > 0:
            return "BUY"
        elif rsi > 70 and macd < 0:
            return "SELL"
        
        # Default to trend
        return "BUY" if trend == "bullish" else "SELL"
    
    def _calculate_expiration(self, timeframe):
        """Calculate expiration time based on timeframe"""
        now = datetime.now()
        
        if timeframe == "12h":
            expiration = now + timedelta(hours=12)
        elif timeframe == "24h":
            expiration = now + timedelta(hours=24)
        elif timeframe == "3d":
            expiration = now + timedelta(days=3)
        elif timeframe == "1w":
            expiration = now + timedelta(weeks=1)
        else:
            expiration = now + timedelta(hours=24)  # Default
        
        return expiration.strftime("%I:%M %p %m/%d/%Y")
