# Trading Blotter API (FastAPI + PostgreSQL + WebSockets)

This is an **end-to-end prototype** for a trading blotter that:

- Accepts trade submissions via **REST API**
- Stores trades in **PostgreSQL**
- Fetches **real-time market data** from **Alpha Vantage**
- Streams **positions, P&L, and prices** in real time over **WebSocket**
- Provides REST endpoints for trade history, positions, and P&L

---

## **Quick Start (Docker + Virtual Environment)**

### **1. Set up environment variables**

Copy `.env.example` to `.env` and update values as needed:

```bash
cp .env.example .env
```
# trade-blotter
