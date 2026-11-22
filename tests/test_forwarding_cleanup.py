import os
from pathlib import Path
import subprocess
import tempfile
import unittest

import yaml


ACTION = yaml.safe_load((Path(__file__).resolve().parents[1] / "action.yml").read_text())
STEPS = {step["name"]: step for step in ACTION["runs"]["steps"]}


class ForwardingCleanupTest(unittest.TestCase):
    def test_restores_original_value_even_when_enabling_fails(self):
        for initial in ("0", "1"):
            for fail_enable in (False, True):
                with self.subTest(initial=initial, fail_enable=fail_enable), tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    (root / "state").write_text(initial)
                    (root / "sudo").write_text('#!/bin/bash\nexec "$@"\n')
                    (root / "sysctl").write_text(
                        '#!/bin/bash\n'
                        'if [ "$1" = "-n" ]; then cat "$STATE"; exit; fi\n'
                        'value=${2#*=}\n'
                        'printf "%s" "$value" > "$STATE"\n'
                        'if [ "${FAIL_ENABLE:-}" = 1 ]; then exit 1; fi\n'
                    )
                    for name in ("sudo", "sysctl"):
                        (root / name).chmod(0o755)
                    output = root / "output"
                    env = os.environ | {
                        "PATH": f"{root}:{os.environ['PATH']}", "STATE": str(root / "state"),
                        "GITHUB_OUTPUT": str(output), "TMPDIR": tmp,
                        "FAIL_ENABLE": "1" if fail_enable else "",
                        **{key: "test" for key in (
                            "WG_PRIVATE_KEY", "WG_ADDRESS", "WG_DNS", "WG_PEER_PUBLIC_KEY",
                            "WG_PRESHARED_KEY", "WG_ENDPOINT", "WG_ALLOWED_IPS",
                        )},
                    }
                    setup = subprocess.run(["bash", "-e", "-c", STEPS["Setup WireGuard configuration"]["run"]], env=env, capture_output=True, text=True)
                    self.assertEqual(setup.returncode == 0, not fail_enable, setup.stderr)
                    outputs = dict(line.split("=", 1) for line in output.read_text().splitlines())
                    self.assertEqual(outputs["previous-ip-forward"], initial)
                    env.update({
                        "VALIDATION_OUTCOME": "success", "WG_STARTED": "", "SSH_KEY_DIR": "",
                        "SSH_KNOWN_HOST_ENTRY_ADDED": "", "WG_DIR": outputs["wg-dir"],
                        "WG_INTERFACE": outputs["wg-interface"],
                        "PREVIOUS_IP_FORWARD": outputs["previous-ip-forward"], "FAIL_ENABLE": "",
                    })
                    cleanup = subprocess.run(["bash", "-e", "-c", STEPS["Cleanup"]["run"]], env=env, capture_output=True, text=True)
                    self.assertEqual(cleanup.returncode, 0, cleanup.stderr)
                    self.assertEqual((root / "state").read_text(), initial)
                    self.assertFalse(Path(outputs["wg-dir"]).exists())

    def test_setup_does_not_modify_sysctl_configuration(self):
        script = STEPS["Setup WireGuard configuration"]["run"]
        self.assertNotIn("/etc/sysctl.conf", script)
        self.assertNotIn("sysctl -p", script)
        self.assertEqual(STEPS["Cleanup"]["env"]["PREVIOUS_IP_FORWARD"],
                         "${{ steps.setup-wireguard.outputs.previous-ip-forward }}")
