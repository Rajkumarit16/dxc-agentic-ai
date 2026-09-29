# Lab A — Workbench setup + Bedrock Playground (40 min)

## Part 1 — Setup (≈20 min)
Follow `setup\SETUP_GUIDE.md` until `SETUP.bat` shows **ALL GREEN**.

## Part 2 — Bedrock Playground (≈20 min)
1. Sign in to the **AWS console** with the user the trainer gave you. Region (top right): **N. Virginia (us-east-1)**.
2. Search **Bedrock** → left menu **Playgrounds → Chat / Text**.
3. Paste this ticket as your prompt:
   > You are AskIT, the IT helpdesk assistant at Orbit Corp. A user writes: "I'm locked out of my laptop since this morning after changing my password. I have a client call at 11." What should they do first? Answer in 3 sentences.

### Task A1 — Three models, one ticket
Run the prompt on **3 models** (e.g. a Claude Haiku, a Claude Sonnet, an Amazon Nova model). Use **Compare mode** if available.
Record in `submission\labA_playground.md`: latency, input tokens, output tokens, and your 1–5 rating of the answer.

### Task A2 — Temperature
With one model: run the prompt **3× at temperature 0** and **3× at temperature 1**. What changed between runs?

### ⭐ Stretch
Try an open-weight model (Llama or Mistral). Better, worse, or just different?

> Model not in the list or "access denied"? Tell the trainer — don't spend time on it.
