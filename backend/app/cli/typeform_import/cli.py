import click
from flask.cli import with_appcontext

from .importer import import_typeform_form

@click.command("typeform-import")
@click.argument("form_id")
@click.option("--dry-run", is_flag=True, help="Don't commit, just log.")
@click.option("--force",  is_flag=True, help="Import even if schema unchanged.")
@with_appcontext
def import_cmd(form_id, dry_run, force):
    sid = import_typeform_form(form_id, commit=not dry_run, force=force)
    if dry_run:
        click.echo(f"[DRY‑RUN] Would have imported survey {sid}")