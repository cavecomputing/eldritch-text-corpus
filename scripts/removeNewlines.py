from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('sourceFile')
args = parser.parse_args()

textSource = ''
with open(args.sourceFile, 'r', encoding='utf-8') as file:
    textSource = file.read()

    lines = textSource.split('\n')
    lines = [line.rstrip() for line in lines]
    textSource = '\n'.join(lines)

    textSource = textSource.replace('\n\n', '||PARAGRAPH||')
    textSource = textSource.replace('\n', ' ')
    textSource = textSource.replace('||PARAGRAPH||','\n\n')
with open(args.sourceFile, 'w', encoding='utf-8') as file:
    file.write(textSource)
