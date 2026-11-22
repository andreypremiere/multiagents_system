from claude_agent_sdk import list_sessions, delete_session, get_session_messages

sessions = list_sessions()

# delete_session(session_id='a3ef4515-9e33-44cf-aee4-49389c727240')
# delete_session(session_id='65a9b0ba-69b0-413d-a9f8-7b025e6c4796')
# delete_session(session_id='e5d1a328-afa8-4652-a136-6d338ac4553e')
# delete_session(session_id='d0296776-9592-4bf5-96de-5b4a27bd83df')
# delete_session(session_id='bbeb206b-bcc9-4b98-9783-7d3b8a6556a6')





for session in sessions:
    print("Session ID:", session.session_id)
    print("Project:", session.cwd)
    print("Summary:", session.summary)
    print("Branch:", session.git_branch)
    print("Last modified:", session.last_modified)
    print("-" * 50)


