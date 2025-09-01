print("Testing Flask app import...")
try:
    from app import app
    print("✓ Successfully imported Flask app")
    print(f"App name: {app.name}")
    print(f"Debug mode: {app.debug}")
    print(f"Testing configuration: {app.testing}")
except Exception as e:
    print(f"✗ Error importing Flask app: {str(e)}")
    import traceback
    traceback.print_exc()
