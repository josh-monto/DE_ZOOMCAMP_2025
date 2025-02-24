{#
    This macro returns the quarter
#}

{% macro get_quarter(month) -%}

    case {{ dbt.safe_cast("extract(month from trips_unioned.pickup_datetime)", api.Column.translate_type("integer")) }}  
        when 1 then 1
        when 2 then 1
        when 3 then 1
        when 4 then 2
        when 5 then 2
        when 6 then 2
        when 7 then 3
        when 8 then 3
        when 9 then 3
        when 10 then 4
        when 11 then 4
        when 12 then 4
    end

{%- endmacro %}