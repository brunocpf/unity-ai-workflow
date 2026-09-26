#!/usr/bin/env python3
"""Regression probes for the syntax checker; run after adopting/restoring tooling."""
from pathlib import Path
import json
import subprocess
import tempfile


def main():
    quality = Path(__file__).resolve().parent
    root = quality.parents[1]
    project = quality / 'CodeOrganization/CodeOrganization.csproj'
    subprocess.run(['dotnet', 'build', str(project), '--configuration', 'Release', '--no-restore'],
                   cwd=root, check=True)
    checker = project.parent / 'bin/Release/net10.0/CodeOrganization.dll'
    good = '''namespace Example
{
    public sealed class Widget
    {
        public int Value { get; }

        private sealed class Helper { }
    }
}
'''
    cases = [
        ('nested helper', 'Widget.cs', good, None),
        ('partial', 'Widget.Part.cs', good.replace('sealed class', 'sealed partial class'), None),
        ('file scoped', 'Widget.cs', 'namespace Example;\npublic class Widget {}\n', None),
        ('delegate', 'Signal.cs', 'public delegate void Signal();\n', None),
        ('trivia', 'Widget.cs', good.replace('public int Value { get; }',
            '// class Hidden {}\n        public string Value => "{ class Fake {}; one; two; }";'), None),
        ('extra type', 'Widget.cs', good + 'public interface IExtra {}\n', 'ORG001'),
        ('filename', 'Wrong.cs', good, 'ORG002'),
        ('statements', 'Widget.cs', 'public class Widget\n{\n    public Widget() { int x = 0; x++; }\n}\n', 'ORG003'),
        ('member spacing', 'Widget.cs', 'public class Widget\n{\n    public void A() {}\n    public void B() {}\n}\n', 'ORG004'),
        ('compact members', 'Widget.cs', 'public class Widget\n{\n    public int A { get; } public int B { get; }\n}\n', 'ORG004'),
        ('configuration', 'Widget.cs', 'public class Widget\n{\n    public object A() => new Thing { X = 1, Y = 2 };\n}\n', 'ORG005'),
        ('parameters', 'Widget.cs', 'public class Widget\n{\n    public Widget(string veryLongArgumentNameOne, string veryLongArgumentNameTwo, string veryLongArgumentNameThree, string veryLongArgumentNameFour) {}\n}\n', 'ORG005'),
        ('syntax', 'Widget.cs', 'public class Widget {', 'error CS'),
    ]
    with tempfile.TemporaryDirectory(prefix='organization-probes-') as directory:
        scratch = Path(directory)
        file_list = scratch / 'files.json'
        for name, filename, source, diagnostic in cases:
            file = scratch / filename
            file.write_text(source)
            file_list.write_text(json.dumps([str(file)]))
            result = subprocess.run(['dotnet', str(checker), str(file_list)], cwd=root,
                                    capture_output=True, text=True)
            output = result.stdout + result.stderr
            expected = 1 if diagnostic else 0
            if result.returncode != expected or diagnostic and diagnostic not in output:
                raise RuntimeError(f'{name}: expected {diagnostic or "clean"}; got {output}')
        file_list.write_text('[]')
        result = subprocess.run(['dotnet', str(checker), str(file_list)], cwd=root,
                                capture_output=True, text=True)
        if result.returncode != 2 or 'No source files' not in result.stderr:
            raise RuntimeError('Empty selection must be rejected.')
    print(f'PASS: {len(cases) + 1} organization probes. Semantic/IDE acceptance remains separate.')


if __name__ == '__main__':
    main()
