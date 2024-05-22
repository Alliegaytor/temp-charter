import pandas as pd
df = pd.read_csv("import.csv")
df.Time = pd.to_datetime(df.Time, origin='unix', unit='ms')
x = df.Time.values
print(*x, sep="Z\n", end="Z\n")
