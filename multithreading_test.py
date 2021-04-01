from client.agents import Agent
from multiprocessing.dummy import Pool as ThreadPool


def run_agent(agent_id, time_secs, update_interval):
    a = Agent(agent_id=agent_id)
    a.agent_trading_session(time_secs, update_interval)


n_agents = 9
pool = ThreadPool(processes=n_agents)
# a sequence of argument tuples for starmap function
parameter_settings = [('A', 100, 5),
                      ('B', 100, 3),
                      ('C', 100, 2),
                      ('D', 100, 5),
                      ('E', 100, 3),
                      ('F', 100, 2),
                      ('G', 100, 5),
                      ('H', 100, 3),
                      ('I', 100, 3)
                      ]
assert len(parameter_settings) == n_agents
results = pool.starmap(run_agent, parameter_settings)