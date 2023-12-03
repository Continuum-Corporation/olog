import sys
import json

def generate_mermaid_diagram(olog_json):
    """
    Generates a Mermaid JS diagram from an olog JSON schema.

    Parameters:
    olog_json (dict): The olog JSON schema.

    Returns:
    str: Mermaid JS diagram script.
    """
    mermaid_script = "graph TD\n"
    
    # Process types
    for type_item in olog_json["Olog"]["Types"]:
        type_id = type_item["ID"]
        type_name = type_item["Name"]
        mermaid_script += f"    {type_id}[\"{type_name}\"]\n"

    # Process aspects
    for aspect in olog_json["Olog"]["Aspects"]:
        aspect_id = aspect["ID"]
        aspect_label = aspect["Label"]
        source = aspect["Source"]
        target = aspect["Target"]
        mermaid_script += f"    {source} -->|{aspect_label}| {target}\n"

    return mermaid_script

if __name__ == '__main__':
    with open(sys.argv[1]) as fp:
        olog = json.load(fp)

    mmd = generate_mermaid_diagram(olog)
    print(mmd)
