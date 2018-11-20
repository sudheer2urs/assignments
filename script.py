import sys

starting_tokens = ['*', '.']
old_line = ''
expand = '+'
collapse = '-'
current_selection = None
section_number = []
output = []
multi_lines = []

def parse_line(line):
    selected_token = ''
    token_count = 0
    for token in starting_tokens:
        if not line.startswith(token):
            continue

        selected_token = token
        for char in line:
            if char != token:
                break

            token_count += 1

    if selected_token:
        line = line.strip(selected_token).strip(' ')
    return selected_token, token_count, line

def get_section(count, section_number):
    if len(section_number) < count:
        section_number.extend([1] * (count - len(section_number)))
    elif len(section_number) > count:
        section_number = section_number[:count]
        section_number[-1] = section_number[-1] + 1
    else:
        section_number[-1] = section_number[-1] + 1

    return '.'.join(map(str, section_number)), section_number

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    if not old_line:
        old_line = line
        continue

    old_token, old_token_count, updated_old_line = parse_line(old_line)
    new_token, new_token_count, updated_new_line = parse_line(line)

    if not new_token:
        multi_lines.append(updated_new_line)
        continue

    if old_token != new_token:
        current_selection = None
        if old_token == '*':
            line_number, section_number = get_section(old_token_count, section_number)
            print('%s %s' % (line_number, updated_old_line))
        elif old_token == '.':
            spaces = ' ' * old_token_count
            print('%s %s %s' % (spaces, collapse, updated_old_line))
    else:
        if old_token == '.':
            if not current_selection or old_token_count < new_token_count:
                current_selection = expand

            if old_token_count == new_token_count:
                current_selection = collapse

            spaces = ' ' * old_token_count
            print('%s %s %s' % (spaces, current_selection, updated_old_line))
        elif old_token == '*':
            line_number, section_number = get_section(old_token_count, section_number)
            print('%s %s' % (line_number, updated_old_line))

    if multi_lines and new_token:
        for multi_line in multi_lines:
            print('%s   %s' % (spaces, multi_line))
        multi_lines = []

    old_line = line

spaces = ' ' * new_token_count
print('%s %s %s' % (spaces, collapse, updated_new_line))
