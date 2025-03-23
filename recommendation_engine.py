import sys
sys.path.append('/opt/.manus/.sandbox-runtime')
from data_api import ApiClient
import json
from datetime import datetime
from data_fetcher import DataFetcher

class TradingRecommendationEngine:
    def __init__(self):
        self.data_fetcher = DataFetcher()
        self.supported_assets = {
            "stocks": ["AAPL", "MSFT", "AMZN", "GOOGL", "META"],
            "forex": ["EURUSD=X", "GBPUSD=X", "USDJPY=X", "AUDUSD=X"],
            "crypto": ["BTC-USD", "ETH-USD", "XRP-USD", "SOL-USD"],
            "commodities": ["GC=F", "SI=F", "CL=F", "NG=F"]
        }
        
    def get_recommendations(self, timeframe="24h", assets=None):
        """
        Generate trading recommendations for specified assets and timeframe
        
        Args:
            timeframe (str): Timeframe for analysis (12h, 24h, 3d, 1w)
            assets (list): List of specific assets to analyze, or None for default selection
            
        Returns:
            dict: Trading recommendations for each asset
        """
        if timeframe not in ["12h", "24h", "3d", "1w"]:
            timeframe = "24h"  # Default to 24h if invalid timeframe
        
        # If no specific assets requested, use a default selection
        if not assets:
            assets = self._get_default_assets()
        
        recommendations = {}
        for asset in assets:
            asset_type = self._determine_asset_type(asset)
            if not asset_type:
                continue  # Skip unsupported assets
                
            # Fetch data and generate recommendation
            asset_data = self.data_fetcher.get_stock_data(asset, timeframe)
            if asset_data:
                recommendations[asset] = {
                    "symbol": asset,
                    "name": self._get_asset_name(asset),
                    "type": asset_type,
                    "price": asset_data["price"],
                    "currency": asset_data["currency"],
                    "recommendation": asset_data["recommendation"],
                    "potential": round(asset_data["potential"], 2),
                    "entry_price": asset_data["price"],
                    "stop_loss": asset_data["stop_loss"],
                    "take_profit": asset_data["take_profit"],
                    "confidence": asset_data["confidence"],
                    "expiration": asset_data["expiration"],
                    "timeframe": timeframe
                }
        
        # Sort recommendations by potential (descending)
        sorted_recommendations = dict(sorted(
            recommendations.items(), 
            key=lambda item: abs(item[1]["potential"]), 
            reverse=True
        ))
        
        return {
            "timestamp": datetime.now().strftime("%I:%M %p %m/%d/%Y"),
            "timeframe": timeframe,
            "recommendations": sorted_recommendations
        }
    
    def _get_default_assets(self):
        """Get a default selection of assets across different types"""
        default_assets = []
        default_assets.extend(self.supported_assets["stocks"][:2])  # Top 2 stocks
        default_assets.extend(self.supported_assets["forex"][:1])   # Top 1 forex
        default_assets.extend(self.supported_assets["crypto"][:1])  # Top 1 crypto
        default_assets.extend(self.supported_assets["commodities"][:1])  # Top 1 commodity
        return default_assets
    
    def _determine_asset_type(self, symbol):
        """Determine the type of asset based on symbol"""
        if symbol in self.supported_assets["stocks"]:
            return "Stock"
        elif symbol in self.supported_assets["forex"]:
            return "Forex"
        elif symbol in self.supported_assets["crypto"]:
            return "Crypto"
        elif symbol in self.supported_assets["commodities"]:
            return "Commodity"
        return None
    
    def _get_asset_name(self, symbol):
        """Get full name for an asset symbol"""
        asset_names = {
            # Stocks
            "AAPL": "Apple Inc.",
            "MSFT": "Microsoft Corporation",
            "AMZN": "Amazon.com Inc.",
            "GOOGL": "Alphabet Inc.",
            "META": "Meta Platforms Inc.",
            
            # Forex
            "EURUSD=X": "Euro / US Dollar",
            "GBPUSD=X": "British Pound / US Dollar",
            "USDJPY=X": "US Dollar / Japanese Yen",
            "AUDUSD=X": "Australian Dollar / US Dollar",
            
            # Crypto
            "BTC-USD": "Bitcoin / US Dollar",
            "ETH-USD": "Ethereum / US Dollar",
            "XRP-USD": "Ripple / US Dollar",
            "SOL-USD": "Solana / US Dollar",
            
            # Commodities
            "GC=F": "Gold",
            "SI=F": "Silver",
            "CL=F": "Crude Oil",
            "NG=F": "Natural Gas"
        }
        
        return asset_names.get(symbol, symbol)

# Test the recommendation engine
if __name__ == "__main__":
    engine = TradingRecommendationEngine()
    recommendations = engine.get_recommendations("24h")
    print(json.dumps(recommendations, indent=2))
