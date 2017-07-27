import os
import json

def generate_virt_builder_repo_metadata(repo_dir, images):
    """
    Generates the index metadata file for this repo, as needed to be used
    by the virt-builder client

    Args:
        repo_dir (str): Repo to generate the metadata file for
        specs (list of str): Spec files to generate the metadata for
        uncompressed_infos (dict of str: UncompressedTplInfo): uncompressed
            images info

    Returns:
        None
    """
    images_metadata = []

    for image in images:
        images_metadata.append(image.get_libguestfs_metadata())

    with open(os.path.join(repo_dir, 'index'), 'w') as fd:
        fd.write('\n\n'.join(images_metadata) + '\n')


def generate_lago_repo_metadata(repo_dir, repo_name, url):
    """
    Generates the json metadata file for this repo, as needed to be used by the
    lago clients

    Args:
        repo_dir (str): Repo to generate the metadata file for
        name (str): Name of this repo
        url (str): External URL for this repo

    Returns:
        None
    """
    templates = {}
    metadata = {
        'name': repo_name,
        'templates': templates,
    }
    _, _, files = os.walk(repo_dir).next()
    for file_name in files:
        if not file_name.endswith('.xz'):
            continue
        name = file_name.rsplit('.', 1)[0]
        templates[name] = {
            "versions": {
                "latest": {
                    "source": repo_name,
                    "handle": file_name.rsplit('.', 1)[0],
                    "timestamp": os.stat(
                        os.path.join(repo_dir, file_name)
                    ).st_mtime,
                },
            },
        }

    metadata['sources'] = {
        repo_name: {
            "args": {
                "baseurl": url,
            },
            "type": "http"
        }
    }

    with open(os.path.join(repo_dir, 'repo.metadata'), 'w') as fd:
        fd.write(json.dumps(metadata))

