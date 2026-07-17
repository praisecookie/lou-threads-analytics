select
    collection_name,
    google_trends_score
from {{ source('raw_source', 'raw_trends') }}