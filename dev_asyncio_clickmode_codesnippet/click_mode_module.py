"""
script: click_mode_module.py

This module provides functionality to run a click mode that can execute a function repeatedly at specified intervals asynchronously.


Created by: Vineet

Created Date: 9th June 25

Interface Functions:
- start_click_mode_with_function: Starts the click mode that repeatedly calls a given function every nth milliseconds
- stop: Stops the currently running click mode


"""


import asyncio
import time

# Global variable to control the click mode execution
click_mode_task = None
stop_event = None

# Was used to developed the inital logic. Will be depricated in future commits
async def click_mode():
    """
    Asynchronous function that runs a counter every 100ms and writes to a text file.
    Continues until stopped by the stop() function.
    """
    global stop_event
    # Create a new stop event for this execution
    stop_event = asyncio.Event()
    counter = 0
    try:
        while not stop_event.is_set():
            # Increment counter
            counter += 1
            # Write to text file
            with open("click_counter.txt", "w") as f:
                f.write(f"Counter: {counter}\nTimestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            # Wait for 100ms or until stop event is set
            try:
                await asyncio.wait_for(stop_event.wait(), timeout=0.1)
                break # Stop event was set
            except asyncio.TimeoutError:
                continue # Continue the loop after 100ms
    except asyncio.CancelledError:
        pass
    finally:
        pass

async def click_mode_with_function(func, x, y, time_interval_in_ms=500):
    """
    Asynchronous function that repeatedly calls a given function every 500ms.
    Continues until stopped by the stop() function.
    
    Args:
        func: The function to be called repeatedly (e.g., click_x_y). Can be sync or async.
        x: X coordinate to pass to the function
        y: Y coordinate to pass to the function
        time_interval_in_ms: Time interval in milliseconds between function calls (default is 500ms)
    """
    global stop_event
    # Create a new stop event for this execution
    stop_event = asyncio.Event()
    
    call_count = 0
    try:
        while not stop_event.is_set():
            # Increment call counter
            call_count += 1
            
            try:
                # Check if the function is a coroutine (async function)
                if asyncio.iscoroutinefunction(func):
                    await func(x, y)
                else:
                    # Call synchronous function with coordinates
                    func(x, y)
            except Exception as e:
                # Log any errors from the function call but continue running
                print(f"Error calling function on iteration {call_count}: {e}")
            
            # Wait for 500ms or until stop event is set
            try:
                await asyncio.wait_for(stop_event.wait(), timeout=(time_interval_in_ms/1000.0))  # Convert ms to seconds
                break  # Stop event was set
            except asyncio.TimeoutError:
                continue  # Continue the loop after 500ms
                
    except asyncio.CancelledError:
        pass
    finally:
        print(f"click_mode_with_function stopped after {call_count} function calls")

def stop():
    """
    Function to stop the currently running click_mode.
    """
    global stop_event
    if stop_event and not stop_event.is_set():
        stop_event.set()

async def start_click_mode():
    """
    Helper function to start click_mode and manage the task.
    """
    global click_mode_task
    # Cancel any existing task
    if click_mode_task and not click_mode_task.done():
        click_mode_task.cancel()
        try:
            await click_mode_task
        except asyncio.CancelledError:
            pass
    # Start new click mode task
    click_mode_task = asyncio.create_task(click_mode())
    return click_mode_task

async def start_click_mode_with_function(func, x, y, time_interval_in_ms=500):
    """
    Helper function to start click_mode_with_function and manage the task.
    
    Args:
        func: The function to be called repeatedly (e.g., click_x_y)
        x: X coordinate to pass to the function
        y: Y coordinate to pass to the function
    """
    global click_mode_task
    # Cancel any existing task
    if click_mode_task and not click_mode_task.done():
        click_mode_task.cancel()
        try:
            await click_mode_task
        except asyncio.CancelledError:
            pass
    
    # Start new click mode task with function and coordinates
    click_mode_task = asyncio.create_task(click_mode_with_function(func, x, y, time_interval_in_ms))
    return click_mode_task

def is_click_mode_running():
    """
    Check if click mode is currently running.
    """
    global click_mode_task
    return click_mode_task and not click_mode_task.done()

# Example click function for testing
def click_x_y(x: int, y: int):
    """
    Example click function that simulates clicking at coordinates.
    This is what would be called repeatedly.
    """
    timestamp = time.strftime('%H:%M:%S')
    print(f"[{timestamp}] Clicking at coordinates ({x}, {y})")
    
    # Write to a file to demonstrate it's working
    with open("click_log.txt", "a") as f:
        f.write(f"[{timestamp}] Clicked at ({x}, {y})\n")

# Example async click function for testing
async def async_click_x_y(x: int, y: int):
    """
    Example async click function that simulates clicking at coordinates.
    """
    timestamp = time.strftime('%H:%M:%S')
    print(f"[{timestamp}] Async clicking at coordinates ({x}, {y})")
    
    # Simulate some async work
    await asyncio.sleep(0.01)
    
    # Write to a file to demonstrate it's working
    with open("async_click_log.txt", "a") as f:
        f.write(f"[{timestamp}] Async clicked at ({x}, {y})\n")
