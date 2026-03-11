def generate_forecast(topics, spikes, crisis, propaganda_score):

    forecast = []

    # topic yoğunluğu
    if len(topics) > 5:
        forecast.append("high topic volatility")

    # event spike
    if spikes:
        forecast.append("emerging event spike")

    # kriz sinyalleri
    for k, v in crisis.items():

        if v >= 2:

            if k == "war_risk":
                forecast.append("possible military escalation")

            if k == "economic_crisis":
                forecast.append("economic instability risk")

            if k == "cyber_warfare":
                forecast.append("cyber conflict escalation")

            if k == "diplomatic_crisis":
                forecast.append("diplomatic breakdown risk")

    # propaganda yoğunluğu
    if propaganda_score > 2:
        forecast.append("information warfare campaign likely")

    return forecast
