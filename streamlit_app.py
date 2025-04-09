# 簡易網頁工具版：互動式高低利率資金配置模擬

import streamlit as st
import pandas as pd

# 模擬函數
def simulate_expected_return(high_rate, low_daily_rate, scenarios):
    total_capital = 1_000_000
    low_annual = low_daily_rate * 365
    allocation_range = [i / 100 for i in range(101)]

    results = []
    for ratio in allocation_range:
        high_amt = total_capital * ratio
        low_amt = total_capital * (1 - ratio)

        expected_high = 0
        for prob, days in scenarios:
            high_annual = high_rate * days * (days / 365)
            expected_high += prob * high_amt * high_annual

        expected_low = low_amt * low_annual
        total_expected = expected_high + expected_low

        results.append({
            '高利比例': ratio,
            '期望報酬率 (%)': total_expected / total_capital * 100
        })

    best = max(results, key=lambda x: x['期望報酬率 (%)'])
    return best, results

# Streamlit 互動界面
st.title("高低利率資金配置模擬工具")

high_rate = st.number_input("高利率（日利）", value=0.0056, min_value=0.0, step=0.0001, format="%.4f")
low_daily_rate = st.number_input("低利率（日利）", value=0.0005, min_value=0.0, step=0.0001, format="%.4f")

st.markdown("### 請輸入機率分布（最多三組）")
prob1 = st.slider("情境1機率", 0.0, 1.0, 0.9)
days1 = st.number_input("情境1：可操作天數", value=90, step=5)
prob2 = st.slider("情境2機率", 0.0, 1.0 - prob1, 0.1)
days2 = st.number_input("情境2：可操作天數", value=180, step=5)

scenarios = [(prob1, days1)]
if prob2 > 0:
    scenarios.append((prob2, days2))

# 計算與顯示結果
if st.button("開始模擬"):
    best, results = simulate_expected_return(high_rate, low_daily_rate, scenarios)
    st.metric("最佳高利比例", f"{round(best['高利比例'] * 100)}%")
    st.metric("期望報酬率", f"{round(best['期望報酬率 (%)'], 2)}%")

    df = pd.DataFrame(results)
    st.line_chart(df.set_index('高利比例'))