# Streamlit run demo.py
import streamlit as st
import json
from agents.mentor_agent import MentorAgent
from agents.code_agent import CodeAgent
from agents.evaluation_agent import EvaluationAgent
from agents.orchestrator import AgentOrchestrator
from datetime import datetime

st.set_page_config(
    page_title="AI DSA Coach",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .css-1d391kg {display: none;}
    .main-container {
        background-color: #ffffff;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    .top-nav {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 15px 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .problem-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .problem-title {
        font-size: 24px;
        font-weight: 700;
        color: #1a202c;
        margin-bottom: 16px;
    }
    .difficulty-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 16px;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 16px;
    }
    .difficulty-easy { background-color: #d4edda; color: #155724; }
    .difficulty-medium { background-color: #fff3cd; color: #856404; }
    .difficulty-hard { background-color: #f8d7da; color: #721c24; }
    .problem-description {
        line-height: 1.6;
        color: #4a5568;
        font-size: 16px;
        margin-bottom: 20px;
    }
    .code-editor-container {
        background: #1e1e1e;
        border-radius: 8px;
        padding: 0;
        margin-bottom: 20px;
        border: 1px solid #333;
    }
    .chat-container {
        max-height: 400px;
        overflow-y: auto;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 16px;
    }
    .chat-message {
        margin-bottom: 12px;
        padding: 12px;
        border-radius: 8px;
    }
    .user-message {
        background: #e3f2fd;
        border-left: 3px solid #2196f3;
        color: #1a202c;
    }
    .mentor-message {
        background: #f3e5f5;
        border-left: 3px solid #9c27b0;
        color: #1a202c;
    }
    .agent-message {
        background: #e8f5e8;
        border-left: 3px solid #4caf50;
        color: #1a202c;
    }
    .example-container {
        background: #f7fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 16px;
        margin: 12px 0;
    }
    .example-code {
        background: #2d3748;
        color: #e2e8f0;
        padding: 8px 12px;
        border-radius: 4px;
        font-family: 'Courier New', monospace;
        margin: 4px 0;
    }
</style>
""", unsafe_allow_html=True)

LANGUAGE_TEMPLATES = {
    "Python": """def solution():
    pass

if __name__ == "__main__":
    pass""",
    "Java": """public class Solution {
    public void solution() {}
    public static void main(String[] args) {}
}""",
    "C++": """#include <iostream>
using namespace std;
class Solution {
public:
    void solution() {}
};
int main() { return 0; }""",
    "JavaScript": """function solution() {}
console.log(solution());""",
    "Go": """package main
import "fmt"
func solution() {}
func main() {}"""
}

@st.cache_data
def load_problems():
    try:
        with open("data/problems.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return [{
            "title": "Two Sum",
            "difficulty": "Easy",
            "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
            "examples": [
                {"input": "nums = [2,7,11,15], target = 9", "output": "[0,1]"},
                {"input": "nums = [3,2,4], target = 6", "output": "[1,2]"}
            ]
        }]

problems = load_problems()

def initialize_session_state():
    defaults = {
        "orchestrator": AgentOrchestrator(),
        "mentor_agent": MentorAgent(),
        "code_agent": CodeAgent(),
        "evaluation_agent": EvaluationAgent(),
        "current_problem": None,
        "selected_language": "Python",
        "skill_level": None,
        "user_approach": "",
        "mentor_conversation": [],
        "code_conversation": [],
        "user_code": "",
        "hints_used": 0,
        "session_data": {},
        "approach_approved": False,
        "active_tab": "problem",
        "problems_solved": 0,
        "certificates": [],
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

initialize_session_state()

def render_top_nav():
    problem_titles = [p["title"] for p in problems]
    with st.container():
        st.markdown('<div class="top-nav">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            st.markdown("### AI DSA Coach")
        with col2:
            selected_problem = st.selectbox("Select Problem", problem_titles, index=0, key="nav_problem_selector")
            if selected_problem != (st.session_state.current_problem["title"] if st.session_state.current_problem else ""):
                for p in problems:
                    if p["title"] == selected_problem:
                        st.session_state.current_problem = p
                        st.session_state.approach_approved = False
                        st.session_state.user_code = ""
                        st.session_state.mentor_conversation = []
                        st.session_state.code_conversation = []
                        st.rerun()
        with col3:
            st.markdown(f"Solved: {st.session_state.problems_solved}")
        st.markdown('</div>', unsafe_allow_html=True)

def render_problem_description():
    if not st.session_state.current_problem:
        st.warning("Please select a problem to begin.")
        return
    problem = st.session_state.current_problem
    with st.container():
        st.markdown('<div class="problem-card">', unsafe_allow_html=True)
        diff_class = f"difficulty-{problem['difficulty'].lower()}"
        st.markdown(f'<span class="difficulty-badge {diff_class}">{problem["difficulty"]}</span>', unsafe_allow_html=True)
        st.markdown(f'<h1 class="problem-title">{problem["title"]}</h1>', unsafe_allow_html=True)
        st.markdown(f'<div class="problem-description">{problem["description"]}</div>', unsafe_allow_html=True)
        if "examples" in problem:
            st.markdown("### Examples")
            for i, example in enumerate(problem["examples"], 1):
                st.markdown(f'<div class="example-container">', unsafe_allow_html=True)
                st.markdown(f'**Example {i}:**')
                st.markdown(f'<div class="example-code">Input: {example["input"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="example-code">Output: {example["output"]}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

def render_mentoring_phase():
    st.markdown("### Phase 1: Approach Discussion")
    if st.session_state.approach_approved:
        st.success("Your approach has been approved! You can now proceed to coding.")
        return
    if not st.session_state.user_approach:
        st.info("Describe your approach to solving this problem. The Mentor Agent will review it before you start coding.")
        approach = st.text_area("Your Approach:", height=150, placeholder="Explain your thought process, algorithm choice, data structures, and time/space complexity analysis...")
        if st.button("Submit Approach for Review"):
            if approach.strip():
                st.session_state.user_approach = approach
                st.rerun()
            else:
                st.error("Please describe your approach first.")
    else:
        st.markdown("#### Your Approach:")
        st.info(st.session_state.user_approach)
        if st.button("Get Mentor Feedback"):
            with st.spinner("Mentor Agent is reviewing your approach..."):
                feedback = st.session_state.mentor_agent.validate_approach(
                    st.session_state.current_problem,
                    st.session_state.user_approach,
                    st.session_state.skill_level or "intermediate"
                )
                st.session_state.mentor_conversation.append({"role": "user", "content": st.session_state.user_approach})
                st.session_state.mentor_conversation.append({"role": "assistant", "content": feedback})
                if "approved" in feedback.lower() or "looks good" in feedback.lower():
                    st.session_state.approach_approved = True
                    st.success("Approach approved! You can now start coding.")
                else:
                    st.warning("Please revise your approach based on the feedback.")
                st.rerun()
        if st.session_state.mentor_conversation:
            st.markdown("#### Conversation with Mentor:")
            for msg in st.session_state.mentor_conversation:
                if msg["role"] == "user":
                    st.markdown(f'<div class="chat-message user-message"><strong>You:</strong> {msg["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="chat-message mentor-message"><strong>Mentor:</strong> {msg["content"]}</div>', unsafe_allow_html=True)

def render_coding_phase():
    st.markdown("### Phase 2: Implementation")
    if not st.session_state.approach_approved:
        st.warning("Please get your approach approved first!")
        return
    col1, col2 = st.columns([1, 4])
    with col1:
        st.markdown("**Language:**")
    with col2:
        st.session_state.selected_language = st.selectbox("", list(LANGUAGE_TEMPLATES.keys()), index=list(LANGUAGE_TEMPLATES.keys()).index(st.session_state.selected_language), key="coding_language")
    default_code = st.session_state.user_code if st.session_state.user_code else LANGUAGE_TEMPLATES[st.session_state.selected_language]
    user_code = st.text_area("Write your code:", value=default_code, height=400, key="code_editor")
    st.session_state.user_code = user_code
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("Get Code Review"):
            with st.spinner("Code Agent is reviewing..."):
                review = st.session_state.code_agent.review_code(st.session_state.current_problem, user_code, st.session_state.selected_language)
                st.session_state.code_conversation.append({"role": "user", "content": f"Please review my code:\n\n{user_code}"})
                st.session_state.code_conversation.append({"role": "assistant", "content": review})
                st.rerun()
    with col2:
        if st.button("Get Hint"):
            st.session_state.hints_used += 1
            with st.spinner("Getting hint..."):
                hint = st.session_state.code_agent.get_hint(st.session_state.current_problem, user_code, st.session_state.hints_used)
                st.info(f"**Hint:** {hint}")
    with col3:
        if st.button("Submit Solution"):
            with st.spinner("Evaluating solution..."):
                evaluation = st.session_state.evaluation_agent.evaluate_solution(st.session_state.current_problem, user_code, st.session_state.selected_language, st.session_state.skill_level or "intermediate")
                st.session_state.session_data["evaluation"] = evaluation
                if "correct" in evaluation.lower() or "passed" in evaluation.lower():
                    st.success("Congratulations! Your solution is correct!")
                    st.session_state.problems_solved += 1
                    certificate = {"problem_title": st.session_state.current_problem["title"], "difficulty": st.session_state.current_problem["difficulty"], "timestamp": datetime.now().isoformat()}
                    st.session_state.certificates.append(certificate)
                    st.balloons()
                else:
                    st.warning("Your solution needs improvement. Review the feedback below.")
                st.rerun()
    if st.session_state.code_conversation:
        st.markdown("#### Code Review History:")
        for msg in st.session_state.code_conversation:
            if msg["role"] == "user":
                st.markdown(f'<div class="chat-message user-message"><strong>You:</strong> {msg["content"][:200]}...</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message agent-message"><strong>Code Agent:</strong> {msg["content"]}</div>', unsafe_allow_html=True)

def render_evaluation_summary():
    st.markdown("### Phase 3: Performance Summary")
    if "evaluation" not in st.session_state.session_data:
        st.info("Complete a problem to see your performance summary.")
        return
    evaluation = st.session_state.session_data["evaluation"]
    with st.container():
        st.markdown(f'''<div class="problem-card"><h3>Evaluation Results</h3><p>{evaluation}</p></div>''', unsafe_allow_html=True)
    st.markdown("### Your Achievements")
    if st.session_state.certificates:
        cols = st.columns(min(3, len(st.session_state.certificates)))
        for i, cert in enumerate(st.session_state.certificates):
            with cols[i % 3]:
                diff_emoji = "🟢" if cert["difficulty"].lower() == "easy" else "🟡" if cert["difficulty"].lower() == "medium" else "🔴"
                st.markdown(f"""<div class="problem-card" style="text-align: center;"><div style="font-size: 48px;">{diff_emoji}</div><strong>{cert["problem_title"]}</strong><br><small>{cert["difficulty"]}</small><br><small>{cert["timestamp"][:10]}</small></div>""", unsafe_allow_html=True)
    else:
        st.info("Solve problems to earn achievement certificates!")

def main():
    render_top_nav()
    if not st.session_state.current_problem and problems:
        st.session_state.current_problem = problems[0]
    tab1, tab2, tab3 = st.tabs(["Problem & Approach", "Coding", "Summary"])
    with tab1:
        render_problem_description()
        st.markdown("---")
        render_mentoring_phase()
    with tab2:
        render_coding_phase()
    with tab3:
        render_evaluation_summary()

if __name__ == "__main__":
    main()
