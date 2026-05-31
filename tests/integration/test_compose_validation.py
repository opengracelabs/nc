import shutil
import subprocess

import pytest


def test_docker_compose_config_validates() -> None:
    docker = shutil.which("docker")
    if docker is None:
        pytest.skip("docker is not installed")

    result = subprocess.run(
        [docker, "compose", "-f", "infrastructure/docker/compose.yml", "config"],
        check=False,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stderr
    assert "discovery-worker:" in result.stdout
    assert "ingestion-worker:" in result.stdout
    assert "preservation-worker:" in result.stdout
