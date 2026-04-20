import os
import json

def test_readme_exists():
    assert os.path.exists('README.md')

def test_project_structure_exists():
    assert os.path.exists('docs/PROJECT_STRUCTURE.md')

def test_project_goals_exists():
    assert os.path.exists('docs/PROJECT_GOALS.md')

def test_contributing_exists():
    assert os.path.exists('docs/CONTRIBUTING.md')

def test_self_improvement_plan_exists():
    assert os.path.exists('docs/SELF_IMPROVEMENT_PLAN.md')

def test_main_py_exists():
    assert os.path.exists('src/main.py')

def test_goal_txt_exists():
    assert os.path.exists('goal.txt')

def test_readme_not_empty():
    with open('README.md', 'r') as f:
        assert f.read() != ''

def test_project_structure_not_empty():
    with open('docs/PROJECT_STRUCTURE.md', 'r') as f:
        assert f.read() != ''

def test_project_goals_not_empty():
    with open('docs/PROJECT_GOALS.md', 'r') as f:
        assert f.read() != ''

def test_contributing_not_empty():
    with open('docs/CONTRIBUTING.md', 'r') as f:
        assert f.read() != ''

def test_self_improvement_plan_not_empty():
    with open('docs/SELF_IMPROVEMENT_PLAN.md', 'r') as f:
        assert f.read() != ''

def test_goal_txt_not_empty():
    with open('goal.txt', 'r') as f:
        assert f.read() != ''

def test_package_json_valid():
    try:
        with open('package.json', 'r') as f:
            json.load(f)
    except FileNotFoundError:
        pass
    except json.JSONDecodeError:
        assert False, 'package.json is not valid JSON'