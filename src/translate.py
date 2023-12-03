import json
import openai
import os
import sys

client = openai.OpenAI(api_key="")

def get_resource(name):
    if '.' not in name:
        name += '.txt'
    with open(f'../res/{name}') as fp:
        return fp.read()

def extract_facts(content):
    prompt = get_resource('fact')
    prompt += 'Extract a list of facts from the provided text or code. Return them as a simple json object: {"facts": [...]} where each element of the array is simply a string representing a fact'
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        response_format={ "type": "json_object" },
        messages=[
              {"role": "system", "content": prompt},
              {"role": "user", "content": content}
        ],
    )
    out = response.choices[0].message.content
    return json.loads(out)['facts']

def generate_types(content):
    prompt = ""
    subprompts = ['intro', 'general', 'types-ex']
    for p in subprompts:
        s = get_resource(p)
        prompt += ' ' + s

    prompt += 'Generate a list of types contained within the provided information adhering to the principles given above. Return the types as a simple json object: {"types": [...]} where each element of the array is a string representing a type. Ensure you do not include as types what should really be later included as instances; adhere to the type/instance distinction carefully, representing only the highest-level conceptual categories necessary. Do not duplicate types'
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        response_format={ "type": "json_object" },
        messages=[
              {"role": "system", "content": prompt},
              {"role": "user", "content": content}
        ],
    )
    out = response.choices[0].message.content
    return json.loads(out)['types']

# def generate_aspects(content, types):
#     prompt = ""
#     subprompts = ['intro', 'general', 'aspects-ex', 'commute']
#     for p in subprompts:
#         s = get_resource(p)
#         prompt += ' ' + s
# 
#     prompt += 'Generate a list of aspects contained within the provided information connecting the EXTRACTED TYPES and adhering to the principles given above. Return the aspects as a simple json object: {"aspects": [...]} where each element of the array is a string representing an aspect. return only the aspects i.e. the part represented in the [[ ]] - exclude the types. (we will build a full olog of these components later) Do not duplicate aspects.'
#     content += 'EXTRACTED TYPES =\n'
#     content += '\n'.join(types)
# 
#     response = client.chat.completions.create(
#         model="gpt-4-1106-preview",
#         response_format={ "type": "json_object" },
#         messages=[
#               {"role": "system", "content": prompt},
#               {"role": "user", "content": content}
#         ],
#     )
#     out = response.choices[0].message.content
#     return json.loads(out)['aspects']

def build_olog(content, types):
    prompt = ""
    subprompts = ['intro', 'general', 'commute', 'aspects-ex', 'schema']
    for p in subprompts:
        s = get_resource(p)
        prompt += ' ' + s

    prompt += 'You will be provided with some INFORMATION as well as a list of TYPES that have been pre-identified. Your goal is to use the provided TYPES (using ALL of them and NONE that are NOT included in the provided ones) to construct an olog representing the INFORMATION. This is a sort of "final assembly" step applying structure to the precalculated TYPES. Aim to represent ALL meaningful relationships between the provided TYPES reflected in the INFORMATION. DO NOT leave any types disconnected. Generate ALL meaningful connections to ensure maximal connectivity; this includes connections not explicitly specified in the INFORMATION (i.e., those left implicit). Aim to adhere to structural properties of transitivity, associativity, and commutativity. ALWAYS Adhere to the provided schema.'
    content = 'INFORMATION =\n' + content
    content += '\nTYPES =\n' + '\n'.join(types)
    # content += '\nASPECTS =\n' + '\n'.join(aspects)

    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        response_format={ "type": "json_object" },
        messages=[
              {"role": "system", "content": prompt},
              {"role": "user", "content": content}
        ],
    )
    out = response.choices[0].message.content
    return json.loads(out)

def ologify(content, pull_facts=False):
    prompt = ""
    subprompts = ['intro', 'general', 'types-ex', 'aspects-ex', 'commute', 'schema']
    for p in subprompts:
        s = get_resource(p)
        prompt += ' ' + s

    prompt += ' You are a text processing system which takes text in and outputs a valid olog represented as JSON. Follow all instructions and ensure valid types and aspects. Aim to represent ALL meaningful connections both explicit and implicit in the provided source information. Produce maximal meaningful connectivity within the generated olog. Adhere to categorical principles of structural coherence (transitivity, associativity, etc). Realize that INSTANCES cannot be connected to TYPES via ASPECTS. ALWAYS conform to the provided JSON schema. Generate an olog of the provided information.'

    print(prompt)
    print('----------------------------')

    if pull_facts:
        facts = extract_facts(content)
        content = '\n'.join(facts)

    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        response_format={ "type": "json_object" },
        messages=[
              {"role": "system", "content": prompt},
              {"role": "user", "content": content}
        ],
    )
    out = response.choices[0].message.content
    return out


if __name__ == '__main__':
    content = None
    try:
        content = sys.argv[1]
        if os.path.exists(sys.argv[1]):
            with open(content) as fp:
                content = fp.read()
    except IndexError:
        print('need to specify a target!')
        exit(-1)
    except:
        print('failed opening argument file')
        exit(-1)

    print(f'ologifying CONTENT[{content[:42]}...]')
    out = ologify(content)
    with open('olog-out.json', 'w') as fp:
        fp.write(out)
