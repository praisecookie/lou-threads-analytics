select
    Order_ID as order_id,
    Star_Rating as star_rating,
    Return_Status as return_status,
    Sentiment as sentiment
from {{ source('raw_source', 'raw_reviews') }}