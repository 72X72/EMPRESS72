def narrate_etsy_metrics(metrics):
    if metrics["orders"] > 0:
        return f"EMPRESS: {metrics['orders']} orders received. Revenue mutation successful."
    elif metrics["views"] > 100:
        return "EMPRESS: High visibility detected. Rerouting to promo loop."
    else:
        return "EMPRESS: Storefront dormant. Injecting urgency protocol."
