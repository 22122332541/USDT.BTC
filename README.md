# USDT.BTC

A minimal cryptocurrency converter utility for exchanging between **USDT (Tether)** and **BTC (Bitcoin)**.

## Project structure

```
converter.js   – Core conversion and formatting functions
server.js      – HTTP/REST API server (wraps converter.js)
README.md      – Project documentation
```

## API

### `convertUsdtToBtc(usdtAmount, btcPriceInUsdt)`

Converts an amount in USDT to its equivalent value in BTC.

```js
const { convertUsdtToBtc } = require("./converter");
const btcReceived = convertUsdtToBtc(10000, 50000); // 0.2 BTC
```

### `convertBtcToUsdt(btcAmount, btcPriceInUsdt)`

Converts an amount in BTC to its equivalent value in USDT.

```js
const { convertBtcToUsdt } = require("./converter");
const usdtReceived = convertBtcToUsdt(0.5, 50000); // 25000 USDT
```

### `formatBtcAmount(btcAmount)`

Formats a BTC value as a human-readable string (8 decimal places).

```js
formatBtcAmount(0.00123456); // "0.00123456 BTC"
```

### `formatUsdtAmount(usdtAmount)`

Formats a USDT value as a human-readable string (2 decimal places).

```js
formatUsdtAmount(1234.5); // "1234.50 USDT"
```

## HTTP API

Start the server (defaults to port 3000, override with `PORT` env var):

```sh
node server.js
# USDT.BTC API server listening on http://localhost:3000
```

### `GET /convert/usdt-to-btc`

| Query parameter  | Type   | Description                          |
|------------------|--------|--------------------------------------|
| `usdtAmount`     | number | Amount of USDT to convert            |
| `btcPriceInUsdt` | number | Current price of 1 BTC expressed in USDT |

```sh
curl "http://localhost:3000/convert/usdt-to-btc?usdtAmount=10000&btcPriceInUsdt=50000"
# {"usdtAmount":10000,"btcPriceInUsdt":50000,"btcAmount":0.2}
```

### `GET /convert/btc-to-usdt`

| Query parameter  | Type   | Description                          |
|------------------|--------|--------------------------------------|
| `btcAmount`      | number | Amount of BTC to convert             |
| `btcPriceInUsdt` | number | Current price of 1 BTC expressed in USDT |

```sh
curl "http://localhost:3000/convert/btc-to-usdt?btcAmount=0.5&btcPriceInUsdt=50000"
# {"btcAmount":0.5,"btcPriceInUsdt":50000,"usdtAmount":25000}
```

### `GET /format/btc`

| Query parameter | Type   | Description           |
|-----------------|--------|-----------------------|
| `btcAmount`     | number | BTC amount to format  |

```sh
curl "http://localhost:3000/format/btc?btcAmount=0.00123456"
# {"btcAmount":0.00123456,"formatted":"0.00123456 BTC"}
```

### `GET /format/usdt`

| Query parameter | Type   | Description            |
|-----------------|--------|------------------------|
| `usdtAmount`    | number | USDT amount to format  |

```sh
curl "http://localhost:3000/format/usdt?usdtAmount=1234.5"
# {"usdtAmount":1234.5,"formatted":"1234.50 USDT"}
```

All endpoints return JSON. Errors are returned as `{"error": "<message>"}` with an appropriate HTTP status code (`400` for bad input, `404` for unknown routes, `405` for non-GET requests).

## Naming conventions

All variables and functions use **full, descriptive names** that make the intent clear at a glance:

| Pattern | Example |
|---|---|
| Conversion functions | `convertUsdtToBtc`, `convertBtcToUsdt` |
| Formatting functions | `formatBtcAmount`, `formatUsdtAmount` |
| Amount parameters | `usdtAmount`, `btcAmount` |
| Price parameter | `btcPriceInUsdt` |
