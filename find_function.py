with open('src/metaexpert/cli/argument_parser.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        if 'def validate_new_command_args' in line:
            start = i
            break
    
    print('Start line:', start+1)
    for i in range(start, min(start+15, len(lines))):
        print(f'{i+1}: {lines[i].rstrip()}')