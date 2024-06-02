## Progress

Follow the progress table below to see the different milestones / branches for this workshop.

| Branch                      | Status | Type | Description                                              |
|-----------------------------|--------|------|----------------------------------------------------------|
| `0-start-here`              | ✅      | Start | Set up the project, get familiar with the codebase.      |
| `1-integrate-llm-task`      | ✅      | Task | Integrate the LLM within the htmx chat.                  |
| `2-integrate-llm-solution`  | ✅      | Solution |                                                          |
| `3-client-events-task`      | ✅      | Task | Enable the LLM to trigger dark mode & fullscreen mode. |
| `4-client-events-solution`  | ✅      | **Solution** |                                                          |
| `5-server-functions-task`     | ⏳      | Task | Enable the LLM to create, update, and delete pizza orders. |
| `6-server-functions-solution` | ⏭      | Solution |                                                          |

To switch to another branch, use `git switch`.

**Note**: You don't need to run `docker compose up` for each branch. Just switch branch & refresh browser.

---

There is now a 🍕 icon on the top right that enables pizza mode.

In pizza mode, you can create, update, and delete pizza orders.

You will see there's a new `pizza_orders` application in the project.

It includes:
- A model `PizzaOrder` with fields:
  - `name` (choices: 'pepperoni', 'cheese', 'vegetarian') 
  - `size` (choices: 'small', 'medium', 'large')
- CRUD views
- Templates for the views

The CRUD functionality is inside `services.py` instead of the views. This is intentional. You can let the LLM use those
functions directly this way.

You will see the pizza orders container uses a different htmx pattern than our chat. 
1. When `pizzaOrdersUpdated` client is received from server
2. Issues GET request to `/pizza-orders` to update the pizza orders list
3. The `/pizza-orders` renders the index template from which we `hx-select` only the `#pizza-orders` element
4. This makes it easy to propagate server-side changes to the pizza orders (triggered by LLM), by adding `pizzaOrdersUpdated` to our response.


Notes: 
- There is a `PizzaOrderIn` Pydantic model in `views.py`. Use it with the `instructor` library.

You should be able to achieve task by modifying only `views.py` and `prompts.py`.


Good luck! 🍕

# Next Steps

Switch to the `6-server-functions-solution` branch to see the solution.
```bash
git switch 6-server-functions-solution
```