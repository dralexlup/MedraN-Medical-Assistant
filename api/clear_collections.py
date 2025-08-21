#!/usr/bin/env python3
"""
Utility script to clear ChromaDB collections when there's a dimension mismatch.
Run this if you see "Embedding dimension X does not match collection dimensionality Y" errors.
"""

import chromadb
from app.settings import settings
import sys

def clear_collections():
    """Clear all ChromaDB collections to resolve dimension mismatches."""
    try:
        # Connect to ChromaDB
        host = settings.chroma_url.split("//")[1].split(":")[0]
        port = int(settings.chroma_url.split(":")[-1])
        client = chromadb.HttpClient(host=host, port=port)
        
        print("🔍 Checking existing collections...")
        collections = client.list_collections()
        
        if not collections:
            print("✅ No collections found. Nothing to clear.")
            return
            
        print(f"📋 Found {len(collections)} collections:")
        for col in collections:
            print(f"  - {col.name}")
        
        response = input("\n⚠️  This will permanently delete all collections and their data. Continue? (y/N): ")
        if response.lower() not in ['y', 'yes']:
            print("❌ Operation cancelled.")
            return
        
        print("\n🗑️  Clearing collections...")
        for col in collections:
            try:
                client.delete_collection(col.name)
                print(f"✅ Deleted collection: {col.name}")
            except Exception as e:
                print(f"❌ Failed to delete {col.name}: {e}")
        
        print("\n✅ Collection clearing complete!")
        print("🚀 You can now restart the application. New collections will be created with the correct dimensions.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure ChromaDB is running and accessible.")
        sys.exit(1)

if __name__ == "__main__":
    clear_collections()
