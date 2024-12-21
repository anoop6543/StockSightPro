import streamlit as st
import os
from openai import OpenAI
import json
from typing import Dict, List, Optional, Tuple

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

class DeploymentIssue:
    def __init__(self, issue_type: str, description: str, severity: str, fix: str):
        self.issue_type = issue_type
        self.description = description
        self.severity = severity
        self.fix = fix

def analyze_deployment_config() -> List[DeploymentIssue]:
    """
    Analyze current deployment configuration and identify potential issues.
    
    Returns:
        List of deployment issues found
    """
    issues = []
    
    # Check Streamlit config
    try:
        with open('.streamlit/config.toml', 'r') as f:
            config_content = f.read()
            
        # Get AI analysis of the configuration
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": """You are a deployment expert. Analyze the Streamlit configuration for potential deployment issues.
                    Respond in JSON format with an array of issues:
                    {
                        "issues": [
                            {
                                "type": "configuration|security|performance",
                                "description": "Description of the issue",
                                "severity": "high|medium|low",
                                "suggested_fix": "Specific fix suggestion"
                            }
                        ]
                    }"""
                },
                {
                    "role": "user",
                    "content": f"Analyze this Streamlit configuration for deployment issues:\n{config_content}"
                }
            ],
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        for issue in result['issues']:
            issues.append(DeploymentIssue(
                issue['type'],
                issue['description'],
                issue['severity'],
                issue['suggested_fix']
            ))
    except Exception as e:
        st.error(f"Error analyzing config: {str(e)}")
    
    return issues

def check_dependencies() -> List[DeploymentIssue]:
    """
    Check project dependencies for potential deployment issues.
    
    Returns:
        List of dependency-related issues
    """
    issues = []
    
    try:
        # Read requirements or pyproject.toml
        with open('pyproject.toml', 'r') as f:
            deps_content = f.read()
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": """Analyze Python project dependencies for deployment issues.
                    Check for:
                    - Version conflicts
                    - Security vulnerabilities
                    - Performance impact
                    - Missing production requirements
                    
                    Respond in JSON format:
                    {
                        "issues": [
                            {
                                "type": "dependency",
                                "description": "Issue description",
                                "severity": "high|medium|low",
                                "suggested_fix": "How to fix"
                            }
                        ]
                    }"""
                },
                {
                    "role": "user",
                    "content": f"Analyze these dependencies:\n{deps_content}"
                }
            ],
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        for issue in result['issues']:
            issues.append(DeploymentIssue(
                issue['type'],
                issue['description'],
                issue['severity'],
                issue['suggested_fix']
            ))
    except Exception as e:
        st.error(f"Error checking dependencies: {str(e)}")
    
    return issues

def suggest_code_fix(code: str, error_message: str) -> Optional[str]:
    """
    Generate AI-powered fix suggestion for code issues.
    
    Args:
        code: Problematic code snippet
        error_message: Error message or issue description
        
    Returns:
        Suggested fix as code string
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": """You are an expert code fixer. Analyze the code and error message to provide a specific fix.
                    Only respond with the corrected code. No explanations."""
                },
                {
                    "role": "user",
                    "content": f"""Fix this code that has the following error:
                    Error: {error_message}
                    
                    Code:
                    {code}"""
                }
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Error generating fix suggestion: {str(e)}")
        return None

def display_deployment_assistant():
    """Display the deployment assistant interface"""
    st.subheader("🔧 Deployment Assistant")
    
    with st.expander("🔍 Analyze Deployment Configuration"):
        if st.button("Run Analysis"):
            issues = analyze_deployment_config()
            
            if issues:
                for issue in issues:
                    with st.container():
                        severity_color = {
                            'high': '🔴',
                            'medium': '🟡',
                            'low': '🟢'
                        }.get(issue.severity.lower(), '⚪')
                        
                        st.markdown(f"""
                        {severity_color} **{issue.issue_type.title()}** ({issue.severity.upper()})
                        - {issue.description}
                        
                        Suggested Fix:
                        ```python
                        {issue.fix}
                        ```
                        """)
                        
                        if st.button(f"Apply Fix for {issue.issue_type}", key=f"fix_{issue.issue_type}"):
                            # Implement fix application logic
                            st.info("Fix application feature coming soon!")
            else:
                st.success("No deployment issues found!")
    
    with st.expander("📦 Check Dependencies"):
        if st.button("Analyze Dependencies"):
            dep_issues = check_dependencies()
            
            if dep_issues:
                for issue in dep_issues:
                    with st.container():
                        severity_color = {
                            'high': '🔴',
                            'medium': '🟡',
                            'low': '🟢'
                        }.get(issue.severity.lower(), '⚪')
                        
                        st.markdown(f"""
                        {severity_color} **Dependency Issue** ({issue.severity.upper()})
                        - {issue.description}
                        
                        Recommended Action:
                        ```
                        {issue.fix}
                        ```
                        """)
            else:
                st.success("No dependency issues found!")
    
    with st.expander("🛠️ Code Fix Suggestions"):
        code = st.text_area("Paste code with issues:", height=200)
        error_msg = st.text_area("Error message:", height=100)
        
        if st.button("Get Fix Suggestion") and code and error_msg:
            with st.spinner("Generating fix suggestion..."):
                fix = suggest_code_fix(code, error_msg)
                if fix:
                    st.code(fix, language='python')
                    if st.button("Copy Fix"):
                        st.code(fix)
                        st.success("Fix copied to clipboard!")
