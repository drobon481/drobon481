#!/usr/bin/env python
# coding: utf-8

# In[73]:


def github() -> str:
    """
    Returns a link to solutions on GitHub.
    """
    return "https://github.com/drobon481/drobon481/tree/main"

print(github())


# In[74]:


import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

path = 'auctions.db'

class DataBase:
    def __init__(self, loc: str, db_type: str = "sqlite") -> None:
        """Initialize the class and connect to the database"""
        self.loc = loc
        self.db_type = db_type
        self.engine = create_engine(f'{self.db_type}:///{self.loc}')
    def query(self, q: str) -> pd.DataFrame:
        """Run a query against the database and return a DataFrame"""
        with Session(self.engine) as session:
            df = pd.read_sql(q, session.bind)
        return(df)

auctions = DataBase(path)

q = 'select * from bids'
print(auctions.query(q).head(50))


# In[75]:


def std() -> str:
    """
    Generates a SQL query to calculate the standard deviation of bids 

    Returns:
        str: SQL query string
    """
    query = """
    SELECT 
        itemId, 
        SQRT(SUM((bidAmount - mean_bid) * (bidAmount - mean_bid)) / (COUNT(bidAmount) - 1)) AS std
    FROM (
        SELECT 
            itemId, 
            bidAmount,
            AVG(bidAmount) OVER (PARTITION BY itemId) AS mean_bid,
            COUNT(bidAmount) OVER (PARTITION BY itemId) AS count_bids
        FROM 
            bids
        WHERE
            bidAmount IS NOT NULL
    ) subquery
    WHERE count_bids >= 2
    GROUP BY itemId
    """
    return query

# Prepare the query
query = std()

# Execute the query using your data retrieval method (assumed to be `auctions.query` here)
result = auctions.query(query)

# Show the first few results
print(result.head(50))


# In[76]:


def get_item_ids_with_zero_std() -> str:
    """
    Generates a SQL query to get the `itemId` values that have a standard deviation of zero.

    Returns:
        str: SQL query string
    """
    query = """
    SELECT
        b.itemId,
        b.bidAmount
    FROM bids AS b
    WHERE b.itemId IN (
        SELECT
            itemId
        FROM (
            SELECT 
                itemId, 
                SQRT(SUM((bidAmount - mean_bid) * (bidAmount - mean_bid)) / (COUNT(bidAmount) - 1)) AS std
            FROM (
                SELECT 
                    itemId, 
                    bidAmount,
                    AVG(bidAmount) OVER (PARTITION BY itemId) AS mean_bid,
                    COUNT(bidAmount) OVER (PARTITION BY itemId) AS count_bids
                FROM 
                    bids
                WHERE
                    bidAmount IS NOT NULL
            ) subquery
            WHERE count_bids >= 2
            GROUP BY itemId
            HAVING std = 0
        )
    )
    """
    return query

# Prepare the query
query = get_item_ids_with_zero_std()

# Execute the query using your data retrieval method (assumed to be `auctions.query` here)
result = auctions.query(query)

# Show the results
print(result)


# In[77]:


def bidder_spend_frac() -> str:
    """
    Generates a SQL query to calculate the total spend, total bids, and spend fraction for each bidder.

    Returns:
        str: SQL query string
    """
    query = """
    WITH max_bids AS (
        SELECT
            bidderName,
            itemId,
            MAX(bidAmount) AS maxBid
        FROM
            bids
        GROUP BY
            itemId
    )
    SELECT 
        bidderName,
        SUM(CASE WHEN winningBidAmount IS NULL THEN 0 ELSE winningBidAmount END) AS total_spend,
        SUM(CASE WHEN maxBidAmount IS NULL THEN 0 ELSE maxBidAmount END) AS total_bids,
        CASE 
            WHEN SUM(CASE WHEN maxBidAmount IS NULL THEN 0 ELSE maxBidAmount END) > 0 
            THEN SUM(CASE WHEN winningBidAmount IS NULL THEN 0 ELSE winningBidAmount END) / SUM(CASE WHEN maxBidAmount IS NULL THEN 0 ELSE maxBidAmount END)
            ELSE 0 
        END AS spend_frac
    FROM
        (SELECT 
            bidderName, 
            itemId, 
            MAX(bidAmount) AS maxBidAmount,
            CASE WHEN MAX(bidAmount) = MAX(itemPrice) THEN MAX(bidAmount) ELSE NULL END AS winningBidAmount
         FROM bids
         GROUP BY bidderName, itemId) b
    GROUP BY bidderName;
    """
    return query

# Sample usage
query = bidder_spend_frac()
result = auctions.query(query)
print(result)


# In[78]:


def find_biddername():
    query = """
    SELECT *
    FROM bids
    WHERE bidderName = 'A****a';
    """
    return query

query = find_biddername()
result = auctions.query(query)
print(result.head(20))


# In[79]:


def find_itemid():
    query = """
    SELECT *
    FROM bids
    WHERE itemId = '177954527';
    """
    return query

query = find_itemid()
result = auctions.query(query)
print(result.head(20))


# In[81]:


from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
import pandas as pd

class DataBase:
    def __init__(self, loc: str, db_type: str = "sqlite") -> None:
        """Initialize the class and connect to the database"""
        self.loc = loc
        self.db_type = db_type
        self.engine = create_engine(f'{self.db_type}:///{self.loc}')
    
    def query(self, q: str) -> pd.DataFrame:
        """Run a query against the database and return a DataFrame"""
        with Session(self.engine) as session:
            df = pd.read_sql(q, session.bind)
        return df
    
    def execute(self, q: str) -> None:
        """Execute statement on the database"""
        with self.engine.connect() as conn:
            conn.execute(text(q))


path = 'auctions.db'
auctions = DataBase(path)

q = """
create table full_data as
select i.*, b.*
from items as i
inner join bids as b
on i.itemid = b.itemid
where i.isbuynowused = 0
"""
auctions.execute("drop table if exists full_data")
auctions.execute(q)
print(auctions.query("select * from full_data limit 1"))

q = """
create table full_data as
select * from items
"""



# In[82]:


""" i give up"""
def min_increment_freq() -> str:

    return q
    


# In[83]:


def win_perc_by_timestamp() -> str:
  """
  Generate SQL query to count winning bids per timestamp bin.
  """
  query = """
WITH max_bids AS (
    SELECT
      bidderName,
      itemId,
      MAX(bidAmount) AS maxBid
    FROM
      bids
    GROUP BY
      itemId
  ),
  auction_length AS (
    SELECT 
      itemid, 
      starttime, 
      endtime,
      julianday(endtime) - julianday(starttime) as length
    FROM items
  ),
  bid_times AS (
    SELECT
      b.itemid,
      b.bidtime,
      b.bidAmount,
      a.endtime,
      (julianday(a.endtime) - julianday(b.bidtime)) / a.length AS time_norm
    FROM bids AS b
    INNER JOIN auction_length AS a ON b.itemid = a.itemid
  ),
  timestamp_bins AS (
    SELECT
      time_norm,
      FLOOR(time_norm * 10) + 1 AS timestamp_bin
    FROM bid_times AS b
    INNER JOIN max_bids AS w ON b.itemid = w.itemId
),
timestamp_bins_stats AS (
    SELECT
      timestamp_bin,
      SUM(CASE WHEN b.bidAmount = w.maxBid THEN 1 ELSE 0 END) AS num_winning_bids,
      COUNT(*) AS total_bids
    FROM bid_times AS b
    INNER JOIN max_bids AS w ON b.itemid = w.itemId
    INNER JOIN timestamp_bins AS t ON b.time_norm = t.time_norm
    GROUP BY timestamp_bin
  )
SELECT
  timestamp_bin,
  CAST(SUM(num_winning_bids) AS REAL) / (SELECT SUM(total_bids) FROM timestamp_bins_stats) AS winning_bid_frac
FROM timestamp_bins_stats
GROUP BY timestamp_bin;



  """
  return query

query = win_perc_by_timestamp()
result = auctions.query(query)
print(result)


# In[ ]:




