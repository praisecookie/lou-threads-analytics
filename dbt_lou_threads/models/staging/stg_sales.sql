select
    Order_ID as order_id,
    Collection_Name as collection_name,
    Item_Type as item_type,
    Units_Sold as units_sold,
    Unit_Price as unit_price,
    Total_Revenue as total_revenue,
    Collection_Category as collection_category
from {{ source('raw_source', 'raw_sales') }}