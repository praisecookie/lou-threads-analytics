select
    Collection_Name as collection_name,
    TikTok_Spend as tiktok_spend,
    IG_Spend as ig_spend,
    Google_Ads_Spend as google_ads_spend,
    Total_Spend as total_spend,
    Clicks as clicks
from {{ source('raw_source', 'raw_marketing') }}