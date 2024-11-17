{% macro generate_schema_name(custom_schema_name, node) -%}

    {%- if custom_schema_name is none -%} {{ node.name.split("_", 1)[1].split("__")[0] }}

    {%- else -%} {{ custom_schema_name | trim }}

    {%- endif -%}

{%- endmacro %}
