# USDT.BTC

A minimal cryptocurrency converter utility for exchanging between **USDT (Tether)** and **BTC (Bitcoin)**.

## Project structure

```
converter.js   – Core conversion and formatting functions
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

## Naming conventions

All variables and functions use **full, descriptive names** that make the intent clear at a glance:

| Pattern | Example |
|---|---|
| Conversion functions | `convertUsdtToBtc`, `convertBtcToUsdt` |
| Formatting functions | `formatBtcAmount`, `formatUsdtAmount` |
| Amount parameters | `usdtAmount`, `btcAmount` |
| Price parameter | `btcPriceInUsdt` |
