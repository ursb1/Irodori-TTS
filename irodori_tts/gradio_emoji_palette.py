from __future__ import annotations

from dataclasses import dataclass
from html import escape

import gradio as gr


@dataclass(frozen=True)
class EmojiPaletteItem:
    emoji: str
    label: str
    description: str


EMOJI_PALETTE_CSS = """
.emoji-palette {
    max-width: 100%;
}

.emoji-palette-grid {
    display: flex;
    gap: 3px;
    flex-wrap: wrap;
    align-items: flex-start;
    max-height: 124px;
    overflow-y: auto;
}

.emoji-palette-button {
    flex: 0 0 28px !important;
    min-width: 28px !important;
    max-width: 28px !important;
}

.emoji-palette-button button {
    width: 28px !important;
    min-width: 28px !important;
    height: 28px !important;
    min-height: 28px !important;
    border-radius: 4px;
    font-size: 17px;
    line-height: 1;
    padding: 0 !important;
}

button.emoji-palette-button {
    width: 28px;
    min-width: 28px;
    height: 28px;
    min-height: 28px;
    border-radius: 4px;
    font-size: 17px;
    line-height: 1;
    padding: 0;
    cursor: pointer;
}
"""


EMOJI_PALETTE_ITEMS: tuple[EmojiPaletteItem, ...] = (
    EmojiPaletteItem("👂", "Whisper", "Sound near the ear"),
    EmojiPaletteItem("😮‍💨", "Sigh", "Sighing, sleeping breath"),
    EmojiPaletteItem("⏸️", "Pause", "Silence"),
    EmojiPaletteItem("🤭", "Giggle", "Snickering, suppressed laughter"),
    EmojiPaletteItem("🥵", "Moan", "Groaning, panting"),
    EmojiPaletteItem("📢", "Echo", "Reverb effect"),
    EmojiPaletteItem("😏", "Tease", "Coquettishly, playfully"),
    EmojiPaletteItem("🥺", "Tremble", "Timidly, lacking confidence"),
    EmojiPaletteItem("🌬️", "Out of Breath", "Heavy breathing, gasping"),
    EmojiPaletteItem("😮", "Gasp", "Sharp intake of breath"),
    EmojiPaletteItem("👅", "Licking Sound", "Chewing sounds, wet mouth noises"),
    EmojiPaletteItem("💋", "Lip Smack", "Kissing sound, lip pop"),
    EmojiPaletteItem("🫶", "Tenderly", "Softly, affectionately"),
    EmojiPaletteItem("😭", "Crying", "Sobbing, sadness"),
    EmojiPaletteItem("😱", "Scream", "Shouting, shrieking"),
    EmojiPaletteItem("😪", "Sleepy", "Drowsily, lethargically"),
    EmojiPaletteItem("😴", "Talk in Sleep", "Snoring"),
    EmojiPaletteItem("⏩", "Fast Talk", "Rapidly, hurriedly"),
    EmojiPaletteItem("📞", "On Phone", "Through a speaker/telephone filter"),
    EmojiPaletteItem("🐢", "Slowly", "Deliberately, at a slow pace"),
    EmojiPaletteItem("🥤", "Swallow", "Sound of swallowing saliva"),
    EmojiPaletteItem("🤧", "Cough/Sneeze", "Coughing, sniffles"),
    EmojiPaletteItem("😒", "Tut", "Clicking tongue in annoyance"),
    EmojiPaletteItem("😰", "Panicked", "Flustered, nervous, stuttering"),
    EmojiPaletteItem("😆", "Joyful", "Happily, cheerfully"),
    EmojiPaletteItem("💥", "Forcefully", "With strong momentum"),
    EmojiPaletteItem("😠", "Angry", "Dissatisfied, sulking"),
    EmojiPaletteItem("😲", "Surprised", "Amazed, astonished"),
    EmojiPaletteItem("🥱", "Yawn", "Stretching due to tiredness"),
    EmojiPaletteItem("😖", "Agonized", "In pain, struggling"),
    EmojiPaletteItem("😟", "Worried", "Anxiously, concerned"),
    EmojiPaletteItem("🫣", "Embarrassed", "Shyly, bashfully"),
    EmojiPaletteItem("🙄", "Exasperated", "Fed up, rolling eyes"),
    EmojiPaletteItem("😊", "Cheerful", "Pleased, happy"),
    EmojiPaletteItem("😎", "Smug", "Confidently, coolly"),
    EmojiPaletteItem("👌", "Acknowledge", "Nodding sound, 'uh-huh'"),
    EmojiPaletteItem("🙏", "Begging", "Imploringly, pleading"),
    EmojiPaletteItem("🥴", "Drunk", "Intoxicated, dizzy"),
    EmojiPaletteItem("🎵", "Humming", "Singing softly with closed mouth"),
    EmojiPaletteItem("🤐", "Muffled", "Covered mouth, indistinct speech"),
    EmojiPaletteItem("😌", "Relieved", "Contentedly, relieved"),
    EmojiPaletteItem("🤔", "Questioning", "Thinking, doubtful"),
    EmojiPaletteItem("💪", "Strong", "Putting strength into it"),
    EmojiPaletteItem("👃", "Sniff", "Sound of smelling/sniffing"),
    EmojiPaletteItem("📖", "Narration", "Reading aloud, storytelling"),
)


_INSERT_EMOJI_ON_POINTER_DOWN = (
    "event.preventDefault();"
    "const root=this.closest('[data-irodori-emoji-palette]');"
    "const input=root?document.querySelector(root.dataset.target):null;"
    "if(!input)return;"
    "const emoji=this.dataset.emoji;"
    "const text=input.value||'';"
    "const focused=document.activeElement===input;"
    "const start=focused&&typeof input.selectionStart==='number'?input.selectionStart:text.length;"
    "const end=focused&&typeof input.selectionEnd==='number'?input.selectionEnd:text.length;"
    "const next=text.slice(0,start)+emoji+text.slice(end);"
    "const caret=start+emoji.length;"
    "input.value=next;"
    "input.focus({preventScroll:true});"
    "input.setSelectionRange(caret,caret);"
    "input.dispatchEvent(new Event('input',{bubbles:true}));"
    "input.dispatchEvent(new Event('change',{bubbles:true}));"
)


def _textbox_selector(textbox: gr.Textbox) -> str:
    elem_id = getattr(textbox, "elem_id", None)
    root_selector = f"#{elem_id}" if elem_id else f"#component-{textbox._id}"
    return f"{root_selector} textarea, {root_selector} input:not([type='hidden'])"


def _emoji_palette_html(textbox: gr.Textbox) -> str:
    target = escape(_textbox_selector(textbox), quote=True)
    handler = escape(_INSERT_EMOJI_ON_POINTER_DOWN, quote=True)
    buttons = []
    for item in EMOJI_PALETTE_ITEMS:
        emoji = escape(item.emoji, quote=True)
        title = escape(f"{item.label}: {item.description}", quote=True)
        buttons.append(
            '<button type="button" '
            'class="emoji-palette-button" '
            f'data-emoji="{emoji}" '
            f'title="{title}" '
            f'aria-label="{title}" '
            f'onpointerdown="{handler}">'
            f"{emoji}</button>"
        )
    return (
        '<div class="emoji-palette-grid" '
        'data-irodori-emoji-palette="true" '
        f'data-target="{target}">'
        f"{''.join(buttons)}</div>"
    )


def build_emoji_palette(textbox: gr.Textbox, *, open: bool = True) -> None:
    with gr.Accordion("Emoji Palette", open=open, elem_classes=["emoji-palette"]):
        gr.HTML(_emoji_palette_html(textbox))
