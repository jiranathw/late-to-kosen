import re

with open('Assembly-CSharp.csproj', 'r', encoding='utf-8') as f:
    text = f.read()

text = re.sub(r'\s*<Compile Include="Assets[\\/]Scripts[\\/]BicyclePickup\.cs" />', '', text)

with open('Assembly-CSharp.csproj', 'w', encoding='utf-8') as f:
    f.write(text)

print('Successfully cleaned up Assembly-CSharp.csproj')
