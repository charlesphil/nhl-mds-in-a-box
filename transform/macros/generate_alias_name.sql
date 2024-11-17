{% macro generate_alias_name(custom_alias_name=none, node=none) -%}

    {%- if custom_alias_name -%} {{ custom_alias_name | trim }}

    {%- elif node.version -%}

        {{ return(node.name ~ "_v" ~ (node.version | replace(".", "_"))) }}

    {%- else -%}

        {%- set prefix = node.name.split("_", 1)[0] -%}

        {%- if prefix == "seed" -%}

            {{ node.name.split("_", 1)[1] }}

        {%- else -%}

            {{ node.name.split("__")[1] }}

        {%- endif -%}

    {%- endif -%}

{%- endmacro %}
