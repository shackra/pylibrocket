import rocket


class _PyrokitManager(object):
    def __init__(self):
        self.invisibleContexts = set()

        self.frameStartCallbacks = []
        self.framePreContextCallbacks = []
        self.framePostContextCallbacks = []
        self.frameEndCallbacks = []

    def addFrameStartCallback(self, callback):
        self.frameStartCallbacks.append(callback)

    def addFramePreContextCallback(self, callback):
        self.framePreContextCallbacks.append(callback)

    def addFramePostContextCallback(self, callback):
        self.framePostContextCallbacks.append(callback)

    def addFrameEndCallback(self, callback):
        self.frameEndCallbacks.append(callback)

    def showContext(self, context):
        self.invisibleContexts.remove(context)

    def hideContext(self, context):
        self.invisibleContexts.add(context)

    def render(self, data):
        activeContexts = set(rocket.contexts) - self.invisibleContexts

        for callback in self.frameStartCallbacks:
            callback()

        for context in activeContexts:
            for callback in self.framePreContextCallbacks:
                callback(context)

            context.Update()
            context.Render()

            for callback in self.framePostContextCallbacks:
                callback(context)

        for callback in self.frameEndCallbacks:
            callback()


manager = _PyrokitManager()
