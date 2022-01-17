from setup import *
from tools import gen_report

parser = argparse.ArgumentParser(description="贷款计算器")

parser.add_argument("-cl", "--CommercialLoan", type=float, default=0.00,
                    metavar="商业贷款额度",
                    help="单位元, 非负实数, 缺省值为0")
parser.add_argument("-cr", "--CommercialRate", type=float, default=0.00,
                    metavar="商业贷款利率(年化)",
                    help="非负实数, 缺省值为0, 输入时应当已乘以100, 例如%%3输入3即可")
parser.add_argument("-cm", "--CommercialMode", type=int, default=0,
                    metavar="商业贷款模式",
                    help="0:等额本息, 1:等额本金")

parser.add_argument("-ncl", "--NonCommercialLoan", type=float, default=0,
                    metavar="公积金贷款额度",
                    help="单位元, 非负实数, 缺省值为0")
parser.add_argument("-ncr", "--NonCommercialRate", type=float, default=0,
                    metavar="公积金贷款利率(年化)",
                    help=" 非负实数, 缺省值为0, 输入时应当已乘以100, 例如%%3输入3即可")
parser.add_argument("-ncm", "--NonCommercialMode", type=int, default=0,
                    metavar="公积金贷款模式",
                    help="0:等额本息, 1:等额本金")

parser.add_argument("-m", "--Months", type=int, default=12,
                    metavar="贷款期数",
                    help="单位月, 缺省值为12, 例如贷款30年则应输入360")

args = parser.parse_args()
if args.CommercialMode not in [0, 1]:
    print("商业贷款模式参数不正确, 请确认")
    sys.exit()
if args.NonCommercialMode not in [0, 1]:
    print("公积金贷款模式参数不正确, 请确认")
    sys.exit()

df_commercial = gen_report(c0=args.CommercialLoan, annualized_rate=args.CommercialRate, n=args.Months, mode=args.CommercialMode)
df_non_commercial = gen_report(c0=args.NonCommercialLoan, annualized_rate=args.NonCommercialRate, n=args.Months, mode=args.NonCommercialMode)
res_df = pd.merge(left=df_commercial, right=df_non_commercial, on=["期数"], how="outer", suffixes=["_商业贷款", "_公积金贷款"]).fillna(0)
for z in ["期初贷款余额", "孳息", "偿还本金", "偿还利息", "当期还款总额", "期末贷款余额"]:
    res_df["总" + z] = res_df[z + "_商业贷款"] + res_df[z + "_公积金贷款"]

res_file = "还款方案.[商业贷款_{}_{:.2f}万_R{:.2f}].[公积金贷款_{}_{:.2f}万_R{:.2f}]_{}期.xlsx".format(
    "等额本息" if args.CommercialMode == 0 else "等额本金", args.CommercialLoan / 1e4, args.CommercialRate,
    "等额本息" if args.NonCommercialMode == 0 else "等额本金", args.NonCommercialLoan / 1e4, args.NonCommercialRate,
    args.Months
)
res_df.to_excel(res_file, index=False, float_format="%.2f")
