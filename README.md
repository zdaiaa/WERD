# WealthX / NexusOS

这个仓库已支持部署到 Render，并提供 Stripe 订阅所需的后端接口。

## 提供的接口

- `GET /api/health`：健康检查
- `POST /api/stripe/create-checkout-session`：创建订阅 Checkout Session（`plan` 传 `monthly` 或 `yearly`）
- `POST /api/stripe/webhook`：接收并验证 Stripe webhook

## 本地运行

```bash
npm install
npm start
```

默认端口：`3000`

## Render 部署（GitHub 私有仓库）

1. 把代码推送到 GitHub 私有仓库。
2. 在 Render 选择 **New +** → **Blueprint**。
3. 连接该仓库并选择默认分支（仓库根目录有 `render.yaml` 即可自动识别）。
4. 在 Render 环境变量里设置：
   - `STRIPE_SECRET_KEY`
   - `STRIPE_WEBHOOK_SECRET`
   - `WEALTHX_STRIPE_MONTHLY_PRICE_ID`
   - `WEALTHX_STRIPE_YEARLY_PRICE_ID`
   - `WEALTHX_PUBLIC_BASE_URL`
5. 先部署一次，得到公网地址（例：`https://xxx.onrender.com`）。
6. 将 `WEALTHX_PUBLIC_BASE_URL` 更新为这个公网地址后，再部署一次。

## Stripe webhook 设置

在 Stripe Workbench 创建 webhook endpoint：

```text
https://xxx.onrender.com/api/stripe/webhook
```

建议只订阅这 3 个核心事件：

- `checkout.session.completed`
- `customer.subscription.updated`
- `customer.subscription.deleted`

将 Stripe 返回的 `whsec_...` 写入 Render 的 `STRIPE_WEBHOOK_SECRET`，然后重新部署。

## 本地 App 配置

本地应用应把：

- `WEALTHX_STRIPE_API_BASE_URL`

设置为：

```text
https://xxx.onrender.com
```

## 安全提醒

如果曾经泄露过 `sk_live_...`，必须先在 Stripe 后台 rotate key，再替换成新 key，旧 key 不应继续使用。
