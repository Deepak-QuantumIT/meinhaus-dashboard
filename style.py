STYLE="""
<style>
    div[data-testid="stChatMessage"]{
        background-color: transparent !important;
    }

    [data-testid="stChatMessage"]:has([aria-label="Chat message from user"]) {
        justify-content: flex-end !important;
    }
    [data-testid="stChatMessage"]:has([aria-label="Chat message from user"]) 
    [data-testid="stChatMessageAvatarUser"] {
        order: 2;
        margin-left: 8px;
    }
    [data-testid="stChatMessage"]:has([aria-label="Chat message from user"]) 
    [data-testid="stChatMessageContent"] {
        order: 1;
        align-items: flex-end !important;
        text-align: right !important;
        
    }
    [data-testid="stChatMessage"]:has([aria-label="Chat message from user"]) 
    [data-testid="stMarkdown"] > div {
        text-align: right !important;
    }
</style>
"""