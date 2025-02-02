from collections.abc import Iterator
from typing import cast

import click
import mkdocs_click._docs


# Functions modified to my taste from the originals at:
# https://github.com/mkdocs/mkdocs-click/blob/master/mkdocs_click/_docs.py

# Changes:
# - Don't show a command group's usage when it has subcommands
# - Keep original commands order
# - Format types differently
# - Format table differently


def unbreakable(str):
    return f'<span style="white-space: nowrap;">`{str}`</span>'


def patched_recursively_make_command_docs(
    prog_name: str,
    command: click.BaseCommand,
    parent: click.Context | None = None,
    depth: int = 0,
    style: str = "plain",
    remove_ascii_art: bool = False,
    show_hidden: bool = False,
    list_subcommands: bool = False,
    has_attr_list: bool = False,
) -> Iterator[str]:
    """Create the raw Markdown lines for a command and its sub-commands."""

    from mkdocs_click._docs import (
        _build_command_context,
        _get_sub_commands,
        _make_description,
        _make_options,
        _make_subcommands_links,
        _make_title,
        _make_usage,
    )

    ctx = _build_command_context(prog_name=prog_name, command=command, parent=parent)

    if ctx.command.hidden and not show_hidden:
        return

    subcommands = _get_sub_commands(ctx.command, ctx)

    # TODO: Can also display if command is a group with `invoke_without_command`
    if len(subcommands) == 0:
        yield from _make_title(ctx, depth, has_attr_list=has_attr_list)
        yield from _make_usage(ctx)
        yield from _make_description(ctx, remove_ascii_art=remove_ascii_art)
        yield from _make_options(ctx, style, show_hidden=show_hidden)
        return

    # subcommands.sort(key=lambda cmd: str(cmd.name))

    if list_subcommands:
        yield from _make_subcommands_links(
            subcommands,
            ctx,
            has_attr_list=has_attr_list,
            show_hidden=show_hidden,
        )

    for command in subcommands:
        yield from patched_recursively_make_command_docs(
            cast(str, command.name),
            command,
            parent=ctx,
            depth=depth + 1,
            style=style,
            show_hidden=show_hidden,
            list_subcommands=list_subcommands,
            has_attr_list=has_attr_list,
        )


def patched_format_table_option_type(option: click.Option) -> str:
    typename = option.type.name

    if option.name == "font":
        return "font"

    if isinstance(option.type, click.Choice):
        # @click.option(..., type=click.Choice(["A", "B", "C"]))
        # -> `A` | `B` | `C`
        return " \\| ".join(f'`"{choice}"`' for choice in option.type.choices)

    if isinstance(option.type, click.DateTime):
        # @click.option(..., type=click.DateTime(["A", "B", "C"]))
        # -> datetime (`%Y-%m-%d` | `%Y-%m-%dT%H:%M:%S` | `%Y-%m-%d %H:%M:%S`)
        formats = " \\| ".join(f"`{fmt}`" for fmt in option.type.formats)  # type: ignore[attr-defined]
        return f"{typename} ({formats})"

    if isinstance(option.type, (click.IntRange, click.FloatRange)):
        left = "(" if option.type.min_open else "["
        right = ")" if option.type.max_open else "]"
        if option.type.min is not None and option.type.max is not None:
            # @click.option(..., type=click.IntRange(min=0, max=10))
            # -> integer (0, 10]
            return f"{typename} {left}{option.type.min}, {option.type.max}{right}"
        elif option.type.min is not None:
            # @click.option(..., type=click.IntRange(min=0))
            # -> integer range (`0` and above)
            return f"{typename} {left}{option.type.min}, ∞)"
        else:
            # @click.option(..., type=click.IntRange(max=10))
            # -> integer range (`10` and below)
            return f"{typename} (-∞, {option.type.max}{right}"

    # -> "boolean", "text", etc.
    return typename


def patched_format_table_option_row(option):
    # -> "`-V`, `--version`"
    names = ",<br>".join(unbreakable(opt) for opt in option.opts)

    if option.secondary_opts:
        # -> "`-V`, `--version` / `--show-info`"
        names += ",<br>"
        names += ",<br>".join(unbreakable(opt) for opt in option.secondary_opts)

    # -> "boolean"
    value_type = patched_format_table_option_type(option)

    # -> "Show version info."
    description = option.help if option.help is not None else "N/A"
    description = f"_{description}_"

    # -> `False`
    none_default_msg = "_required_" if option.required else "None"
    default = f"`{option.default}`" if option.default is not None else none_default_msg

    return f"| {names} | {value_type} | {description} | {default} |"


mkdocs_click._docs._recursively_make_command_docs = (
    patched_recursively_make_command_docs
)
mkdocs_click._docs._format_table_option_type = patched_format_table_option_type
mkdocs_click._docs._format_table_option_row = patched_format_table_option_row
