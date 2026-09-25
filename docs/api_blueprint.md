# MVP Core API Blueprint

## 1. Authentication (用户认证)
- `POST /api/v1/auth/register` - 用户注册 (Client / Buyer)
- `POST /api/v1/auth/login` - 登录获取 JWT Token

## 2. Demand Posts (求购需求)
- `GET /api/v1/demands` - 获取求购需求列表 (支持 category 筛选)
- `POST /api/v1/demands` - 发布新的代购/Popup求购需求
- `GET /api/v1/demands/{id}` - 获取特定需求详情

## 3. Offers & Matching (接单与撮合)
- `POST /api/v1/demands/{id}/offers` - 买手/代购提交报价
- `POST /api/v1/offers/{id}/accept` - 买家确认接受报价（完成匹配）