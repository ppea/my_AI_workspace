# nextme/src/cli/main.py
from __future__ import annotations

import asyncio
from pathlib import Path
from typing import TYPE_CHECKING

import typer
from rich.console import Console
from rich.table import Table
if TYPE_CHECKING:
    from src.scheduler.scheduler import NextMeScheduler

app = typer.Typer(name="nextme", help="Personal AI Life Management System")
console = Console()


@app.command()
def status() -> None:
    """Show system health status."""
    from src.core.rag import RAGPipeline
    from src.core.memory import MemoryManager

    console.print("\n[bold]NextMe System Status[/bold]")
    console.print("=" * 40)

    try:
        rag = RAGPipeline()
        stats = rag.get_stats()
        console.print(f"RAG Index:     ✅ {stats['document_count']} documents indexed")
    except Exception as e:
        console.print(f"RAG Index:     ❌ Error: {e}")

    try:
        memory = MemoryManager()
        stats = memory.get_stats()
        console.print(f"Memory (Mem0): ✅ {stats['total_memories']} memories stored")
    except Exception as e:
        console.print(f"Memory (Mem0): ❌ Error: {e}")

    console.print()


@app.command()
def reindex(
    full: bool = typer.Option(False, "--full", help="Full reindex (not incremental)"),
    directory: str = typer.Option("knowledge/", "--dir", help="Directory to index"),
) -> None:
    """Rebuild RAG index."""
    from src.core.rag import RAGPipeline

    console.print(f"[bold]Indexing {directory}...[/bold]")
    rag = RAGPipeline()
    count = rag.index_directory(Path(directory))
    console.print(f"✅ Indexed {count} documents")


@app.command()
def note(
    text: str = typer.Argument(..., help="Note content"),
    area: str = typer.Option("inbox", "--area", "-a", help="Knowledge area"),
    tags: str = typer.Option("", "--tags", "-t", help="Comma-separated tags"),
) -> None:
    """Add a quick note to the knowledge base."""
    from datetime import date

    area_dir = Path(f"knowledge/areas/{area}" if area != "inbox" else "knowledge/inbox")
    if not area_dir.exists():
        area_dir.mkdir(parents=True, exist_ok=True)

    today = date.today().isoformat()
    tag_list = [t.strip() for t in tags.split(",") if t.strip()] if tags else []

    # Create note file
    filename = f"{today}-note.md"
    filepath = area_dir / filename

    # If file exists, append; otherwise create
    if filepath.exists():
        with open(filepath, "a") as f:
            f.write(f"\n\n## {today}\n{text}\n")
        console.print(f"📝 Appended to {filepath}")
    else:
        frontmatter = (
            f"---\ntype: note\ndate: {today}\n"
            f"tags: {tag_list}\nadvisor: {area}\n"
            f"confidentiality: normal\n---\n\n"
            f"# Note — {today}\n\n{text}\n"
        )
        filepath.write_text(frontmatter)
        console.print(f"📝 Created {filepath}")


@app.command()
def chat(
    advisor: str | None = typer.Option(None, "--advisor", "-a", help="Direct advisor"),
) -> None:
    """Interactive chat with Chief of Staff or specific advisor."""
    from src.agents.chief_of_staff import ChiefOfStaff
    from src.advisors.health.advisor import HealthAdvisor
    from src.advisors.schedule.advisor import ScheduleAdvisor
    from src.advisors.finance.advisor import FinanceAdvisor
    from src.advisors.career.advisor import CareerAdvisor
    from src.advisors.legal.advisor import LegalAdvisor
    from src.advisors.family.advisor import FamilyAdvisor
    from src.advisors.mental_health.advisor import MentalHealthAdvisor
    from src.advisors.learning.advisor import LearningAdvisor
    from src.advisors.entrepreneurship.advisor import EntrepreneurshipAdvisor
    from src.core.context import ConversationContext

    chief = ChiefOfStaff()
    chief.register_advisor(HealthAdvisor())
    chief.register_advisor(ScheduleAdvisor())
    chief.register_advisor(FinanceAdvisor())
    chief.register_advisor(CareerAdvisor())
    chief.register_advisor(LegalAdvisor())
    chief.register_advisor(FamilyAdvisor())
    chief.register_advisor(MentalHealthAdvisor())
    chief.register_advisor(LearningAdvisor())
    chief.register_advisor(EntrepreneurshipAdvisor())

    context = ConversationContext(session_id="cli-session", channel="cli")

    console.print("[bold]🤖 NextMe Chief of Staff ready. Type 'exit' to quit.[/bold]\n")

    while True:
        try:
            query = console.input("[bold green]> [/bold green]")
        except (KeyboardInterrupt, EOFError):
            break

        if query.strip().lower() in ("exit", "quit", "q"):
            break

        if not query.strip():
            continue

        if advisor:
            context.active_advisor = advisor

        response = asyncio.run(chief.process(query, context))
        rendered = response.render_for("cli")
        console.print(f"\n{rendered}\n")


@app.command()
def memory(
    action: str = typer.Argument("list", help="Action: list, search, forget"),
    query: str = typer.Argument("", help="Search query or memory to forget"),
) -> None:
    """Manage long-term memory."""
    from src.core.memory import MemoryManager

    mem = MemoryManager()

    match action:
        case "list":
            memories = mem.list_all(limit=20)
            if not memories:
                console.print("No memories stored yet.")
                return
            table = Table(title="Stored Memories")
            table.add_column("ID", style="dim")
            table.add_column("Memory")
            for m in memories:
                table.add_row(m.id[:8], m.text[:80])
            console.print(table)

        case "search":
            if not query:
                console.print("Please provide a search query.")
                return
            results = mem.search(query)
            for r in results:
                console.print(f"  • {r.text}")

        case "forget":
            if not query:
                console.print("Please provide the memory ID to forget.")
                return
            success = mem.delete(query)
            if success:
                console.print(f"✅ Memory {query} deleted.")
            else:
                console.print(f"❌ Could not delete memory {query}.")

        case _:
            console.print(f"Unknown action: {action}. Use list, search, or forget.")


@app.command()
def serve(
    host: str = typer.Option("0.0.0.0", "--host", "-h", help="Host to bind to"),
    port: int = typer.Option(8080, "--port", "-p", help="Port to bind to"),
) -> None:
    """Start the FastAPI REST API server."""
    import uvicorn

    console.print(f"[bold]Starting NextMe API server on {host}:{port}...[/bold]")
    uvicorn.run(
        "src.api.app:create_app",
        factory=True,
        host=host,
        port=port,
        log_level="info",
    )


@app.command()
def scheduler(
    action: str = typer.Argument("start", help="Action: start, status"),
) -> None:
    """Manage the proactive scheduler (start, status)."""
    from src.core.config import load_scheduler_config, load_secrets
    from src.scheduler.scheduler import NextMeScheduler

    cfg = load_scheduler_config()

    if action == "status":
        console.print("[bold]Scheduler Config[/bold]")
        console.print(f"  Daily briefing: {cfg.daily_briefing_hour:02d}:{cfg.daily_briefing_minute:02d} ({cfg.timezone})")
        console.print(f"  Weekly review:  weekday={cfg.weekly_review_weekday}, {cfg.weekly_review_hour:02d}:00")
        console.print(f"  Quiet hours:    {cfg.quiet_hours.start_hour}:00–{cfg.quiet_hours.end_hour}:00 (enabled={cfg.quiet_hours.enabled})")
        return

    if action == "start":
        secrets = load_secrets()
        send_fn = None

        if secrets.telegram_bot_token and secrets.telegram_owner_chat_id:
            from src.integrations.telegram.bot import NextMeTelegramBot, create_chief
            chief = create_chief()
            bot = NextMeTelegramBot(
                token=secrets.telegram_bot_token,
                owner_chat_id=secrets.telegram_owner_chat_id,
                chief=chief,
            )
            send_fn = bot.send_notification

        sched = NextMeScheduler(config=cfg, send_fn=send_fn)

        console.print("[bold]Starting NextMe scheduler...[/bold]")
        asyncio.run(_run_scheduler(sched))


async def _run_scheduler(sched: "NextMeScheduler") -> None:
    await sched.start()
    try:
        while True:
            await asyncio.sleep(60)
    except (KeyboardInterrupt, asyncio.CancelledError):
        sched.stop()


@app.command()
def costs(
    period: str = typer.Option("daily", "--period", "-p", help="Period: daily, monthly, total"),
) -> None:
    """Show LLM cost summary per advisor."""
    import asyncio
    from src.core.cost_tracker import CostTracker

    tracker = CostTracker()

    async def _show():
        await tracker.initialize()
        if period == "total":
            total = await tracker.total_cost()
            console.print(f"[bold]Total lifetime LLM cost: ${total:.4f}[/bold]")
        elif period == "monthly":
            summaries = await tracker.monthly_summary()
            _print_cost_table(summaries, "Monthly Cost Summary")
        else:
            summaries = await tracker.daily_summary()
            _print_cost_table(summaries, "Daily Cost Summary")

    asyncio.run(_show())


def _print_cost_table(summaries: list, title: str) -> None:
    table = Table(title=title)
    table = Table(title=title)
    table.add_column("Advisor")
    table.add_column("Calls", justify="right")
    table.add_column("Input Tokens", justify="right")
    table.add_column("Output Tokens", justify="right")
    table.add_column("Cost (USD)", justify="right")
    for s in summaries:
        table.add_row(s.advisor, str(s.total_calls),
                      str(s.total_input_tokens), str(s.total_output_tokens),
                      f"${s.total_cost_usd:.4f}")
    if not summaries:
        table.add_row("(no data)", "-", "-", "-", "$0.0000")
    console.print(table)

if __name__ == "__main__":
    app()
