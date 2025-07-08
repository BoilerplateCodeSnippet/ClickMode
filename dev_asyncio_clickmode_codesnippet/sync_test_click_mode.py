"""
script: sync_test_click_mode.py
Approach 1
Invoke async function from Normal (Synchronous) Function.
"""
# test_click_mode_sync.py
# Synchronous CLI to drive the async click_mode_module in the background
import threading
import asyncio
import time
import click_mode_module

def dummy_click_function(x, y):
    """
    Custom click function that simulates a click at given coordinates.
    """
    timestamp = time.strftime('%H:%M:%S')
    full_timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    print(f"[Dummy] Click at ({x}, {y}) at {timestamp}")
    # Write to file for visualization
    with open("sync_click_log.txt", "a") as f:
        f.write(f"[{full_timestamp}] Clicked at coordinates ({x}, {y})\n")

def _start_event_loop(loop: asyncio.AbstractEventLoop):
    """
    Target for the loop thread: run the event loop forever.
    """
    asyncio.set_event_loop(loop)
    loop.run_forever()  # Keeps running until .stop() is called

def main():
    # 1. Create and start a dedicated event loop in another thread
    loop = asyncio.new_event_loop()
    loop_thread = threading.Thread(target=_start_event_loop, args=(loop,), daemon=True)
    loop_thread.start()
    
    try:
        while True:
            print("\n" + "="*40)
            print("1: Start click mode")
            print("2: Stop click mode")
            print("3: Check status")
            print("4: Exit")
            print("="*40)
            choice = input("Enter choice (1-4): ").strip()
            
            if choice == "1":
                if click_mode_module.is_click_mode_running():
                    print("🔄 Click mode already running.")
                else:
                    print("▶️ Scheduling click mode to start...")
                    # Schedule the async start on the background loop
                    asyncio.run_coroutine_threadsafe(
                        click_mode_module.start_click_mode_with_function(
                            dummy_click_function, 100, 200, time_interval_in_ms=1000
                        ),
                        loop
                    )
            
            elif choice == "2":
                if click_mode_module.is_click_mode_running():
                    print("⏹️ Stopping click mode...")
                    click_mode_module.stop()
                else:
                    print("⚠️ Click mode is not running.")
            
            elif choice == "3":
                status = "running" if click_mode_module.is_click_mode_running() else "stopped"
                print(f"ℹ️ Click mode is currently {status}.")
            
            elif choice == "4":
                print("👋 Exiting...")
                if click_mode_module.is_click_mode_running():
                    click_mode_module.stop()
                # Give the click task a moment to finish up
                time.sleep(0.2)
                # Stop the event loop
                loop.call_soon_threadsafe(loop.stop)
                break
            
            else:
                print("❌ Invalid choice. Please enter 1-4.")
    
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user.")
        if click_mode_module.is_click_mode_running():
            click_mode_module.stop()
        loop.call_soon_threadsafe(loop.stop)
    
    # Wait for the loop thread to exit cleanly
    loop_thread.join()
    print("✅ Program ended.")

if __name__ == "__main__":
    main()
