
Jozo = None

async def add_task(task, jozo = None):
    global Jozo
    assert jozo is not None or Jozo is not None
    Jozo = Jozo or jozo
    jozo = jozo or Jozo
    await jozo.put(task)