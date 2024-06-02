## Progress

Follow the progress table below to see the different milestones / branches for this workshop.

| Branch                      | Status | Type | Description                                              |
|-----------------------------|--------|------|----------------------------------------------------------|
| `0-start-here`              | ✅      | Start | Set up the project, get familiar with the codebase.      |
| `1-integrate-llm-task`      | ✅      | Task | Integrate the LLM within the htmx chat.                  |
| `2-integrate-llm-solution`  | ✅      | Solution |                                                          |
| `3-client-events-task`      | ✅      | Task | Enable the LLM to trigger dark mode & fullscreen mode. |
| `4-client-events-solution`  | ⏳      | **Solution** |                                                          |
| `5-server-functions-task`     | ⏭      | Task | Enable the LLM to create, update, and delete pizza orders. |
| `6-server-functions-solution` | ⏭      | Solution |                                                          |

To switch to another branch, use `git switch`.

**Note**: You don't need to run `docker compose up` for each branch. Just switch branch & refresh browser.

---

**Congratulations** on completing the `3-client-events-task` branch! 🎉

The assistant is now able to toggle dark & fullscreen mode.

Maybe you noticed some weird behaviours from the assistant while implementing this task (or maybe not).

Let's discuss that.

---

**Note**: To see the entire LLM response, modify this line in `views.py`:
```python
chat_messages.append({'role': 'assistant', 'content': llm_response.message})
```
to
```python
chat_messages.append({'role': 'assistant', 'content': llm_response.json()})
```

### Problem: Impulsive Behaviour

Telling the assistant it can trigger client events is like putting a kid in front of a **"Do not press"** button. 🤣

<img src="https://cdn.jsdelivr.net/gh/scriptogre/functional-chatbots-assets@main/4-client-events-solution/assistant_resisting_client_events.png" alt="Assistant resisting client events" width=400 />

It rarely resists from toggling a state or two.

**Assistant toggling states impulsively:**

<img src="https://cdn.jsdelivr.net/gh/scriptogre/functional-chatbots-assets@main/4-client-events-solution/assistant_toggling_states_impulsively.gif" alt="Assistant toggling states impulsively" width=800 />

### Solution: Reasoning
The most important thing you should start with is **the system prompt**.

However, if you don't see improvements with the prompt, you can add an internal `reasoning` process for the assistant.

It will not be shown to the user, but will improve the assistant's decision-making process tremendously (just like it does in humans!).

This is just a simplified version of the [**Chain of Thought**](https://www.promptingguide.ai/techniques/cot) prompting technique.

**Assistant reasoning before toggling states:**
<img src="https://cdn.jsdelivr.net/gh/scriptogre/functional-chatbots-assets@main/4-client-events-solution/assistant_toggling_states_with_reasoning.gif" alt="Assistant reasoning before toggling states" width=800 />

It's answers become much more thoughtful and less impulsive.

### Impact of Field Order on LLM Response Schema Effectiveness

Will the following two schemas produce the same result?

```python
"""
Schema 1
"""
class LLMResponseOne(BaseModel):
    message: str
    client_events: List[Literal["toggleDarkMode", "toggleFullscreenMode"]] = []
    reasoning: str

"""
Schema 2
"""
class LLMResponseTwo(BaseModel):
    reasoning: str
    client_events: List[Literal["toggleDarkMode", "toggleFullscreenMode"]] = []
    message: str

# Note: Fields order is different.
```

Let's think of how the LLM works.

They predict next tokens based on previous tokens, but this includes its own output.

#### Schema 1
In the first schema, the LLM would start by creating the `message`:
```json
{
  "message": "Do you want me to toggle dark mode?",
  ...
}
```
It would then continue choosing the `client_events`:
```json
{
  "message": "Do you want me to toggle dark mode?",
  "client_events": ["toggleDarkMode"],
  ...
}
```
Finally, it would generate the `reasoning` part:
```json
{
  "client_events": ["toggleDarkMode"],
  "message": "I've toggled dark mode for you.",
  "reasoning": "You wanted a darker theme so I toggled dark mode."
}
```

We might get frustrated that the assistant triggers dark mode while asking if we want it toggled. 

However, put yourself in the shoes of a LLM. 

It does not have context about the timing of the effect that it includes. Without that context, adding `toggleDarkMode` 
right after the `message` is a valid option.

Additionally, the `reasoning` is unnecessary in this schema. 

By the time it is generated, the `client_events` and the `message` have already occurred, making it merely a post-action justification.

#### Schema 2

In the second schema, the LLM would start by `reasoning`:
```json
{
  "reasoning": "I think you'd like to see the chat in a darker theme.",
  ...
}
```
The `client_events` it triggers would be influenced by the `reasoning` (what we want):
```json
{
  "reasoning": "I think you'd like to see the chat in a darker theme.",
  "client_events": ["toggleDarkMode"],
  ...
}
```
The `message` included would then be influenced by the `client_events`:
```json
{
  "reasoning": "I think you'd like to see the chat in a darker theme.",
  "client_events": ["toggleDarkMode"],
  "message": "I've toggled dark mode for you."
}
```

This schema allows the LLM to reason before taking any action.

---

Many interesting things to think about, right?

Let's see what we have in store for the next task: **server functions**.

# Next Steps

Switch to the `5-server-functions-task` branch to see the next task.
```bash
git switch 5-server-functions-task
```