def allowed_exposure(capital, volatility, drawdown):
    if drawdown > 0.05:
        return capital * 0.25
    if volatility == "HIGH":
        return capital * 0.30
    if volatility == "LOW":
        return capital * 0.65
    return capital * 0.45
