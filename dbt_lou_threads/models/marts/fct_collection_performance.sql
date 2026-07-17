with sales_summary as (
    select
        collection_name,
        collection_category,
        sum(units_sold) as total_units_sold,
        sum(total_revenue) as total_gross_revenue,
        count(distinct order_id) as total_orders
    from {{ ref('stg_sales') }}
    group by 1, 2
),

marketing_summary as (
    select
        collection_name,
        total_spend,
        clicks
    from {{ ref('stg_marketing') }}
),

reviews_summary as (
    select
        s.collection_name,
        avg(r.star_rating) as avg_rating,
        count(case when r.return_status = 'Yes' then 1 end) * 1.0 / count(r.order_id) as return_rate
    from {{ ref('stg_reviews') }} r
    join {{ ref('stg_sales') }} s on r.order_id = s.order_id
    group by 1
),

trends_summary as (
    select
        collection_name,
        google_trends_score
    from {{ ref('stg_trends') }}
)

select
    s.collection_name,
    s.collection_category,
    s.total_units_sold,
    s.total_gross_revenue,
    m.total_spend as marketing_spend,
    -- Financial Performance
    (s.total_gross_revenue - m.total_spend) as net_profit,
    round((s.total_gross_revenue - m.total_spend) / nullif(m.total_spend, 0) * 100, 2) as marketing_roi_pct,
    -- Product Quality & Feedback
    round(r.avg_rating, 2) as avg_customer_rating,
    round(r.return_rate * 100, 2) as return_rate_pct,
    -- Social Demand Hype
    t.google_trends_score
from sales_summary s
left join marketing_summary m on s.collection_name = m.collection_name
left join reviews_summary r on s.collection_name = r.collection_name
left join trends_summary t on s.collection_name = t.collection_name