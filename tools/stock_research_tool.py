import yfinance as yf
from crewai.tools import tool


@tool("Live Stock Information Tool")
def get_stock_price(stock_symbol: str) -> str:
    """Retrieve the latest available price, daily change, and trading volume from Yahoo Finance."""

    try:
        symbol = stock_symbol.strip().upper()
        stock = yf.Ticker(symbol)

        intraday = stock.history(period="1d", interval="5m")
        daily = stock.history(period="5d", interval="1d")

        if intraday.empty and daily.empty:
            return (
                f"No market data returned for {symbol}. "
                "Check the ticker symbol or Yahoo Finance availability."
            )

        if not daily.empty:
            latest_daily = daily.iloc[-1]
            latest_date = daily.index[-1].date()

            if len(daily) >= 2:
                previous_close = float(daily.iloc[-2]["Close"])
            else:
                previous_close = None
        else:
            latest_daily = None
            latest_date = None
            previous_close = None

        if not intraday.empty:
            latest = intraday.iloc[-1]
            current_price = float(latest["Close"])
            volume = int(latest["Volume"])
            price_time = str(intraday.index[-1])
        else:
            current_price = float(latest_daily["Close"])
            volume = int(latest_daily["Volume"])
            price_time = str(daily.index[-1])

        if latest_date is not None and not intraday.empty:
            if intraday.index[-1].date() != latest_date:
                current_price = float(latest_daily["Close"])
                volume = int(latest_daily["Volume"])
                price_time = str(daily.index[-1])

        if previous_close is not None and previous_close != 0:
            change = current_price - previous_close
            change_percent = (change / previous_close) * 100
            change_text = (
                f"{change:+.2f} ({change_percent:+.2f}%)"
            )
        else:
            change_text = "Unavailable (insufficient daily history)"

        try:
            currency = stock.fast_info.get("currency") or "INR"
        except Exception:
            currency = "INR"

        return (
            f"Symbol: {symbol}\n"
            f"Latest available price: {current_price:.2f} {currency}\n"
            f"Change from previous close: {change_text}\n"
            f"Latest reported volume: {volume:,}\n"
            f"Price timestamp: {price_time}\n"
            "Source: Yahoo Finance. Data availability and timing may vary."
        )

    except Exception as exc:
        return (
            f"Yahoo Finance lookup failed for {stock_symbol}: "
            f"{type(exc).__name__}: {exc}"
        )
