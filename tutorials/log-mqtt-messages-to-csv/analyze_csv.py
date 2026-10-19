import glob
import pandas as pd

files = sorted(glob.glob("mqtt_logs/mqtt_*.csv"))
df = pd.concat((pd.read_csv(f, encoding="utf-8-sig") for f in files), ignore_index=True)
df["received_at"] = pd.to_datetime(df["received_at"], utc=True)

numeric = df.dropna(subset=["value"])
wide = numeric.pivot_table(index="received_at", columns="topic", values="value")
print(wide.resample("1min").mean().tail())

# Message rate per topic, useful for spotting chatty or silent devices
print(df.groupby("topic").size().sort_values(ascending=False))
