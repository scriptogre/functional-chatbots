## Progress

Follow the progress table below to see the different milestones / branches for this workshop.

| Branch                      | Status | Type     | Description                                                |
|-----------------------------|--------|----------|------------------------------------------------------------|
| `0-start-here`              | ✅      | Start    | Set up the project, get familiar with the codebase.        |
| `1-integrate-llm-task`      | ✅      | Task     | Integrate the LLM within the htmx chat.                    |
| `2-integrate-llm-solution`  | ✅      | Solution |                                                            |
| `3-client-events-task`      | ⏳      | **Task** | **Enable the LLM to trigger dark mode & fullscreen mode.** |
| `4-client-events-solution`  | ⏭      | Solution |                                                            |
| `5-server-functions-task`     | ⏭      | Task     | Enable the LLM to create, update, and delete pizza orders. |
| `6-server-functions-solution` | ⏭      | Solution |                                                            |

To switch to another branch, use `git switch`.

**Note**: You don't need to run `docker compose up` for each branch. Just switch branch & refresh browser.

---

## Context

### Update: Dark Mode & Fullscreen Mode

The UI now has **2 checkboxes** in the top right corner.

- Left checkbox toggles dark mode.
- Right checkbox toggles fullscreen mode.

The assistant is currently both unable to trigger them, and unaware of their existence.

<img src="https://cdn.jsdelivr.net/gh/scriptogre/functional-chatbots-assets@main/3-client-events-task/assistant_cant_toggle_dark_fullscreen_modes.gif" alt="Assistant can't toggle dark mode and fullscreen mode" width="800"/>

_(Here it's hallucinating about toggling dark mode and fullscreen mode.)_

The checkboxes use the `hx-post` attribute and their `checked` states depends on the `is_dark_mode` and `is_fullscreen_mode` values in the session. 

Check out `views.py` and `index.jinja` to see how they're implemented.

Here's their current logic, for context:

![Toggle Dark Mode And Fullscreen Mode Diagram](https://cdn.jsdelivr.net/gh/scriptogre/functional-chatbots-assets@main/3-client-events-task/toggle_dark_fullscreen_modes_diagram.webp)

---

### Task: Enable the LLM to trigger dark mode & fullscreen mode based on user input

The `views.py` includes some instructions on how to do this.

Good luck fellow Djangonaut! 🚀

---

### **Challenges**

1. #### Try to include a 3rd `reasoning` field in the assistant's response schema. It might help improve the assistant's responses' accuracy.
2. #### Make the assistant aware of whether dark and fullscreen modes are active.
---

# Next Steps

Switch to the `4-client-events-solution` branch to see the solution.
```bash
git switch 4-client-events-solution
```