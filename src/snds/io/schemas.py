import httpx
import pprint

GITLAB_BASE_REPO_URL = "https://gitlab.com/api/v4/projects/11935694/repository/"
GITLAB_BASE_REPO_FILES_URL = "https://gitlab.com/healthdatahub/applications-du-hdh/schema-snds/-/raw/master/schemas/"


def get_schemas_list() -> list[str]:
    """ Get the list of schemas paths on the Gitlab repo """
    # resp = httpx.get("https://gitlab.com/healthdatahub/applications-du-hdh/schema-snds/-/raw/master/schemas/DCIR/ER_ANO_F.json?ref_type=heads")
    # print(resp.status_code)

    resp_tree = httpx.get(
        "https://gitlab.com/api/v4/projects/11935694/repository/tree?path=schemas"
    )

    schemas_sub_dirs = [o["path"] for o in resp_tree.json()]

    all_schemas_path = []

    for sub_dir in schemas_sub_dirs:
        # TODO filter on sub_dir if we dont want everything
        resp_sub_dir = httpx.get(f"https://gitlab.com/api/v4/projects/11935694/repository/tree?path={sub_dir}")
        paths = [o["path"] for o in resp_sub_dir.json()]
        all_schemas_path = all_schemas_path + paths

    return all_schemas_path[0:10]
