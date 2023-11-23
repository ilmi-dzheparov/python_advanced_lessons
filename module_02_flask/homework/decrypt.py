import sys

data = sys.stdin.read()

def decrypt(text: str) -> None:
    count = 0
    new_text = ''
    while count <= len(text) - 1:
        if text[count] != '.':
            new_text += text[count]
            count += 1
        elif text[count] == '.' and count <= len(text) - 2:
            if text[count+1] != '.':
                count += 1
            elif text[count+1] == '.':
                if count != 0:
                    new_text = new_text[:-1]
                    count += 2
                else:
                    count += 2
    print(new_text)


decrypt(data)



