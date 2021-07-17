import re


s = """(vpc-prod-tracker-handler01), i-039cf67f1139546f8 (vpc_prod_vertex10), i-047d8a6e5418699c1 (vpc_prod_vertex23), i-04d58e7ddec3fbfc7 (vpc_prod_vertex06), i-04fda78dd637b50b4 (vpc_prod_vertex14), i-062623a53383168bc (vpc_prod_vertex34), i-06b9956e61442aad2 (vpc_prod_vertex41), i-072673ba8c23fb170 (vpc_prod_vertex43), i-073c6234193c99d69 (vpc_prod_vertex16), i-075fbc3f2b5fab0f6 (vpc_prod_vertex49), i-09a16f2d3b3ab3254 (vpc_prod_vertex08), i-0a6ba325afcb2592d (vpc_prod_vertex31), i-0adfcca4e58e70932 (vpc_prod_vertex09), i-0af123ac8ce08a85e (vpc_prod_vertex11), i-0bbb9b789c0951f02 (vpc_prod_vertex13), i-0d94a26bf063c536d (vpc_prod_vertex40), i-0db5769e2d1f7b818 (vpc-prod-vertex-trackers-api02), i-0e4c77a60760bfd88 (vpc_prod_vertex15), i-0f5b1fb98cb1fae61 (vpc_prod_vertex26), i-0ff5a58aef3168565 (vpc_prod_vertex25), i-4256ac6f (vpc_prod_vertex21), i-30612980 (vpc_staging_spark_01), i-31612981 (vpc_staging_spark_02)"""

m = re.search(r"\([A-Za-z0-90-9_]+)", s)

print m.groups()
for list in m.group():
    print list