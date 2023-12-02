import openai
import os
import sys

client = openai.OpenAI(api_key="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")

def get_resource(name):
    if '.' not in name:
        name += '.txt'
    with open(f'../res/{name}') as fp:
        return fp.read()

def ologify(content):
    prompt = ""
    subprompts = ['intro', 'general', 'instruction', 'types-ex', 'aspects-ex', 'schema']
    for p in subprompts:
        s = get_resource(p)
        prompt += ' ' + s

    prompt += ' You are a text processing system which takes text in and outputs a valid olog represented as JSON. Follow all instructions and ensure valid types and aspects. ALWAYS conform to the provided JSON schema.'

    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        response_format={ "type": "json_object" },
        messages=[
              {"role": "system", "content": prompt},
              {"role": "user", "content": 'Please create an olog of this text: ' + content}
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
