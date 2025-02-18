words = []
with open('american-english') as f:
    
    words = [line.upper() for line in f.readlines() if '\'' not in line]

with open('clean-words', 'w+') as f:
    f.writelines(words)