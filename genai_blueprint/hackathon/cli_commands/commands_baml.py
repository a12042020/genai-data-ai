"""BAML-based version of structured extraction CLI commands.

This module provides an alternative implementation of the structured_extract function
that uses BAML instead of langchain for structured output extraction. It leverages
the BAML-generated client to extract structured data from markdown files into any
Pydantic BaseModel provided at runtime.

Key Features:
    - Uses BAML's ExtractRainbow function for structured data extraction
    - Maintains the same CLI interface as the original version
    - Compatible with existing KV store and batch processing infrastructure
    - Supports any Pydantic BaseModel (validated at runtime)

Usage Examples:
    ```bash
    # Extract structured data from Markdown files using BAML
    uv run cli structured-extract-baml "*.md" --class ReviewedOpportunity --force

    # Process recursively with custom settings
    uv run cli structured-extract-baml ./reviews/ --recursive --batch-size 10 --force --class ReviewedOpportunity
    ```

Data Flow:
    1. Markdown files → BAML ExtractRainbow → model instances
    2. Model instances → KV Store → JSON structured data
    3. Processed data → Available for EKG agent querying
"""

import asyncio
import time
from pathlib import Path
from typing import Annotated, Generic, Type, TypeVar

import typer
from loguru import logger
from pydantic import BaseModel
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn, MofNCompleteColumn
from rich.status import Status
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
from upath import UPath

import genai_blueprint.hackathon.baml_client.types as baml_types
from genai_blueprint.hackathon.baml_client.async_client import b as baml_async_client

LLM_ID = None
KV_STORE_ID = "file"

console = Console()

class ProcessingStats:
    """Track processing statistics for Rich display."""
    
    def __init__(self) -> None:
        self.start_time = time.time()
        self.files_discovered = 0
        self.files_processed = 0
        self.cache_hits = 0
        self.errors = 0
        self.error_details: list[dict[str, str]] = []
        
    def add_error(self, file_name: str, error: str) -> None:
        """Add an error to the stats."""
        self.errors += 1
        self.error_details.append({"file": file_name, "error": error})
    
    def get_elapsed_time(self) -> float:
        """Get elapsed time since start."""
        return time.time() - self.start_time
    
    def create_summary_table(self) -> Table:
        """Create a summary table of processing stats."""
        table = Table(title="Processing Summary", show_header=True, header_style="bold magenta")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", justify="right", style="green")
        
        table.add_row("Files Discovered", str(self.files_discovered))
        table.add_row("Files Processed", str(self.files_processed))
        table.add_row("Cache Hits", str(self.cache_hits))
        table.add_row("Errors", str(self.errors), style="red" if self.errors > 0 else "green")
        table.add_row("Total Time", f"{self.get_elapsed_time():.2f}s")
        
        if self.files_processed > 0:
            avg_time = self.get_elapsed_time() / self.files_processed
            table.add_row("Avg Time/File", f"{avg_time:.2f}s")
        
        return table
    
    def create_error_table(self) -> Table | None:
        """Create an error details table if there are errors."""
        if not self.error_details:
            return None
            
        table = Table(title="Error Details", show_header=True, header_style="bold red")
        table.add_column("File", style="cyan")
        table.add_column("Error", style="red")
        
        for error in self.error_details[-10:]:  # Show last 10 errors
            table.add_row(error["file"], error["error"])
            
        if len(self.error_details) > 10:
            table.add_row("...", f"and {len(self.error_details) - 10} more errors")
            
        return table


T = TypeVar("T", bound=BaseModel)


class BamlStructuredProcessor(Generic[T]):
    """Processor that uses BAML for extracting structured data from documents."""

    def __init__(self, model_cls: Type[T], kvstore_id: str | None = None, force: bool = False) -> None:
        self.model_cls = model_cls
        self.kvstore_id = kvstore_id or KV_STORE_ID
        self.force = force
        self.stats = ProcessingStats()

    async def abatch_analyze_documents(self, document_ids: list[str], markdown_contents: list[str]) -> list[T]:
        """Process multiple documents asynchronously with caching using BAML."""
        from genai_tk.utils.pydantic.kv_store import PydanticStore, save_object_to_kvstore

        analyzed_docs: list[T] = []
        remaining_ids: list[str] = []
        remaining_contents: list[str] = []

        # Check cache first (unless force is enabled)
        if self.kvstore_id and not self.force:
            with console.status("[yellow]Checking cache..."):
                for doc_id, content in zip(document_ids, markdown_contents, strict=True):
                    cached_doc = PydanticStore(kvstore_id=self.kvstore_id, model=self.model_cls).load_object(doc_id)

                    if cached_doc:
                        analyzed_docs.append(cached_doc)
                        self.stats.cache_hits += 1
                        console.print(f"[green]✓[/green] Loaded cached: [cyan]{doc_id}[/cyan]")
                    else:
                        remaining_ids.append(doc_id)
                        remaining_contents.append(content)
        else:
            remaining_ids = document_ids
            remaining_contents = markdown_contents

        if not remaining_ids:
            return analyzed_docs

        # Process uncached documents using BAML concurrent calls pattern
        console.print(f"[yellow]Processing {len(remaining_ids)} documents with BAML async client...[/yellow]")

        # Create concurrent tasks for all remaining documents
        tasks = [baml_async_client.ExtractFromDocument(content) for content in remaining_contents]

        # Execute all tasks concurrently with progress tracking
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            MofNCompleteColumn(),
            TimeElapsedColumn(),
            console=console
        ) as progress:
            task_id = progress.add_task("Processing documents", total=len(tasks))
            
            # Execute tasks and update progress
            results = []
            for i, task in enumerate(asyncio.as_completed(tasks)):
                try:
                    result = await task
                    results.append(result)
                    progress.update(task_id, advance=1, description=f"Processing documents ({i+1}/{len(tasks)})")
                except Exception as e:
                    results.append(e)
                    progress.update(task_id, advance=1, description=f"Processing documents ({i+1}/{len(tasks)}) [red]- errors occurred[/red]")

        # Process results and save to KV store
        for doc_id, result in zip(remaining_ids, results, strict=True):
            if isinstance(result, Exception):
                error_msg = str(result)
                self.stats.add_error(doc_id, error_msg)
                console.print(f"[red]✗[/red] Failed to process [cyan]{doc_id}[/cyan]: {error_msg}")
                continue

            try:
                # Add document_id as a custom attribute
                result_dict = result.model_dump()
                result_dict["document_id"] = doc_id
                result_with_id = self.model_cls(**result_dict)

                analyzed_docs.append(result_with_id)
                self.stats.files_processed += 1
                console.print(f"[green]✓[/green] Processed: [cyan]{doc_id}[/cyan]")

                # Save to KV store
                if self.kvstore_id:
                    save_object_to_kvstore(doc_id, result_with_id, kv_store_id=self.kvstore_id)

            except Exception as e:
                error_msg = str(e)
                self.stats.add_error(doc_id, error_msg)
                console.print(f"[red]✗[/red] Failed to save [cyan]{doc_id}[/cyan]: {error_msg}")

        return analyzed_docs

    def analyze_document(self, document_id: str, markdown: str) -> T:
        """Analyze a single document synchronously using BAML."""
        try:
            results = asyncio.run(self.abatch_analyze_documents([document_id], [markdown]))
        except RuntimeError:
            # If we're in an async context, try nest_asyncio
            try:
                import nest_asyncio

                nest_asyncio.apply()
                loop = asyncio.get_running_loop()
                results = loop.run_until_complete(self.abatch_analyze_documents([document_id], [markdown]))
            except Exception as e:
                raise ValueError(f"Failed to process document {document_id}: {e}") from e

        if results:
            return results[0]
        else:
            raise ValueError(f"Failed to process document: {document_id}")

    async def process_files(self, md_files: list[UPath], batch_size: int = 5) -> None:
        """Process markdown files in batches using BAML."""
        document_ids = []
        markdown_contents = []
        valid_files = []

        # Read files with progress indicator
        with console.status("[yellow]Reading files..."):
            for file_path in md_files:
                try:
                    content = file_path.read_text(encoding="utf-8")
                    document_ids.append(file_path.stem)
                    markdown_contents.append(content)
                    valid_files.append(file_path)
                    console.print(f"[green]✓[/green] Read: [cyan]{file_path.name}[/cyan]")
                except Exception as e:
                    error_msg = str(e)
                    self.stats.add_error(file_path.name, error_msg)
                    console.print(f"[red]✗[/red] Error reading [cyan]{file_path.name}[/cyan]: {error_msg}")

        if not document_ids:
            console.print("[red]No valid files to process[/red]")
            return

        console.print(f"[bold blue]Processing {len(valid_files)} files using BAML[/bold blue]")
        console.print(f"[dim]Output will be saved to '{self.kvstore_id}' KV Store[/dim]")

        # Process all documents (BAML handles batching internally)
        _ = await self.abatch_analyze_documents(document_ids, markdown_contents)
        
        # Display final stats
        self.display_final_summary()
    
    def display_final_summary(self) -> None:
        """Display final processing summary with Rich formatting."""
        console.print()
        console.print(Panel(self.stats.create_summary_table(), title="[bold green]Processing Complete[/bold green]"))
        
        # Show error details if there are errors
        error_table = self.stats.create_error_table()
        if error_table:
            console.print()
            console.print(Panel(error_table, title="[bold red]Errors Encountered[/bold red]"))


def register_baml_commands(cli_app: typer.Typer) -> None:
    """Register BAML-based commands with the CLI application."""

    @cli_app.command()
    def structured_extract_baml(
        file_or_dir: Annotated[
            Path,
            typer.Argument(
                help="Markdown files or directories to process",
                exists=True,
                file_okay=True,
                dir_okay=True,
            ),
        ],
        class_name: Annotated[str, typer.Argument(help="Name of the Pydantic model class to instantiate")],
        recursive: bool = typer.Option(False, help="Search for files recursively"),
        batch_size: int = typer.Option(5, help="Number of files to process in each batch"),
        force: bool = typer.Option(False, "--force", help="Overwrite existing KV entries"),
    ) -> None:
        """Extract structured project data from Markdown files using BAML and save as JSON in a key-value store.

        This command uses BAML's ExtractRainbow function to extract data from markdown files
        and instantiate the provided Pydantic model class. It provides the same functionality
        as structured_extract but uses BAML for structured output.

        Example:
           uv run cli structured-extract-baml "*.md" --force --class ReviewedOpportunity
           uv run cli structured-extract-baml "**/*.md" --recursive --class ReviewedOpportunity
        """

        # Display startup information with Rich
        console.print(Panel(
            f"[bold cyan]BAML-based structured extraction[/bold cyan]\n"
            f"[dim]Source:[/dim] {file_or_dir}\n"
            f"[dim]Model:[/dim] {class_name}\n"
            f"[dim]Recursive:[/dim] {recursive}\n"
            f"[dim]Force:[/dim] {force}",
            title="[bold blue]Starting Processing[/bold blue]"
        ))

        # Resolve model class from the BAML types module
        with console.status("[yellow]Validating model class..."):
            try:
                model_cls = getattr(baml_types, class_name)
            except AttributeError as e:
                console.print(f"[red]✗ Unknown class '{class_name}' in baml_client.types: {e}[/red]")
                return

            if not isinstance(model_cls, type) or not issubclass(model_cls, BaseModel):
                console.print(f"[red]✗ Provided class '{class_name}' is not a Pydantic BaseModel[/red]")
                return
                
            console.print(f"[green]✓ Model class '{class_name}' validated[/green]")

        # Collect all Markdown files with progress
        all_files = []
        with console.status("[yellow]Discovering files..."):
            if file_or_dir.is_file() and file_or_dir.suffix.lower() in [".md", ".markdown"]:
                # Single Markdown file
                all_files.append(file_or_dir)
            elif file_or_dir.is_dir():
                # Directory - find Markdown files inside
                if recursive:
                    md_files = list(file_or_dir.rglob("*.[mM][dD]"))  # Case-insensitive match
                else:
                    md_files = list(file_or_dir.glob("*.[mM][dD]"))
                all_files.extend(md_files)
            else:
                console.print(f"[red]✗ Invalid path: {file_or_dir} - must be a Markdown file or directory[/red]")
                return

        md_files = all_files  # All files are already Markdown files at this point

        if not md_files:
            console.print("[yellow]⚠ No Markdown files found matching the provided patterns.[/yellow]")
            return

        console.print(f"[green]✓ Found {len(md_files)} Markdown files to process[/green]")

        if force:
            console.print("[yellow]⚠ Force option enabled - will reprocess all files and overwrite existing KV entries[/yellow]")

        # Create BAML processor
        processor = BamlStructuredProcessor(model_cls=model_cls, kvstore_id=KV_STORE_ID, force=force)
        processor.stats.files_discovered = len(md_files)

        # Filter out files that already have JSON in KV unless forced
        if not force:
            from genai_tk.utils.pydantic.kv_store import PydanticStore

            unprocessed_files = []
            with console.status("[yellow]Checking for cached results..."):
                for md_file in md_files:
                    key = md_file.stem
                    cached_doc = PydanticStore(kvstore_id=KV_STORE_ID, model=model_cls).load_object(key)
                    if not cached_doc:
                        unprocessed_files.append(md_file)
                    else:
                        console.print(f"[blue]ℹ[/blue] Skipping [cyan]{md_file.name}[/cyan] - already processed (use --force to overwrite)")
            md_files = unprocessed_files

        if not md_files:
            console.print(Panel(
                "[green]All files have already been processed.[/green]\n[dim]Use --force to reprocess.[/dim]",
                title="[bold green]Nothing to Process[/bold green]"
            ))
            return

        console.print(f"[bold]Processing {len(md_files)} files...[/bold]")
        asyncio.run(processor.process_files(md_files, batch_size))
