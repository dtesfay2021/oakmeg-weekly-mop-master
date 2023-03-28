from sqlalchemy import sql

from mop.validator import validate_project
from core_funcs import connect_db

engines = connect_db()

def pull_campaigns(project):
        
    validate_project(project)
    
    campaign_query = """
        WITH
        campaigns_to_search AS (
        SELECT
            DISTINCT dt.adtype
        FROM
            dash_table dt
        WHERE
            dt.project = :p
            AND dt.date_served >= (current_date - 7)
        ),
        last_wk AS (
        SELECT
            dt2.adtype,
            CASE 
                WHEN sum(impressions) = 0 THEN 1
                ELSE sum(impressions)
            END AS impressions,
            sum(dt2.clicks) AS clicks
        FROM
            dash_table dt2
        WHERE
            dt2.date_served >= (current_date - 7)
                AND dt2.adtype IN (
                SELECT
                    adtype
                FROM
                    campaigns_to_search)
            GROUP BY
                dt2.adtype
        ),
        wk_prior AS (
        SELECT
            dt3.adtype,
            CASE 
                WHEN sum(impressions) = 0 THEN 1
                ELSE sum(impressions)
            END AS impressions,
            sum(dt3.clicks) AS clicks
        FROM
            dash_table dt3
        WHERE
            dt3.date_served BETWEEN (current_date - 14) AND (current_date - 8)
                AND dt3.adtype IN (
                SELECT
                    adtype
                FROM
                    campaigns_to_search)
            GROUP BY
                dt3.adtype
        ),
        all_time AS (
        SELECT
            dt3.adtype,
            CASE 
                WHEN sum(impressions) = 0 THEN 1
                ELSE sum(impressions)
            END AS impressions,
            sum(dt3.clicks) AS clicks
        FROM
            dash_table dt3
        WHERE
            dt3.adtype IN (
            SELECT
                    adtype
            FROM
                    campaigns_to_search)
        GROUP BY
                dt3.adtype
        ),
        fig_perf AS (
        SELECT
            adtype,
            date_served,
            CASE 
                WHEN sum(impressions) = 0 THEN 1
                ELSE sum(impressions)
            END AS impressions,
            sum(clicks) AS clicks
        FROM
            dash_table dt2
        WHERE
            dt2.adtype IN (
            SELECT
                adtype
            FROM
                campaigns_to_search)
            AND dt2.date_served >= (current_date - 7)
        GROUP BY
            dt2.adtype,
            dt2.date_served
        ORDER BY
            date_served)
        SELECT
            json_build_object(
        'campaign_name', dt.adtype,
        'campaigntag', split_part(dt.adtype, '-', 1),
        'startdate-enddate', min(dt.date_served) || ' - ' || max(dt.date_served),
        'formats', string_agg(DISTINCT dt.format, ', '),
        'countries', string_agg(DISTINCT dt.country_code, ', '),
        'td_impressions', to_char(COALESCE((alt.impressions), 1), 'FM99,999,999'),
        'td_clicks', to_char(COALESCE((alt.clicks), 1), 'FM999,999,999'),
        'td_ctr', to_char((sum(alt.clicks) / sum(alt.impressions))* 100, 'FM999,999,999D00%'),
        'lw_impressions', to_char(COALESCE(lw.impressions, 1), 'FM99,999,999'),
        'lw_clicks', to_char(COALESCE(lw.clicks, 1), 'FM99,999,999'),
        'lw_ctr', to_char((sum(lw.clicks) / sum(lw.impressions))* 100, 'FM99,999,999D00%'),
        'wp_impressions', to_char(COALESCE(wp.impressions, 1), 'FM99,999,999'),
        'wp_clicks', to_char(COALESCE(wp.clicks, 1), 'FM99,999,999'),
        'wp_ctr', to_char((sum(wp.clicks) / sum(wp.impressions))* 100, 'FM99,999,999D00%'),
        'daily_fig_performance', jsonb_agg(DISTINCT jsonb_build_object(fp.date_served, jsonb_build_array(fp.impressions, fp.clicks, round(fp.clicks / fp.impressions, 2))))
        )
        FROM
            dash_table dt,
            all_time AS alt,
            last_wk AS lw,
            wk_prior AS wp,
            fig_perf AS fp
        WHERE
            dt.adtype IN (
            SELECT
                    adtype
            FROM
                    campaigns_to_search)
            AND dt.adtype = alt.adtype
            AND alt.adtype = lw.adtype
            AND lw.adtype = wp.adtype
            AND wp.adtype = fp.adtype
        GROUP BY
            dt.adtype,
            fp.adtype,
            alt.impressions,
            alt.clicks,
            lw.impressions,
            lw.clicks,
            wp.impressions,
            wp.clicks
        ORDER BY
            dt.adtype
        ;
    """
    
    write_engine = engines[0]
    
    with write_engine.connect() as conn:
        res = conn.execute(sql.text(campaign_query), {'p': project})
        rows = res.fetchall()

    return rows