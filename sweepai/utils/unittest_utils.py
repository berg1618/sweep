from dataclasses import dataclass

from black import FileMode, format_str


@dataclass
class DecomposedScript:
    imports: str
    definitions: str
    main: str


def split_script(script: str):
    import_section = []
    class_section = []
    main_section = []
    current_section = import_section

    for line in script.split("\n"):
        if line.startswith("import"):
            current_section = import_section
        elif line.startswith("class") or line.startswith("def"):
            current_section = class_section
        elif line.startswith("if __name__"):
            current_section = main_section
        current_section.append(line)

    return DecomposedScript(
        imports="\n".join(import_section),
        definitions="\n".join(class_section),
        main="\n".join(main_section),
    )

def remove_duplicates(seq):
    seen = set()
    return [x for x in seq if not (x in seen or seen.add(x))]


def fuse_scripts(
    sections: list[str], do_remove_main: bool = True, do_format: bool = True
):
    decomposed_scripts = [split_script(section) for section in sections]
    imports = remove_duplicates([script.imports for script in decomposed_scripts])
    definitions = remove_duplicates([script.definitions for script in decomposed_scripts])
    main = remove_duplicates([script.main for script in decomposed_scripts])
    result = "\n\n".join(
        [
            "\n".join(imports),
            "\n".join(definitions),
            "\n".join(main)
            if not do_remove_main
            else "",
        ]
    )

    if do_format:
        result = format_str(result, mode=FileMode())

    return result


script_content_1 = """
import a
import b

class Foo:
    pass

if __name__ == '__main__':
    pass
"""

script_content_2 = """
import b
import d

def bar():
    pass

if __name__ == '__main__':
    pass
"""

if __name__ == "__main__":
    # Example usage:
    fused_script = fuse_scripts([script_content_2, script_content_2])
    print(fused_script)
