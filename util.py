from google.cloud import secretmanager


def access_secrets(project_id, secret_id, version_id="latest"):
    """
    Access a secret version in Secret Manager.
    """
    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version.
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    # Access the secret version.
    response = client.access_secret_version(request={"name": name})

    # Return the payload as a string.
    return response.payload.data.decode("UTF-8")