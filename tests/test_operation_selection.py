import os
from pathlib import Path
import re
import subprocess
import unittest

import yaml


ACTION = yaml.safe_load((Path(__file__).resolve().parents[1] / "action.yml").read_text())
STEPS = {step["name"]: step for step in ACTION["runs"]["steps"]}


class OperationSelectionTest(unittest.TestCase):
    def validate(self, operation, direction, source="file", destination="file"):
        env = os.environ | {
            "OPERATION": operation,
            "SCP_DIRECTION": direction,
            "SCP_SOURCE": source,
            "SCP_DESTINATION": destination,
            "SSH_PORT": "22",
            "SSH_HOSTNAME": "host",
            "SSH_USER": "user",
            "SSH_HOST_IP": "192.0.2.1",
        }
        return subprocess.run(
            ["bash", "-e", "-c", STEPS["Validate inputs"]["run"]],
            env=env, capture_output=True, text=True, check=False,
        )

    def test_valid_inputs_select_one_work_step(self):
        work_steps = ["Execute SSH command", "SCP Upload (Local to Remote)", "SCP Download (Remote to Local)"]
        for operation, direction, expected in [
            ("ssh", "upload", work_steps[0]),
            ("ssh", "ignored", work_steps[0]),
            ("scp", "upload", work_steps[1]),
            ("scp", "download", work_steps[2]),
        ]:
            with self.subTest(operation=operation, direction=direction):
                self.assertEqual(self.validate(operation, direction).returncode, 0)
                selected = []
                for name in work_steps:
                    condition = STEPS[name]["if"]
                    terms = re.fullmatch(r"\$\{\{\s*(.*?)\s*\}\}", condition).group(1).split(" && ")
                    matches = []
                    for term in terms:
                        match = re.fullmatch(r"inputs\.(operation|scp-direction) == '([^']+)'", term)
                        self.assertIsNotNone(match, term)
                        value = {"operation": operation, "scp-direction": direction}[match.group(1)]
                        matches.append(value.lower() == match.group(2).lower())
                    if all(matches):
                        selected.append(name)
                self.assertEqual(selected, [expected])

    def test_invalid_inputs_fail_validation(self):
        for operation, direction, source, destination in [
            ("sftp", "upload", "file", "file"),
            ("SSH", "upload", "file", "file"),
            ("scp", "uplod", "file", "file"),
            ("scp", "UPLOAD", "file", "file"),
            ("scp", "upload", "", "file"),
            ("scp", "download", "file", ""),
        ]:
            with self.subTest(operation=operation, direction=direction, source=source, destination=destination):
                self.assertNotEqual(self.validate(operation, direction, source, destination).returncode, 0)

    def test_failed_validation_skips_cleanup_commands(self):
        self.assertEqual(ACTION["runs"]["steps"][0]["id"], "validate-inputs")
        cleanup = STEPS["Cleanup"]
        self.assertEqual(cleanup["if"], "always()")
        self.assertEqual(cleanup["env"]["VALIDATION_OUTCOME"], "${{ steps.validate-inputs.outcome }}")
        result = subprocess.run(
            ["/bin/bash", "-eu", "-c", cleanup["run"]],
            env=os.environ | {"VALIDATION_OUTCOME": "failure", "PATH": ""},
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
