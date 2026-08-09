from engine import Engine
if (__name__ == '__main__'):
    if Engine.Initialize():
        Engine.EngineRun()
        Engine.Shutdown()
