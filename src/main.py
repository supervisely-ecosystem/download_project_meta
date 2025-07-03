import os
import json

import supervisely as sly
from dotenv import load_dotenv

TMP_DIR = os.path.join(os.getcwd(), "tmp")
os.makedirs(TMP_DIR, exist_ok=True)

if sly.is_development():
    load_dotenv("local.env")

team_id = sly.env.team_id()
workspace_id = sly.env.workspace_id()
project_id = sly.env.project_id()

sly.logger.info(f"Team ID: {team_id}, Workspace ID: {workspace_id}, Project ID: {project_id}")

api = sly.Api.from_env()

# Download project meta and save it to a file.
project_meta_json = api.project.get_meta(project_id, with_settings=True)
sly.logger.info("Project meta downloaded successfully.")
save_path = os.path.join(TMP_DIR, "meta.json")

with open(save_path, "w") as f:
    json.dump(project_meta_json, f, indent=4)
sly.logger.info(f"Project meta saved to {save_path}")

# Upload the project meta to the Files.
file_info = sly.output.set_download(save_path)
if file_info:
    # Show the remote path in logs.
    sly.logger.info(f"Project meta uploaded to Files: {file_info.path}")
