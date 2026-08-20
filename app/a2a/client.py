class A2AClient:

    def __init__(self, agents):
        self.agents = agents

    async def send(self, agent_name, state):

        print(
            f"[A2A] Sending request -> {agent_name}"
        )

        agent = self.agents[agent_name]

        result = await agent.process(state)

        if result is None:
            raise RuntimeError(
                f"{agent_name} returned None"
            )

        if not isinstance(result, dict):
            raise TypeError(
                f"{agent_name} returned "
                f"{type(result).__name__}, expected dict"
            )

        print(
            f"[A2A] Response <- {agent_name}"
        )

        print(
            f"[A2A] State keys after {agent_name}: "
            f"{sorted(result.keys())}"
        )

        return result