"""
Mapping 
"""
import sys
import argparse
from pathlib import Path

import yaml
from pydantic import ValidationError
from structlog import get_logger

from remote_to_controller.models import MappingDefinition
from remote_to_controller.console import get_user_selection

log = get_logger()


def load_yaml_to_model(filename: Path) -> MappingDefinition:
    """
    Loads a YAML file and parses it into a pydantic model.
    """
    with open(filename, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    try:
        return MappingDefinition.model_validate(data)
    except ValidationError:
        log.exception("Error Parsing Mapping File", filename=filename)
        raise


def build_yaml_selection() -> tuple[list[dict[str, str]], dict[int, MappingDefinition]]:
    """
    Returns list of yaml mapping files with 'id', 'MappingDefinition.name', and 'Filename' columns
    and a dictionary mapping ids to MappingDefinition instances.
    """
    current_file_dir = Path(__file__).parent
    yaml_files = list(current_file_dir.joinpath("mappings").glob("*.yaml"))

    selections = []
    mapping_definitions = {}

    for idx, file in enumerate(yaml_files):
        try:
            mapping_def = load_yaml_to_model(file)
            selections.append(
                {
                    "id": str(idx),
                    "Name": mapping_def.name,
                    "Filename": file.name,
                }
            )
            mapping_definitions[idx] = mapping_def
        except ValidationError:
            log.error(f"Failed to load YAML: {file}")

    return selections, mapping_definitions


def select_mapping_yaml() -> MappingDefinition:
    """
    Select which file to use to map the remote to input events
    """
    (
        yaml_files,
        mapping_definitions,
    ) = build_yaml_selection()

    if not yaml_files:
        print("No YAML files found in mappings directory.")
        sys.exit()

    selected = get_user_selection(yaml_files)

    return mapping_definitions[int(selected["id"])]


def get_mapping(parsed_args: argparse.Namespace):
    """
    Get Mappings from arg or let user select
    """
    if parsed_args.mapping_file:
        return load_yaml_to_model(parsed_args.mapping_file)

    return select_mapping_yaml()
