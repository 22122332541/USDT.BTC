/**
 * USDT.BTC – HTTP API server
 *
 * Exposes the converter utilities over HTTP as a lightweight JSON REST API.
 * Uses only Node.js built-in modules; no external dependencies required.
 *
 * Start:
 *   node server.js            – runs standalone
 *   const { start } = require('./server'); start();  – programmatic use
 *
 * Endpoints:
 *   GET /convert/usdt-to-btc?usdtAmount=<n>&btcPriceInUsdt=<n>
 *   GET /convert/btc-to-usdt?btcAmount=<n>&btcPriceInUsdt=<n>
 *   GET /format/btc?btcAmount=<n>
 *   GET /format/usdt?usdtAmount=<n>
 */

"use strict";

const http = require("http");
const { URL } = require("url");
const {
  convertUsdtToBtc,
  convertBtcToUsdt,
  formatBtcAmount,
  formatUsdtAmount,
} = require("./converter");

const PORT = process.env.PORT || 3000;

/**
 * Parses a query-string parameter as a finite number.
 * Returns NaN when the parameter is absent or non-numeric.
 */
function parseParam(searchParams, name) {
  const raw = searchParams.get(name);
  if (raw === null) return NaN;
  const value = Number(raw);
  return Number.isFinite(value) ? value : NaN;
}

/**
 * Sends a JSON response.
 */
function sendJson(res, statusCode, body) {
  const payload = JSON.stringify(body);
  res.writeHead(statusCode, {
    "Content-Type": "application/json",
    "Content-Length": Buffer.byteLength(payload),
  });
  res.end(payload);
}

const server = http.createServer((req, res) => {
  // Only allow GET requests
  if (req.method !== "GET") {
    return sendJson(res, 405, { error: "Method Not Allowed" });
  }

  let pathname, searchParams;
  try {
    ({ pathname, searchParams } = new URL(req.url, `http://localhost:${PORT}`));
  } catch {
    return sendJson(res, 400, { error: "Invalid request URL" });
  }

  try {
    if (pathname === "/convert/usdt-to-btc") {
      const usdtAmount = parseParam(searchParams, "usdtAmount");
      const btcPriceInUsdt = parseParam(searchParams, "btcPriceInUsdt");
      if (isNaN(usdtAmount) || isNaN(btcPriceInUsdt)) {
        return sendJson(res, 400, {
          error: "Missing or invalid query parameters: usdtAmount, btcPriceInUsdt",
        });
      }
      const btcAmount = convertUsdtToBtc(usdtAmount, btcPriceInUsdt);
      return sendJson(res, 200, { usdtAmount, btcPriceInUsdt, btcAmount });
    }

    if (pathname === "/convert/btc-to-usdt") {
      const btcAmount = parseParam(searchParams, "btcAmount");
      const btcPriceInUsdt = parseParam(searchParams, "btcPriceInUsdt");
      if (isNaN(btcAmount) || isNaN(btcPriceInUsdt)) {
        return sendJson(res, 400, {
          error: "Missing or invalid query parameters: btcAmount, btcPriceInUsdt",
        });
      }
      const usdtAmount = convertBtcToUsdt(btcAmount, btcPriceInUsdt);
      return sendJson(res, 200, { btcAmount, btcPriceInUsdt, usdtAmount });
    }

    if (pathname === "/format/btc") {
      const btcAmount = parseParam(searchParams, "btcAmount");
      if (isNaN(btcAmount)) {
        return sendJson(res, 400, { error: "Missing or invalid query parameter: btcAmount" });
      }
      return sendJson(res, 200, { btcAmount, formatted: formatBtcAmount(btcAmount) });
    }

    if (pathname === "/format/usdt") {
      const usdtAmount = parseParam(searchParams, "usdtAmount");
      if (isNaN(usdtAmount)) {
        return sendJson(res, 400, { error: "Missing or invalid query parameter: usdtAmount" });
      }
      return sendJson(res, 200, { usdtAmount, formatted: formatUsdtAmount(usdtAmount) });
    }

    return sendJson(res, 404, { error: "Not Found" });
  } catch (err) {
    return sendJson(res, 400, { error: err instanceof RangeError ? err.message : "Bad Request" });
  }
});

function start() {
  server.listen(PORT, () => {
    console.log(`USDT.BTC API server listening on http://localhost:${PORT}`);
  });
}

if (require.main === module) {
  start();
}

module.exports = { server, start };
