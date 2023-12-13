import json
import sys

def validate_olog(olog_json):
    try:
        olog = json.loads(olog_json)["Olog"]

        # Validate Types
        if "Types" not in olog:
            raise ValueError("Olog missing 'types'")
        for type in olog["Types"]:
            if "ID" not in type or "Description" not in type:
                raise ValueError("Each type must have 'id' and 'description'")

        # Validate Aspects
        if "Aspects" not in olog:
            raise ValueError("Olog missing 'aspects'")
        aspect_dict = {}
        for aspect in olog["Aspects"]:
            if not all(k in aspect for k in ("ID", "Source", "Target", "Label")):
                raise ValueError("Each aspect must have 'id', 'source', 'target', and 'label'")

            if aspect["Source"] not in [t["ID"] for t in olog["Types"]] or aspect["Target"] not in [t["ID"] for t in olog["Types"]]:
                raise ValueError("Aspect's source and target must be valid types")

            aspect_dict[aspect["ID"]] = aspect

        # Validate Facts (Commutative Diagrams)
        if "facts" in olog:
            for fact in olog["Facts"]:
                if "description" not in fact or "involvedAspects" not in fact or "commutative" not in fact:
                    raise ValueError("Each fact must have 'description', 'involvedAspects', and 'commutative'")
                if not all(a in aspect_dict for a in fact["involvedAspects"]):
                    raise ValueError("Facts must involve valid aspects")

                # Validate if the aspects in the fact form a valid commutative diagram
                if not validate_commutative_diagram(fact, aspect_dict):
                    raise ValueError("Invalid commutative diagram in facts")

        print("Olog validation successful.")

    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format")

def validate_commutative_diagram(fact, aspect_dict):
    # Here, implement logic to check if the involved aspects in the fact form a valid commutative diagram
    # This is a complex task and requires understanding the relationships between the aspects and how they compose
    # A simplified version might just check if aspects have matching target and source types
    for i, aspect_id in enumerate(fact["involvedAspects"][:-1]):
        current_aspect = aspect_dict[aspect_id]
        next_aspect = aspect_dict[fact["involvedAspects"][i+1]]
        if current_aspect["target"] != next_aspect["source"]:
            return False
    return True

if __name__ == '__main__':
    with open(sys.argv[1]) as fp:
        print(validate_olog(fp.read()))
