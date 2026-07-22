from __future__ import annotations

import json
from typing import Annotated

import typer

from src.cli.app import CLIApp

app = typer.Typer(
    help="Semantic Search RAG CLI",
    no_args_is_help=True,
)

cli = CLIApp()


@app.command()
def version() -> None:
    """Display the CLI version."""
    typer.echo(cli.version())


@app.command()
def query(
    question: Annotated[
        str,
        typer.Argument(help="Question to ask the RAG system."),
    ],
    top_k: Annotated[
        int,
        typer.Option(
            "--top-k",
            "-k",
            min=1,
            help="Number of retrieved documents.",
        ),
    ] = 5,
    json_output: Annotated[
        bool,
        typer.Option(
            "--json",
            help="Output results as JSON.",
        ),
    ] = False,
) -> None:
    """Query the RAG system."""
    try:
        result = cli.query(question=question, top_k=top_k)

        if json_output:
            typer.echo(json.dumps(result, indent=2, ensure_ascii=False))
            raise typer.Exit()

        typer.echo(f"\nQUESTION\n{'=' * 72}")
        typer.echo(result["question"])

        typer.echo(f"\nANSWER\n{'=' * 72}")
        typer.echo(result["answer"])

        typer.echo(f"\nSOURCES ({len(result['sources'])})\n{'=' * 72}")

        if not result["sources"]:
            typer.echo("No sources found.")
            raise typer.Exit()

        for source in result["sources"]:
            typer.echo(
                f"- document={source.get('document_id')} "
                f"page={source.get('page_number')} "
                f"chunk={source.get('chunk_index')} "
                f"score={source.get('score'):.4f}"
                if source.get("score") is not None
                else (
                    f"- document={source.get('document_id')} "
                    f"page={source.get('page_number')} "
                    f"chunk={source.get('chunk_index')}"
                )
            )

    except Exception as exc:
        typer.secho(f"Error: {exc}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)


@app.command()
def ingest(
    source_path: Annotated[
        str,
        typer.Option(
            "--path",
            "-p",
            help="Directory containing source documents.",
        ),
    ] = "data/raw",
    json_output: Annotated[
        bool,
        typer.Option(
            "--json",
            help="Output results as JSON.",
        ),
    ] = False,
) -> None:
    """Ingest documents into the knowledge base."""
    try:
        result = cli.ingest(source_path=source_path)

        if json_output:
            typer.echo(json.dumps(result, indent=2, ensure_ascii=False))
            raise typer.Exit()

        typer.echo("\nINGEST SUMMARY")
        typer.echo("=" * 72)
        typer.echo(f"Status           : {result['status']}")
        typer.echo(f"Files Ingested   : {result['files_ingested']}")
        typer.echo(f"Files Skipped    : {result['files_skipped']}")

    except Exception as exc:
        typer.secho(f"Error: {exc}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
