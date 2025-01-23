import sysconfig
import json
import numpy
from pathlib import Path


def generate_vscode_config():
    python_include = sysconfig.get_path("include")
    numpy_include = numpy.get_include()

    config = {
        "configurations": [
            {
                "name": "Mac",
                "includePath": [
                    python_include,
                    numpy_include,
                    "${workspaceFolder}/**"
                ],
                "macFrameworkPath": [
                    "/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/System/Library/Frameworks"
                ],
                "defines": [],
                "compilerPath": "/usr/bin/clang",
                "cStandard": "c17",
                "cppStandard": "c++17",
                "intelliSenseMode": "macos-clang-arm64"
            },
        ],
        "version": 4
    }

    vscode_folder = Path.cwd() / ".vscode"
    vscode_folder.mkdir(exist_ok=True)

    config_path = Path(vscode_folder / "c_cpp_properties.json")
    with open(config_path, "w") as f:
        json.dump(config, f, indent=4)

    print(f"Configuration written to {config_path}")


if __name__ == "__main__":
    generate_vscode_config()
