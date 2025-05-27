---
# init.sql - Structure base de données
CREATE TABLE IF NOT EXISTS trades (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    symbol VARCHAR(20) NOT NULL,
    action VARCHAR(10) NOT NULL, -- BUY/SELL
    price DECIMAL(20,10) NOT NULL,
    quantity DECIMAL(20,4) NOT NULL,
    amount_usd DECIMAL(12,2) NOT NULL,
    strategy VARCHAR(20) NOT NULL, -- MEME/TECHNICAL
    profit_score INTEGER,
    expected_roi DECIMAL(5,2),
    actual_roi DECIMAL(5,2),
    holding_time_minutes INTEGER,
    status VARCHAR(20) DEFAULT 'OPEN', -- OPEN/CLOSED/STOPPED
    platform VARCHAR(20) NOT NULL,
    wallet_address VARCHAR(100),
    chain VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS portfolio_snapshots (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_balance DECIMAL(12,2) NOT NULL,
    available_balance DECIMAL(12,2) NOT NULL,
    positions_count INTEGER NOT NULL,
    total_pnl DECIMAL(12,2) NOT NULL,
    daily_pnl DECIMAL(12,2) NOT NULL,
    win_rate DECIMAL(5,2) NOT NULL,
    strategy VARCHAR(20) NOT NULL,
    chain VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS market_conditions (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    condition VARCHAR(20) NOT NULL, -- BULL/BEAR/CRAB
    volatility_level VARCHAR(20) NOT NULL, -- HIGH/MEDIUM/LOW
    volume_24h DECIMAL(15,2),
    strategy_allocation JSONB NOT NULL, -- {"meme": 70, "technical": 30}
    confidence_score INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS ai_learning (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    strategy VARCHAR(20) NOT NULL,
    pattern_type VARCHAR(50) NOT NULL,
    pattern_data JSONB NOT NULL,
    success_rate DECIMAL(5,2) NOT NULL,
    trades_count INTEGER NOT NULL,
    avg_roi DECIMAL(5,2) NOT NULL,
    confidence INTEGER NOT NULL
);

-- Indexes pour performance
CREATE INDEX idx_trades_timestamp ON trades(timestamp);
CREATE INDEX idx_trades_symbol ON trades(symbol);
CREATE INDEX idx_trades_strategy ON trades(strategy);
CREATE INDEX idx_portfolio_timestamp ON portfolio_snapshots(timestamp);
CREATE INDEX idx_market_timestamp ON market_conditions(timestamp);
