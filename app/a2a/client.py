class A2AClient:

    def __init__(self, agents):
        self.agents = agents

    async def send(self, agent_name, state):

        print(f"[A2A] Sending request -> {agent_name}")

        agent = self.agents[agent_name]

        result = await agent.process(state)

        print(f"[A2A] Response <- {agent_name}")

        return result
