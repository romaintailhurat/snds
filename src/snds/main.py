import httpx
import pprint

#resp = httpx.get("https://gitlab.com/healthdatahub/applications-du-hdh/schema-snds/-/raw/master/schemas/DCIR/ER_ANO_F.json?ref_type=heads")

#print(resp.status_code)

resp_tree = httpx.get("https://gitlab.com/api/v4/projects/11935694/repository/tree?path=schemas")

schemas_sub_dirs = [o["path"] for o in resp_tree.json()]

print(schemas_sub_dirs)
