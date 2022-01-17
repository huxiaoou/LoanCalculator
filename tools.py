import numpy as np
import pandas as pd


def cal_pmt(c0: float, annualized_rate: float, n: int, mode: int):
    if (mode == 0) and (annualized_rate > 0):
        d = 1 / (1 + annualized_rate / 100 / 12)
        c = c0 * (1 - d) / d / (1 - d ** n)
    else:
        c = c0 / n
    return c


def gen_report(c0: float, annualized_rate: float, n: int, mode: int):
    if c0 > 0:
        # intermediary variable
        c = cal_pmt(c0, annualized_rate, n, mode)

        res = []
        t, balance = 0, c0
        while abs(balance) > 0.01:
            c_init = balance
            interest = c_init * annualized_rate / 100 / 12
            c_sum = c_init + interest
            if mode == 0:
                paid_interest = interest
                paid_premium = c - interest
                paid_sum = c
            else:
                paid_interest = interest
                paid_premium = c
                paid_sum = c + interest
            balance = c_sum - paid_sum
            res.append({
                "期数": t,
                "期初贷款余额": c_init,
                "孳息": interest,
                "偿还本金": paid_premium,
                "偿还利息": paid_interest,
                "当期还款总额": paid_sum,
                "期末贷款余额": balance
            })
            t += 1
        df = pd.DataFrame(res)

    else:
        df = pd.DataFrame({
            "期数": [],
            "期初贷款余额": [],
            "孳息": [],
            "偿还本金": [],
            "偿还利息": [],
            "当期还款总额": [],
            "期末贷款余额": []
        })

    return df
