## Progress

Follow the progress table below to see the different milestones / branches for this workshop.

| Branch                      | Status | Type | Description                                              |
|-----------------------------|--------|------|----------------------------------------------------------|
| `0-start-here`              | ✅      | Start | Set up the project, get familiar with the codebase.      |
| `1-integrate-llm-task`      | ✅      | Task | Integrate the LLM within the htmx chat.                  |
| `2-integrate-llm-solution`  | ✅      | Solution |                                                          |
| `3-client-events-task`      | ✅      | Task | Enable the LLM to trigger dark mode & fullscreen mode. |
| `4-client-events-solution`  | ✅      | **Solution** |                                                          |
| `5-server-actions-task`     | ⏳      | Task | Enable the LLM to create, update, and delete pizza orders. |
| `6-server-actions-solution` | ⏭      | Solution |                                                          |

To switch to another branch, use `git switch`.

---

**Congratulations** on completing the `3-client-events-task` branch! 🎉

The assistant is now able to toggle dark & fullscreen mode.

Maybe you noticed some weird behaviours from the assistant while implementing this task (or maybe not).

Let's discuss that.

---

### Problem: Impulsive Behaviour

Telling the assistant it can trigger client events is like putting a kid in front of a **"Do not press"** button. 🤣

<img src="https://cdn.jsdelivr.net/gh/scriptogre/functional-chatbots-assets@main/4-client-events-solution/assistant_resisting_client_events.png" alt="Assistant resisting client events" width=400 />

It rarely resists from toggling a state or two.

**Assistant toggling states impulsively:**

<img src="https://cdn.jsdelivr.net/gh/scriptogre/functional-chatbots-assets@main/4-client-events-solution/assistant_toggling_states_impulsively.gif" alt="Assistant toggling states impulsively" width=800 />

### Solution: Reasoning
I've tried multiple ways to tame it.

A clear system prompt makes a **big** difference.

Including an internal `reasoning` process for the assistant also helped.

**Assistant reasoning before toggling states:**

<img src="https://cdn.jsdelivr.net/gh/scriptogre/functional-chatbots-assets@main/4-client-events-solution/assistant_toggling_states_with_reasoning.gif" alt="Assistant reasoning before toggling states" width=800 />

It's answers become much more thoughtful and less impulsive.

### Another Problem: Race Conditions (I think?)

When the assistant triggers both `toggleDarkMode` & `toggleFullscreenMode` simultaneously, the results are unpredictable:
- Both actions may execute.
- Only one action may execute.
- Neither action may execute.

**States working abnormally without delay:**

<img src="https://cdn.jsdelivr.net/gh/scriptogre/functional-chatbots-assets@main/4-client-events-solution/toggle_both_states_without_delay.gif" alt="Toggle both states without delay" width=800>

Initially, I've blamed the assistant's chaotic behavior.

However, the assistant actually triggered the client events correctly every time (to my surprise).

The issue was caused by htmx requesting both `/toggle-dark-mode` and `/toggle-fullscreen-mode` in parallel.

Adding the `delay` modifier to one of the checkbox toggles' `hx-trigger` attribute solved the issue.

_To be honest, I still don't fully understand why the parallel requests cause this issue. Please let me know if you figure it out!_

**States working correctly with delay:**

<img src="https://cdn.jsdelivr.net/gh/scriptogre/functional-chatbots-assets@main/4-client-events-solution/toggle_both_states_with_delay.gif" alt="Toggle both states with delay" width=800>

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
  "message": "Do you want me to toggle dark mode?",
  "client_events": ["toggleDarkMode"],
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

This schema is effective.

### Conclusion

Adding the fields in the correct order is very important if we want to generate coherent responses.

Try to think like an LLM when designing your response schema.

---

There were many interesting things to learn from this task alone!

Let's see what we have in store for the next task: **server actions**.

# Next Steps

Switch to the `5-server-actions-task` branch to see the next task.
```bash
git switch 5-server-actions-task
```