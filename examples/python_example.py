"""
Example: Using the Connector Platform Python SDK

This example demonstrates how to:
1. List available connectors
2. Create a connection
3. Complete OAuth flow
4. Use a connector to make API calls
"""

from sdk.python import ConnectorPlatformClient
from connector_platform.connectors.gmail_connector import GmailConnector
import webbrowser

def main():
    platform_url = "http://localhost:5000"
    client = ConnectorPlatformClient(platform_url)
    
    print("=== Connector Platform Example ===\n")
    
    print("1. Listing available connectors...")
    connectors = client.list_connectors()
    print(f"Found {len(connectors)} connectors:")
    for conn in connectors:
        print(f"  - {conn['display_name']} ({conn['name']}): {conn['description']}")
    print()
    
    print("2. Creating a Gmail connection...")
    connection = client.create_connection(
        connector_type="gmail",
        name="My Gmail Connection",
        user_id="demo_user_123"
    )
    print(f"Created connection: {connection['id']}")
    print(f"Status: {connection['status']}")
    print()
    
    print("3. Initiating OAuth flow...")
    oauth_response = client.initiate_oauth(
        connector_type="gmail",
        redirect_uri="http://localhost:3000/callback"
    )
    
    auth_url = oauth_response['authorization_url']
    state = oauth_response['state']
    
    print(f"Authorization URL: {auth_url}")
    print(f"State: {state}")
    print()
    
    print("Opening browser for OAuth authorization...")
    print("After authorizing, you'll be redirected to the callback URL.")
    print("Copy the 'code' parameter from the callback URL.")
    
    
    code = input("\nEnter the authorization code: ").strip()
    
    if code:
        print("\n4. Completing OAuth flow...")
        result = client.complete_oauth(
            connection_id=connection["id"],
            code=code,
            redirect_uri="http://localhost:3000/callback"
        )
        
        if result.get("success"):
            print("OAuth completed successfully!")
            print()
            
            print("5. Using the Gmail connector...")
            gmail = GmailConnector(
                connection_id=connection["id"],
                config={"platform_url": platform_url}
            )
            
            print("Fetching messages...")
            messages_response = gmail.list_messages(maxResults=5)
            
            if messages_response.get("success"):
                messages = messages_response.get("data", {}).get("messages", [])
                print(f"Found {len(messages)} messages:")
                for msg in messages[:3]:
                    print(f"  - Message ID: {msg.get('id')}")
            else:
                print(f"Error: {messages_response.get('error')}")
            
            print("\nFetching labels...")
            labels_response = gmail.list_labels()
            
            if labels_response.get("success"):
                labels = labels_response.get("data", {}).get("labels", [])
                print(f"Found {len(labels)} labels:")
                for label in labels[:5]:
                    print(f"  - {label.get('name')}")
            else:
                print(f"Error: {labels_response.get('error')}")
        else:
            print(f"OAuth failed: {result.get('error')}")
    else:
        print("No code provided. Skipping OAuth completion.")
    
    print("\n=== Example Complete ===")


if __name__ == "__main__":
    main()
