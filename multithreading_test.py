from client.agents import Agent
from multiprocessing.dummy import Pool as ThreadPool


def run_agent(agent_id, time_secs, update_interval):
    a = Agent(agent_id=agent_id)
    a.agent_trading_session(time_secs, update_interval)


n_agents = 9
pool = ThreadPool(processes=n_agents)
# a sequence of argument tuples for starmap function
parameter_settings = [('A', 1000, 1),
                      ('B', 1000, 1),
                      ('C', 1000, 1),
                      ('D', 1000, 1),
                      ('E', 1000, 1),
                      ('F', 1000, 1),
                      ('G', 1000, 1),
                      ('H', 1000, 1),
                      ('I', 1000, 0.5)
                      ]
assert len(parameter_settings) == n_agents
results = pool.starmap(run_agent, parameter_settings)