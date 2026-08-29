import os

csproj_path = 'Assembly-CSharp.csproj'
with open(csproj_path, 'r', encoding='utf-8') as f:
    content = f.read()

all_cs = []
for root, dirs, files in os.walk('Assets'):
    for file in files:
        if file.endswith('.cs'):
            rel = os.path.join(root, file).replace('/', '\\').replace('&', '&amp;')
            all_cs.append(rel)

start_pos = content.find('<Compile Include=')
if start_pos != -1:
    group_start = content.rfind('<ItemGroup>', 0, start_pos)
    group_end = content.find('</ItemGroup>', start_pos) + len('</ItemGroup>')
    
    items = '\n'.join(f'    <Compile Include="{cs}" />' for cs in sorted(all_cs))
    new_group = f'<ItemGroup>\n{items}\n  </ItemGroup>'
    
    new_content = content[:group_start] + new_group + content[group_end:]
    with open(csproj_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f'Successfully updated Assembly-CSharp.csproj with {len(all_cs)} files!')
