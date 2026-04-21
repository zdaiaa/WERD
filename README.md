# WealthX / NexusOS

这个仓库现在已经可以直接部署到 Render，并提供 Stripe webhook 接口。

## 本地运行

```bash
npm install
npm start
```

默认端口：`3000`

- 首页：`http://localhost:3000/`
- 健康检查：`http://localhost:3000/api/health`
- Stripe webhook：`http://localhost:3000/api/stripe/webhook`

## Render 部署（私有 GitHub 仓库）

### 方式 A：使用 `render.yaml`（推荐）

1. 把代码推送到 GitHub 私有仓库。
2. 在 Render 选择 **New +** → **Blueprint**。
3. 连接该仓库并创建服务。
4. 在 Render 的服务环境变量中配置：
   - `STRIPE_SECRET_KEY`
   - `STRIPE_WEBHOOK_SECRET`
5. 部署完成后会拿到 URL：`https://<your-service>.onrender.com`

Webhook 地址填写：

```text
https://<your-service>.onrender.com/api/stripe/webhook
```

### 方式 B：手动创建 Web Service

- Environment: `Node`
- Build Command: `npm install`
- Start Command: `npm start`

同样需要配置：

- `STRIPE_SECRET_KEY`
- `STRIPE_WEBHOOK_SECRET`

## Stripe webhook 验签说明

- 若同时配置了 `STRIPE_SECRET_KEY` 与 `STRIPE_WEBHOOK_SECRET`，服务会对 webhook 进行签名验证。
- 若未配置，服务仍会接收 webhook 并返回 `{"received": true}`，但不会验签（仅建议调试使用）。
