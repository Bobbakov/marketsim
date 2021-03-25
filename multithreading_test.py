from client.agents import Agent, ORDER_BOOK_ENDPOINT
from multiprocessing.dummy import Pool as ThreadPool


def run_agent(agent_id, time_secs, update_interval):
    a = Agent(agent_id=agent_id)
    a.agent_trading_session(time_secs, update_interval)


n_agents = 3
pool = ThreadPool(processes=n_agents)
# a sequence of argument tuples for starmap function
parameter_settings = [('A', 10, 5),
                      ('B', 25, 3),
                      ('C', 10, 2)
                      ]
assert len(parameter_settings) == n_agents
results = pool.starmap(run_agent, parameter_settings)