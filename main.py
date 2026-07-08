# {
#   "servers": {
#     "github": {
#       "type": "http",
#       "url": "https://api.githubcopilot.com/mcp/",
#       "headers": {
#         "Authorization": "Bearer ${input:github_mcp_pat}"
#       }
#     }
#   },
#   "inputs": [
#     {
#       "type": "promptString",
#       "id": "github_mcp_pat",
#       "description": "GitHub Personal Access Token",
#       "password": true
#     }
#   ]
# }


import asyncio
import json

import httpx
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
from mcp import types


SERVER_URL = "https://api.githubcopilot.com/mcp/"

headers = {
    "Authorization": "Bearer ${input:github_mcp_pat}"
}

client = httpx.AsyncClient(headers=headers, verify=False)


async def main():


    
    # Connect to remote MCP server
    async with streamable_http_client(SERVER_URL , http_client=client) as (
        read_stream,
        write_stream,
        _
    ):

        # Create session
        async with ClientSession(
            read_stream,
            write_stream
        ) as session:

            print("Initializing...")

            # initialize()
            await session.initialize()

            print("Connected!\n")

            # ---------------------------------------------------
            # List tools
            # ---------------------------------------------------

            response = await session.list_tools()

            tools = response.tools

            print("=" * 60)
            print(f"Found {len(tools)} tools")
            print("=" * 60)
            write_data = json.dumps(tools, indent=4, default=lambda o: o.__dict__)
            with open("tools.json", "w") as f:
                f.write(write_data) 
            print("Tools written to tools.json")    

            result = await session.call_tool(
                "create_branch",
                arguments={
                    "owner": "debnathdhruba",
                    "repo": "whats-app-chat-analyser",
                    "branch": "test-branch"
                }
            ) 
            

            print(result) 
            # for tool in tools:

            #     print(f"\nTool Name : {tool.name}")

            #     print(f"Title     : {tool.title}")

            #     print(f"Description:")

            #     print(tool.description)

            #     print("\nInput Schema")

            #     print(
            #         json.dumps(
            #             tool.inputSchema,
            #             indent=4
            #         )
            #     )

            # # ---------------------------------------------------
            # # Call first tool
            # # ---------------------------------------------------

            # if len(tools) == 0:
            #     print("No tools available.")
            #     return

            # tool = tools[0]

            # print("\n")
            # print("=" * 60)
            # print(f"Calling Tool : {tool.name}")
            # print("=" * 60)

            # #
            # # Replace arguments according to the tool schema
            # #
            # result = await session.call_tool(
            #     tool.name,
            #     arguments={}
            # )

            # print("\nResult\n")

            # for content in result.content:

            #     if isinstance(content, types.TextContent):

            #         print(content.text)

            #     else:

            #         print(content)

            # print("\nStructured Output")

            # print(result.structuredContent)

            


if __name__ == "__main__":
    asyncio.run(main())