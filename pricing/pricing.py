# -*- coding: utf-8 -*-
import json

import pandas as pd
import numpy as np
from fastapi.encoders import jsonable_encoder


def price_item(
    item: "pd.Series",
    marketplace_pricing,
    our_margin: "float" = 0.1,
    outbound: "float" = 2.8,
    vat: "float" = 0.1667,
):
    logistics_inbound = 2.86
    warehouse_costs = 1.55
    offset_price = float(item) + logistics_inbound + warehouse_costs + float(outbound)
    total = offset_price / (1.0 - our_margin)
    commissions = marketplace_pricing(pd.Series({"price": total}), our_margin)
    grand_total = float(total) + (float(vat) * (float(total) - float(item))) + float(commissions)
    return np.round(grand_total, 2)


def price_vestiaire(item: "pd.Series", margin: "float" = 0.0):
    if item["price"] < 130:
        return 13.0
    if (item["price"] >= 130) & (item["price"] < 300):
        return item["price"] * 0.15
    if (item["price"] >= 300) & (item["price"] < 500):
        return item["price"] * 0.2
    if (item["price"] >= 500) & (item["price"] < 7000):
        return item["price"] * 0.25
    if item["price"] >= 7000:
        return 1750
    else:
        raise ArithmeticError(f"Cannot compute commission for ${item}")


def price_videdressing(item: "pd.Series", margin: "float" = 0.0):
    price = item["price"]
    local_margin = np.maximum(np.minimum(0.15 * price, 300.0), 5.0)
    return np.round((1 + margin) * local_margin)


def price_ebay(item: "pd.Series", margin: "float" = 0.0):
    price = item["price"]
    local_margin = 0.12 * price
    return local_margin


def price_depop(item: "pd.Series", margin: "float" = 0.0):
    price = item["price"]
    local_margin = 0.10 * price
    return local_margin


def price_non(item, margin):
    return 0


def price_hewi(item: "pd.Series", margin: "float" = 0.0):
    hewi_margin = 1.2 * (item["price"] * 0.18)
    total = (1 + margin) * hewi_margin
    return np.round(np.maximum(15.0, total), 3)


def price_rebelle(item: "pd.Series", margin: "float" = 0.0):
    price = item["price"] / 0.85
    commission = 20.0
    try:
        if price > 40.0:
            price = price - 40.0
            local = pd.DataFrame(
                [
                    {"low": 41, "high": 150, "margin": 0.33 * (1 + margin)},
                    {"low": 151, "high": 500, "margin": 0.3 * (1 + margin)},
                    {"low": 501, "high": 800, "margin": 0.28 * (1 + margin)},
                    {"low": 801, "high": 1250, "margin": 0.24 * (1 + margin)},
                    {"low": 1251, "high": 1600, "margin": 0.22 * (1 + margin)},
                    {"low": 1601, "high": 2400, "margin": 0.18 * (1 + margin)},
                    {"low": 2401, "high": 1e6, "margin": 0.17 * (1 + margin)},
                ]
            )
            x = local[local["low"] < (item["price"] / 0.85)].copy()
            x["diff"] = x["high"] - (x["low"] - 1)
            x.loc[x.iloc[-1].name, "diff"] = (
                price - x[x["low"] < price].iloc[:-1]["diff"].sum()
            )
            x["cost"] = x["margin"] * x["diff"]
            commission = np.ceil(commission + x["cost"].sum())
    except IndexError:
        commission = np.NAN
    return commission


def price_marketplace(listing_request, marketplace, margin):
    marketplace_dispatcher = {
        "hewi": price_hewi,
        "rebelle": price_rebelle,
        "ebay": price_ebay,
        "videdressing": price_videdressing,
        "vestiairecollective": price_vestiaire,
        "depop": price_depop,
        "vinted": price_non,
    }
    listing_df = pd.json_normalize(listing_request, record_path=['items'], errors='ignore')

    listing_df["margin"] = margin
    listing_df_specific = listing_df.copy()
    listing_df_specific.rename(columns={"price": "net_price"}, inplace=True)
    listing_df_specific["price"] = listing_df_specific["net_price"].map(
        lambda x: price_item(x, marketplace_dispatcher[marketplace], margin)
    )
    listing_df_specific = listing_df_specific.to_json(orient='records')
    print(listing_df_specific)

    return listing_df_specific
