# test_agent.py
from parsing_agent import parsing_agent
from calculator_agent import calculator_agent
from rl_agent import rl_agent

# Sample rule for Mumbai
sample_rule = {
    "city": "Mumbai",
    "authority": "MCGM",
    "clause_no": "DCPR 2034-12.3",
    "conditions": "Height <= 24m",
    "entitlements": "Max 7 floors"
}

def test_parsing_agent():
    case_id = parsing_agent(sample_rule)
    print(f"Parsing Agent test case ID: {case_id}")

def test_calculator_agent():
    outputs = calculator_agent("Mumbai")
    print("Calculator outputs:", outputs)

def test_rl_agent():
    # Replace with real case_id obtained from parsing agent test
    case_id = "testcase123"
    reward = rl_agent(case_id, "up")
    print("RL agent reward:", reward)

if __name__ == "__main__":
    test_parsing_agent()
    test_calculator_agent()
    test_rl_agent()
