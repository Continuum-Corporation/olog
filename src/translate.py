import openai
import os
import sys

client = openai.OpenAI(api_key="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")

with open('../res/1102.1889-trunc.tex') as fp:
    OLOG_PAPER = fp.read()
with open('../res/form.txt') as fp:
    OLOG_FORM = fp.read()
with open('../res/instruction.txt') as fp:
    INSTRUCTION = fp.read()
with open('../res/struct.txt') as fp:
    OLOG_STRUCT = fp.read()


def ologify(content):
    response = client.chat.completions.create(
      model="gpt-4-1106-preview",
      response_format={ "type": "json_object" },
      messages=[
          {"role": "system", "content": f"## OLOG RESEARCH WHITEPAPER {OLOG_PAPER} ## OLOG ESSENTIAL FORM {OLOG_FORM} You are a document processing system which takes documents in and outputs a valid olog represented as JSON. Instructions follow: {INSTRUCTION} Take the document or input provided and render it as an olog respecting the best practices as best you can. You must ensure that all types are valid types as defined in the paper, and that all aspects are valid aspects, and that the categorical structure of the olog is coherent. {OLOG_STRUCT} ALWAYS Conform to the olog JSON structure provided above this is absolutely essential."},
          {"role": "user", "content": 'Please create an olog of this text: ' + content}
      ]
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
