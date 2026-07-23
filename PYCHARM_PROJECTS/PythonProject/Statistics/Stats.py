import statistics
import matplotlib.pyplot as plt
from collections import Counter

nums = [6,7,8,4,3,7,6,1,7,2,4,7,6,2]
minimum = min(nums)
maximum = max(nums)
data_range = maximum - minimum
length = len(nums)
total = sum(nums)
mean = statistics.mean(nums)
median = statistics.median(nums)
mode = statistics.mode(nums)

variance = statistics.pvariance(nums)
std = statistics.pstdev(nums)

cv = (std / mean) * 100

def z_score(x):
    return (x - mean) / std

z2 = z_score(2)
z7 = z_score(7)

freq = Counter(nums)

skewness = 3 * (mean - median) / std

print("----- Descriptive Statistics -----")
print("Minimum =", minimum)
print("Maximum =", maximum)
print("Range =", data_range)
print("Length =", length)
print("Sum =", total)
print("Mean =", round(mean,2))
print("Median =", median)
print("Mode =", mode)
print("Variance =", round(variance,2))
print("Standard Deviation =", round(std,2))
print("Coefficient of Variation =", round(cv,2), "%")
print("Z-score(2) =", round(z2,2))
print("Z-score(7) =", round(z7,2))

print("\nFrequency Table")
print("----------------")
for value in sorted(freq):
    print(f"{value} : {freq[value]}")

print("\nPearson's Skewness Ratio =", round(skewness,2))

if skewness > 0:
    print("Distribution is Positively (Right) Skewed")
elif skewness < 0:
    print("Distribution is Negatively (Left) Skewed")
else:
    print("Distribution is Symmetric")

    plt.figure(figsize=(8,5))
plt.bar(freq.keys(), freq.values())
plt.title("Frequency Distribution")
plt.xlabel("Numbers")
plt.ylabel("Frequency")
plt.xticks(sorted(freq.keys()))
plt.grid(axis='y')
plt.show()