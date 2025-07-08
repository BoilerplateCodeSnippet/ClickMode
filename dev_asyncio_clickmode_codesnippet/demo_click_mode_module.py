"""
test_click_mode.py
This script is used to test the click mode functionality using the new tool definition
Created by : Vineet
Created Date: 9th June 25
"""
import asyncio
import click_mode_module

def dummy_click_function(x, y):
    """
    Custom click function that simulates a click at given coordinates.
    This can be replaced with any function you want to run repeatedly.
    """
    print(f"[Dummy Click Function from test_click_mode.py] Custom click at ({x}, {y})")

async def handle_user_input():
    """
    Handle user input asynchronously while click_mode might be running.
    """
    while True:
        print("\n" + "="*50)
        print("Options:")
        print("1 - Start click mode")
        print("2 - Stop click mode")
        print("3 - Check if click mode is running")
        print("4 - Exit program")
        print("="*50)
        
        try:
            # Get user input (this will block, but that's okay for demo purposes)
            choice = await asyncio.get_event_loop().run_in_executor(
                None, input, "Enter your choice (1-4): "
            )
            
            if choice == "1":
                if click_mode_module.is_click_mode_running():
                    print("Click mode is already running!")
                else:
                    print("Starting click mode...")
                    # Start click mode with function at coordinates (100, 200)
                    # await click_module.start_click_mode_with_function(
                    #     click_module.click_x_y, 100, 200
                    # )
                    # Control returns here immediately, click_mode continues in background
                    await click_mode_module.start_click_mode_with_function(
                        dummy_click_function, 2, 3, time_interval_in_ms=1000
                    )
                    
            elif choice == "2":
                print("Stopping click mode...")
                click_mode_module.stop()
                
            elif choice == "3":
                if click_mode_module.is_click_mode_running():
                    print("Click mode is currently running")
                else:
                    print("Click mode is not running")
                    
            elif choice == "4":
                print("Exiting program...")
                # Stop click mode if running
                if click_mode_module.is_click_mode_running():
                    click_mode_module.stop()
                # Wait a bit for cleanup
                await asyncio.sleep(0.2)
                break
                
            else:
                print("Invalid choice. Please enter 1, 2, 3, or 4.")
                
        except KeyboardInterrupt:
            print("\nProgram interrupted. Stopping click mode...")
            click_mode_module.stop()
            break
        except Exception as e:
            print(f"Error: {e}")

async def main():
    """
    Main function that runs the demo.
    """
    print("WebSocket Click Mode Demo")
    print("This demo simulates your WebSocket scenario with async operations")
    
    try:
        await handle_user_input()
    finally:
        # Cleanup: make sure click mode is stopped
        if click_mode_module.is_click_mode_running():
            click_mode_module.stop()
        await asyncio.sleep(0.2)  # Give time for cleanup
        print("Program ended.")

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
