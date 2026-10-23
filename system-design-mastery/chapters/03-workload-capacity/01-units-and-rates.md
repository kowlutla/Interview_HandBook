# Lesson 03.01 — Units and rates

## 3.1 Units and rates

Use consistent units. One byte is 8 bits. Decimal storage units commonly use KB = 1,000 bytes, MB = 10^6 bytes, GB = 10^9 bytes; binary units use KiB = 1,024 bytes, MiB = 2^20 bytes, GiB = 2^30 bytes. State which convention is used.

A rate is quantity divided by time. Requests/s, MB/s, and events/s are not interchangeable; each event may have a different payload size and processing cost.


## 3.2 Average traffic and peak traffic

Suppose a service receives 30 million requests per day.

- Seconds/day = 86,400.
- Average rate = 30,000,000 / 86,400 ≈ 347.22 requests/s.
- If a measured peak-to-average factor is 5, peak estimate ≈ 1,736 requests/s.

The factor 5 is an explicit assumption, not a universal property. Traffic may be more bursty around releases, notifications, or daily batch jobs. Use time-series data when available.

Averages hide synchronized bursts. Capacity must be sized against the workload interval that matters, not just the daily mean.


## 3.3 Read/write mix

If 70% of the estimated 1,736 requests/s are reads:
- Reads ≈ 1,215/s.
- Writes ≈ 521/s.

This arithmetic does not imply equal resource cost. One write may update several indexes and replicas; one read may scan millions of rows. Request mix is a starting point, and operation-weighted CPU, I/O and lock demand matter more.


---

**Chapter:** [Workload and Capacity Estimation](README.md) · **Next:** [Bandwidth](02-bandwidth.md)
