from data_fetcher import DataFetcher
import random
from datetime import datetime, timedelta

class TradingRecommendationEngine:
    def __init__(self):
        """Initialize the trading recommendation engine"""
        self.data_fetcher = DataFetcher()
        
        # Define supported assets with their types
        self.supported_assets = {
            # Stocks
            "AAPL": {"name": "Apple Inc.", "type": "stock"},
            "MSFT": {"name": "Microsoft Corporation", "type": "stock"},
            "AMZN": {"name": "Amazon.com Inc.", "type": "stock"},
            "GOOGL": {"name": "Alphabet Inc.", "type": "stock"},
            "META": {"name": "Meta Platforms Inc.", "type": "stock"},
            "TSLA": {"name": "Tesla Inc.", "type": "stock"},
            "NVDA": {"name": "NVIDIA Corporation", "type": "stock"},
            
            # Forex
            "EURUSD=X": {"name": "EUR/USD", "type": "forex"},
            "GBPUSD=X": {"name": "GBP/USD", "type": "forex"},
            "USDJPY=X": {"name": "USD/JPY", "type": "forex"},
            "AUDUSD=X": {"name": "AUD/USD", "type": "forex"},
            
            # Cryptocurrencies
            "BTC-USD": {"name": "Bitcoin USD", "type": "crypto"},
            "ETH-USD": {"name": "Ethereum USD", "type": "crypto"},
            "XRP-USD": {"name": "Ripple USD", "type": "crypto"},
            "SOL-USD": {"name": "Solana USD", "type": "crypto"},
            
            # Commodities
            "GC=F": {"name": "Gold", "type": "commodity"},
            "SI=F": {"name": "Silver", "type": "commodity"},
            "CL=F": {"name": "Crude Oil", "type": "commodity"},
            "NG=F": {"name": "Natural Gas", "type": "commodity"}
        }
    
    def get_recommendations(self, timeframe="24h", assets=None):
        """
        Get trading recommendations for specified assets and timeframe
        
        Args:
            timeframe (str): Timeframe for analysis (12h, 24h, 3d, 1w)
            assets (list): List of asset symbols to get recommendations for
                          If None, returns recommendations for all supported assets
        
        Returns:
            dict: Trading recommendations with metadata
        """
        # Validate timeframe
        if timeframe not in ["12h", "24h", "3d", "1w"]:
            timeframe = "24h"  # Default to 24h if invalid
        
        # Determine which assets to analyze
        if assets:
            # Filter to only include supported assets
            asset_list = [a for a in assets if a in self.supported_assets]
        else:
            # Use a subset of assets if none specified
            asset_list = list(self.supported_assets.keys())[:8]  # Limit to 8 for performance
        
        # Get recommendations for each asset
        recommendations = []
        for symbol in asset_list:
            # Get data for this asset
            asset_data = self.data_fetcher.get_stock_data(symbol, timeframe)
            
            if asset_data:
                # Create recommendation object
                recommendation = {
                    "symbol": symbol,
                    "name": self._get_asset_name(symbol),
                    "type": self._get_asset_type(symbol),
                    "price": asset_data["price"],
                    "currency": asset_data["currency"],
                    "recommendation": asset_data["recommendation"],
                    "confidence": asset_data["confidence"],
                    "entry": asset_data["price"],  # Current price is entry point
                    "stop_loss": asset_data["stop_loss"],
                    "take_profit": asset_data["take_profit"],
                    "potential": round(asset_data["potential"], 2),
                    "expiration": asset_data["expiration"],
                    "timeframe": timeframe
                }
                recommendations.append(recommendation)
        
        # Sort recommendations by confidence and potential
        recommendations.sort(key=lambda x: (
            0 if x["confidence"] == "High" else (1 if x["confidence"] == "Medium" else 2),
            -x["potential"]
        ))
        
        # Return recommendations with metadata
        return {
            "timestamp": datetime.now().strftime("%I:%M %p %m/%d/%Y"),
            "timeframe": timeframe,
            "count": len(recommendations),
            "recommendations": recommendations
        }
    
    def _get_asset_name(self, symbol):
        """Get the display name for an asset symbol"""
        if symbol in self.supported_assets:
            return self.supported_assets[symbol]["name"]
        return symbol
    
    def _get_asset_type(self, symbol):
        """Get the asset type for a symbol"""
        if symbol in self.supported_assets:
            return self.supported_assets[symbol]["type"]
        return "unknown"
