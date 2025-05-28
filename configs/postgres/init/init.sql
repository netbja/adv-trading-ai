-- 🗃️ POSTGRESQL INITIALIZATION TRADING AI - VERSION MODERNE
-- Utilise gen_random_uuid() natif PostgreSQL 13+ (pas d'extension requise)

-- Créer la base N8N (IMPORTANT pour N8N!)
CREATE DATABASE n8n;

-- Table des trades (UUID natif PostgreSQL 13+)
CREATE TABLE IF NOT EXISTS trades (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workflow_type VARCHAR(50) NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    side VARCHAR(10) NOT NULL,
    amount DECIMAL(18,8) NOT NULL,
    price DECIMAL(18,8) NOT NULL,
    status VARCHAR(20) DEFAULT 'OPEN',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table des métriques de santé  
CREATE TABLE IF NOT EXISTS health_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    service_name VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL,
    latency_ms INTEGER,
    error_message TEXT,
    checked_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index pour performance
CREATE INDEX IF NOT EXISTS idx_trades_symbol ON trades(symbol);
CREATE INDEX IF NOT EXISTS idx_trades_created_at ON trades(created_at);
CREATE INDEX IF NOT EXISTS idx_health_checked_at ON health_metrics(checked_at);

-- Données de test
INSERT INTO trades (workflow_type, symbol, side, amount, price, status) VALUES 
('MEME_SCALPING', 'PEPE', 'BUY', 1000000, 0.00001, 'CLOSED'),
('TECHNICAL', 'ETH', 'BUY', 0.5, 2000, 'OPEN'),
('MEME_SCALPING', 'DOGE', 'SELL', 10000, 0.08, 'CLOSED')
ON CONFLICT DO NOTHING;