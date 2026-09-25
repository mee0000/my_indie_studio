-- 1. 用户表 (Users)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'client', -- 'client' (买家) 或 'buyer' (代购/买手)
    created_at TIMESTAMP WITH TIMEZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. 求购/代购需求单表 (Demand Posts)
CREATE TABLE demand_posts (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,            -- 例: "弘大 Gentle Monster 限量款墨镜代购"
    category VARCHAR(50) NOT NULL,           -- 'fashion', 'beauty', 'popup'
    target_price_krw INT NOT NULL,           -- 买家期望韩币价格
    status VARCHAR(20) DEFAULT 'pending',    -- 'pending', 'matched', 'completed', 'cancelled'
    description TEXT,
    created_at TIMESTAMP WITH TIMEZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. 报价/接单表 (Offers)
CREATE TABLE offers (
    id SERIAL PRIMARY KEY,
    demand_id INT REFERENCES demand_posts(id) ON DELETE CASCADE,
    buyer_id INT REFERENCES users(id) ON DELETE CASCADE,
    offered_price_rmb DECIMAL(10, 2) NOT NULL, -- 代购出价（人民币）
    status VARCHAR(20) DEFAULT 'submitted',     -- 'submitted', 'accepted', 'rejected'
    created_at TIMESTAMP WITH TIMEZONE DEFAULT CURRENT_TIMESTAMP
);