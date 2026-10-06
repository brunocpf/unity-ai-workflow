"""Run the isolated native-input fixture. Requires a licensed Editor and graphical session."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_TESTS = {
    "KeyboardAndControllerUseNativeMoveSubmitAndCancel",
    "ModalRestoresFocusAndPendingHandoffsCannotStealIt",
    "ReopenAndReplaceDisposeEachLifetimeOnce",
    "GameplaySubmitDoesNotLeakThroughClosingMenu",
    "CoveredScreensAndNestedModalsCannotReceiveFocus",
    "PointerActivationAndHiddenControlSkippingAreNative",
    "ChildCancelConsumptionAndPersistentRootAreRespected",
    "TeardownFailureStillReleasesAllEntriesAndGate",
    "NativeRepeatStillMovesWhileHeld",
    "DuplicateRouterMutationIsDetected",
}


def validate_results(path):
    root = ET.parse(path).getroot()
    cases = list(root.iter("test-case"))
    names = [case.get("name") for case in cases]
    if (root.get("result") != "Passed" or len(cases) != len(EXPECTED_TESTS)
            or set(names) != EXPECTED_TESTS
            or any(case.get("result") != "Passed" for case in cases)):
        failures = [(case.get("name"), case.get("result"),
                     case.findtext("failure/message", "")[:1500])
                    for case in cases if case.get("result") != "Passed"]
        raise RuntimeError(f"Incomplete/failed native navigation coverage: {failures}; found {names}")
    return len(cases)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--editor", type=Path, required=True, help="Unity executable, not Hub/app directory")
    parser.add_argument("--workspace", type=Path, required=True, help="New disposable directory; must not exist")
    args = parser.parse_args()
    editor = args.editor.resolve(strict=True)
    workspace = args.workspace.resolve()
    workspace.mkdir(parents=True, exist_ok=False)  # Never overwrite a project or reuse old results.
    project = workspace / "project"

    def run(stage, options):
        log = workspace / f"{stage}.log"
        with (workspace / f"{stage}-process.log").open("w", encoding="utf-8") as output:
            result = subprocess.run([str(editor), *options, "-logFile", str(log)],
                                    stdout=output, stderr=subprocess.STDOUT, timeout=600)
        if result.returncode:
            raise RuntimeError(f"{stage} failed ({result.returncode}); see {log}")

    run("create", ["-batchmode", "-nographics", "-quit", "-createProject", str(project)])
    version = (project / "ProjectSettings/ProjectVersion.txt").read_text()
    if "m_EditorVersion: 6000.7.0b3\n" not in version:
        raise RuntimeError("Fixture pins Unity 6000.7.0b3; qualify a separate profile before changing this guard")
    manifest = project / "Packages/manifest.json"
    data = json.loads(manifest.read_text())
    data["dependencies"].update({"com.unity.inputsystem": "6.7.0",
                                 "com.unity.test-framework": "1.9.0"})
    manifest.write_text(json.dumps(data, indent=2) + "\n")
    shutil.copytree(ROOT / "examples/Verification/NavigationPlayMode", project / "Assets/NavigationTests")
    reference = project / "Assets/NavigationReference"
    shutil.copytree(ROOT / "examples/Unity/UI/Navigation", reference)
    (reference / "Navigation.Reference.asmdef").write_text(json.dumps({"name": "Navigation.Reference"}))
    for folder in (reference, project / "Assets/NavigationTests", project / "Assets/NavigationTests/Editor"):
        (folder / "csc.rsp").write_text("-nullable:enable\n-warnaserror+\n")
    run("configure", ["-batchmode", "-nographics", "-quit", "-projectPath", str(project),
                      "-executeMethod", "NavigationSetup.Configure"])
    results = workspace / "results.xml"
    # Default UITK input is not exercised by batchmode in this qualified profile.
    # Do not add -batchmode, -nographics or -quit to this Play Mode invocation.
    run("playmode", ["-projectPath", str(project), "-runTests", "-testPlatform", "PlayMode",
                     "-testResults", str(results)])
    count = validate_results(results)
    shutil.copy2(project / "Packages/packages-lock.json", workspace / "packages-lock.json")
    print(f"PASS: {count} native navigation tests; full evidence: {workspace}")


if __name__ == "__main__":
    main()
