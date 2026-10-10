from pathlib import Path
import zipfile


def main():
    root = Path(__file__).resolve().parent.parent
    source = root / "src"
    mesh_path = Path("Meshes/heathaze/heathaze_cylinder.nif")
    mesh = source / mesh_path
    if not mesh.is_file():
        raise FileNotFoundError(f"Missing mesh: {mesh}")
    output = root / "dist" / "HeatHaze-ESPless.zip"
    output.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(source.rglob("*")):
            if not path.is_file():
                continue
            relative = path.relative_to(source)
            if relative.parts[0] == "Meshes" and relative != mesh_path:
                continue
            archive.write(path, relative.as_posix())
    print(f"Built {output} (mesh: {mesh.name})")


if __name__ == "__main__":
    main()
