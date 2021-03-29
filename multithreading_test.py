from client.agents import Agent
from multiprocessing.dummy import Pool as ThreadPool


def run_agent(agent_id, time_secs, update_interval):
    a = Agent(agent_id=agent_id)
    a.agent_trading_session(time_secs, update_interval)


n_agents = 9
pool = ThreadPool(processes=n_agents)
# a sequence of argument tuples for starmap function
parameter_settings = [('A', 10, 5),
                      ('B', 25, 3),
                      ('C', 10, 2),
                      ('D', 10, 5),
                      ('E', 25, 3),
                      ('F', 10, 2),
                      ('G', 10, 5),
                      ('H', 25, 3),
                      ('I', 25, 3)
                      ]
assert len(parameter_settings) == n_agents
results = pool.starmap(run_agent, parameter_settings)