"""
📈 MARKET DATA MODEL - MODÈLE DONNÉES MARCHÉ
Stockage des données de marché et analyses
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean
from sqlalchemy.sql import func
from app.database.connection import Base

class MarketData(Base):
    """
    📊 Modèle pour les données de marché
    """
    __tablename__ = "market_data"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), nullable=False, index=True)
    timeframe = Column(String(10), nullable=False)  # 1m, 5m, 1h, 1d, etc.
    
    # Prix OHLCV
    open_price = Column(Float, nullable=False)
    high_price = Column(Float, nullable=False)  
    low_price = Column(Float, nullable=False)
    close_price = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)
    
    # Indicateurs techniques
    volatility = Column(Float)
    trend_strength = Column(Float)
    volume_ratio = Column(Float)
    
    # Sentiment et analyse
    sentiment_score = Column(Float)
    news_impact = Column(Float)
    
    # Métadonnées
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<MarketData(symbol={self.symbol}, close={self.close_price}, time={self.timestamp})>"

class TradingSignal(Base):
    """
    🎯 Modèle pour les signaux de trading
    """
    __tablename__ = "trading_signals"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), nullable=False, index=True)
    
    # Signal
    signal_type = Column(String(10), nullable=False)  # BUY, SELL, HOLD
    confidence = Column(Float, nullable=False)
    strength = Column(Float, nullable=False)
    
    # Prix
    entry_price = Column(Float)
    stop_loss = Column(Float)
    take_profit = Column(Float)
    
    # Métadonnées
    reasoning = Column(Text)
    source = Column(String(50))  # technical_ai, sentiment_ai, etc.
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    executed_at = Column(DateTime(timezone=True))
    closed_at = Column(DateTime(timezone=True))
    
    def __repr__(self):
        return f"<TradingSignal(symbol={self.symbol}, type={self.signal_type}, confidence={self.confidence})>" 