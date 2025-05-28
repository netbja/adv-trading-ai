// 🌐 ENHANCED DATA SOURCES - MULTICHAIN SCANNER
console.log("🔍 Initializing Enhanced Multi-Source Scanner...");

// 📊 CONFIGURATION DES SOURCES
const DATA_SOURCES = {
  // Solana Sources
  solana: {
    pumpfun: {
      enabled: true,
      endpoint: "https://api.pump.fun/coins/trending",
      rateLimit: 10, // requests per minute
      priority: 1
    },
    boopfun: {
      enabled: true,
      endpoint: "https://api.boop.fun/tokens/new",
      rateLimit: 20,
      priority: 2
    },
    meteora: {
      enabled: true,
      endpoint: "https://api.meteora.ag/pools",
      rateLimit: 30,
      priority: 3
    },
    jupiter: {
      enabled: true,
      endpoint: "https://quote-api.jup.ag/v6/tokens",
      rateLimit: 100,
      priority: 4
    },
    birdeye: {
      enabled: true,
      endpoint: "https://public-api.birdeye.so/defi/tokenlist",
      apiKey: process.env.BIRDEYE_API_KEY,
      rateLimit: 100,
      priority: 5
    }
  },
  
  // Ethereum Sources
  ethereum: {
    coingecko: {
      enabled: true,
      endpoint: "https://api.coingecko.com/api/v3/coins/markets",
      rateLimit: 50,
      priority: 1
    },
    dexscreener: {
      enabled: true,
      endpoint: "https://api.dexscreener.com/latest/dex/tokens",
      rateLimit: 300,
      priority: 2
    },
    uniswap: {
      enabled: true,
      endpoint: "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3",
      rateLimit: 1000,
      priority: 3
    },
    etherscan: {
      enabled: true,
      endpoint: "https://api.etherscan.io/api",
      apiKey: process.env.ETHERSCAN_API_KEY,
      rateLimit: 200,
      priority: 4
    }
  },
  
  // Base Sources
  base: {
    basescan: {
      enabled: true,
      endpoint: "https://api.basescan.org/api",
      apiKey: process.env.BASESCAN_API_KEY,
      rateLimit: 200,
      priority: 1
    },
    dexscreener_base: {
      enabled: true,
      endpoint: "https://api.dexscreener.com/latest/dex/search/?q=base",
      rateLimit: 300,
      priority: 2
    }
  }
};

// 🚀 ENHANCED MULTICHAIN SCANNER CLASS
class EnhancedMultichainScanner {
  constructor() {
    this.sources = DATA_SOURCES;
    this.cache = new Map();
    this.rateLimit = new Map();
    this.lastUpdate = new Map();
  }

  // 🔍 SCAN BOOP.FUN (Alternative à Pump.fun)
  async scanBoopFun() {
    console.log("🟣 Scanning Boop.fun for new tokens...");
    
    try {
      // Vérifier rate limit
      if (!this.canMakeRequest('boopfun')) {
        console.log("⏰ Boop.fun rate limited, using cache");
        return this.getFromCache('boopfun');
      }
      
      const response = await fetch(`${this.sources.solana.boopfun.endpoint}?limit=20&sort=created_desc`);
      
      if (!response.ok) {
        throw new Error(`Boop.fun API error: ${response.status}`);
      }
      
      const data = await response.json();
      
      // Normaliser les données Boop.fun
      const normalizedTokens = data.tokens?.map(token => ({
        symbol: token.symbol,
        name: token.name,
        address: token.mint,
        price: parseFloat(token.price_usd || 0),
        marketCap: parseFloat(token.market_cap || 0),
        volume24h: parseFloat(token.volume_24h || 0),
        ageMinutes: this.calculateAgeMinutes(token.created_at),
        bondingProgress: parseFloat(token.bonding_curve_progress || 0),
        socialSignals: this.calculateSocialSignals(token),
        platform: "boop.fun",
        source: "boopfun",
        rawData: token
      })) || [];
      
      // Filtrer selon critères
      const filtered = this.applyMemeFilters(normalizedTokens);
      
      this.updateCache('boopfun', filtered);
      this.updateRateLimit('boopfun');
      
      console.log(`✅ Boop.fun: Found ${filtered.length} qualifying tokens`);
      return filtered;
      
    } catch (error) {
      console.error("❌ Boop.fun scan failed:", error);
      return this.getFromCache('boopfun') || [];
    }
  }

  // 🌊 SCAN METEORA POOLS (Concentrated Liquidity)
  async scanMeteoraPools() {
    console.log("🌊 Scanning Meteora concentrated liquidity pools...");
    
    try {
      if (!this.canMakeRequest('meteora')) {
        return this.getFromCache('meteora');
      }
      
      const response = await fetch(`${this.sources.solana.meteora.endpoint}?status=active&limit=50`);
      const data = await response.json();
      
      // Normaliser les données Meteora
      const normalizedPools = data.pools?.map(pool => ({
        symbol: pool.token_a.symbol + "/" + pool.token_b.symbol,
        name: `${pool.token_a.name}-${pool.token_b.name} Pool`,
        address: pool.pool_address,
        price: parseFloat(pool.price || 0),
        marketCap: parseFloat(pool.tvl || 0), // TVL comme proxy market cap
        volume24h: parseFloat(pool.volume_24h || 0),
        ageMinutes: this.calculateAgeMinutes(pool.created_at),
        liquidity: parseFloat(pool.liquidity || 0),
        apr: parseFloat(pool.apr || 0),
        fees24h: parseFloat(pool.fees_24h || 0),
        platform: "meteora",
        source: "meteora",
        poolType: "concentrated_liquidity",
        tokens: [pool.token_a, pool.token_b],
        rawData: pool
      })) || [];
      
      // Filtrer pools intéressants
      const filtered = normalizedPools.filter(pool => 
        pool.volume24h > 10000 && // Volume minimum
        pool.liquidity > 50000 && // Liquidité minimum
        pool.apr > 10 // APR minimum
      );
      
      this.updateCache('meteora', filtered);
      this.updateRateLimit('meteora');
      
      console.log(`✅ Meteora: Found ${filtered.length} interesting pools`);
      return filtered;
      
    } catch (error) {
      console.error("❌ Meteora scan failed:", error);
      return this.getFromCache('meteora') || [];
    }
  }

  // 📊 SCAN DEXSCREENER MULTICHAIN
  async scanDexScreener(chains = ['solana', 'ethereum', 'base']) {
    console.log("📊 Scanning DexScreener across multiple chains...");
    
    const results = [];
    
    for (const chain of chains) {
      try {
        if (!this.canMakeRequest(`dexscreener_${chain}`)) {
          continue;
        }
        
        const endpoint = `https://api.dexscreener.com/latest/dex/search/?q=${chain}`;
        const response = await fetch(endpoint);
        const data = await response.json();
        
        // Normaliser données DexScreener
        const normalized = data.pairs?.map(pair => ({
          symbol: pair.baseToken.symbol,
          name: pair.baseToken.name,
          address: pair.baseToken.address,
          price: parseFloat(pair.priceUsd || 0),
          marketCap: parseFloat(pair.marketCap || 0),
          volume24h: parseFloat(pair.volume?.h24 || 0),
          priceChange24h: parseFloat(pair.priceChange?.h24 || 0),
          liquidity: parseFloat(pair.liquidity?.usd || 0),
          ageMinutes: this.calculateAgeMinutes(pair.pairCreatedAt),
          dexId: pair.dexId,
          chain: chain,
          platform: "dexscreener",
          source: `dexscreener_${chain}`,
          pairAddress: pair.pairAddress,
          rawData: pair
        })).filter(token => 
          token.volume24h > 5000 && // Volume minimum
          token.liquidity > 10000 && // Liquidité minimum
          token.ageMinutes < 1440 // Moins de 24h
        ) || [];
        
        results.push(...normalized);
        this.updateRateLimit(`dexscreener_${chain}`);
        
        console.log(`✅ DexScreener ${chain}: Found ${normalized.length} tokens`);
        
      } catch (error) {
        console.error(`❌ DexScreener ${chain} scan failed:`, error);
      }
    }
    
    return results;
  }

  // 🐦 SCAN BIRDEYE (Premium Solana Data)
  async scanBirdEye() {
    console.log("🐦 Scanning BirdEye for premium Solana data...");
    
    try {
      if (!this.sources.solana.birdeye.apiKey) {
        console.log("⚠️ BirdEye API key not configured, skipping");
        return [];
      }
      
      if (!this.canMakeRequest('birdeye')) {
        return this.getFromCache('birdeye');
      }
      
      const headers = {
        'X-API-KEY': this.sources.solana.birdeye.apiKey,
        'Content-Type': 'application/json'
      };
      
      // Trending tokens
      const trendingResponse = await fetch(
        'https://public-api.birdeye.so/defi/trending?offset=0&limit=20',
        { headers }
      );
      
      if (!trendingResponse.ok) {
        throw new Error(`BirdEye API error: ${trendingResponse.status}`);
      }
      
      const trendingData = await trendingResponse.json();
      
      // Normaliser données BirdEye
      const normalized = trendingData.data?.items?.map(token => ({
        symbol: token.symbol,
        name: token.name,
        address: token.address,
        price: parseFloat(token.price || 0),
        marketCap: parseFloat(token.mc || 0),
        volume24h: parseFloat(token.v24hUSD || 0),
        priceChange24h: parseFloat(token.priceChange24h || 0),
        liquidity: parseFloat(token.liquidity || 0),
        holders: parseInt(token.numberMarkets || 0),
        platform: "birdeye",
        source: "birdeye",
        chain: "solana",
        rawData: token
      })) || [];
      
      const filtered = this.applyMemeFilters(normalized);
      
      this.updateCache('birdeye', filtered);
      this.updateRateLimit('birdeye');
      
      console.log(`✅ BirdEye: Found ${filtered.length} trending tokens`);
      return filtered;
      
    } catch (error) {
      console.error("❌ BirdEye scan failed:", error);
      return this.getFromCache('birdeye') || [];
    }
  }

  // 🔍 SCAN ÉTABLI (CoinGecko + Technical)
  async scanEstablishedTokens() {
    console.log("🔍 Scanning established tokens for technical opportunities...");
    
    try {
      if (!this.canMakeRequest('coingecko')) {
        return this.getFromCache('coingecko');
      }
      
      const endpoint = 'https://api.coingecko.com/api/v3/coins/markets?' +
        'vs_currency=usd&order=market_cap_desc&per_page=100&page=1&' +
        'sparkline=true&price_change_percentage=1h,24h,7d';
      
      const response = await fetch(endpoint);
      const data = await response.json();
      
      // Normaliser pour analyse technique
      const normalized = data.map(coin => ({
        symbol: coin.symbol.toUpperCase(),
        name: coin.name,
        address: coin.id, // CoinGecko ID
        price: parseFloat(coin.current_price || 0),
        marketCap: parseFloat(coin.market_cap || 0),
        volume24h: parseFloat(coin.total_volume || 0),
        priceChange1h: parseFloat(coin.price_change_percentage_1h_in_currency || 0),
        priceChange24h: parseFloat(coin.price_change_percentage_24h || 0),
        priceChange7d: parseFloat(coin.price_change_percentage_7d_in_currency || 0),
        marketCapRank: parseInt(coin.market_cap_rank || 999),
        sparkline: coin.sparkline_in_7d?.price || [],
        platform: "coingecko",
        source: "coingecko",
        chain: "ethereum", // Majoritairement
        category: "established",
        rawData: coin
      }));
      
      // Filtrer pour opportunités techniques
      const filtered = normalized.filter(token =>
        token.marketCapRank <= 500 && // Top 500
        token.volume24h > 1000000 && // Volume >$1M
        Math.abs(token.priceChange24h) > 3 // Mouvement >3%
      );
      
      this.updateCache('coingecko', filtered);
      this.updateRateLimit('coingecko');
      
      console.log(`✅ CoinGecko: Found ${filtered.length} technical opportunities`);
      return filtered;
      
    } catch (error) {
      console.error("❌ CoinGecko scan failed:", error);
      return this.getFromCache('coingecko') || [];
    }
  }

  // 🎯 MASTER SCAN - TOUTES SOURCES
  async performMasterScan() {
    console.log("🎯 Performing master scan across all sources...");
    
    const scanResults = {
      meme_tokens: [],
      liquidity_pools: [],
      established_tokens: [],
      timestamp: new Date().toISOString(),
      sources_scanned: [],
      total_candidates: 0
    };
    
    try {
      // Scan sources en parallèle pour performance
      const [
        pumpTokens,
        boopTokens,
        meteoraPools,
        dexScreenerTokens,
        birdEyeTokens,
        establishedTokens
      ] = await Promise.allSettled([
        this.scanPumpFun(), // Existant
        this.scanBoopFun(),
        this.scanMeteoraPools(),
        this.scanDexScreener(['solana', 'ethereum', 'base']),
        this.scanBirdEye(),
        this.scanEstablishedTokens()
      ]);
      
      // Compiler résultats réussis
      if (pumpTokens.status === 'fulfilled') {
        scanResults.meme_tokens.push(...pumpTokens.value);
        scanResults.sources_scanned.push('pump.fun');
      }
      
      if (boopTokens.status === 'fulfilled') {
        scanResults.meme_tokens.push(...boopTokens.value);
        scanResults.sources_scanned.push('boop.fun');
      }
      
      if (meteoraPools.status === 'fulfilled') {
        scanResults.liquidity_pools.push(...meteoraPools.value);
        scanResults.sources_scanned.push('meteora');
      }
      
      if (dexScreenerTokens.status === 'fulfilled') {
        scanResults.meme_tokens.push(...dexScreenerTokens.value);
        scanResults.sources_scanned.push('dexscreener');
      }
      
      if (birdEyeTokens.status === 'fulfilled') {
        scanResults.meme_tokens.push(...birdEyeTokens.value);
        scanResults.sources_scanned.push('birdeye');
      }
      
      if (establishedTokens.status === 'fulfilled') {
        scanResults.established_tokens.push(...establishedTokens.value);
        scanResults.sources_scanned.push('coingecko');
      }
      
      // Dédoublonner et scorer
      scanResults.meme_tokens = this.deduplicateTokens(scanResults.meme_tokens);
      scanResults.established_tokens = this.deduplicateTokens(scanResults.established_tokens);
      
      scanResults.total_candidates = 
        scanResults.meme_tokens.length + 
        scanResults.liquidity_pools.length + 
        scanResults.established_tokens.length;
      
      console.log(`🎯 Master scan completed:`, {
        meme_tokens: scanResults.meme_tokens.length,
        liquidity_pools: scanResults.liquidity_pools.length,
        established_tokens: scanResults.established_tokens.length,
        sources: scanResults.sources_scanned.length,
        total: scanResults.total_candidates
      });
      
      return scanResults;
      
    } catch (error) {
      console.error("❌ Master scan failed:", error);
      return scanResults;
    }
  }

  // 🧹 UTILITAIRES
  calculateAgeMinutes(createdAt) {
    if (!createdAt) return 999;
    const created = new Date(createdAt);
    const now = new Date();
    return Math.floor((now - created) / (1000 * 60));
  }

  calculateSocialSignals(token) {
    let signals = 0;
    if (token.twitter) signals++;
    if (token.telegram) signals++;
    if (token.website) signals++;
    if (token.discord) signals++;
    return signals;
  }

  applyMemeFilters(tokens) {
    return tokens.filter(token =>
      token.ageMinutes <= 120 && // Max 2h
      token.marketCap >= 5000 && token.marketCap <= 200000 && // Sweet spot
      token.volume24h >= 5000 // Volume minimum
    );
  }

  deduplicateTokens(tokens) {
    const seen = new Set();
    return tokens.filter(token => {
      const key = `${token.address}_${token.chain || 'unknown'}`;
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    });
  }

  canMakeRequest(source) {
    const lastRequest = this.rateLimit.get(source) || 0;
    const now = Date.now();
    const rateLimitWindow = 60000; // 1 minute
    
    return (now - lastRequest) > rateLimitWindow;
  }

  updateCache(source, data) {
    this.cache.set(source, {
      data: data,
      timestamp: Date.now()
    });
  }

  getFromCache(source) {
    const cached = this.cache.get(source);
    if (!cached) return [];
    
    const cacheAge = Date.now() - cached.timestamp;
    const maxAge = 300000; // 5 minutes
    
    return cacheAge < maxAge ? cached.data : [];
  }

  updateRateLimit(source) {
    this.rateLimit.set(source, Date.now());
  }

  // Placeholder pour scanPumpFun (déjà existant)
  async scanPumpFun() {
    // Utiliser le code existant du scanner pump.fun
    return [];
  }
}

// 🚀 EXPORT POUR N8N
async function executeEnhancedScan() {
  const scanner = new EnhancedMultichainScanner();
  return await scanner.performMasterScan();
}

return executeEnhancedScan();
