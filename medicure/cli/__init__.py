from medicure.typer_patch.core import patch_param_type

if True:
    patch_param_type()

from medicure.cli.base import app
from medicure.cli.save import save_collection_info, save_tmdb_info
from medicure.cli.treat import treat_media, treat_subtitle
