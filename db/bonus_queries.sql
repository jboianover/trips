-- Most common regions with the latest datasource (vehicles)
WITH top_regions AS (
    SELECT region, COUNT(*) AS region_count
    FROM trip
    GROUP BY region
    ORDER BY region_count DESC
    LIMIT 2
)
SELECT t1.vehicle, t1.region
FROM trip t1
INNER JOIN
(
SELECT region, vehicle, date, time
FROM (
  SELECT region, vehicle, date, time,
         ROW_NUMBER() OVER (PARTITION BY region ORDER BY date DESC, time DESC) AS rn
  FROM trip
) subquery
WHERE rn = 1 and region in (SELECT DISTINCT REGION FROM top_regions)
ORDER BY region
) t2
ON t1.region = t2.region AND t1.date = t2.date and t1.time = t2.time
ORDER BY t1.vehicle ASC;


-- Regions which have the "cheap_mobile" datasource (vehicle) appeared in
SELECT DISTINCT region
FROM trip
WHERE vehicle = 'cheap_mobile';
This query simply selects the distinct region values from the trip table where the datasource is "cheap_mobile". This gives us a list of regions where the "cheap_mobile" datasource has appeared.