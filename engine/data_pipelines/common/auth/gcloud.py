"""Gcloud auth module."""

import subprocess

from engine.data_pipelines.common.logging import LOGGER


def get_auth_token() -> str:
    """Retrieve a Google Cloud SDK authentication token.

    Returns: Authentication token.

    Raises:
      subprocess.CalledProcessError: If authentication fails.

    """
    try:
        result = subprocess.run(
            args=["gcloud", "auth", "application-default", "print-access-token"],
            text=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        token = result.stdout.strip()

        if token:
            LOGGER.info("Successfully authenticated with Google Cloud SDK.")
            return token
        else:
            LOGGER.error("No token returned during authentication.")
            raise subprocess.CalledProcessError(returncode=1, cmd=result.args, stderr="No token returned")

    except subprocess.CalledProcessError as e:
        msgs = e.stderr.split("\n")
        for msg in msgs:
            if "WARNING" in msg:
                LOGGER.warning(msg)
            else:
                LOGGER.error(msg)
        raise


def am_i_authenticated() -> bool:
    """Check if the user is authenticated with Google Cloud SDK.

    Returns: True if this functions' runner is authentified to gcloud, False otherwise.
    """
    try:
        return bool(get_auth_token())
    except Exception:
        LOGGER.info("User is not authenticated with Google Cloud SDK.")
        return False
