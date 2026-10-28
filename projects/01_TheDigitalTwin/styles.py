"""Styling for the Digital Twin Gradio app (light, professional layout).

app.py only needs:  from styles import CSS, JS, EXAMPLES
Everything else (header, suggested questions, tags, footer) is built here.
"""

import json

# (emoji, short label, full question sent to the twin)
_SUGGESTIONS = [
    ("👋", "About Dhaval", "Tell me about your background and experience."),
    ("🏦", "Banking projects", "Tell me about your banking and payments projects."),
    ("🧩", "Architecture", "How do you approach cloud architecture?"),
    ("🤝", "Leadership", "What is your leadership style and how do you build engineering teams?"),
    ("🤖", "Applied AI", "How are you applying AI in enterprise engineering?"),
    ("☕", "Beyond work", "What do you enjoy outside of work?"),
]

EXAMPLES = [prompt for _, _, prompt in _SUGGESTIONS]

CSS = """
:root {
  --dt-bg: #f6f8fc;
  --dt-card: #ffffff;
  --dt-soft: #f8fafc;
  --dt-line: #e3e9f1;
  --dt-navy: #16324f;
  --dt-user: #17365a;
  --dt-teal: #0b8f80;
  --dt-text: #1e3047;
  --dt-muted: #64748b;
  --dt-bot: #eff4f8;
  --dt-radius: 18px;
  --dt-avatar: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='16' fill='%2317365a'/%3E%3Cline x1='32' y1='11' x2='32' y2='19' stroke='%23e8f4fb' stroke-width='2.5'/%3E%3Ccircle cx='32' cy='10' r='3.5' fill='%2335c2ae'/%3E%3Crect x='13' y='19' width='38' height='28' rx='10' fill='%23e8f4fb'/%3E%3Crect x='8' y='28' width='5' height='10' rx='2' fill='%2335c2ae'/%3E%3Crect x='51' y='28' width='5' height='10' rx='2' fill='%2335c2ae'/%3E%3Ccircle cx='24' cy='32' r='4.5' fill='%2317365a'/%3E%3Ccircle cx='40' cy='32' r='4.5' fill='%2317365a'/%3E%3Crect x='26' y='40' width='12' height='2.5' rx='1.25' fill='%2335c2ae'/%3E%3C/svg%3E");
}

footer, .built-with, .show-api, .api-docs { display: none !important; }

html, body, gradio-app {
  background: var(--dt-bg) !important;
  color-scheme: light;
}

/* ---------- Page: wide layout ---------- */
.gradio-container {
  background: var(--dt-bg) !important;
  color: var(--dt-text) !important;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
  width: 100% !important;
  max-width: min(1360px, 96vw) !important;
  margin: 0 auto !important;
  padding: 0 !important;
}
.block, .form { box-shadow: none !important; }
.dt-stack { gap: 0 !important; }
.app, .gradio-container .app {
  padding: 5px !important;
}
.block, .form { box-shadow: none !important; }

/* ---------- Top bar ---------- */
.dt-topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 26px;
}
.dt-brand { display: flex; align-items: center; gap: 12px; }
.dt-badge {
  width: 40px; height: 40px;
  border-radius: 12px;
  background: var(--dt-user);
  color: #fff;
  font-weight: 800;
  font-size: 15px;
  display: flex; align-items: center; justify-content: center;
  letter-spacing: 0.02em;
}
.dt-brand-name { font-size: 15px; font-weight: 700; color: var(--dt-navy); line-height: 1.2; }
.dt-brand-sub { font-size: 12px; color: var(--dt-muted); }
.dt-pill {
  display: inline-flex; align-items: center; gap: 8px;
  background: #e8f7f3;
  border: 1px solid #c6eadf;
  color: #0b6b5c;
  font-size: 12px; font-weight: 700;
  padding: 7px 14px;
  border-radius: 999px;
}
.dt-pill-dot, .dt-live {
  width: 8px; height: 8px; border-radius: 50%;
  background: var(--dt-teal);
  box-shadow: 0 0 0 0 rgba(11, 143, 128, 0.5);
  animation: dt-pulse 2.2s infinite;
}
.dt-live { background: #22c55e; width: 9px; height: 9px; margin-right: 8px; }

@keyframes dt-pulse {
  0% { box-shadow: 0 0 0 0 rgba(11, 143, 128, 0.45); }
  70% { box-shadow: 0 0 0 7px rgba(11, 143, 128, 0); }
  100% { box-shadow: 0 0 0 0 rgba(11, 143, 128, 0); }
}

/* ---------- Headline + description + tags ---------- */
.gradio-container h1 {
  text-align: left !important;
  color: var(--dt-navy) !important;
  font-size: clamp(30px, 4.6vw, 48px) !important;
  font-weight: 800 !important;
  letter-spacing: -0.035em !important;
  line-height: 1.1 !important;
  margin: 0 0 12px !important;
  padding: 0 !important;
  border: 0 !important;
}
.gradio-container h1 .dt-accent { color: var(--dt-teal); }

.prose, .md, .gradio-container .block:has(h1) {
  overflow: visible !important;
  max-height: none !important;
  height: auto !important;
  background: transparent !important;
  border: 0 !important;
}
.gradio-container .prose p, .gradio-container .md p {
  color: var(--dt-muted) !important;
  font-size: 15px !important;
  line-height: 1.6 !important;
  text-align: left !important;
  max-width: 920px;
}
.dt-tags { display: flex; flex-wrap: wrap; gap: 8px; margin: 14px 0 24px; }
.dt-tag {
  background: #e9f0f6;
  color: #3c5873;
  font-size: 11.5px; font-weight: 600;
  padding: 6px 12px;
  border-radius: 999px;
}

/* ---------- One joined card: suggestions / conversation bar / chat / input ---------- */
.dt-panel, .chatbot, .block.chatbot, .chatbot.block, .dt-input-block {
  background: var(--dt-card) !important;
  border: 1px solid var(--dt-line) !important;
  border-radius: 0 !important;
}

.dt-suggest {
  border-radius: var(--dt-radius) var(--dt-radius) 0 0 !important;
  padding: 16px 20px 18px;
}
.dt-suggest-head { display: flex; align-items: baseline; flex-wrap: wrap; gap: 8px; }
.dt-suggest-head strong { font-size: 13px; color: var(--dt-navy); }
.dt-suggest-head span { font-size: 12px; color: var(--dt-muted); }
.dt-chips {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
  margin-top: 12px;
}
.dt-chip {
  display: flex !important; align-items: center; gap: 9px;
  background: var(--dt-soft) !important;
  border: 1px solid var(--dt-line) !important;
  border-radius: 12px !important;
  color: var(--dt-navy) !important;
  font: 600 13.5px/1.2 'Inter', -apple-system, 'Segoe UI', sans-serif !important;
  text-align: left;
  padding: 12px 14px !important;
  cursor: pointer;
  transition: transform 0.12s ease, border-color 0.12s ease, box-shadow 0.12s ease, background 0.12s ease;
}
.dt-chip:hover {
  background: #fff !important;
  border-color: var(--dt-teal) !important;
  transform: translateY(-1px);
  box-shadow: 0 6px 16px -8px rgba(11, 143, 128, 0.45);
}
.dt-chip:focus-visible, .dt-newchat:focus-visible { outline: 2px solid var(--dt-teal); outline-offset: 2px; }
.dt-chip-emoji { font-size: 16px; }

.dt-conv {
  display: flex; align-items: center; justify-content: space-between; gap: 12px;
  border-top: 0 !important;
  background: #fbfcfe !important;
  padding: 12px 20px;
  font-size: 13px; font-weight: 700; color: var(--dt-navy);
}
.dt-conv-left { display: flex; align-items: center; }
.dt-conv-right { font-size: 12px; font-weight: 500; color: var(--dt-muted); }

/* ---------- Chat area: taller, easy to read ---------- */
.chatbot, .block.chatbot, .chatbot.block {
  border-top: 0 !important;
  height: max(560px, calc(100vh - 430px)) !important;
  min-height: 560px !important;
  max-height: none !important;
  overflow: hidden !important;
}
.chatbot > .block-label, .chatbot > label, .chatbot .label-wrap, .chatbot .block-label { display: none !important; }
.chatbot .placeholder, .chatbot .placeholder * { color: var(--dt-muted) !important; }
.bubble-wrap, .chatbot .bubble-wrap {
  background: transparent !important;
  padding: 22px 26px !important;
}

/* Native Gradio examples are replaced by the suggestion chips above */
body:has(.dt-suggest) .examples,
body:has(.dt-suggest) .examples-container,
body:has(.dt-suggest) [data-testid="examples"] { display: none !important; }

/* Top-right chat toolbar (share / clear / copy): hidden, New chat is in the footer */
.chatbot .top-panel, .chatbot .icon-button-wrapper.top-panel { display: none !important; }
.chatbot .icon-button-wrapper button, .chatbot .icon-buttons button {
  background: #fff !important; color: var(--dt-muted) !important;
  border: 1px solid var(--dt-line) !important; border-radius: 8px !important;
}

/* ---------- Messages ---------- */
.message-row, .message-wrap {
  background: transparent !important;
  border: 0 !important;
  box-shadow: none !important;
  animation: dt-in 0.25s ease both;
}
.message-row { margin: 8px 0 !important; align-items: flex-start; }
@keyframes dt-in { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }

.message-row .flex-wrap { max-width: min(86%, 980px) !important; }
.message-row .message, .message-row .message-bubble, .message-row .bubble {
  font-size: 15px !important;
  line-height: 1.7 !important;
  box-shadow: none !important;
  max-width: 100% !important;
}

/* Assistant bubble */
.message-row.bot-row .message, .message-row.bot-row .message-bubble, .message.bot {
  background: var(--dt-bot) !important;
  border: 0 !important;
  border-radius: 16px !important;
  padding: 14px 20px !important;
  color: var(--dt-text) !important;
}
/* User bubble */
.message-row.user-row .message, .message-row.user-row .message-bubble, .message.user {
  background: var(--dt-user) !important;
  border: 0 !important;
  border-radius: 16px !important;
  padding: 12px 20px !important;
  color: #fff !important;
}
.message-row.user-row .message * { color: #fff !important; background: transparent !important; border: 0 !important; }

/* No nested boxes or stray lines inside a bubble */
.message-row .message .message, .message-row .message .bubble,
.message-row .message-bubble .message, .message-row .bubble .bubble {
  background: transparent !important; border: 0 !important; padding: 0 !important; border-radius: 0 !important;
}
.message-row.bot-row .message div, .message-row.bot-row .message span.prose {
  background: transparent !important; border: 0 !important; box-shadow: none !important;
}

/* Long-answer typography */
.message-row .message p { margin: 0 0 12px !important; color: inherit !important; font-size: 15px !important; line-height: 1.7 !important; max-width: none !important; }
.message-row .message p:last-child { margin-bottom: 0 !important; }
.message-row .message h1, .message-row .message h2, .message-row .message h3, .message-row .message h4 {
  color: var(--dt-navy) !important; margin: 18px 0 8px !important; line-height: 1.3 !important; letter-spacing: -0.01em;
}
.message-row .message h1 { font-size: 20px !important; }
.message-row .message h2 { font-size: 18px !important; }
.message-row .message h3, .message-row .message h4 { font-size: 16px !important; }
.message-row .message ul, .message-row .message ol { margin: 6px 0 12px !important; padding-left: 22px !important; }
.message-row .message li { margin: 4px 0 !important; line-height: 1.65 !important; }
.message-row .message strong { color: var(--dt-navy); }
.message-row.user-row .message strong { color: #fff; }
.message-row .message a { color: var(--dt-teal) !important; text-decoration: underline; text-underline-offset: 2px; }
.message-row .message blockquote {
  margin: 10px 0 !important; padding: 4px 14px !important;
  border-left: 3px solid var(--dt-teal) !important; color: var(--dt-muted) !important;
}
.message-row .message code {
  background: #e3ebf3 !important; color: var(--dt-navy) !important;
  border-radius: 6px !important; padding: 1px 6px !important; font-size: 13.5px !important;
}
.message-row .message pre {
  background: #0f1f33 !important; color: #e6edf7 !important;
  border-radius: 12px !important; padding: 14px 16px !important; overflow-x: auto !important;
}
.message-row .message pre code { background: transparent !important; color: inherit !important; padding: 0 !important; }
.message-row .message table { border-collapse: collapse; width: 100%; margin: 10px 0; font-size: 14px; }
.message-row .message th, .message-row .message td { border: 1px solid var(--dt-line) !important; padding: 8px 10px !important; text-align: left; }
.message-row .message th { background: #e4ecf4 !important; }
.message-row .message hr { border: 0; border-top: 1px solid var(--dt-line); margin: 14px 0; }

/* Per-message copy button: subtle */
.message-buttons-left button, .message-buttons-right button {
  background: #fff !important; color: var(--dt-muted) !important;
  border: 1px solid var(--dt-line) !important; border-radius: 8px !important;
}
.message-buttons-left button:hover, .message-buttons-right button:hover { color: var(--dt-teal) !important; }

/* ---------- Avatar (drawn in CSS, no image file needed) ---------- */
.message-row.bot-row .avatar-container, .dt-avatar {
  width: 38px !important; height: 38px !important; min-width: 38px !important;
  flex-shrink: 0 !important;
  border-radius: 11px !important;
  border: 0 !important; padding: 0 !important;
  margin-right: 10px !important;
  background: var(--dt-avatar) center / cover no-repeat !important;
}
.message-row.bot-row .avatar-container img, .message-row.bot-row .avatar-image { opacity: 0 !important; }
.dt-avatar-row { position: relative !important; padding-left: 50px !important; }
.dt-avatar-row > .dt-avatar { position: absolute !important; left: 0; top: 0; }

/* Quiet Gradio's "generating" border animation */
.generating, .pending { animation: none !important; border-color: var(--dt-line) !important; }

/* ---------- Input area ---------- */
.dt-input-block {
  border-top: 0 !important;
  border-radius: 0 0 var(--dt-radius) var(--dt-radius) !important;
  padding: 16px 20px 12px !important;
  display: flex !important; flex-direction: column !important; align-items: stretch !important;
  justify-content: flex-start !important; gap: 10px;
  width: 100% !important; max-width: 100% !important; box-sizing: border-box !important;
  box-shadow: 0 24px 40px -26px rgba(22, 50, 79, 0.28) !important;
}
/* Keep the whole input row full width, before and after the first message */
.dt-input-block > *:not(.dt-disclaimer),
.dt-input-block .block, .dt-input-block .form, .dt-input-block form,
.dt-input-block label, .dt-input-block .container,
.dt-input-block *:has(> textarea) {
  width: 100% !important; max-width: 100% !important; min-width: 0 !important;
  flex: 1 1 auto !important; box-sizing: border-box !important;
}
.dt-input-block textarea, .dt-input-block input[type="text"] { width: 100% !important; }
.dt-input-block button.submit-button, .dt-input-block button.submit,
.dt-input-block button.primary, .dt-input-block button[aria-label="Submit"] { flex: 0 0 auto !important; width: auto !important; }
.dt-input-block .form, .dt-input-block form, .dt-input-block .block, .dt-input-block .input-row {
  background: transparent !important; border: 0 !important; box-shadow: none !important;
  padding: 0 !important; margin: 0 !important;
}
.dt-input-block .form, .dt-input-block form { display: flex; align-items: center; gap: 12px; }

textarea, input[type="text"] {
  background: var(--dt-soft) !important;
  color: var(--dt-text) !important;
  border: 1px solid #d5deea !important;
  border-radius: 12px !important;
  padding: 13px 16px !important;
  min-height: 48px !important;
  font-family: inherit !important;
  font-size: 15px !important;
  line-height: 1.4 !important;
  box-shadow: none !important;
  transition: border-color 0.12s ease, box-shadow 0.12s ease, background 0.12s ease;
}
textarea:focus, input[type="text"]:focus {
  background: #fff !important;
  border-color: var(--dt-teal) !important;
  box-shadow: 0 0 0 3px rgba(11, 143, 128, 0.16) !important;
  outline: none !important;
}
textarea::placeholder, input::placeholder { color: #8a99ad !important; }

/* Send button: teal "Send ↗" */
.dt-input-block button.submit-button, .dt-input-block button.submit,
.dt-input-block button.primary, .dt-input-block button[aria-label="Submit"] {
  background: var(--dt-teal) !important;
  border: 0 !important;
  border-radius: 12px !important;
  width: auto !important; min-width: 96px !important; height: 48px !important;
  padding: 0 24px !important;
  display: inline-flex !important; align-items: center; justify-content: center;
  cursor: pointer;
  transition: background 0.12s ease, transform 0.12s ease;
}
.dt-input-block button.submit-button svg, .dt-input-block button.submit svg,
.dt-input-block button.primary svg, .dt-input-block button[aria-label="Submit"] svg { display: none !important; }
.dt-input-block button.submit-button::after, .dt-input-block button.submit::after,
.dt-input-block button.primary::after, .dt-input-block button[aria-label="Submit"]::after {
  content: "Send ↗"; color: #fff; font: 700 13.5px/1 'Inter', -apple-system, 'Segoe UI', sans-serif;
}
.dt-input-block button.submit-button:hover, .dt-input-block button.primary:hover { background: #087a6d !important; transform: translateY(-1px); }

.dt-disclaimer {
  width: 100%; order: 99;
  display: flex; justify-content: space-between; flex-wrap: wrap; gap: 6px 16px;
  font-size: 11.5px; color: var(--dt-muted);
}
.dt-disclaimer kbd {
  background: #eef2f7; border: 1px solid var(--dt-line); border-radius: 5px;
  padding: 1px 5px; font: 600 10.5px 'JetBrains Mono', Menlo, monospace; color: var(--dt-navy);
}

/* ---------- Footer row ---------- */
.dt-footer {
  display: flex; align-items: center; justify-content: space-between; gap: 12px;
  margin-top: 16px; padding: 0 4px;
  font-size: 12px; color: var(--dt-muted);
}
.dt-newchat {
  background: #fff !important; color: var(--dt-navy) !important;
  border: 1px solid #cbd5e1 !important; border-radius: 999px !important;
  font: 600 12px 'Inter', -apple-system, 'Segoe UI', sans-serif !important;
  padding: 6px 14px !important; cursor: pointer;
  transition: border-color 0.12s ease, color 0.12s ease;
}
.dt-newchat:hover { border-color: var(--dt-teal) !important; color: var(--dt-teal) !important; }

/* ---------- Scrollbars and selection ---------- */
* { scrollbar-width: thin; scrollbar-color: #b6c2d1 transparent; }
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #b6c2d1; border-radius: 8px; }
::selection { background: rgba(11, 143, 128, 0.25); }

/* ---------- Responsive ---------- */
@media (max-width: 900px) {
  .dt-chips { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .message-row .flex-wrap { max-width: 92% !important; }
}
@media (max-width: 560px) {
  /*.gradio-container { padding: 18px 12px 28px !important; }*/
  .gradio-container { padding: 0 !important; }
  /* Hide the suggested questions on phones */
  .dt-suggest { display: none !important; }
  /* The "Conversation" bar becomes the top of the card, so give it the rounded corners */
  .dt-conv { border-radius: var(--dt-radius) var(--dt-radius) 0 0 !important; border-top: 1px solid var(--dt-line) !important; }
  .dt-chips { grid-template-columns: 1fr; }
  .dt-conv-right { display: none; }
  .bubble-wrap, .chatbot .bubble-wrap { padding: 14px !important; }
  .dt-input-block button.submit-button, .dt-input-block button.primary { min-width: 76px !important; padding: 0 16px !important; }
}
@media (prefers-reduced-motion: reduce) {
  * { animation: none !important; transition: none !important; }
}
"""

JS = """
() => {
  const SUGGESTIONS = __SUGGESTIONS__;
  const PLACEHOLDER = "Ask Dhaval's digital twin anything...";
  const TAGS = ["20+ years in technology", "Cloud & AI engineering", "Engineering leadership"];
  document.title = "Dhaval Mistry | Digital Twin";

  // Always use the light theme.
  const forceLight = () => {
    document.body.classList.remove("dark");
    document.documentElement.classList.remove("dark");
    document.documentElement.style.colorScheme = "light";
  };
  forceLight();
  new MutationObserver(forceLight).observe(document.body, { attributes: true, attributeFilter: ["class"] });
  new MutationObserver(forceLight).observe(document.documentElement, { attributes: true, attributeFilter: ["class"] });

  // Small DOM helpers keep the UI-enhancement code readable and centralized.
  const $ = (s, r = document) => r.querySelector(s);
  const make = (tag, cls, html) => {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html !== undefined) e.innerHTML = html;
    return e;
  };
  // Gradio may rebuild the textarea, so always resolve the current instance.
  const getInput = () => {
    const a = document.querySelectorAll("textarea");
    return a.length ? a[a.length - 1] : null;
  };

  // Put a question in the message box and submit it.
  const send = (text) => {
    const area = getInput();
    if (!area || area.disabled) return;
    const setter = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, "value").set;
    setter.call(area, text);
    area.dispatchEvent(new Event("input", { bubbles: true }));
    area.focus();
    setTimeout(() => {
      const btn = $("button.submit-button") || $("button.submit") || $('button[aria-label="Submit"]');
      if (btn) { btn.click(); return; }
      area.dispatchEvent(new KeyboardEvent("keydown", { key: "Enter", code: "Enter", keyCode: 13, which: 13, bubbles: true }));
    }, 80);
  };

  // Prefer Gradio's clear action and fall back to a reload when it is absent.
  const newChat = () => {
    const clear = $('button[aria-label="Clear"]') || $('button[title="Clear"]');
    if (clear) clear.click(); else { location.reload(); return; }
    const a = getInput();
    if (a) a.focus();
  };

  // Apply consistent placeholder and accessibility text to a rebuilt input.
  const tune = (area) => {
    if (area.placeholder !== PLACEHOLDER) area.placeholder = PLACEHOLDER;
    area.title = PLACEHOLDER;
    area.setAttribute("aria-label", PLACEHOLDER);
  };

  // Re-focus the message box after each reply and keep the placeholder.
  const watchTextarea = (area) => {
    if (area.dataset.dtWatched) return;
    area.dataset.dtWatched = "1";
    tune(area);
    let wasDisabled = area.disabled || area.readOnly;
    new MutationObserver(() => {
      const isDisabled = area.disabled || area.readOnly;
      if (wasDisabled && !isDisabled) area.focus();
      wasDisabled = isDisabled;
      tune(area);
    }).observe(area, { attributes: true, attributeFilter: ["disabled", "readonly", "placeholder"] });
  };

  // Add the branded UI around Gradio's generated DOM exactly once.
  const ensure = () => {
    // Header: brand bar + headline
    const h1 = $(".gradio-container h1");
    if (h1 && !h1.dataset.dtDone) {
      h1.dataset.dtDone = "1";
      h1.innerHTML = 'Ideas. Experience. <span class="dt-accent">Real conversations.</span>';
      const blk = h1.closest(".block") || h1.parentNode;
      blk.before(make("div", "dt-topbar",
        '<div class="dt-brand"><div class="dt-badge">DM</div><div><div class="dt-brand-name">Dhaval Mistry</div><div class="dt-brand-sub">Personal Digital Twin</div></div></div>' +
        '<div class="dt-pill"><span class="dt-pill-dot"></span>AI assistant</div>'));
    }

    // Description + tags
    const desc = [...document.querySelectorAll(".gradio-container p")].find((p) => p.textContent.includes("Talk to my AI twin"));
    if (desc && !desc.dataset.dtDone) {
      desc.dataset.dtDone = "1";
      desc.textContent = "Explore Dhaval's work in engineering leadership, enterprise banking, cloud architecture and applied AI. Or ask what he's curious about outside work.";
      const dblk = desc.closest(".block") || desc.parentNode;
      dblk.after(make("div", "dt-tags", TAGS.map((t) => '<span class="dt-tag">' + t + "</span>").join("")));
    }

    // Suggested questions, conversation bar, disclaimer, footer
    const bot = $(".chatbot");
    const area = getInput();
    if (!bot || !area || $(".dt-suggest")) return;

    let common = bot;
    while (common && !common.contains(area)) common = common.parentNode;
    if (!common || common === document.body) return;
    // Find the direct child under the shared container so inserted panels align
    // with Gradio's current layout without depending on a fixed nesting depth.
    const childOf = (n) => { while (n && n.parentNode !== common) n = n.parentNode; return n; };
    const host = childOf(bot);
    const inputBlock = childOf(area);
    if (!host) return;
    common.classList.add("dt-stack");

    const top = make("section", "dt-panel dt-suggest",
      '<div class="dt-suggest-head"><strong>Suggested questions</strong><span>Stay available throughout the conversation</span></div><div class="dt-chips"></div>');
    const chips = $(".dt-chips", top);
    SUGGESTIONS.forEach((s) => {
      const b = make("button", "dt-chip", '<span class="dt-chip-emoji">' + s.emoji + "</span><span>" + s.label + "</span>");
      b.type = "button";
      b.title = s.prompt;
      b.addEventListener("click", () => send(s.prompt));
      chips.appendChild(b);
    });
    const conv = make("div", "dt-panel dt-conv",
      '<div class="dt-conv-left"><span class="dt-live"></span>Conversation</div><div class="dt-conv-right">Ask about projects, expertise, or ideas</div>');
    host.before(top, conv);

    if (inputBlock && inputBlock !== host) {
      inputBlock.classList.add("dt-input-block");
      inputBlock.appendChild(make("div", "dt-disclaimer",
        "<span>This is Dhaval's AI representation, not Dhaval personally. Avoid sharing confidential information.</span>" +
        "<span><kbd>Enter</kbd> to send &middot; <kbd>Shift</kbd> + <kbd>Enter</kbd> for a new line</span>"));
      const footer = make("div", "dt-footer", "<span>Digital Twin &middot; Professional portfolio assistant</span>");
      const nb = make("button", "dt-newchat", "New chat");
      nb.type = "button";
      nb.addEventListener("click", newChat);
      footer.appendChild(nb);
      inputBlock.after(footer);
    }
  };

  // Fallback avatar for assistant rows if Gradio rendered none.
  const addAvatars = () => {
    document.querySelectorAll(".message-row.bot-row").forEach((row) => {
      if (row.dataset.dtAv) return;
      row.dataset.dtAv = "1";
      if (row.querySelector(".avatar-container")) return;
      row.classList.add("dt-avatar-row");
      row.prepend(make("div", "dt-avatar"));
    });
  };

  let queued = false;
  // Reconcile enhancements after Gradio renders or replaces interface nodes.
  const scan = () => {
    queued = false;
    ensure();
    addAvatars();
    document.querySelectorAll("textarea").forEach(watchTextarea);
  };
  // Collapse many DOM mutations into one browser animation-frame update.
  const schedule = () => { if (!queued) { queued = true; requestAnimationFrame(scan); } };

  setTimeout(() => { scan(); const a = getInput(); if (a) a.focus(); }, 400);
  new MutationObserver(schedule).observe(document.body, { childList: true, subtree: true });
}
""".replace(
    "__SUGGESTIONS__",
    json.dumps(
        [{"emoji": e, "label": l, "prompt": p} for e, l, p in _SUGGESTIONS],
        ensure_ascii=False,
    ),
)
