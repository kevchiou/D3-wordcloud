--Aggregate Count on Instances of Hashtag Values
SELECT REPLACE(Name,',','') AS NAME, 5 * COUNT(*) AS CNT_HashtagUse
FROM V_HASHTAGS
WHERE ApplicationId = 'BFFEE970-C8B3-4A2D-89EF-A9C012000ABB'
GROUP BY REPLACE(Name,',','') 
HAVING COUNT(*) > 1 ORDER BY COUNT(*) DESC;