/**
 * USDT.BTC – Cryptocurrency converter utilities
 *
 * Provides functions to convert between USDT (Tether) and BTC (Bitcoin)
 * using a given exchange rate, and to format the results for display.
 */

/**
 * Converts an amount in USDT to its equivalent value in BTC.
 *
 * @param {number} usdtAmount        - The amount of USDT to convert.
 * @param {number} btcPriceInUsdt    - The current price of one BTC expressed in USDT.
 * @returns {number}                   The equivalent amount in BTC.
 */
function convertUsdtToBtc(usdtAmount, btcPriceInUsdt) {
  if (typeof usdtAmount !== "number" || isNaN(usdtAmount) || usdtAmount < 0) {
    throw new RangeError(`usdtAmount must be a non-negative number, received: ${usdtAmount}`);
  }
  if (btcPriceInUsdt <= 0) {
    throw new RangeError(`btcPriceInUsdt must be a positive number, received: ${btcPriceInUsdt}`);
  }
  return usdtAmount / btcPriceInUsdt;
}

/**
 * Converts an amount in BTC to its equivalent value in USDT.
 *
 * @param {number} btcAmount         - The amount of BTC to convert.
 * @param {number} btcPriceInUsdt    - The current price of one BTC expressed in USDT.
 * @returns {number}                   The equivalent amount in USDT.
 */
function convertBtcToUsdt(btcAmount, btcPriceInUsdt) {
  if (typeof btcAmount !== "number" || isNaN(btcAmount) || btcAmount < 0) {
    throw new RangeError(`btcAmount must be a non-negative number, received: ${btcAmount}`);
  }
  if (btcPriceInUsdt <= 0) {
    throw new RangeError(`btcPriceInUsdt must be a positive number, received: ${btcPriceInUsdt}`);
  }
  return btcAmount * btcPriceInUsdt;
}

/**
 * Formats a BTC value as a human-readable string with up to 8 decimal places.
 *
 * @param {number} btcAmount  - The BTC amount to format.
 * @returns {string}            A string like "0.00123456 BTC".
 */
function formatBtcAmount(btcAmount) {
  return `${btcAmount.toFixed(8)} BTC`;
}

/**
 * Formats a USDT value as a human-readable string with 2 decimal places.
 *
 * @param {number} usdtAmount  - The USDT amount to format.
 * @returns {string}             A string like "1234.56 USDT".
 */
function formatUsdtAmount(usdtAmount) {
  return `${usdtAmount.toFixed(2)} USDT`;
}

module.exports = {
  convertUsdtToBtc,
  convertBtcToUsdt,
  formatBtcAmount,
  formatUsdtAmount,
};
